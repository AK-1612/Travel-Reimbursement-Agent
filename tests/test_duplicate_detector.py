"""Duplicate detector tests."""

import logging

logger = logging.getLogger(__name__)


def test_duplicate_detector_finds_existing_receipt() -> None:
    """Duplicate detector finds a matching historical claim."""
    from app.tools.duplicate_detector import detect_duplicate

    claim = {
        "employee_id": "EMP-102",
        "amount": 68.5,
        "expense_date": "2026-06-14",
        "receipt": {"receipt_id": "RCT-DUP-001", "vendor": "City Taxi"},
    }

    result = detect_duplicate(claim)

    assert result["is_duplicate"] is True
    assert result["matches"]
