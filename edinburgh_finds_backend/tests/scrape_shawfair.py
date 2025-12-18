from services.firecrawl_client import FirecrawlClient

URL = "https://www.davidlloyd.co.uk/clubs/edinburgh-shawfair/"

def main():
    client = FirecrawlClient()

    print("\n🔥 Scraping David Lloyd Edinburgh Shawfair (with stealth retry)…\n")
    result = client.scrape_with_retry(URL)

    markdown = result["data"].get("markdown", "")
    status = result["data"]["metadata"].get("statusCode")

    print(f"HTTP status returned by site: {status}")
    print("\n=== MARKDOWN (first 2000 chars) ===")
    print(markdown[:2000])
    print(f"\n--- CHAR COUNT: {len(markdown)} ---")

if __name__ == "__main__":
    main()
