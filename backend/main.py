"""FastAPI application — Oracle Fusion AI Agent API."""

import uuid
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agent.orchestrator import OracleFusionAgent

app = FastAPI(
    title="Oracle Fusion AI Agent API",
    description="Conversational AI for Oracle Fusion ERP data — HCM, Finance, Procurement",
    version="1.0.0-poc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single agent instance (stateful memory per session_id)
agent = OracleFusionAgent()


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    domain: str
    query_type: str
    sql_used: str
    chart_data: Optional[dict] = None
    metrics: Optional[dict] = None
    execution_time_ms: int
    session_id: str
    row_count: int
    error: Optional[str] = None


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a user query and return a structured response."""
    session_id = request.session_id or str(uuid.uuid4())
    response = agent.run(query=request.query, session_id=session_id)
    return ChatResponse(
        answer=response.answer,
        domain=response.domain,
        query_type=response.query_type,
        sql_used=response.sql_used or "",
        chart_data=response.chart_data,
        metrics=response.metrics,
        execution_time_ms=response.execution_time_ms,
        session_id=session_id,
        row_count=response.row_count,
        error=response.error,
    )


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "Oracle Fusion AI Agent POC"}


@app.get("/schema-info")
async def schema_info() -> dict:
    """Return available domains and sample queries."""
    return {
        "domains": ["HCM", "FINANCE", "PROCUREMENT"],
        "sample_queries": {
            "HCM": [
                "How many employees are in Engineering?",
                "What is the attrition rate?",
            ],
            "FINANCE": [
                "Which departments are over budget?",
                "Show overdue AP invoices",
            ],
            "PROCUREMENT": [
                "What is the delta on Engagement E-205?",
                "Show pending POs older than 14 days",
            ],
        },
    }
