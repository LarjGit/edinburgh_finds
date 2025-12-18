# core/entity_registry.py
from typing import Dict, Set, Type
from sqlmodel import SQLModel
from database.db_models import Listing, Venue
from schemas.venue_extraction_schema import VenueSchema


def get_entity_config(entity_type: str) -> Dict[str, object]:
    """
    Return the schema + table + field alignment for a given entity type.
    """

    if entity_type == "venue":
        dto_fields: Set[str] = set(VenueSchema.model_fields.keys())
        listing_fields: Set[str] = set(Listing.model_fields.keys()) & dto_fields
        entity_fields: Set[str] = set(Venue.model_fields.keys()) & dto_fields

        return {
            "schema": VenueSchema,
            "table": Venue,
            "listing_fields": listing_fields,
            "entity_fields": entity_fields,
        }

    # --- Add future types here later ---
    # elif entity_type == "retailer":
    #     from database.db_models import Retailer
    #     from schemas.retailer_schema import RetailerSchema
    #     dto_fields = set(RetailerSchema.model_fields.keys())
    #     listing_fields = set(Listing.model_fields.keys()) & dto_fields
    #     entity_fields = set(Retailer.model_fields.keys()) & dto_fields
    #     return {
    #         "schema": RetailerSchema,
    #         "table": Retailer,
    #         "listing_fields": listing_fields,
    #         "entity_fields": entity_fields,
    #     }

    raise ValueError(f"Unsupported entity_type '{entity_type}'. Add it to entity_registry.")
