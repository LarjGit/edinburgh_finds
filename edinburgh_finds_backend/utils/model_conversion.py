from sqlmodel import SQLModel
from pydantic import create_model

def to_pydantic_model(sqlmodels: list[type[SQLModel]]) -> type:
    """
    Combine multiple SQLModel classes into a single pure Pydantic model.
    Uses the `exclude=True` flag as the only signal for skipping fields.
    """
    fields = {}
    for cls in sqlmodels:
        for name, field in cls.model_fields.items():
            # ✅ Skip only fields explicitly marked as excluded
            if getattr(field, "exclude", False):
                continue
            if name not in fields:
                fields[name] = (field.annotation, field.default)

    return create_model("VenueSchema", **fields)
