"""Structured output validation tool."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def validate_output(output_payload: dict[str, Any]) -> dict[str, Any]:
    """Validate agent output before returning it to callers."""
    # TODO: Add JSON schema validation for external API compatibility.
    required_fields = {
        "claim_id",
        "decision",
        "approved_amount",
        "rejected_amount",
        "policy_references",
        "confidence",
        "explanation",
    }
    missing_fields = sorted(required_fields - set(output_payload))
    return {
        "tool": "output_validator",
        "is_valid": not missing_fields,
        "missing_fields": missing_fields,
    }
