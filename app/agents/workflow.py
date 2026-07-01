"""Workflow graph definitions for reimbursement processing."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ReimbursementWorkflow:
    """Define the claim processing workflow graph."""

    def build(self) -> Any:
        """Build the workflow graph."""
        # TODO: Replace this static outline with LangGraph or another workflow runtime.
        return {
            "nodes": [
                "intake",
                "policy_lookup",
                "eligibility_check",
                "receipt_validation",
                "limit_check",
                "duplicate_detection",
                "decision",
                "output_validation",
                "audit",
            ],
            "edges": [
                ("intake", "policy_lookup"),
                ("policy_lookup", "eligibility_check"),
                ("eligibility_check", "receipt_validation"),
                ("receipt_validation", "limit_check"),
                ("limit_check", "duplicate_detection"),
                ("duplicate_detection", "decision"),
                ("decision", "output_validation"),
                ("output_validation", "audit"),
            ],
        }
