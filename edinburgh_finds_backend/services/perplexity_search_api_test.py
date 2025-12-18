import os
import json
from dotenv import load_dotenv
from perplexity import Perplexity # Importing the official SDK
from typing import Optional, Dict, Any, List # Used for type hinting if processing data further

# --- Configuration ---
# The API key is read automatically from the PERPLEXITY_API_KEY environment variable
load_dotenv(override=True)
API_KEY = os.environ.get("PERPLEXITY_API_KEY")

# The query specifically asks for the social media link
# REFINED QUERY: Explicitly ask for the full link or the social media page name.
QUERY: str = "full facebook URL for Craigmillar Park Tennis & Padel Club in Edinburgh"

if not API_KEY:
    print("Error: PERPLEXITY_API_KEY environment variable not set.")
    print("Please set your key and install the SDK: pip install perplexity")
    exit()

def highlight_facebook_links(results: List[Dict[str, Any]]) -> None:
    """Processes the raw search results to look for 'facebook.com' in the snippet or URL."""
    found_facebook_link = False
    for i, result in enumerate(results):
        print(f"\n[RESULT {i+1}]")
        print(f"  Title:   {result.title}")
        print(f"  URL:     {result.url}")
        
        snippet_content = result.snippet if result.snippet is not None else ""
        
        # Simple check for 'facebook.com' in the URL or snippet
        if "facebook.com" in result.url.lower():
             print(f"  Snippet: {snippet_content}")
             print("  *** POTENTIAL FACEBOOK URL FOUND IN RESULT URL ***")
             found_facebook_link = True
        elif "facebook.com" in snippet_content.lower():
             print(f"  Snippet: {snippet_content}")
             print("  *** POTENTIAL FACEBOOK LINK FOUND IN SNIPPET ***")
             found_facebook_link = True
        else:
            print(f"  Snippet: {snippet_content}")
            
        print(f"  Date:    {result.date}")
    
    if not found_facebook_link:
        print("\nNote: No clear Facebook URL was detected in the top results' URLs or snippets.")


# --- Initialize Client and Execute API Call ---
try:
    # 1. Initialize the client (it reads the API key from the environment variable)
    client = Perplexity()
    
    print(f"Executing Search API call for: '{QUERY}'...\n")
    
    # 2. Use the dedicated search.create() method
    response = client.search.create(
        query=QUERY, 
        max_results=5 # Standard Search API parameter
    )

    # --- Process and Print Output ---
    if response.results:
        print("--- RAW SEARCH RESULTS (SNIPPETS) ---")
        highlight_facebook_links(response.results)
            
    else:
        print("Search successful, but no results found.")

# The Perplexity SDK will raise an HTTPStatusError for bad responses
except Exception as e:
    print(f"\nAPI Request Error: {e}")
    print("If this is an authorization error, please check your API key.")