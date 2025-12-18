# services/upsert_entity.py
from typing import Any, Dict, Optional, Tuple
from sqlmodel import Session, select
from sqlalchemy.orm.attributes import flag_modified
from database.engine import engine
from database.db_models import Listing
from core.entity_registry import get_entity_config

# Minimum confidence required when replacing a value
CHANGE_MIN_CONF = 0.7

# These fields are NOT set directly via setattr
META_KEYS = {"field_confidence", "source_info"}

def _apply_meta(obj, conf: Dict[str, float] | None, src_all: Dict[str, Any] | None):
    """Merge confidence and source info without overwriting data fields."""
    # field_confidence merge
    if conf:
        if obj.field_confidence is None:
            obj.field_confidence = {}
        for k, v in conf.items():
            try:
                v = float(v)
            except Exception:
                continue
            old = obj.field_confidence.get(k)
            if old is None:
                # First time this field has been extracted → record confidence
                obj.field_confidence[k] = v
            elif v > old:
                # Confidence improved → update it
                obj.field_confidence[k] = v
            # else: do nothing (new confidence is weaker or equal)

    # source_info merge
    if src_all:
        if obj.source_info is None:
            obj.source_info = {}
        obj.source_info.update(src_all)


def _set_with_confidence(obj, field: str, new_value: Any, *, new_conf: float):
    """Apply the overwrite rule to a single field."""
    if obj.field_confidence is None:
        obj.field_confidence = {}

    old_value = getattr(obj, field, None)
    old_conf = float(obj.field_confidence.get(field, 0.0))

    # If no change in value, just increase certainty:
    if old_value == new_value:
        obj.field_confidence[field] = max(old_conf, new_conf)
        flag_modified(obj, "field_confidence")
        return False

    # Value changed → allow overwrite only if confident:
    if (new_conf > old_conf) or (new_conf >= CHANGE_MIN_CONF):
        setattr(obj, field, new_value)
        obj.field_confidence[field] = new_conf
        flag_modified(obj, "field_confidence")
        return True

    return False


def _apply_fields(obj, incoming: Dict[str, Any], *, conf: Dict[str, float] | None):
    changed_fields = []

    if obj.field_confidence is None:
        obj.field_confidence = {}

    for field, new_value in incoming.items():
        if field in META_KEYS:
            continue

        new_conf = float(conf.get(field, 0.0)) if conf else 0.0

        if _set_with_confidence(obj, field, new_value, new_conf=new_conf):
            changed_fields.append(field)

    return changed_fields


def upsert_from_schema(
    *,
    data,
    entity_type: str,
    entity_name: str,
    session: Optional[Session] = None,
) -> Tuple[Any, Any, Dict[str, list[str]]]:
    """
    Upsert Listing + entity-specific record (Venue today; Retailer later).
    """

    config = get_entity_config(entity_type)
    Schema = config["schema"]
    EntityTable = config["table"]
    listing_fields = config["listing_fields"]
    entity_fields = config["entity_fields"]

    owns_session = session is None
    if owns_session:
        session = Session(engine)

    try:
        dto_data = data.model_dump(exclude_none=True)

        conf_all = dto_data.get("field_confidence")
        src_all = dto_data.get("source_info")

        conf_listing = {k: v for k, v in (conf_all or {}).items() if k in listing_fields}
        conf_entity  = {k: v for k, v in (conf_all or {}).items() if k in entity_fields}

        update_listing = {k: v for k, v in dto_data.items() if k in listing_fields and k not in META_KEYS}
        update_entity  = {k: v for k, v in dto_data.items() if k in entity_fields and k not in META_KEYS}

        # Always enforce identity on Listing:
        update_listing["entity_name"] = entity_name 
        update_listing["entity_type"] = entity_type

        # Get or create listing
        listing = session.exec(
            select(Listing).where(
                Listing.entity_name == entity_name,
                Listing.entity_type == entity_type,
            )
        ).one_or_none()

        if listing is None:
            listing = Listing(**update_listing)
            session.add(listing)
            _apply_meta(listing, conf_listing, src_all)
            session.flush()  # ensure listing_id exists
            listing_changes = list(update_listing.keys())
        else:
            listing_changes = _apply_fields(listing, update_listing, conf=conf_listing)
            _apply_meta(listing, conf_listing, src_all)

        # Get or create entity record
        entity = session.get(EntityTable, listing.listing_id)
        if entity is None:
            entity = EntityTable(**update_entity, listing_id=listing.listing_id)
            session.add(entity)
            entity_changes = list(update_entity.keys())
        else:
            entity_changes = _apply_fields(entity, update_entity, conf=conf_entity)

        _apply_meta(entity, conf_entity, None)

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
