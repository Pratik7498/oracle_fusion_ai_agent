"""FastAPI application — Oracle Fusion AI Agent API."""

import uuid
import random
import logging
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agent.orchestrator import OracleFusionAgent
from backend.db.connection import execute_query

logger = logging.getLogger(__name__)

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


def _pick(items: list, n: int = 1) -> list:
    """Pick n random items from list, or all if fewer."""
    return random.sample(items, min(n, len(items))) if items else []


@app.get("/sample-queries")
async def sample_queries() -> dict:
    """Generate dynamic sample queries using real entity names from the database."""
    queries: dict[str, list[str]] = {"HCM": [], "FINANCE": [], "PROCUREMENT": []}

    try:
        # ── Pull real entity names ──
        depts = execute_query("SELECT dept_name FROM hcm_departments ORDER BY RANDOM() LIMIT 10")
        dept_names = depts["dept_name"].tolist() if not depts.empty else ["Engineering"]

        suppliers = execute_query("SELECT supplier_name FROM sup_suppliers ORDER BY RANDOM() LIMIT 10")
        sup_names = suppliers["supplier_name"].tolist() if not suppliers.empty else ["Acme Ltd"]

        grades = execute_query("SELECT DISTINCT grade_code FROM hcm_grades ORDER BY RANDOM() LIMIT 5")
        grade_codes = grades["grade_code"].tolist() if not grades.empty else ["G5"]

        cc = execute_query("SELECT cost_centre_name FROM fin_cost_centres ORDER BY RANDOM() LIMIT 5")
        cc_names = cc["cost_centre_name"].tolist() if not cc.empty else ["IT"]

        customers = execute_query("SELECT customer_name FROM fin_ar_customers ORDER BY RANDOM() LIMIT 5")
        cust_names = customers["customer_name"].tolist() if not customers.empty else ["Corp A"]

        categories = execute_query("SELECT DISTINCT category FROM proc_po_headers WHERE category IS NOT NULL ORDER BY RANDOM() LIMIT 5")
        cat_names = categories["category"].tolist() if not categories.empty else ["IT"]

        # ── Build HCM queries ──
        d1, d2 = _pick(dept_names, 2) if len(dept_names) >= 2 else (dept_names[0], dept_names[0])
        g1 = _pick(grade_codes, 1)[0] if grade_codes else "G5"
        hcm_pool = [
            f"How many employees are in {d1}?",
            f"Show average salary by department",
            f"What is the attrition rate for the last year?",
            f"Show headcount breakdown by department",
            f"List employees in grade {g1}",
            f"Show salary distribution by grade",
            f"Which department has the highest average salary?",
            f"Show performance review scores for {d2}",
            f"How many promotions happened this year?",
            f"Show training completion rate by department",
            f"List top 10 highest paid employees",
            f"Show gender distribution across departments",
        ]
        queries["HCM"] = random.sample(hcm_pool, min(4, len(hcm_pool)))

        # ── Build FINANCE queries ──
        s1 = _pick(sup_names, 1)[0] if sup_names else "Acme Ltd"
        c1 = _pick(cc_names, 1)[0] if cc_names else "IT"
        cu1 = _pick(cust_names, 1)[0] if cust_names else "Corp A"
        fin_pool = [
            f"Which cost centres are over budget?",
            f"Show budget vs actual variance for {c1}",
            f"Show total AP invoice amount by supplier",
            f"What is the total outstanding AP?",
            f"Show overdue AP invoices",
            f"Show AP aging analysis",
            f"How much has {s1} been paid this year?",
            f"Show GL journal entries for this quarter",
            f"What is the total AR outstanding for {cu1}?",
            f"Show AP payments by month",
            f"List invoices pending approval",
            f"Show budget utilization by cost centre",
        ]
        queries["FINANCE"] = random.sample(fin_pool, min(4, len(fin_pool)))

        # ── Build PROCUREMENT queries ──
        cat1 = _pick(cat_names, 1)[0] if cat_names else "IT"
        s2 = _pick(sup_names, 1)[0] if sup_names else "Vendor X"
        proc_pool = [
            f"Show purchase orders by status",
            f"Which supplier has the highest total PO spend?",
            f"Show pending POs older than 14 days",
            f"List top 5 suppliers by PO amount",
            f"Show requisitions pending approval",
            f"What is the total contract value by supplier?",
            f"Show PO spending in {cat1} category",
            f"How many POs were approved this month?",
            f"Show quotation status breakdown",
            f"List goods receipts pending inspection",
            f"Show {s2} contract details",
            f"What is the average PO approval time?",
        ]
        queries["PROCUREMENT"] = random.sample(proc_pool, min(4, len(proc_pool)))

    except Exception as e:
        logger.warning("Failed to generate dynamic queries: %s", e)
        # Fallback to static queries
        queries = {
            "HCM": ["How many employees are there?", "Show average salary by department",
                     "What is the attrition rate?", "Show headcount by department"],
            "FINANCE": ["Which cost centres are over budget?", "Show total AP outstanding",
                        "Show overdue AP invoices", "Show budget vs actual variance"],
            "PROCUREMENT": ["Show purchase orders by status", "Which supplier has highest PO spend?",
                            "Show pending POs", "Show requisitions pending approval"],
        }

    return {"queries": queries}
