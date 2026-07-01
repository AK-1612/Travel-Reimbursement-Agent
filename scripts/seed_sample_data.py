"""Validate that sample reimbursement data is available."""

import logging
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.constants import CLAIMS_DIR, POLICY_DIR

logger = logging.getLogger(__name__)


def main() -> None:
    """Seed sample data."""
    # TODO: Generate synthetic sample data from templates when needed.
    required_paths = [
        POLICY_DIR / "travel_policy.md",
        POLICY_DIR / "reimbursement_limits.json",
        POLICY_DIR / "approval_matrix.json",
    ]
    claim_files = sorted(Path(CLAIMS_DIR).glob("*.json"))
    if not claim_files:
        raise FileNotFoundError("No sample claims found.")
    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(path)
    print(f"Sample data ready: {len(claim_files)} claims.")


if __name__ == "__main__":
    main()
