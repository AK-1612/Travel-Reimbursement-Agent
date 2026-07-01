"""Policy lookup tool for file-backed reimbursement policies."""

from __future__ import annotations

import json
import logging
from typing import Any

from app.constants import POLICY_DIR

logger = logging.getLogger(__name__)


def lookup_policy(query: str, policy_dir: str | None = None) -> dict[str, Any]:
    """Look up reimbursement policy context."""
    # TODO: Replace keyword matching with vector retrieval over policy chunks.
    root = POLICY_DIR if policy_dir is None else POLICY_DIR.__class__(policy_dir)
    policy_text = (root / "travel_policy.md").read_text(encoding="utf-8")
    limits = json.loads((root / "reimbursement_limits.json").read_text(encoding="utf-8"))
    category = query.lower().strip()
    references = [
        line.strip("- ").strip()
        for line in policy_text.splitlines()
        if category in line.lower() or "receipt" in line.lower() or "manual review" in line.lower()
    ]
    return {
        "tool": "policy_lookup",
        "category": category,
        "references": references[:5],
        "limits": limits,
    }
