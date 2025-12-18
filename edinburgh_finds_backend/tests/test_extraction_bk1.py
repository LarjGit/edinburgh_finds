from services.extraction import extract_entity

def test_extraction():

    # Extract entity
    listing, venue = extract_entity(
        entity_name="Craigmillar Park Tennis & Padel Club",
        entity_type="venue"
    )

    print("="*70)
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
