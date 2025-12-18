# main.py

import argparse
import json
from pathlib import Path

from services.extraction_pipeline import process_raw_text
from schemas.venue_extraction_schema import VenueSchema 

def main():
    parser = argparse.ArgumentParser(description="Edinburgh Finds — Extraction Pipeline")
    parser.add_argument("--entity-name", required=True)
    parser.add_argument("--entity-type", required=True, choices=["venue", "club", "retailer"])
    parser.add_argument("--file", help="Optional path to a raw text file")
    args = parser.parse_args()

    entity_type = args.entity_type
    entity_name = args.entity_name

    # ------------------------------------------
    # MANUAL INPUT MODE
    # ------------------------------------------
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Raw text file not found: {file_path}")

        print(f"\n📄 Using manual raw text file: {file_path} for {entity_type} {entity_name}")
        raw_text = file_path.read_text(encoding="utf-8")

        result = process_raw_text(
            entity_name=entity_name,
            entity_type=entity_type,
            raw_text=raw_text,
            source_type="manual_file"
        )

        print("\nCOMPLETED (Manual File Mode)")
        return

if __name__ == "__main__":
    main()
