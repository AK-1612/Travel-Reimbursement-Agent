"""Decision service for reimbursement outcomes."""

import logging
from decimal import Decimal
from typing import Any

from app.constants import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    DECISION_APPROVE,
    DECISION_MANUAL_REVIEW,
    DECISION_PARTIAL_APPROVE,
    DECISION_REJECT,
)

logger = logging.getLogger(__name__)


class DecisionService:
    """Create structured reimbursement decisions."""

    async def decide(self, context: dict[str, Any]) -> dict[str, Any]:
        """Produce a reimbursement decision from validated context."""
        # TODO: Replace rule composition with a policy-aware, testable decision graph.
        amount = Decimal(str(context["claim"]["amount"]))
        limit_result = context["limit_result"]
        receipt_result = context["receipt_result"]
        eligibility_result = context["eligibility_result"]
        duplicate_result = context["duplicate_result"]
        confidence = context["confidence"]

        if duplicate_result["is_duplicate"] or not eligibility_result["eligible"]:
            decision = DECISION_REJECT
            approved_amount = Decimal("0.00")
            rejected_amount = amount
        elif receipt_result["missing_documents"] or context["claim"].get("exception_requested") or confidence < DEFAULT_CONFIDENCE_THRESHOLD:
            decision = DECISION_MANUAL_REVIEW
            approved_amount = Decimal("0.00")
            rejected_amount = Decimal("0.00")
        elif limit_result["within_limit"]:
            decision = DECISION_APPROVE
            approved_amount = amount
            rejected_amount = Decimal("0.00")
        else:
            decision = DECISION_PARTIAL_APPROVE
            approved_amount = limit_result["approved_amount"]
            rejected_amount = limit_result["overage"]

        return {
            "decision": decision,
            "approved_amount": approved_amount,
            "rejected_amount": rejected_amount,
        }
