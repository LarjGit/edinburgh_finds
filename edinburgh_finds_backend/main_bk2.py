# main.py
from services.tavily_client import TavilySearch
from services.instructor_client import instructor_client
from schemas.venue_schema import VenueSchema  # dynamically derived Pydantic schema from SQLmodel (dB) classes
from utils.prompt_builder import generate_tavily_query, generate_schema_prompt
from utils.query_compressor import compress_query_with_gemini

def gather_source_data(query: str, min_score: float = 0.7, max_results: int = 10) -> str:
    """Search Tavily for URLs, extract their content, and concatenate all raw text."""
    tavily = TavilySearch()

    # Search Tavily for relevant URLs
    urls = tavily.search_urls(query=query, max_results=max_results, min_score=min_score)

    print("\n🔗 Filtered Tavily URLs:")
    for url in urls:
        print(url)

    # Extract raw content from those URLs
    print("\n📄 Extracting content...")
    results = tavily.extract(urls)

    # Collect all raw page text
    all_text_blocks = [item.get("raw_content", "") for item in results]
    concatenated_block = "\n\n".join(all_text_blocks)

    # Rough token estimate
    char_length = len(concatenated_block)
    approx_tokens = char_length // 4
    print("\n🧩 Concatenated text block ready for Instructor")
    print(f"📏 Character length: {char_length}")
    print(f"🔢 Approx. token count: {approx_tokens}")
    print("--------------------------------------------------")

    return concatenated_block

def extract_structured_data(raw_text: str):
    """Use Instructor + Gemini to map raw text → structured Venue schema."""
    
    system_message = generate_schema_prompt(
        VenueSchema,
        task_description="Extract complete and detailed venue information from the provided text.",
    )

    result = instructor_client.chat.completions.create(
        model="gemini-2.5-flash",
        response_model=VenueSchema,  # uses clean Pydantic schema converted from SQLmodel (dB) classes
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": raw_text},
        ]
    )
    return result

def main():
    # Build schema-aware long Tavily query
    tavily_query = generate_tavily_query("Edinburgh Sports Club", VenueSchema)

    # Compress the long descriptive query using Gemini (under 400 chars)
    print("\n🧠 Compressing Tavily query with Gemini...")
    safe_query = compress_query_with_gemini(tavily_query)

    print("\n📏 Query length before:", len(tavily_query))
    print("✂️ Query length after:", len(safe_query))
    print("🔍 Long query:\n", tavily_query)
    print("🔍 Compressed query used:\n", safe_query)

    # Gather source data using compressed query
    text_block = gather_source_data(safe_query)
        
    # Extract structured data using Instructor
    structured_data = extract_structured_data(text_block)

    print("\n✅ Final Extracted Data")
    print(structured_data.model_dump_json(indent=2))

    with open("debug_raw.txt", "w", encoding="utf-8") as f:
        f.write(text_block)

if __name__ == "__main__":
    main()
