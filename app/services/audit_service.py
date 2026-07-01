"""Audit service for compliance and traceability records."""

import json
import logging
from datetime import datetime, timezone
from typing import Any

from app.constants import OUTPUT_DIR

logger = logging.getLogger(__name__)


class AuditService:
    """Persist audit events for reimbursement decisions."""

    async def record_event(self, event: dict[str, Any]) -> str:
        """Record an audit event."""
        # TODO: Persist audit data to durable storage in production.
        audit_id = event.get("audit_id") or f"audit-{event.get('claim_id', 'unknown')}"
        payload = {
            "audit_id": audit_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            **event,
        }
        audit_dir = OUTPUT_DIR / "audit_logs"
        audit_dir.mkdir(parents=True, exist_ok=True)
        (audit_dir / f"{audit_id}.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return audit_id
