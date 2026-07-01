"""Approval matrix tool."""

import json
import logging
from decimal import Decimal
from typing import Any

from app.constants import POLICY_DIR

logger = logging.getLogger(__name__)


def resolve_approver(claim_payload: dict[str, Any]) -> dict[str, Any]:
    """Resolve approval path for a claim."""
    # TODO: Add org hierarchy, delegation, and regional approval policies.
    matrix = json.loads((POLICY_DIR / "approval_matrix.json").read_text(encoding="utf-8"))
    amount = Decimal(str(claim_payload.get("amount") or "0"))
    for rule in matrix.get("rules", []):
        if amount <= Decimal(str(rule["max_amount"])):
            return {
                "tool": "approval_matrix",
                "approver": rule["approver"],
                "approval_required": bool(rule["approval_required"]),
                "basis": rule["basis"],
            }
    fallback = matrix.get("fallback", {})
    return {
        "tool": "approval_matrix",
        "approver": fallback.get("approver", "finance_director"),
        "approval_required": True,
        "basis": fallback.get("basis", "High-value claim requires senior finance review."),
    }
