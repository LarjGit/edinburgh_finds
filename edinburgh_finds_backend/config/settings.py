# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API keys
    PERPLEXITY_API_KEY: str
    ANTHROPIC_API_KEY: str
    GEMINI_API_KEY: str
    TAVILY_API_KEY: str
    LAOZHANG_API_KEY: str
    FIRECRAWL_API_KEY: str

    # LLM Model
    LLM_PROVIDER: str
    LLM_MODEL: str

    # Database URL
    DATABASE_URL: str

    class Config:
        # Load variables from a .env file automatically
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a single settings instance to use throughout your project
settings = Settings()
