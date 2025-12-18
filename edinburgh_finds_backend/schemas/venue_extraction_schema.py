"""
Dynamically derived Pydantic schema for Venue extraction and validation.

This schema is generated directly from the SQLModel database definitions
(Venue + Listing), removing SQLAlchemy-specific and excluded fields.
It provides a safe, pure Pydantic model for use with Instructor and APIs.
"""

from database.db_models import Venue, Listing
from utils.model_conversion import to_pydantic_model

# ✅ Dynamically generate a pure Pydantic model
VenueSchema = to_pydantic_model([Listing, Venue])
