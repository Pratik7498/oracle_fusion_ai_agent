"""Application settings loaded from environment variables / .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Central configuration for the Oracle Fusion AI Agent POC."""

    openai_api_key: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "oracle_fusion_poc"
    postgres_user: str = "poc_user"
    postgres_password: str = ""
    postgres_url: str = ""
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached Settings instance (reads .env once)."""
    return Settings()
