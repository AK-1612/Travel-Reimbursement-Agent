"""Application startup hooks."""

import logging
from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)


async def run_startup_tasks() -> None:
    """Run startup tasks required before serving traffic."""
    # TODO: Initialize model clients, vector indexes, telemetry, and caches.


StartupTask = Callable[[], Awaitable[None]]
