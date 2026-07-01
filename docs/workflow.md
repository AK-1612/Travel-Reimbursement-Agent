# Workflow

1. Accept a claim through the API, demo script, or Streamlit UI.
2. Plan tool usage using the local reasoning service.
3. Retrieve policy context for the claim category.
4. Check category eligibility.
5. Validate receipt metadata and attachment presence.
6. Check category reimbursement limits.
7. Detect duplicates using historical claim data.
8. Resolve the approval path.
9. Calculate confidence from validation signals.
10. Decide one of `Approve`, `Partially Approve`, `Reject`, or `Manual Review`.
11. Validate the output structure.
12. Persist an audit event.
