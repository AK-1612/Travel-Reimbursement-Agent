"""Claim domain model."""

import logging
from dataclasses import dataclass
from decimal import Decimal

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Claim:
    """Travel reimbursement claim domain entity."""

    claim_id: str
    employee_id: str
    category: str
    amount: Decimal
    currency: str
    expense_date: str

    # TODO: Add richer employee, trip, receipt, and approval metadata.
