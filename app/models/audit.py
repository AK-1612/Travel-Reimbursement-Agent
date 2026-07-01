"""Audit domain model placeholders."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AuditEvent:
    """Audit event domain entity."""

    event_id: str
    created_at: datetime | None = None

    # TODO: Add actor, action, correlation ID, inputs, outputs, and metadata.
