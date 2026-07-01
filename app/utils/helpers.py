"""General helper placeholders."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def require_value(value: Any, name: str) -> Any:
    """Return a required value placeholder."""
    # TODO: Replace with explicit validation helpers.
    if value is None:
        raise ValueError(f"{name} is required.")
    return value
