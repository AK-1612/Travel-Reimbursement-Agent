"""Decision domain model."""

import logging
from dataclasses import dataclass
from decimal import Decimal

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Decision:
    """Reimbursement decision domain entity."""

    decision_id: str
    status: str
    approved_amount: Decimal
    rejected_amount: Decimal
    confidence: float

    # TODO: Add normalized reason codes, reviewer assignment, and SLA metadata.
