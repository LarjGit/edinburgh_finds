import os
from typing import Any
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
        
    api_key = os.getenv(config["api_key_env"])
    if not api_key:
        raise ValueError(f"{config['api_key_env']} environment variable not set.")

    # 1. Instantiate the RAW third-party client
    raw_client = config["client_class"](api_key=api_key)
    
    # 2. Wrap the raw client in the custom adapter
    adapter = config["adapter_class"](
        client=raw_client, 
        model_name=config["model_name"]
    )
    return adapter

def test_extraction(provider_name: str):
    """Runs the data extraction test using the specified provider's adapter."""

    # SETUP ADAPTER
    llm_adapter = _get_llm_adapter(provider_name)
    
    # Extract entity with client and model passed as arguments
    listing, venue = extract_entity(
        entity_name="Craigmillar Park Tennis & Padel Club",
        entity_type="venue",
        llm_adapter=llm_adapter
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
    
    CHOSEN_PROVIDER = "perplexity"
    
    print(f"\n🚀 Starting Extraction Test using {CHOSEN_PROVIDER}\n")
    
    try:
        test_extraction(CHOSEN_PROVIDER)
    except ValueError as e:
        print(f"Configuration Error: {e}")
