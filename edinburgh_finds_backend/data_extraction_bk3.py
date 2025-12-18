import os
import json
from typing import Optional, List, Dict, Any
from listings_data_model import Venue
from perplexity import Perplexity

API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not API_KEY:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

CLIENT = Perplexity(api_key=API_KEY)
MODEL_NAME = "sonar"

# -------------
# Discover URLs
# -------------
def discover_urls(entity_name: str, entity_type: str, max_results: int) -> List[str]:
    query = f"Find the official website URLs for the {entity_type} named '{entity_name}'"
    try:
        results = CLIENT.search.create(query=query, max_results=max_results).results
        urls = [r.url for r in results if r.url]
        return urls
    except Exception as e:
        return []
    
# ---------------------------
# Deep merge function
# ---------------------------
def deep_merge(master: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge `new` dict into `master` dict.
    - Only creates nested dicts/lists if there is actual data.
    - Adds new list items without duplicates.
    - Adds new dict keys without overwriting existing non-null values.
    """
    for key, value in (new or {}).items():
        if value is None:
            continue  # skip None values

        if isinstance(value, dict):
            if value:  # only merge if dict has data
                master_value = master.get(key)
                if not isinstance(master_value, dict):
                    master_value = {}
                merged = deep_merge(master_value, value)
                if merged:  # only set if merged dict is not empty
                    master[key] = merged

        elif isinstance(value, list):
            if value:  # only merge if list has items
                master_list = master.get(key)
                if not isinstance(master_list, list):
                    master_list = []

                # Normalize strings for additional_categories
                if key == "additional_categories":
                    seen = set(s.lower() for s in master_list if isinstance(s, str))
                    for item in value:
                        if isinstance(item, str) and item.lower() not in seen:
                            master_list.append(item)
                            seen.add(item.lower())
                else:
                    seen = {str(item) for item in master_list}
                    for item in value:
                        if item is not None and str(item) not in seen:
                            master_list.append(item)
                            seen.add(str(item))

                if master_list:  # only set if list is not empty
                    master[key] = master_list

        else:
            # Only set if key does not exist or master value is None
            if key not in master or master[key] is None:
                master[key] = value

    return master

# ---------------------------
# PROGRESSIVE AUGMENTATION
# ---------------------------
def progressively_augment_data(urls: List[str], entity_name: str, entity_type: str) -> Optional[Venue]:
    """
    Merge data from multiple URLs into one Venue object.
    Fully additive: every new piece of data is merged in.
    Ensures no empty dicts or lists are left in the final result.
    """
    master_venue = Venue.model_construct(
        listing_id=None,
        entity_name=entity_name,
        entity_type=entity_type,
    )

    for url in urls:
        try:
            # Ask Perplexity to extract structured JSON for this URL
            resp = CLIENT.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a precise JSON data extraction engine."},
                    {"role": "user", "content": f"Analyze ONLY this URL: {url}. Return JSON matching Venue schema."}
                ],
                response_format={"type": "json_schema", "json_schema": {"schema": Venue.model_json_schema()}},
                temperature=0.0,
            )

            raw_json = resp.choices[0].message.content
            new_data = Venue.model_validate_json(raw_json).model_dump()
            master_dict = master_venue.model_dump()

            # Merge without creating empty dicts/lists
            merged = deep_merge(master_dict, new_data)

            master_venue = Venue.model_validate(merged)

        except Exception:
            continue  # skip URLs that fail

    return master_venue

# ---------------------------
# MAIN EXTRACTION
# ---------------------------
def extract_entity_data(entity_name: str, entity_type: str, max_urls: int) -> Optional[Venue]:
    urls = discover_urls(entity_name, entity_type, max_urls)
    if not urls:
        return None
    return progressively_augment_data(urls, entity_name, entity_type)
