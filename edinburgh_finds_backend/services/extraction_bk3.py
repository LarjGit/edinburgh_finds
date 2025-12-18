"""
Perplexity API extraction service using the official perplexityai package.

Extracts entity information using Perplexity's LLM and returns
SQLModel instances ready for database persistence.
"""
import os
import json
import logging
import yaml
from typing import Optional
from pathlib import Path
from perplexity import Perplexity
from models.models import Listing, Venue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic model_class mapping
PYDANTIC_MODEL_CLASS_MAP = {
    "venue": (Listing, Venue)
}

# Fields that should NOT be sent to the LLM
# (they are auto-generated or internal use only)
INTERNAL_FIELDS = {
    'listing_id',
    'entity_name',
    'entity_type',
    'slug',
    'created_at',
    'updated_at',
    'external_ids'
}

# Load prompts from YAML file (load once at module level)
PROMPTS_FILE = Path(__file__).parent / "prompts.yaml"

def load_prompts():
    """Load prompt templates from YAML file."""
    try:
        with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Prompts file not found: {PROMPTS_FILE}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in prompts file: {e}")
        raise

# Cache prompts at module level
_PROMPTS = load_prompts()

# Set Perplexity constants
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not PERPLEXITY_API_KEY:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

CLIENT = Perplexity(api_key=PERPLEXITY_API_KEY)
PERPLEXITY_MODEL_NAME = "sonar"

def get_extraction_schema(listing_class, entity_class) -> dict:
    """
    Combine schemas from two separate classes.

    Args:
        listing_class: Listing model class (general attributes)
        entity_class: Entity-specific model class (eg. Venue specific attributes)
    
    Returns:
        Combined JSON schema
    """
    listing_schema = listing_class.model_json_schema()
    entity_schema = entity_class.model_json_schema()
    
    # Remove internal fields from listing schema
    for field in INTERNAL_FIELDS:
        listing_schema['properties'].pop(field, None)
    
    # Remove listing_id from entity schema
    entity_schema['properties'].pop('listing_id', None)
    
    # Combine properties
    combined_properties = {
        **listing_schema['properties'],
        **entity_schema['properties']
    }
    
    # Build combined schema
    combined_schema = {
        "type": "object",
        "properties": combined_properties   
    }
    
    return combined_schema
    
def extract_entity(
    entity_name: str,
    entity_type: str,
    location: Optional[str] = None
    ):
    
    """
    Extract entity information using Perplexity API.
    
    Two stage process (G&O - generate and organise):
    1. Stage 1: Asks perplexity to find out all info about the entity with no output constraints
    2. Stage 2: Asks perplexity to parse the free form text results from stage 1 into a structured JSON matching schema specified
    3. Splits data into Listing + entity-specific instances
    4. Returns both SQLModel instances ready for database persistence
    
    Returns:
        Tuple of (Listing, EntitySpecific) e.g., (Listing, Venue)
        Both are SQLModel instances with auto-generated IDs and slugs.
        
    Raises:
        ValueError: If entity_type is not recognized
    """    
    
    # Validate entity type
    if entity_type not in PYDANTIC_MODEL_CLASS_MAP:
        raise ValueError(
            f"Unknown entity_type: '{entity_type}'. "
            f"Valid types: {list(PYDANTIC_MODEL_CLASS_MAP.keys())}"
        )
    
    listing_class, entity_class = PYDANTIC_MODEL_CLASS_MAP[entity_type]
    
    # Get schema without internal fields
    schema = get_extraction_schema(listing_class, entity_class)
    schema_json = json.dumps(schema, indent=2)
    
    # Build location string for prompt
    location_str = f" in {location}" if location else ""
  
    # ================================================================
    # STAGE 1: FREE-FORM RESEARCH
    # ================================================================
    
    logger.info(f"Stage 1: Free-form research for {entity_name}")

    stage1_system_prompt = _PROMPTS["stage1_research_system"]
    stage1_user_prompt = _PROMPTS["stage1_research_user"].format(
        entity_name=entity_name,
        entity_type=entity_type,
        location_str=location_str
    )
    
    try:
        research_response = CLIENT.chat.completions.create(
            model=PERPLEXITY_MODEL_NAME,
            messages=[
                {"role": "system", "content": stage1_system_prompt},
                {"role": "user", "content": stage1_user_prompt}
            ],
            temperature=0.0
        )
        
        research_text = research_response.choices[0].message.content
        logger.debug(f"Research results:\n{research_text}")
        
    except Exception as e:
        logger.error(f"Stage 1 research failed: {e}")
        raise
    
    logger.info("="*70)
    logger.info("STAGE 1 RESEARCH OUTPUT (check if social media is here):")
    logger.info("="*70)
    logger.info(research_text)
    logger.info("="*70)

    # ================================================================
    # STAGE 2: STRUCTURED PARSING
    # ================================================================
    
    logger.info(f"Stage 2: Structured parsing for {entity_name}")
    
    stage2_system_prompt = _PROMPTS["stage2_parsing_system"]
    stage2_user_prompt = _PROMPTS["stage2_parsing_user"].format(
        entity_name=entity_name,
        entity_type=entity_type,
        location_str=location_str,
        research_text=research_text,
        schema_json=schema_json
    )
    
    try:
        parsing_response = CLIENT.chat.completions.create(
            model=PERPLEXITY_MODEL_NAME,
            messages=[
                {"role": "system", "content": stage2_system_prompt},
                {"role": "user", "content": stage2_user_prompt}
            ],
            temperature=0.0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": f"{entity_type}_extraction",
                    "schema": schema
                }
            }
        )
        
        raw_json = parsing_response.choices[0].message.content
        logger.debug(f"Structured output: {raw_json}")
        
    except Exception as e:
        logger.error(f"Stage 2 parsing failed: {e}")
        raise

    logger.info(f"Extracting {entity_type}: {entity_name}{location_str}")

    # ================================================================
    # PARSE AND VALIDATE RESPONSE
    # ================================================================

    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {raw_json}")
        raise ValueError(f"Invalid JSON from Perplexity API: {e}")

    # ================================================================
    # SPLIT DATA AND CREATE MODEL INSTANCES
    # ================================================================

    # Get field names for each model (excluding internal fields)
    listing_fields = set(listing_class.model_fields.keys()) - INTERNAL_FIELDS
    entity_fields = set(entity_class.model_fields.keys()) - {'listing_id'}

    # Split data into listing and entity-specific
    listing_data = {k: v for k, v in data.items() if k in listing_fields}
    entity_data = {k: v for k, v in data.items() if k in entity_fields}

    # Add back entity name and type (excluded from LLM extraction)
    listing_data['entity_type'] = entity_type
    listing_data['entity_name'] = entity_name

    # Create Listing instance
    # (listing_id and slug are auto-generated in Listing.__init__)
    try:
        listing = listing_class(**listing_data)
    except Exception as e:
        logger.error(f"Failed to create Listing instance: {listing_data}")
        raise ValueError(f"Invalid listing data: {e}")

    # Create entity instance (linked via listing_id)
    entity_data['listing_id'] = listing.listing_id

    try:
        entity = entity_class(**entity_data)
    except Exception as e:
        logger.error(f"Failed to create {entity_class.__name__} instance: {entity_data}")
        raise ValueError(f"Invalid entity data: {e}")

    logger.info(
        f"Successfully extracted {entity_type}: {listing.listing_id} "
        f"({listing.entity_name})"
    )

    return listing, entity
