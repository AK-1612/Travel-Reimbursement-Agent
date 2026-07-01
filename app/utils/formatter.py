"""Formatting utilities."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def format_decision(decision_payload: dict[str, Any]) -> dict[str, Any]:
    """Format a decision payload for presentation."""
    # TODO: Add locale-aware currency and employee-facing redaction rules.
    return {
        key: str(value) if key.endswith("_amount") else value
        for key, value in decision_payload.items()
    }
