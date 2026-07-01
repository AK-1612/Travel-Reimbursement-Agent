# Architecture

The prototype follows a small layered architecture:

- `api`: FastAPI routes and dependencies.
- `agents`: orchestration of policy lookup, tools, decisioning, explanation, and audit.
- `tools`: deterministic functions that expose policy lookup, receipt validation, limit checks, duplicate detection, approval routing, confidence scoring, and output validation.
- `services`: service abstractions for reasoning, retrieval, validation, decisioning, and audit persistence.
- `knowledge_base`: mock policy documents and rule tables.
- `sample_data`: synthetic claim examples.
- `outputs`: generated decisions and audit logs.

The local reasoning service acts as a free-tier stand-in for an LLM planner/explainer. It can be replaced by a provider-backed tool-calling LLM without changing the API contract.
