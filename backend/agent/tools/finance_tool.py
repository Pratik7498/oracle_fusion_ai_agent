"""LangChain tool for Finance queries (GL balances, AP invoices, budget variance)."""

import json
import logging

import pandas as pd
from langchain.tools import tool

from vector_store.retriever import retrieve_schema_context
from backend.agent.sql_generator import generate_sql
from backend.db.connection import execute_query
from backend.analytics.calculations import calculate_budget_variance, calculate_ap_aging
from backend.analytics.chart_builder import build_variance_chart, build_aging_chart, auto_chart, wants_chart

logger = logging.getLogger(__name__)


@tool
def finance_query_tool(query: str) -> str:
    """Use this tool for all Finance queries: GL balances, budget vs actual,
    AP invoices, payment aging, cost centre variance, spend analysis.
    Input: natural language query about financial data."""

    try:
        schema_context = retrieve_schema_context(query, "FINANCE", top_k=3)
        sql = generate_sql(query, schema_context, "FINANCE")
        df = execute_query(sql)

        if df.empty:
            return json.dumps(
                {"data": [], "sql_used": sql, "message": "No data found for this query."}
            )

        query_lower = query.lower()
        metrics: dict = {}
        chart_data = None
        _wants_vis = wants_chart(query)

        # Budget variance detection
        if any(w in query_lower for w in ["budget", "variance", "over budget"]):
            if "actual_amount" in df.columns and "budget_amount" in df.columns:
                df = calculate_budget_variance(df)
                if _wants_vis:
                    chart_data = build_variance_chart(df, "Budget vs Actual — Cost Centres")
                total_variance = float(df["variance_amount"].sum())
                over_count = int(df["over_budget"].sum())
                metrics = {
                    "total_variance": total_variance,
                    "over_budget_count": over_count,
                    "formatted": f"{'↑' if total_variance > 0 else '↓'} £{abs(total_variance):,.0f} net variance, {over_count} cost centres over budget",
                }

        # AP aging detection
        if any(w in query_lower for w in ["aging", "overdue", "days"]):
            if "due_date" in df.columns or "days_overdue" in df.columns:
                aging = calculate_ap_aging(df)
                if _wants_vis:
                    chart_data = build_aging_chart(aging, "AP Invoice Aging Analysis")
                total_overdue = sum(b["amount"] for b in aging.values())
                metrics = {
                    "aging_buckets": aging,
                    "total_overdue_amount": total_overdue,
                    "formatted": f"£{total_overdue:,.0f} total overdue across {sum(b['count'] for b in aging.values())} invoices",
                }

        # Fallback: auto-generate chart ONLY if user asked for a visual
        if chart_data is None and _wants_vis:
            chart_data = auto_chart(df, query)

        return json.dumps(
            {
                "data": df.to_dict(orient="records"),
                "sql_used": sql,
                "metrics": metrics,
                "chart_data": chart_data,
                "row_count": len(df),
            },
            default=str,
        )

    except Exception as e:
        logger.error("finance_query_tool error: %s", e)
        return json.dumps({"error": str(e), "sql_used": "", "data": []})
