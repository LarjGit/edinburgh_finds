# main.py

import json
from services.tavily_client import TavilySearch
from services.instructor_client import instructor_client
from schemas.venue_extraction_schema import VenueSchema  # dynamically derived Pydantic schema from SQLmodel (dB) classes
from utils.prompt_builder import generate_tavily_query, generate_system_prompt
from utils.query_compressor import compress_query_with_gemini
from config.settings import settings

def gather_source_data(query: str, min_score: float = 0.7, max_results: int = 10) -> str:
    """Search Tavily for URLs, extract their content, and concatenate all raw text."""
    tavily = TavilySearch()

    # Search Tavily for relevant URLs
    urls = tavily.search_urls(query=query, max_results=max_results, min_score=min_score)

    print("\n Filtered Tavily URLs:")
    for url in urls:
        print(url)

    # Extract raw content from those URLs
    print("\n Extracting content...")
    results = tavily.extract(urls)

    # Collect all raw page text
    all_text_blocks = [item.get("raw_content", "") for item in results]
    concatenated_block = "\n\n".join(all_text_blocks)

    # Rough token estimate
    char_length = len(concatenated_block)
    approx_tokens = char_length // 4
    print("\n Concatenated text block ready for Instructor")
    print(f" Character length: {char_length}")
    print(f" Approx. token count: {approx_tokens}")
    print("--------------------------------------------------")

    return concatenated_block

def extract_structured_data(entity_name: str, entity_type: str, raw_text: str):
    """Use Instructor + Claude to map raw text → structured Venue schema."""
    
    system_message = generate_system_prompt(
        entity_name=entity_name,
        entity_type=entity_type,
        model=VenueSchema,
    )

    result = instructor_client.messages.create(
        model=settings.LLM_MODEL,
        response_model=VenueSchema,  # uses clean Pydantic schema converted from SQLmodel (dB) classes
        max_tokens=4000,             # Required for Claude
        temperature=0,               # Deterministic
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": raw_text},
        ]
    )
    return result

def main():
    # Build schema-aware long Tavily query
    entity_name = "Edinburgh Sports Club"
    entity_type = "Venue"
    tavily_query = generate_tavily_query(entity_name, entity_type, VenueSchema)

    # Empty dict to hold merged results
    merged = {}

    # Run 2 or 3 passes (change range(2) to range(3) if you want 3)
    for i in range(1):
        print(f"\n PASS {i+1}")
        
        # Compress the long descriptive query using Gemini (under 400 chars)
        print("\n Compressing Tavily query with Gemini...")
        safe_query = compress_query_with_gemini(tavily_query)

        print("\n Query length before:", len(tavily_query))
        print("Query length after:", len(safe_query))
        print("Long query:\n", tavily_query)
        print("Compressed query used:\n", safe_query)
            
        text_block = gather_source_data(safe_query)
        structured = extract_structured_data(entity_name, entity_type, text_block)
        result_dict = structured.model_dump()

        # Merge: only fill in missing (None/empty) fields
        for key, value in result_dict.items():
            if not merged.get(key) and value not in (None, "", [], {}):
                merged[key] = value

    print("\n✅ FINAL MERGED RESULT")
    print(json.dumps(merged, indent=2))

    with open("debug_raw.txt", "w", encoding="utf-8") as f:
        f.write(text_block)

if __name__ == "__main__":
    main()
