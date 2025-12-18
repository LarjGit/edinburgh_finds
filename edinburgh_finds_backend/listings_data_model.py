from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class BaseCoreMixin(BaseModel):
    """Base fields."""
    listing_id: Optional[str] = Field(None, description="Unique identifier (PK). Must be a standardized UUID or equivalent.")
    entity_name: str = Field(..., description="Name of the entity.")
    entity_type: str = Field(..., description="Type of entity. Must be one of the pre-defined values: 'venue', 'retailer', 'cafe', etc.")
    categories: Optional[List[str]] = Field(None, description="All relevant categories/sports/activities. Provide as a list of lowercase strings (e.g., ['padel', 'pickleball', 'tennis']).")
    other_attributes: Optional[Dict[str, Any]] = Field(None, description="Additional attributes (maps to JSONB).")
    slug: Optional[str] = Field(None, description="A URL-friendly, unique slug. Must be entirely lowercase, using only hyphens (-) as separators (e.g., 'manchester-padel-club').")
    
class LocationCoreMixin(BaseModel):
    """All location/address fields."""
    street_address: Optional[str] = Field(None, description="Full street address including building number, name, and street.")
    city: Optional[str] = Field(None, description="City or town (key search field).")
    postcode: Optional[str] = Field(None, description="Full UK postcode. Must be correctly formatted with a single space (e.g., 'SW1A 0AA').")
    country: Optional[str] = Field(default='UNITED KINGDOM', description="Country.")
    latitude: Optional[float] = Field(default=None, description="The WGS84 Latitude coordinate. Must be a decimal number with 6 to 8 places of precision.")
    longitude: Optional[float] = Field(default=None, description="The WGS84 Longitude coordinate. Must be a decimal number with 6 to 8 places of precision.")
    
    # Detailed components
    sub_building_name: Optional[str] = Field(default=None, description="Flat, unit, or department name/number.")
    building_name: Optional[str] = Field(default=None, description="The main name of the building.")
    building_number: Optional[str] = Field(default=None, description="The street-level house or main building number.")
    thoroughfare: Optional[str] = Field(default=None, description="Primary street name.")
    post_town: Optional[str] = Field(default=None, description="The mandatory postal town name.")

class ContactCoreMixin(BaseModel):
    """All contact and social media fields."""
    phone: Optional[str] = Field(default=None, description="The primary, publicly-listed contact phone number. Must include the country code (e.g., '+44 20 7946 0000').")
    email: Optional[EmailStr] = Field(None, description="The primary public email address.")
    website_url: Optional[str] = Field(default=None, description="The official, main website URL.")
    instagram_url: Optional[str] = Field(default=None, description="The Instagram handle or full profile URL.")
    facebook_url: Optional[str] = Field(default=None, description="The Facebook page URL.")
    twitter_url: Optional[str] = Field(default=None, description="The Twitter (X) handle or full profile URL.")
    linkedin_url: Optional[str] = Field(default=None, description="The LinkedIn company page URL.")
    
class OpeningHoursCoreMixin(BaseModel):
    """Opening hours data (maps to JSONB or a structured array)."""
    opening_hours: Optional[Dict[str, Any]] = Field(None, description="Structured opening hours dictionary. Keys MUST be the full English weekday names (e.g., 'monday', 'tuesday'). Values must be an object with 'open' and 'close' times in 24-hour HH:MM format. If the venue is closed, the value MUST be the literal string 'CLOSED'.") 
    
class MetadataCoreMixin(BaseModel):
    """Metadata fields from the DB schema."""
    created_at: Optional[datetime] = Field(None, description="Creation timestamp. Provide as an ISO 8601 string (e.g., 'YYYY-MM-DDTHH:MM:SSZ').")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp. Provide as an ISO 8601 string (e.g., 'YYYY-MM-DDTHH:MM:SSZ').")
    external_ids: Optional[Dict[str, Any]] = Field(None, description="External IDs (maps to JSONB).")

class CoreListing(BaseCoreMixin, LocationCoreMixin, ContactCoreMixin, OpeningHoursCoreMixin, MetadataCoreMixin):
    """The core model common to all entity types."""
    pass

class VenueAttributes(BaseModel):
    """Attributes unique to the 'venues' table."""
    # Tennis facilities
    tennis_total_courts: Optional[int] = Field(None, description="Total tennis courts")
    tennis_covered_courts: Optional[int] = Field(None, description="Total indoor tennis courts")
    tennis_floodlit_courts: Optional[int] = Field(None, description="Total floodlit tennis courts")
    
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

class Venue(CoreListing, VenueAttributes):
        """Complete venue model"""
        pass

