"""Security utility placeholders."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def verify_api_key(api_key: str | None) -> bool:
    """Verify an inbound API key."""
    # TODO: Implement authentication and authorization checks.
    return bool(api_key)
