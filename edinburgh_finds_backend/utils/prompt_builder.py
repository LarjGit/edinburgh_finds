# utils/prompt_builder.py
from pydantic import BaseModel

def generate_system_prompt(entity_name: str, entity_type: str, model: type[BaseModel]) -> str:
    
    prompt = f"""
Extract structured data for: {entity_name} ({entity_type})

INPUT STRUCTURE
The input text is organized by confidence grades (GRADE A, GRADE B, GRADE C, GRADE X).

CONFIDENCE SCORING (required for every populated field)
- Data from GRADE A section → 1.0
- Data from GRADE B section → 0.8
- Data from GRADE C section → 0.5
- Data from GRADE X section → null (don't populate)

If the same data appears in multiple grade sections, use the highest grade.
If conflicting values appear within same grade, choose the clearest/most specific value and set confidence = 0.5.

RULES
1. Only extract explicitly stated facts - no hallucination
2. Missing data → null (never "N/A", "Unknown", "TBC")
3. URLs (website_url, facebook_url, etc.) must start with http:// or https:// - if just a name or unavailable, set to null
4. opening_hours: Extract the most commonly stated hours. If variations exist, use the primary/clearest one and note variations in other_attributes. Set to null only if genuinely unavailable.
5. Categories: Include exact raw strings for every sport, activity, facility, or amenity mentioned. If a sport is marked "available" or "yes", include it in categories.
6. Summaries: 2-3 sentences, factual tone
7. other_attributes: Populate with ANY factual detail not in schema fields. Should NOT be empty unless genuinely no extra facts exist.
8. Email must be actual format ([email protected]) - if unavailable or descriptive text, set to null
9. street_address should contain only: building number, street name, area, town/city, postcode. Do NOT include country.
10. source_info: Build as {{"sources": [...URLs from input...], "note": "short note if needed"}}

Return only JSON with field_confidence populated for all extracted fields.
"""
    return "\n".join(line.strip() for line in prompt.strip().splitlines())
