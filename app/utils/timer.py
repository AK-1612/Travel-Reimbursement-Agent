"""Timing utility placeholders."""

from __future__ import annotations

import logging
from contextlib import AbstractContextManager
from types import TracebackType

logger = logging.getLogger(__name__)


class Timer(AbstractContextManager["Timer"]):
    """Context manager placeholder for operation timing."""

    def __enter__(self) -> "Timer":
        """Start timing."""
        # TODO: Capture monotonic start time.
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        """Stop timing."""
        # TODO: Capture duration and emit telemetry.
        return False
