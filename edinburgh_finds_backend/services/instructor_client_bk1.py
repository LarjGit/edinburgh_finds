# services/instructor_client.py
import instructor
from google import genai
from config.settings import settings

gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Wrap Gemini in Instructor
instructor_client = instructor.from_genai(
    client=gemini_client,
    mode=instructor.Mode.GENAI_TOOLS,
)
