"""Cross-domain query tool — retrieves schema from ALL domains for multi-table queries."""

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain.tools import tool

from vector_store.retriever import retrieve_schema_context
from backend.agent.sql_generator import generate_sql
from backend.db.connection import execute_query
from backend.analytics.chart_builder import auto_chart, wants_chart
from backend.query_planner import build_query_plan
from backend.agent.sql_sanitizer import validate_and_fix_sql

logger = logging.getLogger(__name__)


@tool
def cross_domain_query_tool(query: str) -> str:
    """Use this tool for queries that span MULTIPLE domains: HCM + Finance, HCM + Procurement,
    Finance + Procurement, or all three together.
    Examples: 'department headcount and budget variance', 'supplier invoices and POs',
    'employees and cost centre spend', 'department PO spend', 'payroll vs budget'.
    Input: natural language query requiring data from multiple ERP domains."""

    try:
        import time as _time
        _t0 = _time.time()

        # \u2500\u2500 Retrieve schema from ALL domains IN PARALLEL \u2500\u2500
        retrieval_tasks = {
            "HCM":          (query, "HCM", 2),
            "FINANCE":      (query, "FINANCE", 2),
            "PROCUREMENT":  (query, "PROCUREMENT", 2),
            "CROSS_DOMAIN": (query, "CROSS_DOMAIN", 3),
        }
        domain_results = {}
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = {
                pool.submit(retrieve_schema_context, q, d, k): label
                for label, (q, d, k) in retrieval_tasks.items()
            }
            for future in as_completed(futures):
                label = futures[future]
                try:
                    domain_results[label] = future.result()
                except Exception as e:
                    logger.warning("[CROSS_DOMAIN] retrieval failed for %s: %s", label, e)
                    domain_results[label] = []

        # Merge and deduplicate by title, cap at 8 docs to keep prompt concise
        seen = set()
        combined_ctx = []
        for domain_key in ("CROSS_DOMAIN", "HCM", "FINANCE", "PROCUREMENT"):
            for doc in domain_results.get(domain_key, []):
                if doc["title"] not in seen:
                    seen.add(doc["title"])
                    combined_ctx.append(doc)
                    if len(combined_ctx) >= 8:
                        break
            if len(combined_ctx) >= 8:
                break

        _rag_ms = int((_time.time() - _t0) * 1000)
        logger.info("[CROSS_DOMAIN] schema docs retrieved: %d in %dms (parallel)", len(combined_ctx), _rag_ms)
        for doc in combined_ctx:
            logger.debug("[CROSS_DOMAIN]   → %s", doc["title"])

        # Build cross-domain query plan for schema-accurate table/column guidance
        query_plan = build_query_plan(query, domain="CROSS_DOMAIN")
        logger.debug("[CROSS_DOMAIN] query plan: metric=%s cross=%s cte_domains=%s",
                     query_plan.get("metric"), query_plan.get("is_cross_domain"),
                     query_plan.get("cte_domains"))

        # Generate SQL with enriched cross-domain context
        raw_sql = generate_sql(query, combined_ctx, "CROSS_DOMAIN", query_plan=query_plan)
        logger.info("[CROSS_DOMAIN] raw generated SQL: %s", raw_sql[:300])

        # Dynamic validation: sanitise → EXPLAIN validate → LLM self-correct
        sql, corrections = validate_and_fix_sql(
            raw_sql, query, combined_ctx, "CROSS_DOMAIN", query_plan=query_plan
        )
        if corrections:
            logger.info("[CROSS_DOMAIN] corrections applied: %s", corrections)

        df = execute_query(sql)
        logger.info("[CROSS_DOMAIN] executed → %d rows", len(df))

        if df.empty:
            logger.warning("[CROSS_DOMAIN] no data returned for query: %r", query[:80])
            return json.dumps({
                "data": [],
                "sql_used": sql,
                "sql_corrections": corrections,
                "message": "No records were found in the database for this query.",
                "row_count": 0,
            })

        chart_data = None
        if wants_chart(query):
            chart_data = auto_chart(df, query)
            logger.info("[CROSS_DOMAIN] chart generated: %s", bool(chart_data))

        return json.dumps({
            "data": df.to_dict(orient="records"),
            "sql_used": sql,
            "metrics": {},
            "chart_data": chart_data,
            "row_count": len(df),
        }, default=str)

    except Exception as e:
        logger.error("[CROSS_DOMAIN] error: %s", e)
        return json.dumps({"error": str(e), "sql_used": "", "data": [], "row_count": 0})
