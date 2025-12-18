from pathlib import Path
from pydantic import BaseModel
from utils.prompt_builder import generate_tavily_query


def save_tavily_query_to_file(
    entity_name: str,
    entity_type: str,
    model: type[BaseModel],
    output_dir: str = "data/queries"
) -> Path:
    """
    Generate a Tavily query and save it to a .txt file for manual LLM use.
    Returns the path to the created file.
    """

    # Generate query text
    query_text = generate_tavily_query(entity_name, entity_type, model)

    # Ensure directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Build filename
    safe_name = entity_name.replace(" ", "_").lower()
    filename = f"{safe_name}__{entity_type}_tavily_query.txt"
    full_path = output_path / filename

    # Write file
    full_path.write_text(query_text, encoding="utf-8")

    return full_path
