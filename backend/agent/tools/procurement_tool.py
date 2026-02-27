"""LangChain tool for Procurement queries (quotations, POs, delta analysis)."""

import json
import logging

import pandas as pd
from langchain.tools import tool

from vector_store.retriever import retrieve_schema_context
from backend.agent.sql_generator import generate_sql
from backend.db.connection import execute_query
from backend.analytics.calculations import calculate_delta
from backend.analytics.chart_builder import build_delta_chart, build_bar_chart

logger = logging.getLogger(__name__)


@tool
def procurement_query_tool(query: str) -> str:
    """Use this tool for all Procurement queries: purchase orders, supplier
    quotations, engagement deltas, PO approval status, supplier spend.
    Input: natural language query about procurement data."""

    try:
        schema_context = retrieve_schema_context(query, "PROCUREMENT", top_k=3)
        sql = generate_sql(query, schema_context, "PROCUREMENT")
        df = execute_query(sql)

        if df.empty:
            return json.dumps(
                {"data": [], "sql_used": sql, "message": "No data found for this query."}
            )

        query_lower = query.lower()
        metrics: dict = {}
        chart_data = None

        # Delta / revision detection
        if any(w in query_lower for w in ["delta", "revised", "change", "e-205", "e205"]):
            if "revised_amount" in df.columns and "original_amount" in df.columns:
                # Find the row with a revised amount
                revised_rows = df[df["revised_amount"].notna()]
                if not revised_rows.empty:
                    row = revised_rows.iloc[0]
                    original = float(row["original_amount"])
                    revised = float(row["revised_amount"])
                    metrics = calculate_delta(original, revised)
                    engagement_label = str(
                        row.get("engagement_id", row.get("engagement_name", "Engagement"))
                    )
                    chart_data = build_delta_chart(original, revised, engagement_label)

        # Pending POs
        if any(w in query_lower for w in ["pending", "purchase order", "po"]):
            if "status" in df.columns:
                status_counts = df["status"].value_counts().to_dict()
                if len(status_counts) > 1 or "PENDING" not in status_counts:
                    chart_data = chart_data or build_bar_chart(
                        data=status_counts,
                        title="Purchase Orders by Status",
                        x_label="Status",
                        y_label="Count",
                    )

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
        logger.error("procurement_query_tool error: %s", e)
        return json.dumps({"error": str(e), "sql_used": "", "data": []})
