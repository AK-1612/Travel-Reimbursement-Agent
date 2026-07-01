"""Reusable Streamlit components."""

import logging
from typing import Any

import streamlit as st
import pandas as pd

logger = logging.getLogger(__name__)


def render_claim_summary(claim: dict[str, Any]) -> None:
    """Render a visual card for a claim."""
    st.subheader(f"Claim: {claim.get('claim_id', 'Unknown')}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Amount", f"{claim.get('amount', 0)} {claim.get('currency', 'USD')}")
    with col2:
        st.metric("Category", str(claim.get('category', '')).title())
    with col3:
        st.metric("Date", claim.get('expense_date', 'N/A'))
        
    st.markdown(f"**Purpose:** {claim.get('trip_purpose', 'N/A')}")
    st.markdown(f"**Notes:** {claim.get('notes', 'None')}")
    
    receipt = claim.get("receipt", {})
    if receipt.get("attachment_present"):
        st.info(f"📎 Receipt attached: {receipt.get('vendor', 'Unknown')} ({receipt.get('transaction_date', 'N/A')})")
    else:
        st.warning("⚠️ No receipt attached.")


def render_decision_result(result: dict[str, Any]) -> None:
    """Render the AI decision output."""
    decision = result.get("decision", "Unknown")
    
    if decision == "Approve":
        st.success(f"### ✅ {decision}")
    elif decision == "Reject":
        st.error(f"### ❌ {decision}")
    elif decision == "Partially Approve":
        st.warning(f"### ⚠️ {decision}")
    else:
        st.info(f"### 🔍 {decision}")
        
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Approved", f"${float(str(result.get('approved_amount', 0))):.2f}")
    with col2:
        st.metric("Rejected", f"${float(str(result.get('rejected_amount', 0))):.2f}")
        
    st.markdown("#### Explanation")
    st.write(result.get("explanation", "No explanation provided."))
    
    refs = result.get("policy_references", [])
    if refs:
        st.markdown("#### Policy References")
        for ref in refs:
            st.markdown(f"- {ref}")
            
    docs = result.get("missing_documents", [])
    if docs:
        st.markdown("#### Missing Documents")
        for doc in docs:
            st.markdown(f"- {doc}")
