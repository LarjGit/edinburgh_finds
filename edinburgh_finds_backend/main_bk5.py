# main.py

import argparse
import json
from pathlib import Path

from services.tavily_client import TavilySearch
from utils.prompt_builder import generate_tavily_query
from utils.query_compressor import compress_query_with_gemini
from services.extraction_pipeline import process_raw_text
from schemas.venue_extraction_schema import VenueSchema 

def gather_source_data(query: str, min_score: float = 0.6, max_results: int = 20) -> str:
    tavily = TavilySearch()
    urls = tavily.search_urls(query=query, max_results=max_results, min_score=min_score)

    print("\n Filtered Tavily URLs:")
    for url in urls:
        print(url)

    print("\n Extracting content...")
    results = tavily.extract(urls)
    all_text_blocks = [item.get("raw_content", "") for item in results]
    concatenated_block = "\n\n".join(all_text_blocks)

    return concatenated_block

def main():
    parser = argparse.ArgumentParser(description="Edinburgh Finds — Extraction Pipeline")
    parser.add_argument("--entity-name", required=True)
    parser.add_argument("--entity-type", required=True, choices=["venue", "club", "retailer"])
    parser.add_argument("--file", help="Optional path to a raw text file")
    args = parser.parse_args()

    entity_type = args.entity_type
    entity_name = args.entity_name

    # ------------------------------------------
    # MANUAL INPUT MODE
    # ------------------------------------------
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            raise FileNotFoundError(f"Raw text file not found: {file_path}")

        print(f"\n📄 Using manual raw text file: {file_path} for {entity_type} {entity_name}")
        raw_text = file_path.read_text(encoding="utf-8")

        result = process_raw_text(
            entity_name=entity_name,
            entity_type=entity_type,
            raw_text=raw_text,
            source_type="manual_file"
        )

        print("\nCOMPLETED (Manual File Mode)")
        return

    # ------------------------------------------
    # AUTOMATED MODE (Tavily → Gemini → Extraction)
    # ------------------------------------------
    print(f"\n🌐 Running Tavily search for: {entity_type} {entity_name}")

    # Build and compress Tavily query
    tavily_query = generate_tavily_query(entity_name, entity_type, VenueSchema)
    safe_query = compress_query_with_gemini(tavily_query)

    # Gather web content
    raw_text = gather_source_data(safe_query)
    if not raw_text.strip():
        print("No text gathered from Tavily — skipping data gathering.")
        return

    # Process via shared pipeline
    result = process_raw_text(
        entity_name=entity_name,
        entity_type=entity_type,
        raw_text=raw_text,
        source_type="tavily"
    )

    print("\nCOMPLETED (Automated Tavily Mode)")

if __name__ == "__main__":
    main()
