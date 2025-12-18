import httpx
import json
import os

# Get API key from environment
api_key = os.getenv("PERPLEXITY_API_KEY")
if not api_key:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

# Path to your JSON schema file
schema_file_path = "master_schema.json"

# Entity info
entity_name = "Edinburgh Sports Club"
entity_type = "Venue"

# Load schema from file
def load_schema(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading schema: {e}")
        return None

# Call Perplexity API
def call_perplexity(prompt, schema, api_key):
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
                "content": (
                    "You are a strict data extraction assistant. "
                    "Return a single JSON object that only contains fields defined in the provided schema. "
                    "Any value you cannot find must be set to null. "
                    "Any extra information must go inside 'other_attributes'. "
                    "Do not add any other top-level fields."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "schema": schema
            }
        }
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

# Post-process to strictly enforce schema keys at the top level
def enforce_schema_keys(listing, schema):
    schema_keys = set(schema["properties"].keys())
    cleaned = {}
    cleaned["other_attributes"] = listing.get("other_attributes", {})

    for key, value in listing.items():
        if key in schema_keys:
            cleaned[key] = value
        elif key != "other_attributes":
            cleaned["other_attributes"][key] = value

    return cleaned

if __name__ == "__main__":
    schema = load_schema(schema_file_path)
    if schema:
        user_prompt = f"Retrieve all attribute data you can find for the {entity_type} {entity_name}"
        print(f"Calling Perplexity with prompt: '{user_prompt}'")
        response_data = call_perplexity(user_prompt, schema, api_key)

        # Extract the structured content
        try:
            message_content = response_data['choices'][0]['message']['content']
            structured_output = json.loads(message_content)

            # Post-process each item if response is a list
            if isinstance(structured_output, list):
                cleaned_output = [enforce_schema_keys(item, schema) for item in structured_output]
            else:
                cleaned_output = enforce_schema_keys(structured_output, schema)

            print("\n--- Cleaned Structured Output ---")
            print(json.dumps(cleaned_output, indent=4))
        except Exception as e:
            print(f"Error processing response: {e}")
            print("\nRaw response:")
            print(json.dumps(response_data, indent=4))
