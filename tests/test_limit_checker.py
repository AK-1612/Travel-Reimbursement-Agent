"""Limit checker tests."""

import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


def test_limit_checker_partially_approves_overage() -> None:
    """Limit checker calculates approved amount and overage."""
    from app.tools.limit_checker import check_limit

    result = check_limit("lodging", Decimal("312.00"))

    assert result["eligible"] is True
    assert result["within_limit"] is False
    assert result["approved_amount"] == Decimal("250")
    assert result["overage"] == Decimal("62.00")
