"""Dashboard views for reimbursement operations."""

import json
import logging
from pathlib import Path

import streamlit as st
import pandas as pd

logger = logging.getLogger(__name__)


def render_dashboard() -> None:
    """Render operational dashboard showing history and metrics."""
    st.header("Operations Dashboard")
    
    sample_output_dir = Path(__file__).resolve().parents[1] / "outputs" / "sample_outputs"
    files = sorted(sample_output_dir.glob("*.json"))
    
    if not files:
        st.info("No processed claims found in `outputs/sample_outputs/`. Run the demo script first.")
        return
        
    data = []
    for path in files:
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
            data.append({
                "Claim ID": content.get("claim_id"),
                "Decision": content.get("decision"),
                "Approved": float(str(content.get("approved_amount", 0))),
                "Rejected": float(str(content.get("rejected_amount", 0))),
                "Confidence": float(str(content.get("confidence", 0))),
            })
        except Exception as e:
            logger.error(f"Failed to read {path}: {e}")
            
    if not data:
        return
        
    df = pd.DataFrame(data)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Processed", len(df))
    with col2:
        st.metric("Total Approved ($)", f"${df['Approved'].sum():.2f}")
    with col3:
        st.metric("Total Rejected ($)", f"${df['Rejected'].sum():.2f}")
    with col4:
        st.metric("Avg Confidence", f"{df['Confidence'].mean():.2f}")
        
    st.markdown("---")
    
    # Split view for charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Decision Breakdown")
        decision_counts = df['Decision'].value_counts().reset_index()
        decision_counts.columns = ['Decision', 'Count']
        st.bar_chart(decision_counts, x='Decision', y='Count')
        
    with chart_col2:
        st.subheader("Financial Impact")
        impact = pd.DataFrame({
            'Amount Type': ['Approved', 'Rejected'],
            'Total': [df['Approved'].sum(), df['Rejected'].sum()]
        })
        st.bar_chart(impact, x='Amount Type', y='Total')

    st.subheader("Recent Decisions")
    st.dataframe(df, use_container_width=True)
