# ✈️ Travel Reimbursement Agent

An enterprise-grade autonomous AI agent for evaluating travel and expense claims. Powered by **Groq (Llama 3.3 70B)** and built on **FastAPI** and **Streamlit**.

This project processes structured employee reimbursement claims, references company travel policies, checks configurable limits via tools, and outputs a structured approval decision with a full audit log.

## 📦 Architecture & Deliverables

This repository is structured as a production-ready enterprise scaffold:

- ✅ **Agentic LLM Pipeline** (`app/agents/`) — Groq API integration with structured outputs (JSON) and tool calling.
- ✅ **Modular Tool Layer** (`app/tools/`) — Policy lookup, limit checking, duplicate detection, and receipt validation.
- ✅ **FastAPI REST API** (`app/main.py`) — Asynchronous web service with a `/claims` endpoint.
- ✅ **Streamlit UI** (`ui/streamlit_app.py`) — Interactive dashboard to evaluate claims and view historical operational metrics.
- ✅ **Audit Logging** (`app/services/audit_service.py`) — Persists LLM decisions and tool traces as immutable JSON records in `outputs/audit_logs/`.
- ✅ **Sample Data** (`sample_data/`) — Includes 5 diverse test claims and historical data.
- ✅ **Unit Tests** (`tests/`) — Pytest suite covering agent logic, schema validation, and tool execution.

## 🚀 Quickstart

### 1. Environment Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and set your Groq API key:

```bash
cp .env.example .env
```

Edit `.env` and add your key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

### 3. Run the CLI Demo

Test the agent logic against all 5 sample claims in bulk:

```bash
python3 scripts/run_demo.py
```
*Outputs a clean ASCII table of decisions and writes full JSON traces to `outputs/sample_outputs/`.*

### 4. Run the Streamlit UI

Launch the interactive dashboard to evaluate individual claims and view system metrics:

```bash
streamlit run ui/streamlit_app.py
```

### 5. Run the FastAPI Server

Start the REST API for programmatic integrations:

```bash
uvicorn app.main:app --reload
```

## 🧠 Design Decisions

1. **Groq + Llama 3.3 70B**: Chosen for lightning-fast inference and excellent structured JSON/tool-calling capabilities.
2. **Tool-Calling over RAG**: Since the reimbursement limits are structured (numbers, categories), we built a deterministic `limit_checker` tool rather than relying purely on LLM math/RAG. The LLM handles the unstructured policy text (`policy_lookup`) and nuanced reasoning.
3. **Deterministic Fallbacks**: If the Groq API fails or the key is missing, the agent gracefully degrades to a deterministic `Manual Review` outcome rather than crashing the pipeline.
4. **Separation of Concerns**: Core agent logic is decoupled from FastAPI routing and Streamlit UI, allowing for easy testing and deployment flexibility.

## 🧪 Testing

Run the full pytest suite:
```bash
python3 -m pytest tests/ -v
```
