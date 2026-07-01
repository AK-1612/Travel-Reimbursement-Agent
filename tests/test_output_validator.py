"""Output validator tests."""

import logging

logger = logging.getLogger(__name__)


def test_output_validator_requires_core_fields() -> None:
    """Output validator identifies missing required fields."""
    from app.tools.output_validator import validate_output

    result = validate_output({"claim_id": "CLM-1"})

    assert result["is_valid"] is False
    assert "decision" in result["missing_fields"]
