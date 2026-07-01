"""Receipt validator tests."""

import logging

logger = logging.getLogger(__name__)


def test_receipt_validator_detects_missing_attachment() -> None:
    """Receipt validator flags missing evidence."""
    from app.tools.receipt_validator import validate_receipt

    result = validate_receipt({"vendor": "Metro Cab", "amount": 54.25})

    assert result["is_valid"] is False
    assert "receipt_attachment" in result["missing_documents"]
