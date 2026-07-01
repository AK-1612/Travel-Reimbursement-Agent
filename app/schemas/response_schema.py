"""Response schemas for reimbursement decisions."""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ClaimResponse(BaseModel):
    """Outbound claim response schema."""

    claim_id: str = Field(..., description="External claim identifier.")
    decision: str = Field(..., description="Approve, Partially Approve, Reject, or Manual Review.")
    approved_amount: Decimal = Field(default=Decimal("0.00"))
    rejected_amount: Decimal = Field(default=Decimal("0.00"))
    deductions: list[dict[str, Any]] = Field(default_factory=list)
    missing_documents: list[str] = Field(default_factory=list)
    policy_references: list[str] = Field(default_factory=list)
    tools_called: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    explanation: str = Field(default="")
    approver: Optional[str] = Field(default=None)
    audit_id: Optional[str] = Field(default=None)
    data: dict[str, Any] = Field(default_factory=dict)

    # TODO: Add links to persisted audit records and evidence bundles.


class AgentDecision(BaseModel):
    """Structured LLM decision output schema."""

    decision: str = Field(description="One of: 'Approve', 'Partially Approve', 'Reject', or 'Manual Review'")
    approved_amount: float = Field(description="The amount approved for reimbursement")
    rejected_amount: float = Field(description="The amount rejected")
    missing_documents: list[str] = Field(description="Any missing required documents like receipts")
    policy_references: list[str] = Field(description="Snippets or rules from the policy that justify the decision")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0 based on clarity of the case")
    explanation: str = Field(description="Short explanation of the decision")
