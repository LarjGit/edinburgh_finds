import uuid
from typing import Optional
from listings_data_model import Venue
from data_extraction import extract_entity_data
import pprint

def run_pipeline(name: str, entity_type: str, max_urls: int):
    final_data: Optional[Venue] = extract_entity_data(name, entity_type, max_urls)
    if final_data:
        final_data.listing_id = str(uuid.uuid4())
        print("\n" + "="*50)
        print("✅ FINAL VALIDATED EXTRACTION OUTPUT (Augmented)")
        print("="*50)
        print(f"Assigned ID: {final_data.listing_id}")
        pprint.pprint(final_data.model_dump(exclude_none=True))
    else:
        print(f"\n❌ Pipeline failed for {name}.")

if __name__ == "__main__":
    run_pipeline(
        name="David Lloyd Club Edinburgh Shawfair",
        entity_type="venue",
        max_urls=10
    )
