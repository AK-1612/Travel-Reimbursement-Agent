"""Receipt domain model."""

import logging
from dataclasses import dataclass
from decimal import Decimal

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class Receipt:
    """Receipt domain entity."""

    receipt_id: str
    vendor: str
    amount: Decimal
    currency: str
    transaction_date: str
    attachment_present: bool

    # TODO: Add attachment path, OCR fields, checksum, and fraud signals.
