"""Reimbursement limit checking tool."""

from __future__ import annotations

import json
import logging
from decimal import Decimal
from typing import Any

from app.constants import POLICY_DIR

logger = logging.getLogger(__name__)


def check_limit(category: str, amount: Decimal, policy_dir: str | None = None) -> dict[str, Any]:
    """Check whether a claim amount is within configured limits."""
    # TODO: Support region, trip type, currency conversion, and employee bands.
    root = POLICY_DIR if policy_dir is None else POLICY_DIR.__class__(policy_dir)
    limits = json.loads((root / "reimbursement_limits.json").read_text(encoding="utf-8"))
    category_key = category.lower()
    rule = limits.get("categories", {}).get(category_key)
    if rule is None:
        return {
            "tool": "limit_checker",
            "category": category_key,
            "eligible": False,
            "within_limit": False,
            "limit": Decimal("0.00"),
            "approved_amount": Decimal("0.00"),
            "overage": amount,
            "reason": "Category is not eligible under current policy.",
        }

    limit = Decimal(str(rule["limit"]))
    approved_amount = min(amount, limit)
    overage = max(Decimal("0.00"), amount - limit)
    return {
        "tool": "limit_checker",
        "category": category_key,
        "eligible": bool(rule.get("eligible", True)),
        "within_limit": amount <= limit,
        "limit": limit,
        "approved_amount": approved_amount,
        "overage": overage,
        "reason": rule.get("basis", ""),
    }
