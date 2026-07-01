"""Application exception hierarchy."""

import logging

logger = logging.getLogger(__name__)


class TravelReimbursementError(Exception):
    """Base exception for travel reimbursement agent errors."""


class ValidationError(TravelReimbursementError):
    """Raised when claim validation fails."""


class PolicyLookupError(TravelReimbursementError):
    """Raised when policy retrieval fails."""


# TODO: Add domain-specific exception types as workflows mature.
