# main.py

import pprint
import uuid
from typing import Optional
import os
import sys

# Add the project root to the path for importing (Good practice for local modules)
# This assumes data_extraction.py and listings_data_model.py are in the same folder
# If your code throws an ImportError, you may need to manually run:
# sys.path.append(os.path.dirname(__file__)) 

from data_extraction import extract_entity_data 
from listings_data_model import Venue 

def run_pipeline(name: str, entity_type: str, max_urls: int):
    """
    Runs the full workflow by calling the extraction layer and printing the final, 
    persisted-ready object.
    """
    
    print(f"--- Starting Pipeline for: {name} ({entity_type}) ---")
    
    # 1. Execute Extraction
    final_data: Optional[Venue] = extract_entity_data(
        entity_name=name, 
        entity_type=entity_type,
        max_urls=max_urls
    )
    
    if final_data:
        print("\n" + "="*50)
        print("✅ FINAL VALIDATED EXTRACTION OUTPUT (Augmented)")
        print("="*50)
        
        # 2. Persistence Step: Inject the final, unique ID
        # The ID is generated here as the last step before saving.
        final_data.listing_id = str(uuid.uuid4()) 
        
        # 3. Print the clean, finalized object
        print(f"Assigned ID: {final_data.listing_id}")
        
        # model_dump(exclude_none=True) cleans up the output
        pprint.pprint(final_data.model_dump(exclude_none=True))
    
    else:
        print(f"\n❌ Pipeline failed to produce valid data for {name}.")

if __name__ == "__main__":
    # --- The Simple Call ---
    URL_LIMIT = 1 # Use a low number to save tokens during testing

    run_pipeline(
        name="Edinburgh Sports Club", 
        entity_type="Venue",
        max_urls=URL_LIMIT
    )