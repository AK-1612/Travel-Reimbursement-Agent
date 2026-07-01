"""Eligibility checking tool."""

import json
import logging
from typing import Any

from app.constants import POLICY_DIR

logger = logging.getLogger(__name__)


def check_eligibility(claim_payload: dict[str, Any]) -> dict[str, Any]:
    """Check whether a claim is eligible for reimbursement."""
    # TODO: Add employee status, travel authorization, and project code checks.
    limits = json.loads((POLICY_DIR / "reimbursement_limits.json").read_text(encoding="utf-8"))
    category = str(claim_payload.get("category", "")).lower()
    rule = limits.get("categories", {}).get(category)
    eligible = bool(rule and rule.get("eligible", True))
    return {
        "tool": "eligibility_checker",
        "eligible": eligible,
        "category": category,
        "reason": rule.get("basis", "Category is not listed in policy.") if rule else "Category is not listed in policy.",
    }
