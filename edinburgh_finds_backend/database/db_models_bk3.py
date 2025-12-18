"""
Data models using SQLModel.

These models work as BOTH:
1. Pydantic models (validation, serialization, LLM extraction)
2. Database tables (PostgreSQL persistence)
"""
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import ARRAY, String, JSON, TIMESTAMP, Column, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from utils.id_generation import generate_listing_id, generate_slug

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

    Stores universal attributes such as:
    - identity & classification
    - location and mapping
    - contact details
    - opening hours
    - source provenance
    - extraction confidence
    """
    
    __tablename__ = "listings"
    
    # ------------------------------------------------------------------
    # IDENTIFICATION (internal)
    # ------------------------------------------------------------------
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
        description="Type of entity (venue, retailer, cafe, event, members_club, etc)",
        exclude=True
    )
    slug: str = Field(
        default=None,
        unique=True,
        index=True,
        description="URL-safe version of entity name (auto-generated)",
        exclude=True
    )

    # ------------------------------------------------------------------
    # CLASSIFICATION
    # ------------------------------------------------------------------    
    categories: Optional[List[str]] = Field(
        default=None,
        sa_column=Column(ARRAY(String)),
        description="Raw free-form categories detected by the LLM (uncontrolled labels)"
    )
    canonical_categories: Optional[List[str]] = Field(
        default=None,
        sa_column=Column(ARRAY(String)),
        description="Cleaned, controlled categories used for navigation and taxonomy",
        exclude=True
    )
     
    # ------------------------------------------------------------------
    # FLEXIBLE ATTRIBUTE BUCKET
    # ------------------------------------------------------------------    
    other_attributes: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Dictionary containing any extra attributes not explicitly defined in Listing or entity models"
    )
    
    # ------------------------------------------------------------------
    # LOCATION
    # ------------------------------------------------------------------
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
    
    # ------------------------------------------------------------------
    # CONTACT
    # ------------------------------------------------------------------
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
    
    # ------------------------------------------------------------------
    # OPENING HOURS
    # ------------------------------------------------------------------
    opening_hours: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description=(
            "Opening hours per day. May contain strings or nested open/close times. "
            "Example: {'monday': {'open': '05:30', 'close': '22:00'}, "
            "'sunday': 'CLOSED'}"
        )
    )

    # ------------------------------------------------------------------
    # SOURCE INFO
    # ------------------------------------------------------------------
    source_info: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Provenance metadata: URLs, method (tavily/manual), timestamps, notes"
    )

    # ------------------------------------------------------------------
    # EXTRACTION CONFIDENCE
    # ------------------------------------------------------------------
    field_confidence: Dict[str, float] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Per-field confidence scores used for overwrite decisions"
    )

    # ------------------------------------------------------------------
    # INTERNAL METADATA
    # ------------------------------------------------------------------
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),      # DB populates on INSERT
        ),
        exclude=True,
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),      # DB populates on INSERT
            onupdate=func.now(),            # DB auto-updates on UPDATE
        ),
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
    
    # ------------------------------------------------------------------
    # AUTO-INIT
    # ------------------------------------------------------------------
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
    Venue-specific attributes (extends Listing).
    
    Works as both Pydantic model and database table.

    Covers:
    - Racquet sports
    - Swimming
    - Gym & classes
    - Spa & wellness
    - Dining & hospitality
    - Family & kids programmes
    - Parking & transport
    - Reviews & social proof

    """
    
    __tablename__ = "venues"
    
    listing_id: str = Field(
        foreign_key="listings.listing_id",
        primary_key=True,
        ondelete="CASCADE",
        exclude=True
    )
    
    # ===========================
    # RACQUET SPORTS
    # ===========================
    tennis: Optional[bool] = Field(None)
    tennis_total_courts: Optional[int] = Field(None)
    tennis_indoor_courts: Optional[int] = Field(None)
    tennis_outdoor_courts: Optional[int] = Field(None)
    tennis_covered_courts: Optional[int] = Field(None)
    tennis_floodlit_courts: Optional[int] = Field(None)

    padel: Optional[bool] = Field(None)
    padel_total_courts: Optional[int] = Field(None)

    pickleball: Optional[bool] = Field(None)
    pickleball_total_courts: Optional[int] = Field(None)

    badminton: Optional[bool] = Field(None)
    badminton_total_courts: Optional[int] = Field(None)

    squash: Optional[bool] = Field(None)
    squash_total_courts: Optional[int] = Field(None)
    squash_glass_back_courts: Optional[int] = Field(None)

    table_tennis: Optional[bool] = Field(None)
    table_tennis_total_tables: Optional[int] = Field(None)
    
    # ===========================
    # SWIMMING
    # ===========================
    indoor_pool: Optional[bool] = Field(None)
    outdoor_pool: Optional[bool] = Field(None)
    indoor_pool_length_m: Optional[int] = Field(None)
    outdoor_pool_length_m: Optional[int] = Field(None)
    family_swim: Optional[bool] = Field(None)
    adult_only_swim: Optional[bool] = Field(None)
    swimming_lessons: Optional[bool] = Field(None)

    # ===========================
    # GYM & CLASSES
    # ===========================
    gym_available: Optional[bool] = Field(None)
    gym_size: Optional[int] = Field(None)  # station count
    classes_per_week: Optional[int] = Field(None)
    hiit_classes: Optional[bool] = Field(None)
    yoga_classes: Optional[bool] = Field(None)
    pilates_classes: Optional[bool] = Field(None)
    strength_classes: Optional[bool] = Field(None)
    cycling_studio: Optional[bool] = Field(None)
    functional_training_zone: Optional[bool] = Field(None)

    # ===========================
    # SPA & WELLNESS
    # ===========================
    spa_available: Optional[bool] = Field(None)
    sauna: Optional[bool] = Field(None)
    steam_room: Optional[bool] = Field(None)
    hydro_pool: Optional[bool] = Field(None)
    hot_tub: Optional[bool] = Field(None)
    outdoor_spa: Optional[bool] = Field(None)
    ice_cold_plunge: Optional[bool] = Field(None)
    relaxation_area: Optional[bool] = Field(None)

    # ===========================
    # DINING & HOSPITALITY
    # ===========================
    restaurant: Optional[bool] = Field(None)
    bar: Optional[bool] = Field(None)
    cafe: Optional[bool] = Field(None)
    childrens_menu: Optional[bool] = Field(None)

    # ===========================
    # FAMILY & KIDS
    # ===========================
    creche_available: Optional[bool] = Field(None)
    creche_age_min: Optional[int] = Field(None)
    creche_age_max: Optional[int] = Field(None)
    kids_swimming_lessons: Optional[bool] = Field(None)
    kids_tennis_lessons: Optional[bool] = Field(None)
    holiday_club: Optional[bool] = Field(None)
    play_area: Optional[bool] = Field(None)

    # ===========================
    # PARKING & TRANSPORT
    # ===========================
    parking_spaces: Optional[int] = Field(None)
    disabled_parking: Optional[bool] = Field(None)
    parent_child_parking: Optional[bool] = Field(None)
    ev_charging_available: Optional[bool] = Field(None)
    ev_charging_connectors: Optional[int] = Field(None)
    public_transport_nearby: Optional[bool] = Field(None)
    nearest_railway_station: Optional[str] = Field(None)

    # ===========================
    # REVIEWS & SOCIAL PROOF
    # ===========================
    average_rating: Optional[float] = Field(None)
    review_count: Optional[int] = Field(None)
    google_review_count: Optional[int] = Field(None)
    facebook_likes: Optional[int] = Field(None)

    # ===========================
    # META
    # ===========================
    field_confidence: Dict[str, float] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Per-field confidence scores used for overwrite decisions"
    )

    # Relationship back to listing
    listing: Optional[Listing] = Relationship(back_populates="venue")
