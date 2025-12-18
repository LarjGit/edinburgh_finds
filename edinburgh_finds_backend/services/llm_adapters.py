"""LLM adapter module to cater for different API call structures for various providers"""

import json
import logging
from typing import Any, Dict, Optional
from perplexity import Perplexity
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class PerplexityAdapter:
    provider_name = "perplexity"

    def __init__(self, client: Perplexity, model_name: str):
        self._client = client
        self._model = model_name

    def generate(self, 
                 system_prompt: str, 
                 user_prompt: str,
                 schema: Optional[dict] = None,
                 enable_web_search: bool = False,
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

    def _strip_markdown_fences(self, text: str) -> str:
        """Remove markdown code fences if present."""
        text = text.strip()
        # Remove ```json ... ``` or ``` ... ```
        if text.startswith('```'):
            # Find the first newline after opening fence
            first_newline = text.find('\n')
            if first_newline != -1:
                text = text[first_newline + 1:]
            # Remove closing fence
            if text.endswith('```'):
                text = text[:-3]
        return text.strip()

    def generate(self, 
                 system_prompt: str, 
                 user_prompt: str, 
                 schema: Optional[dict] = None,
                 enable_web_search: bool = False,
                 **kwargs: Dict[str, Any]) -> str:
        
        max_tokens = kwargs.pop('max_tokens', 4000)
        temperature=kwargs.pop('temperature', 0.0)
        messages=[{"role": "user", "content": user_prompt}]

        # For Anthropic: embed schema in system prompt if provided
        if schema:
            schema_json = json.dumps(schema, indent=2)
            system_prompt = system_prompt.format(schema_json=schema_json)

        # Build API call parameters
        api_params = {
            "model": self._model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt
        }

        # Only add tools parameter if web search is enabled
        if enable_web_search:
            api_params["tools"] = [{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 1
            }]
            logger.info("🔍 Web search ENABLED for this API call")
        else:
            logger.info("📝 Web search DISABLED for this API call")

        # Log the full API call structure (without full content for brevity)
        logger.info("="*70)
        logger.info("ANTHROPIC API CALL PARAMETERS:")
        logger.info(f"  Model: {api_params['model']}")
        logger.info(f"  Max tokens: {api_params['max_tokens']}")
        logger.info(f"  Temperature: {api_params['temperature']}")
        logger.info(f"  System prompt length: {len(api_params['system'])} chars")
        logger.info(f"  User prompt length: {len(messages[0]['content'])} chars")
        logger.info(f"  Tools parameter included: {'tools' in api_params}")
        if 'tools' in api_params:
            logger.info(f"  Tools config: {json.dumps(api_params['tools'], indent=2)}")
        logger.info("="*70)

        response = self._client.messages.create(**api_params)
        
        # Log response metadata
        logger.info("="*70)
        logger.info("ANTHROPIC API RESPONSE:")
        logger.info(f"  Model: {response.model}")
        logger.info(f"  Stop reason: {response.stop_reason}")
        logger.info(f"  Input tokens: {response.usage.input_tokens}")
        logger.info(f"  Output tokens: {response.usage.output_tokens}")
        logger.info(f"  Content blocks: {len(response.content)}")
        logger.info(f"  First content type: {response.content[0].type}")
        logger.info("="*70)
        
        #content = response.content[0].text
        
        # Extract and log all blocks
        text_parts = []
        for i, block in enumerate(response.content):
            logger.info(f"  Block {i}: type={block.type}, "
                        f"chars={len(block.text) if hasattr(block, 'text') else 'N/A'}")
    
            if block.type == "text":
                text_parts.append(block.text)

        content = "\n\n".join(text_parts)

        # Clean markdown fences if present (for JSON responses)
        if schema:
            content = self._strip_markdown_fences(content)
        
        return content
        