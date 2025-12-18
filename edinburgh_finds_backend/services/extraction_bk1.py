"""
Perplexity API extraction service.
Handles extracting entity information from the Perplexity API.
"""
import os
import json
import logging
from typing import Optional
from perplexity import Perplexity
from models.models import Venue

# Pydantic model_class mapping
PYDANTIC_MODEL_CLASS_MAP = {
    "venue": Venue
}

# Fields that should NOT be sent to the LLM
# (they are auto-generated or internal use only)
INTERNAL_FIELDS = {
    'listing_id',
    'slug',
    'created_at',
    'updated_at',
    'external_ids'
}

API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not API_KEY:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

CLIENT = Perplexity(api_key=API_KEY)
PERPLEXITY_MODEL_NAME = "sonar"

def get_extraction_schema(model_class) -> dict:
    """
    Get JSON schema for LLM extraction, excluding internal fields.
    
    Internal fields (IDs, timestamps, slugs) are auto-generated,
    so we don't want the LLM to populate them.
    
    Args:
        model_class: Pydantic model class (Venue, Retailer, etc.)
    
    Returns:
        JSON schema dict with internal fields removed
    """
    schema = model_class.model_json_schema()
    
    # Remove internal fields from properties
    for field in INTERNAL_FIELDS:
        schema['properties'].pop(field, None)
        
        # Also remove from required list if present
        if 'required' in schema and field in schema['required']:
            schema['required'].remove(field)
    
    return schema

def extract_entity(
    entity_name: str,
    entity_type: str,
    location: Optional[str] = None
    ):
    
    """
    Extract comprehensive entity information using Perplexity API.
    
    Args:
        entity_name: Name of the entity to extract (e.g., "Manchester Tennis Club")
        entity_type: Type of entity - must be one of: venue, retailer, cafe, members_club
        location: Optional location to help with search (e.g., "Manchester, UK")
    
    Returns:
        Pydantic model instance (Venue, Retailer, Cafe, or MembersClub) with extracted data
    """
    
    # Get the appropriate model class
    model_class = PYDANTIC_MODEL_CLASS_MAP.get(entity_type)
    if not model_class:
        raise ValueError(
            f"Unknown entity_type: '{entity_type}'. "
            f"Valid types: {list(PYDANTIC_MODEL_CLASS_MAP.keys())}"
        )
    
    # Build location string for prompt
    location_str = f" in {location}" if location else ""
    
    # Get schema without internal fields
    schema = get_extraction_schema(model_class)
    
    # Build the extraction prompt
    prompt = f"""
    Extract detailed information about: {entity_name} (a {entity_type}{location_str})

    INSTRUCTIONS:
    1. Search multiple authoritative sources including:
    - Official website
    - Google Maps and business listings
    - Review sites and directories
    - Social media pages
    - Any other reliable sources

    2. Extract ALL available information that matches the JSON schema fields provided below

    3. Be thorough and complete:
    - Include full address details and coordinates if available
    - Capture all contact information (phone, email, website)
    - Extract operating hours in the structured format specified
    - Note all facilities, amenities, and features
    - Include any relevant details about services, pricing, or offerings

    4. For information that doesn't fit the predefined schema fields, add it to 'other_attributes' as key-value pairs

    5. Only include information you can verify from your sources - do not make assumptions or invent details

    6. If you find conflicting information between sources, prefer:
    - Official website over third-party sites
    - More recent information over older information
    - More detailed/specific information over vague information

    7. For opening hours, use this exact format:
    {{'monday': {{'open': '09:00', 'close': '17:00'}}, 'sunday': 'CLOSED'}}
    - Keys must be lowercase full weekday names
    - Times must be 24-hour format HH:MM
    - Use 'CLOSED' (string) for closed days

    Extract the information into this JSON schema:
    {json.dumps(schema, indent=2)}
    """
    
    # Call Perplexity API
    response = CLIENT.chat.completions.create(
        model=PERPLEXITY_MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": f"{entity_type}_extraction",
                "schema": schema
            }
        }
    )
    
    # Parse the response
    data = json.loads(response.choices[0].message.content)
    
    # Add back the entity_type (we always know this from input)
    data['entity_type'] = entity_type
    
    # Validate and create the model instance
    # Internal fields (listing_id, slug, timestamps) are auto-generated in __init__
    entity = model_class.model_validate(data)
    
    return entity