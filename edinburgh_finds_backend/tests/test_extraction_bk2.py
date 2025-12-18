from services.extraction import extract_entity, get_extraction_schema
from models.models import Listing, Venue
import json

def test_extraction():
    
    # First, inspect the schema being sent
    print("\n" + "="*70)
    print("🔍 INSPECTING SCHEMA SENT TO API")
    print("="*70)
    
    schema = get_extraction_schema(Listing, Venue)
    print(json.dumps(schema, indent=2))
    
    print("\n" + "="*70)
    print("📊 SCHEMA STATISTICS")
    print("="*70)
    print(f"Total fields: {len(schema['properties'])}")
    print(f"Field names: {list(schema['properties'].keys())}")
    
    # Then run extraction
    print("\n" + "="*70)
    print("🚀 STARTING EXTRACTION")
    print("="*70)
    
    listing, venue = extract_entity(
        entity_name="David Lloyd Club Edinburgh Shawfair",
        entity_type="venue"
    )
    
    print("\n" + "="*70)
    print("📄 LISTING DATA (from LLM)")
    print("="*70)
    print(listing.model_dump_json(indent=2))
    
    print("\n" + "="*70)
    print("📄 VENUE DATA (from LLM)")
    print("="*70)
    print(venue.model_dump_json(indent=2))

if __name__ == "__main__":

    print("\n🚀 Starting Extraction Test\n")
    
    test_extraction()