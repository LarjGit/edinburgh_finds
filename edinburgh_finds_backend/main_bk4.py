# main.py

import json
from services.tavily_client import TavilySearch
from services.instructor_client import instructor_client
from schemas.venue_extraction_schema import VenueSchema
from utils.prompt_builder import generate_tavily_query, generate_system_prompt
from utils.query_compressor import compress_query_with_gemini
from config.settings import settings
from services.upsert_entity import upsert_from_schema

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

def extract_structured_data(entity_name: str, entity_type: str, raw_text: str):
    system_message = generate_system_prompt(
        entity_name=entity_name,
        entity_type=entity_type,
        model=VenueSchema,
    )

    print("=== SYSTEM MESSAGE ===")
    print(system_message[:500])
    print("=== RAW TEXT LENGTH ===", len(raw_text))

    result = instructor_client.messages.create(
        model=settings.LLM_MODEL,
        response_model=VenueSchema,
        max_tokens=4000,
        temperature=0,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": raw_text},
        ]
    )
    return result

def main():
    entity_name = "David Lloyd Club Edinburgh Shawfair"
    entity_type = "venue"

    tavily_query = generate_tavily_query(entity_name, entity_type, VenueSchema)

    print("\n Compressing Tavily query with Gemini...")
    safe_query = compress_query_with_gemini(tavily_query)

    raw_text = gather_source_data(safe_query)
    print(f"🔍 Length of concatenated raw text: {len(raw_text)}")
    if not raw_text.strip():
        print("⚠️ No text extracted from Tavily — skipping LLM extraction.")
        return

    dto = extract_structured_data(entity_name, entity_type, raw_text)

    listing, entity, report = upsert_from_schema(
        data=dto,
        entity_name=entity_name,
        entity_type=entity_type,
    )

    print("\n✅ DATABASE UPSERT COMPLETE")
    print(json.dumps(report, indent=2))

    with open("debug_raw.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)

if __name__ == "__main__":
    main()
