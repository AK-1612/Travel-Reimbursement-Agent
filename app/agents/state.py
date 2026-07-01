"""Agent state models for workflow execution."""

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ReimbursementState:
    """State container passed between workflow nodes."""

    claim: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    decision: dict[str, Any] = field(default_factory=dict)

    # TODO: Replace dictionaries with validated domain schemas.
