# test_baseline_perplexity_knowledge.py
import os
from perplexity import Perplexity

api_key = os.getenv("PERPLEXITY_API_KEY")
client = Perplexity(api_key=api_key)

entity_name = "Edinburgh Sports Club"
entity_type = "Venue"

prompt = f"""
Without using any schema or JSON formatting, describe in detail everything you know 
or can find from authoritative sources about the {entity_type} named '{entity_name}'.
Focus on:
- sports facilities (how many courts of each type)
- covered or floodlit courts
- location, accessibility, and key amenities
Respond in plain English prose, NOT JSON.
"""

response = client.chat.completions.create(
    model="sonar",
    messages=[
        {"role": "system", "content": "You are a factual retrieval assistant."},
        {"role": "user", "content": prompt},
    ],
    temperature=0.0,
)

print("\n=== BASELINE FACTUAL KNOWLEDGE ===\n")
print(response.choices[0].message.content)
