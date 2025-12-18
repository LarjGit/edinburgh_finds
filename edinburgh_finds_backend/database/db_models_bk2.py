"""
Data models using SQLModel.

These models work as BOTH:
1. Pydantic models (validation, serialization, LLM extraction)
2. Database tables (PostgreSQL persistence)
"""
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import ARRAY, String, JSON, TIMESTAMP
from datetime import datetime
from utils.id_generation import generate_listing_id, generate_slug
from database.enums import Category

# ====================================================================
# LISTINGS TABLE - Common fields for all entity types
# ====================================================================

class Listing(SQLModel, table=True):
    """
    Main listings table containing fields common to all entity types.
    
    This single class serves multiple purposes:
    - Pydantic model for validation and LLM extraction
    - Database table for PostgreSQL persistence
    - JSON schema generation (DB metadata automatically excluded)
    """
    
    __tablename__ = "listings"
    
    # Primary identification
    listing_id: str = Field(
        default=None,
        primary_key=True,
        description="Unique identifier (auto-generated)",
        exclude=True
    )
    entity_name: str = Field(
        ...,
        index=True,
        description="Official name of the entity",
        exclude=True
    )
    entity_type: str = Field(
        ...,
        index=True,
        description="Type of entity (venue, retailer, cafe, members_club)",
        exclude=True
    )
    slug: str = Field(
        default=None,
        unique=True,
        index=True,
        description="URL-friendly slug (auto-generated)",
        exclude=True
    )
    categories: Optional[List[Category]] = Field(
        default=None,
        sa_column=Column(ARRAY(String)),
        description="All relevant categories/sports/activities. Only include categories from the predefined Category enum."
    )
    other_categories: Optional[List[str]] = Field(
        default=None,
        sa_column=Column(ARRAY(String)),
        description="A list of additional activity labels or sports mentioned in the text that are not part of the primary Category enum."
    )
    other_attributes: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="All other additional attributes that you find that are not specified"
    )
    
    # Location fields
    street_address: Optional[str] = Field(
        None,
        description="Full street address including building number and street name"
    )
    city: Optional[str] = Field(
        None,
        index=True,
        description="City or town"
    )
    postcode: Optional[str] = Field(
        None,
        index=True,
        description="Full UK postcode with correct spacing (e.g., 'SW1A 0AA')"
    )
    country: Optional[str] = Field(
        None,
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
    
    # Contact fields
    phone: Optional[str] = Field(
        None,
        description="Primary contact phone number with country code. MUST be E.164 UK format (e.g. '+441315397071')"
    )
    email: Optional[str] = Field(
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
    
    # Opening hours
    opening_hours: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description=(
            "Opening hours. Example: {'monday': {'open': '09:00', 'close': '17:00'}, 'sunday': 'CLOSED'}"
        )
    )

    # Stores Tavily URLs + meta
    source_info: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Provenance: URLs, search method, timestamps"
    )

    # Stores per-field extraction confidence
    field_confidence: Dict[str, float] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Per-field confidence scores used for overwrite decisions"
    )

    # Metadata (internal - excluded from LLM extraction)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(TIMESTAMP, nullable=False,),
        exclude=True
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(TIMESTAMP, nullable=False),
        exclude=True
    )
    external_ids: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="External system IDs (e.g., {'wordpress': 123, 'google': 'abc'})",
        exclude=True
    )
    
    # Relationships (NOT database columns - Python helpers for joins)
    venue: Optional["Venue"] = Relationship(back_populates="listing")
    
    def __init__(self, **data):
        """Auto-generate listing_id and slug if not provided."""
        super().__init__(**data)
        
        if not self.listing_id:
            self.listing_id = generate_listing_id(self.entity_type)
        
        if not self.slug:
            self.slug = generate_slug(self.entity_name)

# ====================================================================
# ENTITY-SPECIFIC TABLES
# ====================================================================

class Venue(SQLModel, table=True):
    """
    Venues table - contains venue-specific attributes only.
    
    Works as both Pydantic model and database table.
    """
    
    __tablename__ = "venues"
    
    listing_id: str = Field(
        foreign_key="listings.listing_id",
        primary_key=True,
        ondelete="CASCADE",
        exclude=True
    )
    
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

    bar: Optional[bool] = Field(
        None,
        description="Does this venue have a bar"
    )

    restaurant: Optional[bool] = Field(
        None,
        description="Does this venue have a restaurant"
    )

    # Stores per-field extraction confidence
    field_confidence: Dict[str, float] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Per-field confidence scores used for overwrite decisions"
    )

    # Relationship back to listing
    listing: Optional[Listing] = Relationship(back_populates="venue")
