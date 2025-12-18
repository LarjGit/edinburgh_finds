import requests
import json
import os

# Set your Perplexity API key as an environment variable
# It is best practice not to hardcode API keys directly in your script.
# On Linux/macOS: export PERPLEXITY_API_KEY="your_api_key_here"
# On Windows: set PERPLEXITY_API_KEY="your_api_key_here"
# Replace "your_api_key_here" with your actual key from perplexity.ai
api_key = os.getenv("PERPLEXITY_API_KEY")

if not api_key:
    raise ValueError("PERPLEXITY_API_KEY environment variable not set.")

# This line is a workaround for a specific SSL error on this machine.
# It forces the requests library to use the SSL certificate bundle
# located in the virtual environment's certifi package.
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'venv', 'Lib', 'site-packages', 'certifi', 'cacert.pem')

# To bypass any proxies that might be causing the 503 error,
# we explicitly tell the 'requests' library to ignore proxies for this domain.
os.environ['NO_PROXY'] = 'api.perplexity.ai'

# The path to the JSON schema file in your project folder.
schema_file_path = 'master_schema.json'

def load_schema(file_path):
    """Loads a JSON schema from a local file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' is not a valid JSON file.")
        return None

def call_perplexity(prompt, schema, api_key):
    """Calls the Perplexity API with a given prompt and structured output schema."""
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar", # A model with search capabilities
        "messages": [
            {
                "role": "system",
                "content": "You are a specialized AI assistant that retrieves data from live search results. Your task is to extract information and return a complete JSON object that strictly adheres to the provided schema. If a value cannot be found, set it to `null`."
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

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # This will raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e: # Catch network-related errors
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Load the schema from the file
    company_schema = load_schema(schema_file_path)

    if company_schema:
        # Define the prompt to ask Perplexity
        user_prompt = "Retrieve the core details about the venue Edinburgh Sports Club." 
        
        # Make the API call
        print(f"Calling Perplexity with prompt: '{user_prompt}'")
        response_data = call_perplexity(user_prompt, company_schema, api_key)
        
        if response_data:
            # Extract and print the structured content from the response
            try:
                # The structured data is typically in the content of the first message
                message_content = response_data['choices'][0]['message']['content']
                structured_output = json.loads(message_content)
                print("\n--- Structured Output from Perplexity ---")
                print(json.dumps(structured_output, indent=4))
            except (KeyError, json.JSONDecodeError) as e:
                print(f"\nError processing the response from Perplexity: {e}")
                print("\nRaw response:")
                print(json.dumps(response_data, indent=4))
