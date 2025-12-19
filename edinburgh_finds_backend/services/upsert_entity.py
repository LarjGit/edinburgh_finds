# services/upsert_entity.py
import phonenumbers
from typing import Any, Dict, Optional, Tuple
from sqlmodel import Session, select
from sqlalchemy.orm.attributes import flag_modified
from database.engine import engine
from database.db_models import Listing
from core.entity_registry import get_entity_config
from utils.category_mapping import map_categories

# Minimum confidence required when replacing a value
CHANGE_MIN_CONF = 0.7

def normalise_lat_lon(lat: float | None, lon: float | None) -> tuple[float | None, float | None]:
    if lat is not None:
        lat = round(lat, 5)
    if lon is not None:
        lon = round(lon, 5)
    return lat, lon

def normalise_phone_number(phone: str, region: str = "GB") -> Optional[str]:
    if not phone:
        return None
    try:
        parsed = phonenumbers.parse(phone, region)
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        pass
    return phone  # Return original if can't normalize

def _initialize_confidence(obj):
    """Ensure confidence dict exists."""
    if obj.field_confidence is None:
        obj.field_confidence = {}

def _set_field_with_confidence(obj, field: str, new_value: Any, new_conf: float) -> bool:
    """
    Update a single field with confidence tracking.
    Returns True if the field value changed.
    """
    _initialize_confidence(obj)
    
    old_value = getattr(obj, field, None)
    old_conf = float(obj.field_confidence.get(field, 0.0))

    # Value unchanged → just update confidence if higher
    if old_value == new_value:
        obj.field_confidence[field] = max(old_conf, new_conf)
        flag_modified(obj, "field_confidence")
        return False

    # Value changed → allow if confident enough
    if (new_conf > old_conf) or (new_conf >= CHANGE_MIN_CONF):
        setattr(obj, field, new_value)
        obj.field_confidence[field] = new_conf
        flag_modified(obj, "field_confidence")
        return True

    return False

def _apply_updates(obj, updates: Dict[str, Any], confidences: Dict[str, float]) -> list[str]:
    """
    Apply field updates with confidence tracking.
    Returns list of fields that changed.
    """
    changed = []
    
    for field, value in updates.items():
        # Get confidence for this field (default to 0.0 for non-extracted fields)
        conf = float(confidences.get(field, 0.0))
        
        if _set_field_with_confidence(obj, field, value, conf):
            changed.append(field)
    
    return changed

def _update_source_info(obj, source_info: Dict[str, Any] | None):
    """Merge source_info metadata."""
    if source_info:
        if obj.source_info is None:
            obj.source_info = {}
        obj.source_info.update(source_info)
        flag_modified(obj, "source_info")

def upsert_from_schema(
    *,
    data,
    entity_type: str,
    entity_name: str,
    session: Optional[Session] = None,
) -> Tuple[Any, Any, Dict[str, list[str]]]:
    """Upsert Listing + entity-specific record."""
    
    config = get_entity_config(entity_type)
    entity_table = config["table"]
    listing_fields = config["listing_fields"]
    entity_fields = config["entity_fields"]

    owns_session = session is None
    if owns_session:
        session = Session(engine)

    try:
        # Extract data from schema
        dto_data = data.model_dump(exclude_none=True)
        dto_confidences = dto_data.pop("field_confidence", {})
        dto_source_info = dto_data.pop("source_info", None)

        # Split into listing and entity updates
        listing_updates = {k: v for k, v in dto_data.items() if k in listing_fields}
        entity_updates = {k: v for k, v in dto_data.items() if k in entity_fields}
        
        listing_confidence_updates = {k: v for k, v in dto_confidences.items() if k in listing_fields}
        entity_confidence_updates = {k: v for k, v in dto_confidences.items() if k in entity_fields}
        
        # Map LLM categories to canonical categories
        raw_categories = listing_updates.get("categories") or []
        canonical = sorted(set(map_categories(raw_categories)))
        listing_updates["canonical_categories"] = canonical
        listing_confidence_updates["canonical_categories"] = 1.0

        # Add identity fields with full confidence (1.0)
        listing_updates["entity_name"] = entity_name
        listing_updates["entity_type"] = entity_type
        listing_confidence_updates["entity_name"] = 1.0
        listing_confidence_updates["entity_type"] = 1.0
    
        # Normalize phone numbers before processing
        if listing_updates.get("phone"):
            listing_updates["phone"] = normalise_phone_number(listing_updates["phone"])

        # Normalize lat/lon before processing
        if listing_updates.get("latitude") or listing_updates.get("longitude"):
            listing_updates["latitude"], listing_updates["longitude"] = normalise_lat_lon(
                listing_updates.get("latitude"),
                listing_updates.get("longitude"),
        )

        # === Handle Listing ===
        listing = session.exec(
            select(Listing).where(
                Listing.entity_name == entity_name,
                Listing.entity_type == entity_type,
            )
        ).one_or_none()

        if listing is None:
            # Create new listing
            listing = Listing(**listing_updates)
            _initialize_confidence(listing)
            # Set initial confidence for all fields
            for field, conf in listing_confidence_updates.items():
                listing.field_confidence[field] = conf
            if dto_source_info:
                listing.source_info = dto_source_info            
            session.add(listing)
            session.flush()
            listing_changes = list(listing_updates.keys())
        else:
            # Update existing listing
            listing_changes = _apply_updates(listing, listing_updates, listing_confidence_updates)
            _update_source_info(listing, dto_source_info)
        

        # === Handle Entity ===
        entity = session.get(entity_table, listing.listing_id)
        
        if entity is None:
            # Create new entity
            entity = entity_table(**entity_updates, listing_id=listing.listing_id)
            _initialize_confidence(entity)
            for field, conf in entity_confidence_updates.items():
                entity.field_confidence[field] = conf
            session.add(entity)
            entity_changes = list(entity_updates.keys())
        else:
            # Update existing entity
            entity_changes = _apply_updates(entity, entity_updates, entity_confidence_updates)

        session.commit()
        session.refresh(listing)
        session.refresh(entity)

        return listing, entity, {
            "listing_changes": listing_changes,
            "entity_changes": entity_changes,
        }

    finally:
        if owns_session:
            session.close()
