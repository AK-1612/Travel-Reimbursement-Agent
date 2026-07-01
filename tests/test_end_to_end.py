"""End-to-end tests."""

import asyncio
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def test_sample_claims_cover_required_decision_paths() -> None:
    """Sample claims cover approve, partial, reject, and manual review paths."""
    from app.agents.reimbursement_agent import ReimbursementAgent

    async def evaluate_all() -> set[str]:
        agent = ReimbursementAgent()
        decisions: set[str] = set()
        for path in sorted(Path("sample_data/claims").glob("*.json")):
            claim = json.loads(path.read_text(encoding="utf-8"))
            result = await agent.evaluate_claim(claim)
            decisions.add(result["decision"])
        return decisions

    decisions = asyncio.run(evaluate_all())

    assert {"Approve", "Partially Approve", "Reject", "Manual Review"}.issubset(decisions)
