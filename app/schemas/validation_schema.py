"""Validation schemas for reimbursement checks."""

import logging
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ValidationResult(BaseModel):
    """Validation result schema."""

    is_valid: bool = Field(default=False)
    findings: list[dict[str, Any]] = Field(default_factory=list)
    missing_documents: list[str] = Field(default_factory=list)
    reason_codes: list[str] = Field(default_factory=list)

    # TODO: Replace generic finding dictionaries with typed severity models.
