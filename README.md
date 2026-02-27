# Oracle Fusion AI Agent — POC

A conversational AI chatbot that queries a PostgreSQL 15 database (Oracle Fusion ERP replica) and answers business questions across **HCM/HR**, **Finance**, and **Procurement** domains using natural language.

## Architecture

```
User ─→ Streamlit Chat UI ─→ FastAPI ─→ LangChain Agent (GPT-4o)
                                            │
                           ┌────────────────┼────────────────┐
                           ▼                ▼                ▼
                     HCM Tool        Finance Tool    Procurement Tool
                           │                │                │
                     ┌─────┴─────┐   ┌──────┴─────┐   ┌─────┴──────┐
                     │  PGVector  │   │  PGVector   │   │  PGVector   │
                     │  Retriever │   │  Retriever  │   │  Retriever  │
                     └─────┬─────┘   └──────┬──────┘   └──────┬─────┘
                           │                │                  │
                     SQL Generator (GPT-4o + Schema Context)
                           │
                     PostgreSQL 15 (ERP Replica)
                           │
                     Pandas Analytics Engine
                           │
                     Plotly Charts → Streamlit UI
```

**7 Layers:**
1. **Streamlit UI** — Dark-themed chat with domain badges, charts, SQL viewer
2. **FastAPI API** — REST endpoints with session management
3. **LangChain Orchestrator** — GPT-4o agent with tool-calling and memory
4. **Intent Router** — GPT-4o classifies queries into domains + calculation types
5. **SQL Generator** — Generates validated PostgreSQL from natural language + schema context
6. **Analytics Engine** — Pandas/NumPy calculations (LLM never does arithmetic)
7. **PGVector RAG** — Cosine similarity search for schema documentation retrieval

## Prerequisites

- **Python 3.11+**
- **PostgreSQL 15** with **pgvector** extension installed
- **OpenAI API key** (GPT-4o + text-embedding-3-large)

## Setup

```bash
# 1. Install dependencies
cd oracle_fusion_poc
pip install -r requirements.txt

# 2. Configure environment
cp config/.env.example .env
# Edit .env with your OpenAI API key and PostgreSQL credentials

# 3. Create database (in PostgreSQL)
# CREATE DATABASE oracle_fusion_poc;
# CREATE USER poc_user WITH PASSWORD 'your_password';
# GRANT ALL PRIVILEGES ON DATABASE oracle_fusion_poc TO poc_user;

# 4. Run setup (creates tables, seeds data, embeds schema docs)
python setup_db.py

# 5. Start backend
uvicorn backend.main:app --reload --port 8000

# 6. Start frontend (in a new terminal)
streamlit run frontend/app.py
```

## Demo Queries & Expected Outputs

| Query | Domain | Expected Output |
|-------|--------|-----------------|
| "How many employees are in Engineering?" | HCM | **47** active employees + bar chart |
| "Which departments are over budget?" | Finance | **CC003 (Marketing)** over budget in Q4 2025 + variance chart |
| "What is the delta on Engagement E-205?" | Procurement | **+12.4%** delta (£82,000 → £92,180) + delta chart |

## Project Structure

```
oracle_fusion_poc/
├── backend/                    # FastAPI + LangChain agent
│   ├── main.py                # API server
│   ├── agent/                 # LangChain orchestrator + tools
│   │   ├── orchestrator.py    # Main agent with GPT-4o
│   │   ├── router.py          # Intent classifier
│   │   ├── sql_generator.py   # SQL generation + validation
│   │   └── tools/             # Domain-specific LangChain tools
│   ├── analytics/             # Pandas calculations + Plotly charts
│   └── db/                    # PostgreSQL connection helpers
├── frontend/                  # Streamlit chat application
├── database/                  # SQL schema + seed data
├── vector_store/              # PGVector embedding + retrieval
├── config/                    # Settings + .env template
├── tests/                     # pytest test suite
├── setup_db.py               # One-command database setup
└── requirements.txt
```

## Key Design Decisions

- **LLM never calculates** — All arithmetic is done in Pandas (`calculations.py`). GPT-4o only generates SQL and writes narrative text.
- **PGVector for RAG** — Schema documentation is embedded and retrieved via cosine similarity, giving GPT-4o precise context for SQL generation.
- **SQL validation gate** — Every generated SQL is validated (`validate_sql`) to block non-SELECT statements before execution.
- **Session memory** — LangChain `ConversationBufferWindowMemory` (k=10) enables follow-up questions.
- **Plotly dark theme** — All charts use a consistent dark colour scheme matching the Streamlit UI.

## Running Tests

```bash
cd oracle_fusion_poc
pytest tests/ -v
```
