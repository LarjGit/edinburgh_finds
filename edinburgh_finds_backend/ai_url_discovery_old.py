import httpx
import json
import os

# Get API key from environment
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

# Entity info
entity_name = "Edinburgh Sports Club"
entity_type = "Venue"

def call_perplexity(prompt, api_key):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant who finds authoritative URLs for a specific entity."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    user_prompt = f"Find all authoritative URLs for the {entity_type} {entity_name}"
    print(f"Calling Perplexity with prompt: '{user_prompt}'\n")

    response_data = call_perplexity(user_prompt, api_key)

    # --- Assistant’s natural language answer ---
    try:
        assistant_text = response_data["choices"][0]["message"]["content"]
        print("--- Assistant's Answer (Natural Language) ---")
        print(assistant_text)
        print()
    except (KeyError, IndexError):
        print("No assistant text found.\n")

    # --- Structured citations (URLs only) ---
    citations = response_data.get("citations", [])
    print("--- Citations (URLs) ---")
    for url in citations:
        print(url)
