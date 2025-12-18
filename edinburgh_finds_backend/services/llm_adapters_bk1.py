"""LLM adapter module to cater for different API call structures for various providers"""

import json
from typing import Any, Dict, Optional
from perplexity import Perplexity
from anthropic import Anthropic

class PerplexityAdapter:
    provider_name = "perplexity"

    def __init__(self, client: Perplexity, model_name: str):
        self._client = client
        self._model = model_name

    def generate(self, 
                 system_prompt: str, 
                 user_prompt: str,
                 schema: Optional[dict] = None,
                 **kwargs: Dict[str, Any]) -> str:
        
        max_tokens = kwargs.pop('max_tokens', 4000)
        temperature = kwargs.pop('temperature', 0.0)

        # For Perplexity/OpenAI: use response_format parameter
        if schema:
            kwargs['response_format'] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "extraction_schema",
                    "strict": True,
                    "schema": schema
                }
            }

        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs # Includes 'response_format' as created above

        )
        return response.choices[0].message.content

class AnthropicAdapter:
    provider_name = "anthropic"
    
    def __init__(self, client: Anthropic, model_name: str):
        self._client = client
        self._model = model_name

    def generate(self, 
                 system_prompt: str, 
                 user_prompt: str, 
                 schema: Optional[dict] = None,
                 **kwargs: Dict[str, Any]) -> str:
        
        max_tokens = kwargs.pop('max_tokens', 4000)
        temperature=kwargs.pop('temperature', 0.0)
        messages=[{"role": "user", "content": user_prompt}]

        # For Anthropic: embed schema in system prompt if provided
        if schema:
            schema_json = json.dumps(schema, indent=2)
            system_prompt = system_prompt.format(schema_json=schema_json)

        # Anthropic uses 'messages.create' which takes 'system' as a separate parameter
        response = self._client.messages.create(
            model=self._model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt
            
        )
        return response.content[0].text