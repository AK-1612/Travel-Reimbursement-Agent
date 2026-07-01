"""Embedding service abstraction."""

import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Create vector embeddings for policy and claim text."""

    async def embed_text(self, text: str) -> list[float]:
        """Return an embedding vector for text."""
        # TODO: Integrate with an embedding provider.
        raise NotImplementedError("Embedding generation is not implemented.")
