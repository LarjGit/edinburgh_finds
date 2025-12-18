from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field, EmailStr

# ====================================================================
# BASE LISTING
# ====================================================================
class BaseListing(BaseModel):
    """Base fields that ALL entity types share"""
    listing_id: Optional[str] = Field(None, description="Unique identifier")
    entity_name: str = Field(..., description="Name of the entity")
    entity_type: str = Field(..., description="Type of entity e.g., 'venue', 'retailer', cafe")
    categories: Optional[List[str]] = Field(None, description="All relevant categories/sports/activities (e.g., padel, pickleball, tennis, board_games)")
    other_attributes: Optional[Dict[str, Any]] = Field(None, description="Additional attributes that don't fit standard fields")

# ====================================================================
# REUSABLE COMPONENTS
# ====================================================================
class LocationMixin(BaseModel):
    sub_building_name: Optional[str] = Field(default=None, description="Flat, unit, or department name/number (e.g., 'Flat 2', 'Unit A').")
    building_name: Optional[str] = Field(default=None, description="The main name of the building (e.g., 'Victoria House').")
    building_number: Optional[str] = Field(default=None, description="The street-level house or main building number (e.g., '145').")
    thoroughfare: Optional[str] = Field(default=None, description="Primary street name.")
    post_town: Optional[str] = Field(default=None, description="The mandatory postal town name (recommended to be stored in all caps).")
    postcode: Optional[str] = Field(default=None, description="The full, correctly spaced UK postcode (e.g., 'SW1A 0AA').")
    country: Optional[str] = Field(default='UNITED KINGDOM', description="The country (defaults to 'UNITED KINGDOM').")
    latitude: Optional[float] = Field(default=None, description="The WGS84 Latitude coordinate (decimal degrees).")
    longitude: Optional[float] = Field(default=None, description="The WGS84 Longitude coordinate (decimal degrees).")

class ContactMixin(BaseModel):
    phone_number: Optional[str] = Field(default=None, description="The primary, publicly-listed contact phone number for the venue (e.g., +44 20 7946 0000).")
    email: Optional[EmailStr] = Field(None, description="The primary public email address (e.g., info@venue.co.uk).")
    website: Optional[str] = Field(default=None, description="The official, main website URL.")
    social_instagram: Optional[str] = Field(default=None, description="The Instagram handle or full profile URL.")
    social_facebook: Optional[str] = Field(default=None, description="The Facebook page URL.")
    social_twitter: Optional[str] = Field(default=None, description="The Twitter (X) handle or full profile URL.")
    social_linkedin: Optional[str] = Field(default=None, description="The LinkedIn company page URL (more relevant for B2B/Corporate).")
    
class OpeningHoursMixin(BaseModel):
    opening_hours: Optional[List[str]] = Field(None, description="List of human-readable opening hours, one per day or rule.")

# ====================================================================
# ENTITY MODELS
# ====================================================================
class Venue(BaseListing, LocationMixin, ContactMixin, OpeningHoursMixin):
    # Tennis facilities
    tennis_total_courts: Optional[int] = Field(None, description="Total tennis courts")
    tennis_covered_courts: Optional[int] = Field(None, description="Total indoor tennis courts")
    tennis_floodlit_courts: Optional[int] = Field(None, description="Total flodlit tennis courts")
    
    # Padel facilities
    padel_total_courts: Optional[int] = Field(None, description="Total padel courts")
    padel_covered_courts: Optional[int] = Field(None, description="Total indoor padel courts")
    padel_floodlit_courts: Optional[int] = Field(None, description="Total floodlit padel courts")
    
    # Squash facilities
    squash_total_courts: Optional[int] = Field(None, description="Total squash courts")
    squash_covered_courts: Optional[int] = Field(None, description="Total indoor squash courts")
    
    # Pickleball facilities
    pickleball_total_courts: Optional[int] = Field(None, description="Total pickleball courts")
    pickleball_covered_courts: Optional[int] = Field(None, description="Total indoor pickleball courts")
