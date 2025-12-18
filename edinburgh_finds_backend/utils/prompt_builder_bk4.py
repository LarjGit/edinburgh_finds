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
Your only task is to extract structured facts for the entity below, using the schema provided by the system and the rules below.

ENTITY
Name: {entity_name}
Type: {entity_type}

INPUT
You will receive a long raw factual dump.
Extract only facts that belong to this specific entity.

------------------------------------------------------------
GENERAL EXTRACTION RULES
------------------------------------------------------------
1. Do NOT hallucinate or invent anything.
2. Only extract facts explicitly present in the input.
3. When conflicting values appear:
   - Prefer the clearest, most specific, most repeated, or most venue-local one.
   - If two values are equally plausible, choose one and set confidence=0.5.
4. If a value is missing, unknown, not listed, or unreliable → return null.
5. Ignore POSSIBLE_OTHER_ENTITY items for schema fields.
   (You may store them in other_attributes under key "possible_other_entity".)
6. Everything in the VERIFIED section takes precedence over everything else. 

------------------------------------------------------------
TEMPLATE-BLOCK RULE
------------------------------------------------------------
Facts prefixed with “POSSIBLE_TEMPLATE_BLOCK:” indicate boilerplate reused across chain locations.

For these:
- Assign confidence = 0.2.
- Use them only if no more specific venue-local value exists.
- Never let a template-block value override a venue-specific value.

------------------------------------------------------------
OTHER_ATTRIBUTES RULE
------------------------------------------------------------
Populate other_attributes with ANY factual detail about the venue that does not belong to a defined schema field.

Rules:
- Use short snake_case keys.
- Values must be raw factual statements.
- Do not normalise or remove contradictions.
- Do not interpret meaning.
- other_attributes should not be empty unless genuinely no extra facts exist.

------------------------------------------------------------
CATEGORY RULES
------------------------------------------------------------
Populate categories using raw strings exactly as written.
- Do not merge similar categories.
- Do not canonicalise.
- Do not guess.
- Include every sport, activity, facility, or amenity string.
- If any sport or activity is explicitly stated as “available”, “yes”, or has a clear TRUE value then include it in categories even if it was not listed in the main category list.

------------------------------------------------------------
CONFIDENCE SCORING
------------------------------------------------------------
Assign confidence only to fields you populate:
- 1.0  = clear, repeated, authoritative
- 0.8  = stated once but reliable
- 0.5  = selected between conflicting values
- 0.2  = POSSIBLE_TEMPLATE_BLOCK
- (Do not assign confidence for null fields.)

------------------------------------------------------------
SOURCE INFO
------------------------------------------------------------
Build source_info as:
{{
  "sources": [...],   # URLs seen in the input
  "note": "short note if needed"
}}

Rules:
- Include all URLs that influenced extracted values.
- Do not invent URLs.
- Keep notes extremely short.

------------------------------------------------------------
OUTPUT
------------------------------------------------------------
Return only the structured JSON object defined by the schema.
No explanation or narrative.

------------------------------------------------------------
BEGIN EXTRACTION NOW.
"""
    # Clean up indentation
    return "\n".join(line.strip() for line in prompt.strip().splitlines())
