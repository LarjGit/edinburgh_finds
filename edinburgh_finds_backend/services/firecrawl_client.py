import requests
from config.settings import settings


class FirecrawlClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.FIRECRAWL_API_KEY
        self.base_url = "https://api.firecrawl.dev/v2"

    # ----------------------------
    # BASIC SCRAPE with optional stealth proxy
    # ----------------------------
    def scrape(self, url: str, proxy: str | None = None) -> dict:
        payload = {"url": url}

        if proxy:
            payload["proxy"] = proxy  # "basic" | "stealth" | "auto"

        resp = requests.post(
            f"{self.base_url}/scrape",
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=90,
        )
        resp.raise_for_status()
        return resp.json()

    # ----------------------------
    # SCRAPE WITH AUTOMATIC STEALTH RETRY
    # ----------------------------
    def scrape_with_retry(self, url: str) -> dict:
        # 1. Try without stealth
        result = self.scrape(url)

        status_code = result.get("data", {}).get("metadata", {}).get("statusCode", 200)

        if status_code in [401, 403, 500]:
            # Retry with stealth
            return self.scrape(url, proxy="stealth")

        return result
