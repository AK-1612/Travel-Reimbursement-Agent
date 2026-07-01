"""Primary API routes for reimbursement workflows."""

import logging

from fastapi import APIRouter, Depends

from app.agents.reimbursement_agent import ReimbursementAgent
from app.api.dependencies import get_reimbursement_agent
from app.schemas.request_schema import ClaimRequest
from app.schemas.response_schema import ClaimResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["reimbursements"])


@router.post("/claims")
async def submit_claim(
    payload: ClaimRequest,
    agent: ReimbursementAgent = Depends(get_reimbursement_agent),
) -> ClaimResponse:
    """Accept a reimbursement claim for future agent processing."""
    # TODO: Add authentication, idempotency keys, and async job handling.
    result = await agent.evaluate_claim(payload.model_dump(mode="json"))
    return ClaimResponse(**result)
