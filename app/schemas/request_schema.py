"""Request schemas for reimbursement claim intake."""

from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ReceiptMetadata(BaseModel):
    """Receipt metadata supplied with a reimbursement claim."""

    receipt_id: Optional[str] = Field(default=None)
    vendor: Optional[str] = Field(default=None)
    amount: Optional[Decimal] = Field(default=None)
    currency: str = Field(default="USD")
    transaction_date: Optional[str] = Field(default=None)
    attachment_present: bool = Field(default=False)

    # TODO: Add OCR extraction fields and attachment checksum metadata.


class ClaimRequest(BaseModel):
    """Inbound claim request schema."""

    claim_id: str = Field(..., description="External claim identifier.")
    employee_id: str = Field(..., description="Employee identifier.")
    employee_level: str = Field(default="staff")
    department: str = Field(default="general")
    trip_purpose: str = Field(default="")
    category: str = Field(..., description="Expense category.")
    amount: Decimal = Field(..., ge=0)
    currency: str = Field(default="USD")
    expense_date: str = Field(..., description="Expense date in ISO format.")
    receipt: ReceiptMetadata = Field(default_factory=ReceiptMetadata)
    notes: Optional[str] = Field(default=None)
    exception_requested: bool = Field(default=False)
    payload: dict[str, Any] = Field(default_factory=dict)

    # TODO: Add strict date validation and employee master-data lookup.
