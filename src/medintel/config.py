from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-5.6-terra"
    eval_model: str = "gpt-4o-mini"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "medication_documents"
    processed_data_path: Path = Path("data/processed")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()