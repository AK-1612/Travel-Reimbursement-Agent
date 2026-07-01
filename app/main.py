"""FastAPI application entrypoint for the travel reimbursement agent."""

import logging

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.routes import router as api_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # TODO: Add middleware, lifecycle hooks, tracing, and dependency wiring.
    application = FastAPI(title="Travel Reimbursement Agent")
    application.include_router(health_router)
    application.include_router(api_router)
    return application


app = create_app()
