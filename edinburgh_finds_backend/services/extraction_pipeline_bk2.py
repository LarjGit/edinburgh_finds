# services/extraction_pipeline.py

import json
from datetime import datetime
from pathlib import Path
from schemas.venue_extraction_schema import VenueSchema
from services.instructor_client import instructor_client
from services.upsert_entity import upsert_from_schema
from utils.prompt_builder import generate_system_prompt
from config.settings import settings

# --- folder structure helper ---
def get_entity_dirs(entity_type: str, entity_slug: str):
    base = Path("data") / entity_type / entity_slug

    paths = {
        "raw": base / "raw",
        "condense": base / "condense",
        "extract": base / "extract",
        "processed": base / "processed",
        "base": base,
    }
    # create all dirs
    for p in paths.values():
        p.mkdir(parents=True, exist_ok=True)
    return paths

def process_raw_text(
    entity_name: str,
    entity_type: str,
    raw_text: str,
    source_type: str = "unknown"
):
    """
    Core extraction pipeline:
        raw_text → LLM extraction → structured DTO → DB upsert → JSON + debug logs

    This is the single unified pipeline used by:
        - main.py (Tavily or manual single file)
        - services/extraction.py (batch raw-text folder)
    """

    print(f"\n🔧 Running extraction pipeline for '{entity_name}' ({entity_type})")
    print(f"   Source type: {source_type}")

    # -------------------------------
    # slug creation (simple + safe)
    # -------------------------------
    entity_slug = (
        entity_name.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("'", "")
    )

    # -------------------------------
    # ensure folder structure exists
    # -------------------------------
    dirs = get_entity_dirs(f"{entity_type}s", entity_slug)
    
    # -----------------------------------------------------
    # Build the system prompt from your Pydantic schema
    # -----------------------------------------------------
    system_message = generate_system_prompt(
        entity_name=entity_name,
        entity_type=entity_type,
        model=VenueSchema,
    )

    # -----------------------------------------------------
    # Call the LLM (Instructor client enforces schema)
    # -----------------------------------------------------
    dto = instructor_client.chat.completions.create(
        model=settings.LLM_MODEL,
        response_model=VenueSchema,
        max_tokens=30000,   # REQUIRED for long schemas
        temperature=0,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": raw_text},
        ],
    )

    # -----------------------------------------------------
    # Inject provenance into the DTO
    # -----------------------------------------------------
    dto.source_info = {
        "sources": [source_type],
        "note": f"Raw text processed on {datetime.now():%Y-%m-%d %H:%M:%S}"
    }

    # -----------------------------------------------------
    # Persist into the database (Listing + Entity)
    # -----------------------------------------------------
    listing, entity, report = upsert_from_schema(
        data=dto,
        entity_name=entity_name,
        entity_type=entity_type,
    )

    # ---------------------------------------------------
    # Save processed JSON 
    # ---------------------------------------------------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_json = dirs["processed"] / f"{entity_slug}__processed__{timestamp}.json"

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(
            {
                "listing": listing.model_dump(),
                "entity": entity.model_dump(),
                "extraction_report": report,
                "source_type": source_type,
            },
            f,
            indent=2
        )

    print(f"📄 Saved structured JSON → {output_json}")

    # -----------------------------------------------------
    # Save raw text snapshot for reproducibility/debug
    # -----------------------------------------------------
    raw_log = dirs["raw"] / f"{entity_slug}__raw__{timestamp}.txt"
    raw_log.write_text(raw_text, encoding="utf-8")
    
    print(f"🧾 Saved debug raw text snapshot into {raw_log}")

    # -----------------------------------------------------
    # Return results
    # -----------------------------------------------------
    return {
        "listing": listing,
        "entity": entity,
        "report": report,
        "json_path": str(output_json),
        "log_path": str(raw_log),
    }
