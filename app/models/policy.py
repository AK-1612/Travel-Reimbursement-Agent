"""Policy domain model."""

import logging
from dataclasses import dataclass
from decimal import Decimal

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Policy:
    """Travel reimbursement policy domain entity."""

    policy_id: str
    category: str
    limit_amount: Decimal
    receipt_required: bool = True

    # TODO: Add effective dates, regions, exception handling, and policy owners.
