# API

## Health

`GET /health`

Returns service status.

## Submit Claim

`POST /api/v1/claims`

Accepts a reimbursement claim JSON payload and returns a structured decision.

Required fields include:

- `claim_id`
- `employee_id`
- `category`
- `amount`
- `currency`
- `expense_date`
- `receipt`

Response fields include:

- `decision`
- `approved_amount`
- `rejected_amount`
- `missing_documents`
- `policy_references`
- `tools_called`
- `confidence`
- `explanation`
- `audit_id`
