from services.firecrawl_client import FirecrawlClient

URL = "https://www.davidlloyd.co.uk/clubs/edinburgh-shawfair/"

def main():
    client = FirecrawlClient()

    print("\n🔥 Crawling David Lloyd Edinburgh Shawfair…\n")
    result = client.crawl(URL, max_pages=10)

    pages = result.get("data", [])
    print(f"Pages crawled: {len(pages)}\n")

    for i, page in enumerate(pages, start=1):
        url = page.get("metadata", {}).get("sourceURL") or page.get("url", "")
        md = page.get("markdown", "") or ""
        print("=" * 80)
        print(f"Page {i}: {url}")
        print(f"Length: {len(md)} chars")
        print(md[:1000])
        print("\n--- PAGE TRUNCATED ---\n")

if __name__ == "__main__":
    main()
