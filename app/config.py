from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"
print("ENV FILE:", ENV_FILE)

class Settings(BaseSettings):
    google_api_key: str 
    google_model: str = "gemma-4-31b-it"
    database_url: str = "sqlite:///./shopping_assistant.db"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
print(settings.model_dump())
