"""Agent tests."""

import asyncio
import json
import logging
from pathlib import Path

from app.agents.reimbursement_agent import ReimbursementAgent
from app.constants import CLAIMS_DIR

logger = logging.getLogger(__name__)


def test_agent_fallback_on_no_api_key() -> None:
    """Agent should fallback to Manual Review if no API key is provided."""
    # Temporarily remove any API key config from the environment
    import os
    original_key = os.environ.get("GROQ_API_KEY")
    if "GROQ_API_KEY" in os.environ:
        del os.environ["GROQ_API_KEY"]
        
    try:
        agent = ReimbursementAgent()
        
        claim_path = CLAIMS_DIR / "CLM-1001.json"
        if not claim_path.exists():
            return # Skip if sample data missing
            
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        result = asyncio.run(agent.evaluate_claim(claim))

        assert result["decision"] == "Manual Review"
        assert result["approved_amount"] == 0
        assert "fallback" in result["explanation"].lower()
    finally:
        if original_key is not None:
            os.environ["GROQ_API_KEY"] = original_key


# TODO: Add full suite of mocked Groq response tests to verify LLM tool parsing and decision extraction logic.
