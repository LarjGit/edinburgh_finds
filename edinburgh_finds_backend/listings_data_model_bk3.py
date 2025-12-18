from typing import Optional, List, Any, ClassVar
from pydantic import BaseModel, Field, EmailStr
from enum import Enum

# ====================================================================
# ENUM DEFINITIONS
# ====================================================================
class PrimaryCategory(str, Enum):
    PADEL = "padel"
    PICKLEBALL = "pickleball"
    BOARD_GAMES = "board_games"
    TENNIS = "tennis"
    SQUASH = "squash"
    TABLE_TENNIS = "table_tennis"

# ====================================================================
# DISCOVERY ITEM
# ====================================================================
class DiscoveryItem(BaseModel):
    key: str = Field(..., description="The label of the attribute.")
    value: Optional[Any] = Field(None, description="The value of the attribute (any type).")

# ====================================================================
# BASE LISTING
# ====================================================================
class BaseListing(BaseModel):
    listing_id: Optional[str] = Field(None, description="Unique identifier.")
    entity_name: str = Field(..., description="Name of the entity.")
    entity_type: str = Field(..., description="Type of entity, e.g., 'venue'.")
    primary_category: Optional[PrimaryCategory] = Field(None, description="Main category.")
    additional_categories: Optional[List[str]] = Field(None, description="Other relevant categories.")
    other_attributes: Optional[List[DiscoveryItem]] = Field(None, description="Catch-all attributes.")

# ====================================================================
# REUSABLE COMPONENTS
# ====================================================================
class Address(BaseModel):
    city: Optional[str] = Field(None, description="City where the venue is located.")
    street_address: Optional[str] = Field(None, description="Street address of the venue.")
    postcode: Optional[str] = Field(None, description="Postal code for the venue address.")
    country_code: Optional[str] = Field("GB", description="Two-letter ISO country code (default: 'GB').")
    latitude: Optional[float] = Field(None, description="Latitude coordinate of the venue.")
    longitude: Optional[float] = Field(None, description="Longitude coordinate of the venue.")

class ContactInfo(BaseModel):
    phone: Optional[str] = Field(None, description="Contact phone number.")
    email: Optional[EmailStr] = Field(None, description="Contact email address.")
    website_url: Optional[str] = Field(None, description="Official website URL.")

class OpeningHours(BaseModel):
    opening_hours: Optional[List[str]] = Field(None, description="List of human-readable opening hours, one per day or rule.")

class CourtInventory(BaseModel):
    sport: ClassVar[str] = "undefined"
    total_courts: Optional[int] = Field(None, description="Total number of courts for the sport.")
    covered_count: Optional[int] = Field(None, description="Number of covered or indoor courts.")
    floodlit_count: Optional[int] = Field(None, description="Number of floodlit courts for evening play.")

class TennisCourtInventory(CourtInventory):
    sport: ClassVar[str] = "tennis"

class SquashCourtInventory(CourtInventory):
    sport: ClassVar[str] = "squash"

class PickleballCourtInventory(CourtInventory):
    sport: ClassVar[str] = "pickleball"

class PadelCourtInventory(CourtInventory):
    sport: ClassVar[str] = "padel"

# ====================================================================
# VENUE MODEL
# ====================================================================
class Venue(BaseListing):
    location: Optional[Address] = Field(None, description="Address and geographical details of the venue.")
    contact: Optional[ContactInfo] = Field(None, description="Contact information for the venue.")
    hours: Optional[OpeningHours] = Field(None, description="Opening hours of the venue.")
    tennis: Optional[TennisCourtInventory] = Field(None, description="Inventory of tennis courts, if applicable.")
    squash: Optional[SquashCourtInventory] = Field(None, description="Inventory of squash courts, if applicable.")
    pickleball: Optional[PickleballCourtInventory] = Field(None, description="Inventory of pickleball courts, if applicable.")
    padel: Optional[PadelCourtInventory] = Field(None, description="Inventory of padel courts, if applicable.")
    number_of_squash_courts: Optional[int] = Field(None, description="Total number of squash courts available at the venue.")
