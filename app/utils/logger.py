"""Logging configuration utilities."""

import logging

logger = logging.getLogger(__name__)


def configure_logging(level: str = "INFO") -> None:
    """Configure application logging."""
    # TODO: Add JSON logging, correlation IDs, and structured fields.
    logging.basicConfig(level=level)
