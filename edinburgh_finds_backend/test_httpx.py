import os
import httpx

API_KEY = os.getenv("PERPLEXITY_API_KEY")
url = "https://api.perplexity.ai/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "sonar",
    "messages": [{"role": "user", "content": "Hello"}],
    "response_format": {"type": "text"}
}

with httpx.Client(timeout=15.0) as client:
    response = client.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

# Extract assistant message
assistant_message = ""
if "choices" in data and len(data["choices"]) > 0:
    assistant_message = data["choices"][0]["message"]["content"]

print("Assistant says:")
print(assistant_message)
