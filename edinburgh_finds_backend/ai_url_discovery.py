import os
from perplexity import Perplexity

# Get API key from environment
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

def get_authoritative_urls(entity_type: str, entity_name: str, max_results: int = 10):
    """
    Uses the Perplexity SDK to find authoritative URLs for a given entity.
    Returns a list of URLs.
    """
    client = Perplexity(api_key=api_key)
    query = f"Find all authoritative URLs for the {entity_type} {entity_name}"

    try:
        search_response = client.search.create(
            query=query,
            max_results=max_results
        )

        # Extract URLs safely
        urls = [r.url for r in search_response.results] if search_response.results else []
        return urls

    except Exception as e:
        print(f"Error during search: {e}")
        return []

# Example usage
if __name__ == "__main__":
    urls = get_authoritative_urls("Venue", "Edinburgh Sports Club",3)
    print("\n--- Found URLs ---")
    for u in urls:
        print(u)
