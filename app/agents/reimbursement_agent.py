"""Reimbursement agent orchestration."""

from __future__ import annotations

import json
import logging
from decimal import Decimal
from pathlib import Path
from typing import Any

from app.constants import PROJECT_ROOT
from app.services.audit_service import AuditService
from app.services.llm_service import GroqLLMService
from app.tools.limit_checker import check_limit
from app.tools.policy_lookup import lookup_policy

logger = logging.getLogger(__name__)

# --- Tool Definitions ---

def llm_policy_lookup(category: str) -> dict[str, Any]:
    """Look up reimbursement policy context for a given expense category (e.g., 'meals', 'lodging', 'transportation')."""
    return lookup_policy(category)

def llm_check_limit(category: str, amount: float) -> dict[str, Any]:
    """Check if the claim amount is within the policy limit for the given category."""
    return check_limit(category, Decimal(str(amount)))

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "llm_policy_lookup",
            "description": "Look up reimbursement policy context for a given expense category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category of the expense (e.g., 'meals', 'lodging')"
                    }
                },
                "required": ["category"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "llm_check_limit",
            "description": "Check if the claim amount is within the policy limit for the given category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The expense category"
                    },
                    "amount": {
                        "type": "number",
                        "description": "The claimed amount"
                    }
                },
                "required": ["category", "amount"]
            }
        }
    }
]


class ReimbursementAgent:
    """Coordinate claim analysis, policy retrieval, validation, and decisions using Groq."""

    def __init__(
        self,
        audit_service: AuditService | None = None,
        llm_service: GroqLLMService | None = None,
    ) -> None:
        """Initialize the reimbursement agent."""
        self.audit_service = audit_service or AuditService()
        self.llm_service = llm_service or GroqLLMService()
        
        prompt_path = PROJECT_ROOT / "app" / "prompts" / "reimbursement_system_prompt.txt"
        if prompt_path.exists():
            self.system_prompt = prompt_path.read_text(encoding="utf-8")
        else:
            logger.warning(f"System prompt not found at {prompt_path}, using minimal fallback.")
            self.system_prompt = "You are a reimbursement approval agent. Decide: Approve, Partially Approve, Reject, or Manual Review."

    async def evaluate_claim(self, claim_payload: dict[str, Any]) -> dict[str, Any]:
        """Evaluate a travel reimbursement claim using Groq LLM."""
        claim_id = claim_payload.get("claim_id", "unknown")
        
        try:
            if not self.llm_service.is_available:
                logger.warning("GroqLLMService unavailable (no API key). Falling back to deterministic decision.")
                return self._fallback_decision(claim_payload)

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Claim Data:\n{json.dumps(claim_payload, indent=2)}"}
            ]

            response = await self.llm_service.chat(
                messages=messages,
                tools=TOOLS,
                temperature=0.0
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Add the assistant's tool calls to the history
                messages.append(response_message)
                
                # Execute tools
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name == "llm_policy_lookup":
                        function_response = llm_policy_lookup(**function_args)
                    elif function_name == "llm_check_limit":
                        function_response = llm_check_limit(**function_args)
                    else:
                        function_response = {"error": "Unknown function"}
                        
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(function_response, default=str),
                        }
                    )
                
                # Second call with tool results
                response = await self.llm_service.chat(
                    messages=messages,
                    temperature=0.0
                )
                response_message = response.choices[0].message

            if response_message.content:
                text = response_message.content.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.endswith("```"):
                    text = text[:-3]
                decision_data = json.loads(text.strip())
            else:
                decision_data = self._fallback_decision(claim_payload)
                
            output = {
                "claim_id": claim_id,
                "decision": decision_data.get("decision", "Manual Review"),
                "approved_amount": Decimal(str(decision_data.get("approved_amount", 0.0))),
                "rejected_amount": Decimal(str(decision_data.get("rejected_amount", 0.0))),
                "deductions": [],
                "missing_documents": decision_data.get("missing_documents", []),
                "policy_references": decision_data.get("policy_references", []),
                "tools_called": ["llm_policy_lookup", "llm_check_limit"],
                "confidence": decision_data.get("confidence", 0.5),
                "explanation": decision_data.get("explanation", ""),
                "approver": "Finance_Team",
                "data": {
                    "raw_llm_response": decision_data
                },
            }
            
            output["audit_id"] = await self.audit_service.record_event(
                {
                    "audit_id": f"audit-{claim_id}",
                    "claim_id": claim_id,
                    "tools_called": output["tools_called"],
                    "decision": output["decision"],
                    "validation": True,
                }
            )
            return output
            
        except Exception as e:
            logger.error(f"Error evaluating claim with LLM: {e}")
            return self._fallback_decision(claim_payload)

    def _fallback_decision(self, claim_payload: dict[str, Any]) -> dict[str, Any]:
        """Simple deterministic fallback if Groq fails or is not configured."""
        claim_id = claim_payload.get("claim_id", "unknown")
        return {
            "claim_id": claim_id,
            "decision": "Manual Review",
            "approved_amount": Decimal("0.00"),
            "rejected_amount": Decimal("0.00"),
            "deductions": [],
            "missing_documents": [],
            "policy_references": [],
            "tools_called": [],
            "confidence": 0.0,
            "explanation": "Routed to Manual Review due to LLM fallback or missing API key.",
            "approver": "Finance_Team",
            "data": {}
        }
