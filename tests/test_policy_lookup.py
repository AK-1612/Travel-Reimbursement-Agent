"""Policy lookup tests."""

import logging

logger = logging.getLogger(__name__)


def test_policy_lookup_returns_references() -> None:
    """Policy lookup returns relevant context."""
    from app.tools.policy_lookup import lookup_policy

    result = lookup_policy("meals")

    assert result["tool"] == "policy_lookup"
    assert result["references"]
    assert "categories" in result["limits"]
