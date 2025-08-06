# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    model_name: str = "llama3-70b-8192"  # default, but override via .env if needed

    class Config:
        env_file = ".env"

settings = Settings()
