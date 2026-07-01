"""Application configuration facade."""

import logging

from app.core.settings import AppSettings, get_settings

logger = logging.getLogger(__name__)


def get_config() -> AppSettings:
    """Return cached application settings."""
    return get_settings()
