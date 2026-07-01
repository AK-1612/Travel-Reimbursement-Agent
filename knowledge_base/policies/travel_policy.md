# Travel Reimbursement Policy

## Purpose

This mock policy defines reimbursement rules for business travel expenses used by the demo agent.

## General Rules

- Employees must submit claims within 30 days of the expense date.
- Receipts are required for airfare, lodging, meals, taxi, rideshare, parking, and conference fees.
- Missing receipts, exception requests, unclear vendors, or conflicting evidence must be routed to Manual Review.
- Duplicate claims must be rejected when the same employee, receipt, vendor, date, and amount are already present in claim history.
- Non-business expenses are not reimbursable.

## Category Rules

- Airfare is reimbursable up to the configured airfare limit when tied to approved business travel.
- Lodging is reimbursable up to the configured nightly lodging limit.
- Meals are reimbursable up to the configured daily meal limit.
- Taxi and rideshare expenses are reimbursable up to the configured ground transport limit.
- Conference fees are reimbursable up to the configured conference fee limit when the trip purpose is business related.
- Entertainment, minibar, personal upgrades, and family travel are not eligible for reimbursement.

## Manual Review Triggers

- The claim requests an exception to policy.
- Required receipt metadata or attachment evidence is missing.
- The claim amount exceeds approval thresholds or contains ambiguous notes.
- The confidence score falls below the configured threshold.
