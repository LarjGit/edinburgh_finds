# test_nested_json_schema_extraction.py
import os
from pydantic import BaseModel, Field
from typing import Optional
from perplexity import Perplexity

class CourtCounts(BaseModel):
    total_courts: Optional[int] = Field(None, description="Total number of courts of this sport")
    covered_count: Optional[int] = Field(None, description="Number of covered courts")
    floodlit_count: Optional[int] = Field(None, description="Number of floodlit courts")

class Venue(BaseModel):
    entity_name: str = Field(..., description="Name of the venue")
    entity_type: str = Field("Venue", description="Type of entity")
    squash: Optional[CourtCounts] = Field(None, description="Information about squash courts")
    tennis: Optional[CourtCounts] = Field(None, description="Information about tennis courts")
    padel: Optional[CourtCounts] = Field(None, description="Information about padel courts")

api_key = os.getenv("PERPLEXITY_API_KEY")
client = Perplexity(api_key=api_key)

schema = Venue.model_json_schema()

prompt = f"""
Extract structured information about the venue '{'Edinburgh Sports Club'}' (type '{'Venue'}').
Use the provided JSON schema exactly and populate all nested fields wherever information exists.

Guidelines:
- If the schema defines a nested field, assume its value may be implied in text form (e.g., "fully covered padel courts").
- For each nested object, cross-check the narrative facts and fill inferred fields if the wording supports it.
- Do not leave fields null if the description explicitly implies a value (e.g., "three floodlit tennis courts" → floodlit_count=3).
- Use explicit null only where no evidence or inference exists.
Return only valid JSON matching the schema.
"""

response = client.chat.completions.create(
    model="sonar",
    messages=[
        {"role": "system", "content": "You are a structured data extraction engine."},
        {"role": "user", "content": prompt},
    ],
    response_format={"type": "json_schema", "json_schema": {"schema": schema}},
    temperature=0.0,
)

print("\n=== NESTED JSON SCHEMA OUTPUT ===\n")
print(response.choices[0].message.content)
