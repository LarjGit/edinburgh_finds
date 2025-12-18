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

Return valid structured data following this schema.
"""
    # Clean up indentation
    return "\n".join(line.strip() for line in prompt.strip().splitlines())
