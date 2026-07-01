"""API tests."""

import logging

logger = logging.getLogger(__name__)


def test_health_endpoint() -> None:
    """Health endpoint returns ok."""
    from fastapi.testclient import TestClient

    from app.main import app

    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
