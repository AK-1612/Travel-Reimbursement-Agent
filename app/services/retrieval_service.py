"""Retrieval service for policy knowledge access."""

import logging
from typing import Any

from app.tools.policy_lookup import lookup_policy

logger = logging.getLogger(__name__)


class RetrievalService:
    """Retrieve relevant policy context from a vector store."""

    async def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Search indexed policy content."""
        # TODO: Connect to vector index and rank retrieved policy chunks.
        result = lookup_policy(query)
        return [{"text": reference, "source": "travel_policy.md"} for reference in result["references"][:limit]]
