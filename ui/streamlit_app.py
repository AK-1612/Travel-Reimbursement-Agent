"""Streamlit application entrypoint."""

import sys
import asyncio
import json
import logging
from pathlib import Path

# Add project root to path so we can import 'app'
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
from dotenv import load_dotenv

from app.agents.reimbursement_agent import ReimbursementAgent
from ui.components import render_claim_summary, render_decision_result
from ui.dashboard import render_dashboard

# Ensure env vars are loaded for UI runs
load_dotenv()

logger = logging.getLogger(__name__)

# Must be the first Streamlit command
st.set_page_config(
    page_title="Travel Reimbursement AI",
    page_icon="✈️",
    layout="wide",
)

def main() -> None:
    """Render the Streamlit app."""
    st.title("✈️ Travel Reimbursement Agent")
    st.markdown("Enterprise AI Agent powered by **Groq (Llama 3.3 70B)**")
    
    tab_claims, tab_dashboard = st.tabs(["📋 Evaluate Claim", "📊 Dashboard"])
    
    # Setup data paths
    sample_dir = Path(__file__).resolve().parents[1] / "sample_data" / "claims"
    sample_files = sorted(sample_dir.glob("*.json"))
    
    with tab_claims:
        if not sample_files:
            st.error(f"No sample claims found in {sample_dir}")
            return
            
        selected_file = st.selectbox(
            "Select a sample claim to evaluate:", 
            sample_files, 
            format_func=lambda p: p.name
        )
        
        claim_payload = json.loads(selected_file.read_text(encoding="utf-8"))
        
        st.markdown("---")
        render_claim_summary(claim_payload)
        st.markdown("---")
        
        if st.button("🤖 Run AI Agent Evaluation", type="primary", use_container_width=True):
            with st.spinner("Analyzing claim, looking up policies, and checking limits..."):
                try:
                    agent = ReimbursementAgent()
                    result = asyncio.run(agent.evaluate_claim(claim_payload))
                    st.success("Analysis Complete!")
                    render_decision_result(result)
                except Exception as e:
                    st.error(f"Error running agent: {e}")
                    
    with tab_dashboard:
        render_dashboard()


if __name__ == "__main__":
    main()
