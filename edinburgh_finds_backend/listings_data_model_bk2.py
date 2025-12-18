# listings_data_models.py

from typing import Optional, List, Dict, Any, ClassVar
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from enum import Enum

# ====================================================================
# A. ENUM DEFINITIONS
# ====================================================================

class PrimaryCategory(str, Enum):
    """The allowed values for the primary category."""
    PADEL = "padel"
    PICKLEBALL = "pickleball"
    BOARD_GAMES = "board_games"
    TENNIS = "tennis"
    SQUASH = "squash"
    TABLE_TENNIS = "table_tennis"

# ====================================================================
# B. NEW DISCOVERY STRUCTURE 🆕
# ====================================================================

class DiscoveryItem(BaseModel):
    """A structure for a single, unclassified key-value data point."""
    key: str = Field(..., description="The label for the attribute (e.g., 'parking_cost').")
    value: Optional[Any] = Field(None, description="The value of the attribute (can be any type).")

# ====================================================================
# C. BASE MODEL (Inheritance Anchor)
# ====================================================================

class BaseListing(BaseModel):
    """Base class defining core logic, mandatory fields, and exclusion rules."""
    
    model_config = ConfigDict(
        title='Base Listing Schema',
        exclude_defaults=True
    )
    
    listing_id: Optional[str] = Field(
        None, 
        description="A unique identifier for the listing (set upon persistence).",
        json_schema_extra={'exclude': True} 
    )
    entity_name: str = Field(..., description="The name of the listing.")
    entity_type: str = Field("venue", description="The specific type of entity for the listing (fixed to 'venue').")
    primary_category: PrimaryCategory = Field(..., description="The main category the listing belongs to.")
    
    additional_categories: Optional[List[str]] = Field(None)
    
    # --- CATCH-ALL DISCOVERY FIELD (Now a list of structured items) ---
    other_attributes: List[DiscoveryItem] = Field(
        default_factory=list,
        description="A list of unique key-value attributes not covered by the main schema. Output facts only; do not include null values."
    )

# ====================================================================
# D. REUSABLE COMPONENTS
# ====================================================================

class Address(BaseModel):
    """Data model for a physical location ."""
    city: Optional[str] = Field(None, description="The city or major town. Output NULL if not found.")
    street_address: Optional[str] = Field(None, description="The full street address. Output NULL if not found.")
    postcode: Optional[str] = Field(None, description="The postal or zip code. Output NULL if not found.")
    country_code: str = Field("GB", description="The country code (e.g., GB, US). Defaults to GB.")
    latitude: Optional[float] = Field(None, description="The geographical latitude coordinate. Output NULL if not found.")
    longitude: Optional[float] = Field(None, description="The geographical longitude coordinate. Output NULL if not found.")

class ContactInfo(BaseModel):
    """Data model for communication details."""
    phone: Optional[str] = Field(None, description="The primary phone number. Output NULL if not found.")
    email: Optional[EmailStr] = Field(None, description="The primary contact email address. Output NULL if not found.")
    website_url: Optional[str] = Field(None, description="The official website URL. Output NULL if not found.")

class OpeningHours(BaseModel):

    opening_hours: List[str] = Field(default_factory=list, description="The general opening hours for a business, formatted according to Schema.org standards.")

class CourtInventory(BaseModel):
    """
    Stores aggregate inventory counts for a single sport type. 
    Uses the preferred concise Pydantic v2 Field syntax.
    """
    # ClassVar to label the data without forcing it into the serialized output
    sport: ClassVar[str] = "undefined"

    total_courts: Optional[int] = Field(None, description="Total number of courts.")
    covered_count: Optional[int] = Field(None, description="Number of covered courts.")
    floodlit_count: Optional[int] = Field(None, description="Number of floodlit courts.")
    
class TennisCourtInventory(CourtInventory):
    """Inventory for Tennis Courts."""
    sport: ClassVar[str] = "tennis"

class SquashCourtInventory(CourtInventory):
    """Inventory for Squash Courts."""
    sport: ClassVar[str] = "squash"

class PickleballCourtInventory(CourtInventory):
    """Inventory for Pickleball Courts."""
    sport: ClassVar[str] = "pickleball"

# ====================================================================
# E. TARGET ENTITY MODEL
# ====================================================================

class Venue(BaseListing):
    """The target model for Venue entity extraction."""
    location: Address = Field(default_factory=Address, description="Physical address details.")
    contact: ContactInfo = Field(default_factory=ContactInfo, description="Official contact details.")
    hours: OpeningHours = Field(default_factory=OpeningHours, description="Opening hours.")
    tennis: TennisCourtInventory = Field(
        default_factory=TennisCourtInventory, 
        description="Tennis court inventory (Optional)."
    )
    squash: SquashCourtInventory = Field(
        default_factory=SquashCourtInventory, 
        description="Squash court inventory (Optional)."
    )
    pickleball: PickleballCourtInventory = Field(
        default_factory=PickleballCourtInventory, 
        description="Pickleball court inventory (Optional)."
    )
    number_of_squash_courts: int = Field(None, description="The number of squash courts at this venue.")