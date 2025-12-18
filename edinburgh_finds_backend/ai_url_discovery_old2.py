import os
import httpx

# Get API key from environment
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

def get_authoritative_urls(entity_type: str, entity_name: str, max_results: int = 10):
    
    query = f"Find all authoritative URLs related to the {entity_type} {entity_name}"
    url = "https://api.perplexity.ai/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "max_results": max_results
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        # Extract URLs safely
        urls = [item["url"] for item in data.get("results", []) if "url" in item]
        return urls

    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        print(e.response.text)
        return []
    except Exception as e:
        print(f"Other error: {e}")
        return []

# Example usage
if __name__ == "__main__":
    urls = get_authoritative_urls("Venue", "Edinburgh Sports Club")
    print("\n--- Found URLs ---")
    for u in urls:
        print(u)
