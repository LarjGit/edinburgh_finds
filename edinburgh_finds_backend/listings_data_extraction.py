import os
import json
from typing import Optional, List, Dict, Any
from listings_data_model import Venue
from perplexity import Perplexity

API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not API_KEY:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

CLIENT = Perplexity(api_key=API_KEY)
API_MODEL_NAME = "sonar"

MODEL_CLASS_MAP = {
    "venue": Venue
}

# ---------------------------
# MAIN EXTRACTION
# ---------------------------
def extract_entity(entity_name: str, entity_type: str, max_urls: int) -> Optional[Venue]:
    urls = discover_urls(entity_name, entity_type, max_urls)
    if not urls:
        return None
    return progressively_augment_data(urls, entity_name, entity_type)
