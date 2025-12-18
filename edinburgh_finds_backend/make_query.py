from utils.data_gathering_query_exporter import save_tavily_query_to_file
from schemas.venue_extraction_schema import VenueSchema  # Add others later
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python make_query.py \"Entity Name\" entity_type")
        return

    entity_name = sys.argv[1]
    entity_type = sys.argv[2]

    # Pick schema based on entity type
    schema_map = {
        "venue": VenueSchema,
        # "retailer": RetailerSchema,
        # "club": ClubSchema,
    }

    if entity_type not in schema_map:
        print(f"Unknown entity_type '{entity_type}'. Options: {list(schema_map.keys())}")
        return

    schema = schema_map[entity_type]

    path = save_tavily_query_to_file(
        entity_name=entity_name,
        entity_type=entity_type,
        model=schema,
    )

    print(f"\nQuery saved to:\n  {path}\n")
    print("Open the file → copy → paste into your LLM (Claude/Gemini/Perplexity).")


if __name__ == "__main__":
    main()
