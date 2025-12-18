"""
Pydantic models for business logic and API extraction.
"""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from utils.id_generation import generate_listing_id, generate_slug

# ====================================================================
# CORE MIXINS - Fields shared by ALL entities
# ====================================================================

class BaseCoreMixin(BaseModel):
    """Base identification and categorization fields."""
    listing_id: Optional[str] = Field(
        None,
        description="Unique identifier (auto-generated)"
    )
    entity_name: str = Field(
        ...,
        description="Official name of the entity"
    )
    entity_type: str = Field(
        ...,
        description="Type of entity (venue, retailer, cafe, members_club)"
    )
    categories: Optional[List[str]] = Field(
        None,
        description="All relevant categories/sports/activities (e.g., ['padel', 'pickleball', 'tennis'])"
    )
    other_attributes: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional attributes that don't fit standard fields"
    )
    slug: Optional[str] = Field(
        None,
        description="URL-friendly slug (auto-generated)"
    )

class LocationCoreMixin(BaseModel):
    """Location and address fields."""
    # Primary address fields (for LLM extraction)
    street_address: Optional[str] = Field(
        None,
        description="Full street address including building number and street name"
    )
    city: Optional[str] = Field(
        None,
        description="City or town"
    )
    postcode: Optional[str] = Field(
        None,
        description="Full UK postcode with correct spacing (e.g., 'SW1A 0AA')"
    )
    country: Optional[str] = Field(
        default='UNITED KINGDOM',
        description="Country name"
    )
    latitude: Optional[float] = Field(
        None,
        description="WGS84 Latitude coordinate (decimal degrees)"
    )
    longitude: Optional[float] = Field(
        None,
        description="WGS84 Longitude coordinate (decimal degrees)"
    )
    
    # Detailed address components (optional - for future parsing)
    sub_building_name: Optional[str] = Field(
        None,
        description="Flat, unit, or department number"
    )
    building_name: Optional[str] = Field(
        None,
        description="Building name"
    )
    building_number: Optional[str] = Field(
        None,
        description="Street number"
    )
    thoroughfare: Optional[str] = Field(
        None,
        description="Street name"
    )
    post_town: Optional[str] = Field(
        None,
        description="Postal town name"
    )

class ContactCoreMixin(BaseModel):
    """Contact and social media fields."""
    phone: Optional[str] = Field(
        None,
        description="Primary contact phone number with country code (e.g., '+44 20 7946 0000')"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Primary public email address"
    )
    website_url: Optional[str] = Field(
        None,
        description="Official website URL"
    )
    instagram_url: Optional[str] = Field(
        None,
        description="Instagram profile URL or handle"
    )
    facebook_url: Optional[str] = Field(
        None,
        description="Facebook page URL"
    )
    twitter_url: Optional[str] = Field(
        None,
        description="Twitter/X profile URL or handle"
    )
    linkedin_url: Optional[str] = Field(
        None,
        description="LinkedIn company page URL"
    )

class OpeningHoursCoreMixin(BaseModel):
    """Opening hours information."""
    opening_hours: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Structured opening hours. Keys must be lowercase weekday names "
            "(e.g., 'monday', 'tuesday'). Values should be objects with 'open' "
            "and 'close' times in 24-hour HH:MM format, or the string 'CLOSED'. "
            "Example: {'monday': {'open': '09:00', 'close': '17:00'}, 'sunday': 'CLOSED'}"
        )
    )

class MetadataCoreMixin(BaseModel):
    """Internal metadata fields (not for LLM extraction)."""
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Record creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp"
    )
    external_ids: Optional[Dict[str, Any]] = Field(
        None,
        description="External system IDs (e.g., {'wordpress': 123, 'google': 'abc'})"
    )

# ====================================================================
# CORE LISTING - Base for all entities
# ====================================================================

class CoreListing(
    BaseCoreMixin,
    LocationCoreMixin,
    ContactCoreMixin,
    OpeningHoursCoreMixin,
    MetadataCoreMixin
):
    """
    Core listing model containing all common fields.
    Maps to 'listings' table in database.
    """
    
    def __init__(self, **data):
        super().__init__(**data)
        
        # Auto-generate listing_id if not provided
        if not self.listing_id:
            self.listing_id = generate_listing_id(self.entity_type)
        
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = generate_slug(self.entity_name)

# ====================================================================
# ENTITY-SPECIFIC ATTRIBUTES
# ====================================================================

class VenueAttributes(BaseModel):
    """
    Venue-specific attributes.
    Maps to 'venues' table in database.
    """
    # Tennis facilities
    tennis_total_courts: Optional[int] = Field(
        None,
        description="Total number of tennis courts"
    )
    tennis_covered_courts: Optional[int] = Field(
        None,
        description="Number of indoor/covered tennis courts"
    )
    tennis_floodlit_courts: Optional[int] = Field(
        None,
        description="Number of floodlit tennis courts"
    )
    
    # Padel facilities
    padel_total_courts: Optional[int] = Field(
        None,
        description="Total number of padel courts"
    )
    padel_covered_courts: Optional[int] = Field(
        None,
        description="Number of indoor/covered padel courts"
    )
    padel_floodlit_courts: Optional[int] = Field(
        None,
        description="Number of floodlit padel courts"
    )
    
    # Squash facilities
    squash_total_courts: Optional[int] = Field(
        None,
        description="Total number of squash courts"
    )
    squash_covered_courts: Optional[int] = Field(
        None,
        description="Number of indoor/covered squash courts"
    )
    
    # Pickleball facilities
    pickleball_total_courts: Optional[int] = Field(
        None,
        description="Total number of pickleball courts"
    )
    pickleball_covered_courts: Optional[int] = Field(
        None,
        description="Number of indoor/covered pickleball courts"
    )
    
    # Table tennis
    table_tennis_total_tables: Optional[int] = Field(
        None,
        description="Total number of table tennis tables"
    )

# ====================================================================
# COMPLETE ENTITY MODELS
# ====================================================================

class Venue(CoreListing, VenueAttributes):
    """
    Complete venue model.
    Combines core listing fields with venue-specific attributes.
    """
    pass

