"""Health check routes."""

import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Return service health status."""
    # TODO: Add dependency health checks for model providers and vector store.
    return {"status": "ok"}
