# utils/prompt_builder.py
from pydantic import BaseModel

def generate_tavily_query(entity_name: str, model: type[BaseModel]) -> str:
    """
    Generate a descriptive Tavily search query using your explanatory text,
    but listing only field names instead of verbose descriptions due to tavily 400 character limit.
    """

    # Build concise field list (names only)
    field_names = [f"- {name}" for name in model.model_fields.keys()]
    field_list = "\n".join(field_names)
    
    # Compose a clean structured search query
    query = f"""
Find comprehensive, up-to-date information about **{entity_name}**.

Focus on gathering details for the following data attributes:
{field_list}

Prioritize sources such as:
- The official website or 'About' page
- Trusted sports directories or venue databases
- Google Maps / business profiles
- Membership or facility booking pages

Avoid:
- Unrelated news articles or casual mentions on forums
- Aggregated review snippets without factual data

Your goal:
Return URLs that are most likely to contain structured factual information
matching the schema above.
"""
    return "\n".join(line.strip() for line in query.strip().splitlines())

def generate_schema_prompt(model: type[BaseModel], task_description: str = "") -> str:
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
{task_description or "Extract all relevant data according to the schema below."}

Schema fields:
{field_descriptions}

Instructions:
- Match information by meaning, not exact wording.
- Search entire text, including Markdown, HTML, contact blocks, or captions.
- If a value is present anywhere, map it to the correct field.
- If not found, leave it as null.
- Never invent or infer data.
"""
    # Clean up indentation
    return "\n".join(line.strip() for line in prompt.strip().splitlines())
