"""Receipt validation tool."""

import logging
from decimal import Decimal
from typing import Any

logger = logging.getLogger(__name__)


def validate_receipt(receipt_payload: dict[str, Any]) -> dict[str, Any]:
    """Validate receipt evidence for a claim."""
    # TODO: Add OCR confidence, attachment checksum checks, and vendor normalization.
    missing: list[str] = []
    for field_name in ("receipt_id", "vendor", "amount", "transaction_date"):
        if not receipt_payload.get(field_name):
            missing.append(field_name)
    if not receipt_payload.get("attachment_present"):
        missing.append("receipt_attachment")

    amount = Decimal(str(receipt_payload.get("amount") or "0"))
    is_valid = not missing and amount > 0
    return {
        "tool": "receipt_validator",
        "is_valid": is_valid,
        "missing_documents": missing,
        "findings": [] if is_valid else [{"severity": "medium", "message": "Receipt evidence is incomplete."}],
    }
