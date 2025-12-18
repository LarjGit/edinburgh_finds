from tavily import TavilyClient
from config.settings import settings

class TavilySearch:
    """Wrapper around TavilyClient for search + content extraction."""

    def __init__(self):
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def search_urls(self, query: str, max_results: int = 10, min_score: float = 0.7) -> list[str]:
        """
        Perform a Tavily search and return a list of filtered URLs based on score.
        Only URLs with score >= min_score are kept.
        """
        try:
            results = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results
            )

            # Collect all results with score
            urls_with_scores = [
                (item.get("url"), item.get("score", 0.0))
                for item in results.get("results", [])
                if item.get("url")
            ]

            # Filter by score threshold
            filtered_urls = [u for u, s in urls_with_scores if s >= min_score]
            discarded = [u for u, s in urls_with_scores if s < min_score]

            # Simple log
            print(f"\n Found {len(urls_with_scores)} total results")
            print(f"Keeping {len(filtered_urls)} (score ≥ {min_score})")
            print(f"Discarding {len(discarded)} low-score results")

            return filtered_urls

        except Exception as e:
            print(f"Tavily search failed: {e}")
            return []

    def extract(self, urls: list[str]) -> dict:
        """Extract raw content from URLs."""
        try:
            resp = self.client.extract(urls=urls)
            return resp["results"]
        except Exception as e:
            print(f"Tavily extraction failed: {e}")
            return {}
