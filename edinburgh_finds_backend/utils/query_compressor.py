# utils/query_compressor.py

from google import genai
from config.settings import settings

# We *always* use Gemini Flash for query rewriting:
# - it's cheap
# - excellent at summarizing/search phrasing
# - stable / deterministic
gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

def compress_query_with_gemini(long_query: str, max_chars: int = 300) -> str:
    """
    Use Gemini directly (not Instructor) to rewrite a long Tavily query
    into a concise version under the character limit, preserving meaning.
    """
    prompt = f"""
You are an expert query re-writing assistant.
You will rewrite this search query to reduce the character count to around {max_chars} characters.
** It is critical that the query is no longer than {max_chars} **.
Now rewrite accordingly: {long_query}
"""

    result = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    concise_query = result.candidates[0].content.parts[0].text.strip()
    return concise_query
