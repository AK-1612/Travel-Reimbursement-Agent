"""Shared application constants."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

APP_NAME: str = "travel-reimbursement-agent"
PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
POLICY_DIR: Path = PROJECT_ROOT / "knowledge_base" / "policies"
CLAIMS_DIR: Path = PROJECT_ROOT / "sample_data" / "claims"
RECEIPTS_DIR: Path = PROJECT_ROOT / "sample_data" / "receipts"
OUTPUT_DIR: Path = PROJECT_ROOT / "outputs"
DEFAULT_CONFIDENCE_THRESHOLD: float = 0.72

DECISION_APPROVE: str = "Approve"
DECISION_PARTIAL_APPROVE: str = "Partially Approve"
DECISION_REJECT: str = "Reject"
DECISION_MANUAL_REVIEW: str = "Manual Review"

# TODO: Move constants that vary by environment into managed configuration.
