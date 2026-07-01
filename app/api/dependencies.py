"""API dependency providers."""

import logging
from functools import lru_cache

from app.agents.reimbursement_agent import ReimbursementAgent

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_reimbursement_agent() -> ReimbursementAgent:
    """Provide a reimbursement agent instance."""
    # TODO: Wire a full dependency injection container for provider clients.
    return ReimbursementAgent()
