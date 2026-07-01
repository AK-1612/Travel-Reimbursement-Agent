"""Duplicate claim detection tool."""

import json
import logging
from decimal import Decimal
from typing import Any

from app.constants import PROJECT_ROOT

logger = logging.getLogger(__name__)


def detect_duplicate(claim_payload: dict[str, Any]) -> dict[str, Any]:
    """Detect potential duplicate reimbursement claims."""
    # TODO: Replace exact matching with receipt fingerprint and semantic similarity checks.
    history_path = PROJECT_ROOT / "sample_data" / "historical_claims.json"
    historical_claims = json.loads(history_path.read_text(encoding="utf-8"))
    receipt = claim_payload.get("receipt", {})
    amount = Decimal(str(claim_payload.get("amount") or "0"))
    matches = []
    for prior in historical_claims:
        same_employee = prior.get("employee_id") == claim_payload.get("employee_id")
        same_receipt = prior.get("receipt_id") and prior.get("receipt_id") == receipt.get("receipt_id")
        same_vendor_date_amount = (
            prior.get("vendor") == receipt.get("vendor")
            and prior.get("expense_date") == claim_payload.get("expense_date")
            and Decimal(str(prior.get("amount") or "0")) == amount
        )
        if same_employee and (same_receipt or same_vendor_date_amount):
            matches.append(prior)
    return {
        "tool": "duplicate_detector",
        "is_duplicate": bool(matches),
        "matches": matches,
    }
