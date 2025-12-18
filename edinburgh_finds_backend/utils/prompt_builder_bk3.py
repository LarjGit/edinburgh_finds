# utils/prompt_builder.py
from pydantic import BaseModel

def generate_tavily_query(entity_name: str, entity_type: str, model: type[BaseModel]) -> str:
    """
    Generate a descriptive Tavily search query using explanatory text and pydantic field names
    """

    # Build concise field list (names only)
    field_names = [f"- {name}" for name in model.model_fields.keys()]
    field_list = "\n".join(field_names)
    
    # Compose a clean structured search query
    query = f"""
Find comprehensive, up-to-date and authoritative information about the **{entity_type}** **{entity_name}**.

Focus on gathering details for the following data attributes: {field_list}
"""
    return "\n".join(line.strip() for line in query.strip().splitlines())

def generate_system_prompt(entity_name: str, entity_type: str, model: type[BaseModel]) -> str:
    """
    Dynamically generate a detailed system prompt from a Pydantic model.
    Includes field names and descriptions so Gemini understands semantic meaning.
    """

    # Build a field list with names and human-readable descriptions
    field_lines = []
    for name, field in model.model_fields.items():
        desc = field.description or "no description provided"
        field_lines.append(f"- {name}: {desc}")

    # Join into readable markdown-style bullet list
    field_descriptions = "\n".join(field_lines)

    # Combine everything into a single clear system message
    prompt = f"""
You are a structured data extraction model.

Your task:
Extract all relevant data for the {entity_type} {entity_name} according to the schema below.

Schema fields:
{field_descriptions}

Extraction Rules:
- Extract everything that clearly belongs to one of the schema fields.
- Do **not** skip details that do not fit the schema — those must go into `other_attributes`.
- `other_attributes` is a dictionary for all extra factual, descriptive, or contextual details
  about the entity (venue, club, or place) that are not captured by other fields.
  Examples include: facilities, amenities, parking, membership, food & drink, accessibility,
  pricing, awards, history, special features, atmosphere, etc.
- Example usage:
  "other_attributes": {{
      "wifi": "available throughout club",
      "bar": "licensed bar with lounge area",
      "restaurant": "serves food daily",
      "membership_required": "yes",
      "guest_policy": "day passes available"
  }}
- Use concise key names (snake_case or short words) and preserve factual accuracy.
- If a value is found anywhere in the text, include it. Do not leave `other_attributes` empty
  unless absolutely nothing extra is found.
- Never invent or guess information; only use what is explicitly or clearly implied.

Category Extraction Rules:

- Populate the `categories` field using FREE-FORM strings.
- Do NOT try to predict or guess "official" categories.
- Do NOT convert categories to canonical or standardised forms.
- Always return category values exactly as written in the text.

Examples of valid category strings:
  - "padel"
  - "pickleball"
  - "tennis"
  - "gym"
  - "fitness"
  - "wellness"
  - "swimming"
  - "aqua aerobics"
  - "spa"
  - "yoga"
  - "studio"
  - "martial arts"
  - "climbing"

ALL categories (sports, activities, offerings, classes, amenities, facilities) should be included.

Important:
- The system will map these raw strings into canonical categories later.
- The LLM must NOT attempt this mapping.
- Just extract plain category names exactly as found.

Confidence Scoring:
Return a dictionary named `field_confidence`:

- Include one entry per field you set.
- Confidence is a float between 0.0 and 1.0:
    1.00 = directly and clearly confirmed from authoritative source
    0.80 = stated clearly once from reliable source
    0.60 = reasonably inferred but not strongly confirmed
    0.30 = weak or uncertain reference (avoid setting the field unless meaningful)
- If you do not set a field, do not include it in `field_confidence`.

Example:
"website_url": "https://exampleclub.co.uk"
"field_confidence": {{ "website_url": 0.92 }}

Source Tracability:
Return a dictionary named `source_info` containing:
- The list of URLs used to determine the values, if available.
- Optional short note for clarification.

Format example:
"source_info": {{
  "sources": ["https://exampleclub.co.uk/about"],
  "note": "primary official website"
}}

Return valid structured data following this schema.
"""
    # Clean up indentation
    return "\n".join(line.strip() for line in prompt.strip().splitlines())
