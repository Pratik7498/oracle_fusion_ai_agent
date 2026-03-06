"""LangChain tool for HCM / HR queries."""

import json
import logging
from datetime import date, timedelta

import pandas as pd
from langchain.tools import tool

from vector_store.retriever import retrieve_schema_context
from backend.agent.sql_generator import generate_sql
from backend.db.connection import execute_query
from backend.analytics.calculations import (
    calculate_attrition_rate,
    calculate_headcount_summary,
)
from backend.analytics.chart_builder import build_bar_chart, auto_chart, wants_chart
from backend.query_planner import build_query_plan
from backend.agent.sql_sanitizer import validate_and_fix_sql

logger = logging.getLogger(__name__)


@tool
def hcm_query_tool(query: str) -> str:
    """Use this tool for all HCM and HR queries: employee headcount by department,
    attrition rate, salary analysis, grade distribution, workforce metrics.
    Input: natural language query about HR/people data."""

    try:
        # 1. Get schema context
        schema_context = retrieve_schema_context(query, "HCM", top_k=3)

        # 2. Build query plan for accurate table/column guidance
        query_plan = build_query_plan(query, domain="HCM")

        # 3. Generate SQL
        raw_sql = generate_sql(query, schema_context, "HCM", query_plan=query_plan)

        # 4. Dynamic validation: sanitise → EXPLAIN validate → LLM self-correct
        sql, corrections = validate_and_fix_sql(
            raw_sql, query, schema_context, "HCM", query_plan=query_plan
        )

        # 5. Execute query
        df = execute_query(sql)

        if df.empty:
            return json.dumps({
                "data": [], "sql_used": sql, "row_count": 0,
                "message": "No records were found in the database for this query.",
            })

        # 4. Detect if calculation needed
        query_lower = query.lower()
        metrics: dict = {}
        chart_data = None
        _wants_vis = wants_chart(query)

        if any(w in query_lower for w in ["attrition", "turnover", "leaving", "left"]):
            period_start = date.today() - timedelta(days=365)
            period_end = date.today()
            metrics = calculate_attrition_rate(df, period_start, period_end)

        if _wants_vis and any(w in query_lower for w in ["headcount", "how many", "count", "number of"]):
            cols_lower = [c.lower() for c in df.columns]
            if "department" in cols_lower and any("count" in c or "headcount" in c for c in cols_lower):
                chart_data = build_bar_chart(
                    data=dict(zip(df.iloc[:, 0].astype(str), df.iloc[:, 1])),
                    title="Headcount by Department",
                    x_label="Department",
                    y_label="Headcount",
                )

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
        logger.error("hcm_query_tool error: %s", e)
        return json.dumps({"error": str(e), "sql_used": "", "data": []})
