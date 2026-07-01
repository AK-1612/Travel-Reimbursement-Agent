"""Decision confidence calculation tool."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def calculate_confidence(signals: dict[str, Any]) -> float:
    """Calculate confidence score for a reimbursement decision."""
    # TODO: Calibrate confidence using labeled historical outcomes.
    score = 0.88
    if signals.get("missing_documents"):
        score -= 0.28
    if signals.get("exception_requested"):
        score -= 0.22
    if signals.get("is_duplicate"):
        score -= 0.18
    if not signals.get("eligible", True):
        score += 0.04
    if signals.get("over_limit"):
        score -= 0.06
    return max(0.0, min(0.99, round(score, 2)))
