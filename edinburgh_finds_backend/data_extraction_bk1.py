# data_extraction.py

import os
import json
from typing import Optional, List, Dict, Any
from perplexity import Perplexity
from pydantic import ValidationError

# Import all models from the dedicated file (MUST be updated for the new DiscoveryItem)
from listings_data_model import Venue, BaseListing, DiscoveryItem

# --- Configuration ---
API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not API_KEY:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")
CLIENT = Perplexity(api_key=API_KEY)
MODEL_NAME = "sonar" # Using the fast, reliable model


def discover_urls(entity_name: str, entity_type: str, max_results: int) -> List[str]:
    """Uses Perplexity search to find a list of authoritative URLs."""
    query = f"Find the official website URLs for the {entity_type} named '{entity_name}'"
    try:
        search_response = CLIENT.search.create(
            query=query,
            max_results=max_results
        )
        return [r.url for r in search_response.results if r.url]
    except Exception as e:
        print(f"Discovery Error: {e}") 
        return []

def enrich_schema(schema: dict) -> dict:
    """
    Recursively walk a JSON Schema and add generic, contextual descriptions
    to fields that are missing them. Works for any Pydantic model schema.
    """
    def recurse(obj: dict, parent_path: str = ""):
        props = obj.get("properties", {})
        for key, val in props.items():
            path = f"{parent_path}.{key}" if parent_path else key

            # --- Add a description if missing ---
            if "description" not in val or not val["description"].strip():
                # Generate a generic contextual hint
                val["description"] = f"Field '{path}' — extract or infer this value if available; output null if not found."

            # --- Recurse if this is a nested object ---
            if val.get("type") == "object" and "properties" in val:
                recurse(val, path)

            # --- Handle arrays generically too ---
            elif val.get("type") == "array" and "items" in val:
                item_type = val["items"].get("type", "object")
                val["description"] += f" (Array of {item_type} items.)"

        return obj

    return recurse(schema.copy())

def progressively_augment_data(urls: List[str], entity_name: str, entity_type: str) -> Optional[Venue]:
    """
    Processes a list of URLs, enriching the Master Venue object only where 
    fields are currently None or empty, with specific handling for the discovery list.
    """
    Target_Model = Venue
    
    # 1. Initialize the Master Venue Object (Using model_construct to skip validation)
    master_venue = Target_Model.model_construct(
        listing_id=None,
        entity_name=entity_name,
        entity_type=entity_type,
    )
    schema_dict = enrich_schema(Target_Model.model_json_schema())
    
    for i, url in enumerate(urls):
        print(f"\nProcessing Source {i+1}/{len(urls)}: {url}")
        
        prompt = f"""
        Analyze ONLY the webpage at URL: {url}. Extract and classify all structured data for the entity '{entity_name}' of type '{entity_type}'. Adhere STRICTLY to the JSON Schema and ensure all nested fields are correctly populated.
        Use all available or retrieved information to populate every field in the JSON Schema provided separately.

        Guidelines:
        - Follow the JSON Schema exactly, including nested objects and field names.
        - Populate every field you can find evidence for, including nested fields.
        - Use explicit null values for missing information — never omit required fields.
        - Ensure types match the schema (numbers as numbers, strings as strings, arrays as arrays, etc.).
        - Do not add extra fields or comments.
        - Return **only** a single JSON object matching the schema 
        
        Pay special attention to extracting key/value facts into the 'other_attributes' list. 
        """

        try:
            chat_response = CLIENT.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a precise JSON data extraction engine."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_schema", "json_schema": {"schema": schema_dict}},
                temperature=0.0,
            )
            raw_json_string = chat_response.choices[0].message.content
            
            # 2. Validate the incoming data immediately against the model
            new_data_model = Target_Model.model_validate_json(raw_json_string)

            # 3. Progressive Augmentation Logic
            master_dict = master_venue.model_dump()
            
            for key, new_value in new_data_model.model_dump().items():
                current_value = master_dict.get(key)
                
                # A. Mandatory/Core Fields (Fill-Once/Smart Overwrite)
                if key in ['entity_name', 'entity_type', 'primary_category', 'location', 'contact']:
                    # Trust the first source for core identity and mandatory containers
                    if current_value is None and new_value not in (None, "", {}):
                        master_dict[key] = new_value
                    # If primary_category is set, do not overwrite (Locking the classification)
                    elif key == 'primary_category' and current_value is not None:
                        continue 
                
                # B. Discovery Lists (AUGMENTATION: Merge the Lists/Items)
                elif key == 'additional_categories':
                    if new_value and isinstance(new_value, list):
                        # Merge the new unique categories into the master list
                        master_categories = set(master_dict.get(key) or [])
                        master_dict[key] = list(master_categories.union(set(new_value)))
                        
                elif key == 'other_attributes':
                    if new_value and isinstance(new_value, list):
                        # Add new discovery items to the master list
                        master_dict[key].extend(new_value)

                # C. Simple Optional Fields (Fill-Once)
                elif current_value is None and new_value is not None:
                    master_dict[key] = new_value
                    
            # 4. Re-validate and update the master object
            master_venue = Target_Model.model_validate(master_dict)
            
            print(f"-> Master object successfully augmented from source {i+1}.")

        except ValidationError as e:
            # Crucial: Log the invalid JSON, but continue to the next URL
            print(f"-> Validation Error on URL {url}. Data from this source ignored.")
            continue 
        except Exception as e:
            print(f"-> API Error on URL {url}. Full Error: {e}. Skipping source.")
            continue
            
    return master_venue

def extract_entity_data(entity_name: str, entity_type: str, max_urls: int) -> Optional[Venue]:
    """Handles the full extraction pipeline start."""
    if entity_type.lower() != 'venue':
        print(f"Error: Extraction is only set up for 'venue' entities.")
        return None
    
    urls = discover_urls(entity_name, entity_type, max_urls)
    if not urls:
        print(f"Error: No URLs found for {entity_name}.")
        return None
    
    return progressively_augment_data(urls, entity_name, entity_type)