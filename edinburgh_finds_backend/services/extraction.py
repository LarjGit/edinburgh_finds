"""
LLM API data extraction service.

Extracts entity information using a LLM API and returns SQLModel instances ready for database persistence.
"""
import json
import logging
import yaml
from typing import Optional
from pathlib import Path
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

# Cache prompts at module level
def _load_prompts():
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

_PROMPTS = _load_prompts()

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
    llm_adapter: object,
    location: Optional[str] = None
    ):
    
    """
    Extract entity information using LLM API.
    
    Two stage process (G&O - generate and organise):
    1. Stage 1: Asks LLM to find out all info about the entity with no output constraints
    2. Stage 2: Asks LLM to parse the free form text results from stage 1 into a structured JSON matching schema specified
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
    
    # Build location string for prompt
    location_str = f" in {location}" if location else ""
  
    # ================================================================
    # STAGE 1: FREE-FORM RESEARCH
    # ================================================================
    
    logger.info(f"Stage 1: LLM Free-form research for {entity_name}")

    stage1_system_prompt = _PROMPTS["stage1_research_system"]
    stage1_user_prompt = _PROMPTS["stage1_research_user"].format(
        entity_name=entity_name,
        entity_type=entity_type,
        location_str=location_str
    )
    
    research_text = llm_adapter.generate(
        system_prompt=stage1_system_prompt,
        user_prompt=stage1_user_prompt,
        enable_web_search=True  # Enable web search for Stage 1
    )
        
    logger.debug(f"Research results:\n{research_text}")
        
    logger.info("="*70)
    logger.info("STAGE 1 RESEARCH OUTPUT (check if social media is here):")
    logger.info("="*70)
    logger.info(research_text)
    logger.info("="*70)

    # ================================================================
    # STAGE 2: STRUCTURED PARSING
    # ================================================================
    
    logger.info(f"Stage 2: LLM Structured parsing for {entity_name}")
    
    # Get provider-specific system prompt
    stage2_system_prompt = _PROMPTS["stage2_parsing_system"][llm_adapter.provider_name]

    stage2_user_prompt = _PROMPTS["stage2_parsing_user"].format(
        entity_name=entity_name,
        entity_type=entity_type,
        location_str=location_str,
        research_text=research_text
    )
    
    raw_json = llm_adapter.generate(
        system_prompt=stage2_system_prompt,
        user_prompt=stage2_user_prompt,
        schema=schema
    )

    # ================================================================
    # PARSE AND VALIDATE RESPONSE
    # ================================================================

    logger.info(f"Parse and validate LLM response {entity_type}: {entity_name}{location_str}")

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
