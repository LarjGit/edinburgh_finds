import os
from typing import Any
from dotenv import load_dotenv
from perplexity import Perplexity
from anthropic import Anthropic
from services.extraction import extract_entity
from services.llm_adapters import PerplexityAdapter, AnthropicAdapter

LLM_CONFIGS = {
    "perplexity": {
        "client_class": Perplexity,
        "adapter_class": PerplexityAdapter,
        "api_key_env": "PERPLEXITY_API_KEY",
        "model_name": "sonar"
    },
    "anthropic": {
        "client_class": Anthropic,
        "adapter_class": AnthropicAdapter,
        "api_key_env": "ANTHROPIC_API_KEY",
        "model_name": "claude-sonnet-4-5"
    }
}

def _get_llm_adapter(provider_name: str) -> Any:
    """Initializes and returns the specific LLM Adapter instance."""
    
    config = LLM_CONFIGS.get(provider_name)
    if not config:
        raise ValueError(f"Unknown LLM provider: {provider_name}")
        
    load_dotenv(override=True)
    api_key = os.getenv(config["api_key_env"])
    if not api_key:
        raise ValueError(f"{config['api_key_env']} environment variable not set.")

    raw_client = config["client_class"](api_key=api_key)
    adapter = config["adapter_class"](
        client=raw_client, 
        model_name=config["model_name"]
    )
    return adapter


def test_extraction(provider_name: str, entity_name: str, entity_type: str, location: str = None):
    """Runs the data extraction test using the specified provider's adapter."""

    llm_adapter = _get_llm_adapter(provider_name)
    
    listing, venue = extract_entity(
        entity_name=entity_name,
        entity_type=entity_type,
        llm_adapter=llm_adapter,
        location=location
    )

    print("="*70)
    print("📄 LISTING DATA (from LLM)")
    print("="*70)
    print(listing.model_dump_json(indent=2))
    
    print("\n" + "="*70)
    print("📄 VENUE DATA (from LLM)")
    print("="*70)
    print(venue.model_dump_json(indent=2))
    
    return listing, venue


if __name__ == "__main__":
    
    # ========== TEST CONFIGURATION ==========
    CHOSEN_PROVIDER = "perplexity"
    TEST_ENTITY_NAME = "Craigmillar Park Tennis & Padel Club"
    TEST_ENTITY_TYPE = "venue"
    TEST_LOCATION = None  # Optional: "Edinburgh" or None
    # ========================================
    
    print(f"\n🚀 Starting Extraction Test using {CHOSEN_PROVIDER}")
    print(f"   Entity: {TEST_ENTITY_NAME}")
    print(f"   Type: {TEST_ENTITY_TYPE}\n")
    
    try:
        test_extraction(
            provider_name=CHOSEN_PROVIDER,
            entity_name=TEST_ENTITY_NAME,
            entity_type=TEST_ENTITY_TYPE,
            location=TEST_LOCATION
        )
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except Exception as e:
        print(f"❌ Extraction Error: {e}")