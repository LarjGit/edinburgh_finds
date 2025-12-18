# To run this code you need to install the following dependencies:
# pip install google-genai
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from models.models import Listing, Venue

def generate():
    
    load_dotenv(override=True)

    # Ensure your GEMINI_API_KEY environment variable is set before running this.
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""I am in Edinburgh. Tell me as much detailed data as you can related to the venue Craigmillar Park Tennis & Padel Club. Include address, phone number, email, facebook url, opening hours"""),
            ],
        ),
    ]
    
    # *** MODIFICATION 2: ADD THE GOOGLE MAPS TOOL TO THE CONFIG ***
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        tools=[
            types.Tool(google_search=types.GoogleSearch()),
            types.Tool(google_maps=types.GoogleMaps()),
        ],
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()