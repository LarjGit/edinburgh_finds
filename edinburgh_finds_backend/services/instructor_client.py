# services/instructor_client.py

import instructor
from google import genai
from anthropic import Anthropic
from openai import OpenAI
from config.settings import settings

llm_provider = settings.LLM_PROVIDER
llm_model = settings.LLM_MODEL

print(f"Using {llm_provider} {llm_model} via Instructor")

# ============================================================
# 1. CLAUDE via LaoZhang.ai (OpenAI protocol)
# ============================================================

if llm_provider == "laozhang-claude":
    client = OpenAI(
        api_key=settings.LAOZHANG_API_KEY,
        base_url="https://api.laozhang.ai/v1",
    )
    instructor_client = instructor.from_openai(client)


# ============================================================
# 2. GEMINI via Google GenAI
# ============================================================

elif llm_provider == "gemini":
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    instructor_client = instructor.from_genai(
        client=client,
        mode=instructor.Mode.GENAI_TOOLS,
    )


# ============================================================
# 3. DIRECT ANTHROPIC
# ============================================================

elif llm_provider == "claude":
    client = OpenAI(
        api_key=settings.ANTHROPIC_API_KEY,
        base_url="https://api.anthropic.com/v1"
    )
    instructor_client = instructor.from_openai(client)

# ============================================================
# 4. FAIL FAST IF UNKNOWN
# ============================================================

else:
    raise ValueError(f"Unknown LLM_PROVIDER: {llm_provider}")
