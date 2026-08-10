"""CP1 - 12-Factor configuration."""

from __future__ import annotations

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    port: int = 8000
    agent_api_key: str
    redis_url: str = "redis://localhost:6379/0"
    rate_limit_per_minute: int = 10
    monthly_budget_usd: float = 10.0
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("agent_api_key")
    @classmethod
    def validate_agent_api_key(cls, value: str) -> str:
        key = value.strip()
        placeholders = {
            "",
            "changeme",
            "change-me",
            "your-api-key",
            "your-secret-key",
            "your-secret-key-here",
            "replace-me",
            "todo",
        }
        if key.lower() in placeholders:
            raise ValueError("AGENT_API_KEY must be a real secret")
        return key


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Read configuration once and cache it."""
    return Settings()
