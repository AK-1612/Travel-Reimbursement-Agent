"""Application settings model."""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class AppSettings(BaseSettings):
    """Runtime settings loaded from environment variables and .env file."""

    # --- General ---
    app_env: str = "development"
    log_level: str = "INFO"

    # --- LLM Provider: Groq ---
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"
    groq_base_url: str = "https://api.groq.com/openai/v1"

    # --- Legacy / unused keys (ignored gracefully) ---
    openai_api_key: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Return a cached singleton of AppSettings."""
    return AppSettings()
