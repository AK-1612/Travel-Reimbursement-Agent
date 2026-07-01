"""Validation service for claim and receipt checks."""

import logging
from typing import Any

from app.tools.receipt_validator import validate_receipt

logger = logging.getLogger(__name__)


class ValidationService:
    """Validate inbound claim payloads and supporting evidence."""

    async def validate(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Validate a claim payload."""
        # TODO: Add cross-field validation and employee data checks.
        return validate_receipt(payload.get("receipt", {}))
