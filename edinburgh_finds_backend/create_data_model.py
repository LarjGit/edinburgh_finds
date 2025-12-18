import json
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from enum import Enum

# ====================================================================
# ENUM DEFINITIONS
# ====================================================================

class PrimaryCategory(str, Enum):
    """The allowed values for the primary category (Constrained Constants)."""
    PADEL = "padel"
    PICKLEBALL = "pickleball"
    BOARD_GAMES = "board_games"
    TENNIS = "tennis"
    SQUASH = "squash"
    RACKETBALL = "racketball"
    TABLE_TENNIS = "table_tennis"
    GYM = "gym"

# ====================================================================
# BASE MODEL (Shared Logic & Mandatory Core Fields)
# ====================================================================

class BaseListing(BaseModel):
    """
    Base class for all entity listings. Defines core mandatory fields 
    and excludes the internal listing_id from the generated JSON Schema
    (as it's set at persistence stage not discovery).
    """
    
    # --- MODEL CONFIGURATION ---
    # Applies to all classes that inherit from BaseListing
    model_config = ConfigDict(
        title='Base Listing Schema',
    )
    
    # --- CORE MANDATORY FIELDS ---
    
    # listing_id: Required by Python, EXCLUDED from API Schema
    listing_id: str = Field(
        ..., 
        description="A unique identifier for the listing (set upon persistence).",
        json_schema_extra={'exclude': True} 
    )
    
    entity_name: str = Field(..., description="The name of the listing (e.g., club name, venue name).")
    entity_type: str = Field("venue", description="The specific type of entity for the listing (fixed to 'venue').")
    primary_category: PrimaryCategory = Field(..., description="The main category the listing belongs to.")
    
    # --- OPTIONAL DISCOVERY FIELD (Inherited by all) ---
    additional_categories: Optional[List[str]] = Field(None, description="A list of other categories found on the page.")
    
    # --- CATCH-ALL DISCOVERY FIELD (Inherited by all) ---
    other_attributes: Dict[str, Any] = Field(
        default_factory=dict,
        description="A catch-all for any other relevant data not explicitly listed.",
    )

# ====================================================================
# 2. REUSABLE MODEL: ADDRESS 🏠 (Inner fields optional)
# ====================================================================

class Address(BaseModel):
        
    city: str = Field(..., description="The city or major town. MUST be provided.")
    street_address: Optional[str] = Field(None, description="The full street address. Output NULL if not found.")
    postcode: Optional[str] = Field(None, description="The postal or zip code. Output NULL if not found.")
    country_code: str = Field("GB", description="The country code (e.g., GB, US). Defaults to GB.")
    latitude: Optional[float] = Field(None, description="The geographical latitude coordinate. Output NULL if not found.")
    longitude: Optional[float] = Field(None, description="The geographical longitude coordinate. Output NULL if not found.")

# ====================================================================
# 3. REUSABLE MODEL: CONTACT INFO 📞 (All fields optional)
# ====================================================================

class ContactInfo(BaseModel):
    
    phone: Optional[str] = Field(None, description="The primary phone number. Output NULL if not found.")
    email: Optional[EmailStr] = Field(None, description="The primary contact email address. Output NULL if not found.")
    website_url: Optional[str] = Field(None, description="The official website URL. Output NULL if not found.")


# ====================================================================
# 4. TARGET ENTITY MODEL: VENUE 🎯
# ====================================================================

# Venue now inherits all core logic and fields from BaseListing!
class Venue(BaseListing):
    """The main Venue entity, structured for API extraction."""
    
    # --- VENUE-SPECIFIC FIELDS ---
    location: Address = Field(..., description="The complete physical address details (MUST be returned as an object).")
    contact: ContactInfo = Field(..., description="The official contact details (MUST be returned as an object).")

# ====================================================================
# EXECUTION BLOCK (Generate Schema for API use)
# ====================================================================

if __name__ == "__main__":
    # Generate the minimal schema dictionary
    target_model = Venue
    venue_schema = target_model.model_json_schema()

    # Output the result
    print("--- Final Minimal Venue Schema (Token Efficient) ---")
    print(json.dumps(venue_schema, indent=2))

    # Verification: listing_id is NOT in the output schema!
    if 'listing_id' not in venue_schema['properties']:
        print("\nVerification: 'listing_id' successfully excluded from the schema.")
    else:
        print("\nVerification: ERROR - 'listing_id' was NOT excluded.")