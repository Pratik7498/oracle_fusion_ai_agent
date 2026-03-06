"""Query Planner — converts parsed intent + semantic map into a structured query plan.

The plan is then injected into the SQL generator prompt to give the LLM explicit,
schema-accurate table/column guidance instead of relying on inference alone.
"""

import logging
from typing import Optional

from backend.query_intent_parser import parse_intent
from backend.schema_semantics import (
    SEMANTIC_MAP,
    get_semantic_entry,
    get_time_filter_sql,
    JOIN_PATHS,
    TABLE_DATE_COLUMNS,
)

logger = logging.getLogger(__name__)

# ── Domain → metric sets for cross-domain detection ───────────────────────────
_HCM_METRICS = {"salary", "headcount", "employee", "grade", "attrition",
                 "performance", "training", "absence"}
_FINANCE_METRICS = {"budget", "gl_actual", "gl_budget", "gl_variance",
                    "invoice", "payment", "ar_invoice", "cost_centre"}
_PROCUREMENT_METRICS = {"spend", "purchase_order", "requisition", "contract", "supplier"}


def _detect_domains_from_query(q: str) -> list[str]:
    """Detect which ERP domains are referenced in the query text."""
    domains: list[str] = []
    if any(kw in q for kw in [
        "employee", "salary", "headcount", "staff", "worker", "hr", "payroll",
        "grade", "attrition", "performance", "training", "absence", "designation",
    ]):
        domains.append("HCM")
    if any(kw in q for kw in [
        "budget", "actual", "variance", "gl", "invoice", "payment", "cost centre",
        "cost center", "ledger", "receivable", "payable", "finance", "spend",
        "expenditure",
    ]):
        domains.append("FINANCE")
    if any(kw in q for kw in [
        "purchase order", "po ", "procurement", "supplier", "vendor", "contract",
        "requisition", "quotation", "sourcing", "bid",
    ]):
        domains.append("PROCUREMENT")
    return list(dict.fromkeys(domains))  # deduplicate preserving order


def build_query_plan(query: str, domain: Optional[str] = None) -> dict:
    """Build a structured query plan from a natural language query.

    Args:
        query: Raw user query string.
        domain: Classified domain (HCM / FINANCE / PROCUREMENT / CROSS_DOMAIN).
                Used as a hint but intent parsing decides table/column.

    Returns:
        Dict with keys:
            metric_table (str|None)
            metric_column (str|None)
            aggregation (str|None)
            agg_expression (str|None): full aggregation expression e.g. "SUM(amount)"
            joins (list[str]): ordered JOIN clauses
            group_by (str|None): GROUP BY column
            time_filter_sql (str|None): WHERE clause snippet for time
            entity_filter (str|None): named entity value for WHERE
            is_cross_domain (bool)
            cte_domains (list[str]): which domains need CTEs (cross-domain only)
            intent (dict): raw intent parse for debugging
            plan_notes (list[str]): schema rule reminders included in prompt
    """
    intent = parse_intent(query)
    metric = intent.get("metric")
    aggregation = intent.get("aggregation")
    dimension = intent.get("dimension")
    time_filter = intent.get("time_filter")
    entity_filter = intent.get("entity_filter")

    logger.debug("build_query_plan: metric=%s agg=%s dim=%s time=%s domain=%s",
                 metric, aggregation, dimension, time_filter, domain)

    # ── Resolve metric to schema ──
    semantic = get_semantic_entry(metric) if metric else None

    metric_table: Optional[str] = semantic["table"] if semantic else None
    metric_column: Optional[str] = semantic["column"] if semantic else None
    raw_agg_col: Optional[str] = semantic.get("agg_column") if semantic else None

    # Build aggregation expression
    agg_expression: Optional[str] = None
    if aggregation and raw_agg_col:
        if aggregation == "COUNT" and metric in {"headcount", "employee"}:
            agg_expression = f"COUNT(DISTINCT {raw_agg_col})"
        elif "-" in (raw_agg_col or ""):  # e.g. "actual_amount - budget_amount"
            agg_expression = f"SUM({raw_agg_col})"
        else:
            agg_expression = f"{aggregation}({raw_agg_col})"

    # ── Group-by column ──
    group_by: Optional[str] = None
    if dimension == "department":
        group_by = "hcm_departments.dept_name"
    elif dimension == "cost_centre":
        group_by = "fin_cost_centres.cost_centre_name"
    elif dimension == "supplier":
        group_by = "sup_suppliers.supplier_name"
    elif dimension == "month":
        group_by = "EXTRACT(YEAR FROM {date_col}), EXTRACT(MONTH FROM {date_col})"
        if metric_table and metric_table != "fin_budget_lines":
            date_col = TABLE_DATE_COLUMNS.get(metric_table, "created_at")
            group_by = group_by.replace("{date_col}", date_col)
        elif metric_table == "fin_budget_lines":
            group_by = "bl.period_name"  # budget lines use period_name for month grouping
    elif dimension == "quarter":
        group_by = "EXTRACT(YEAR FROM {date_col}), EXTRACT(QUARTER FROM {date_col})"
        if metric_table and metric_table != "fin_budget_lines":
            date_col = TABLE_DATE_COLUMNS.get(metric_table, "created_at")
            group_by = group_by.replace("{date_col}", date_col)
        elif metric_table == "fin_budget_lines":
            group_by = "bh.fiscal_year, bh.fiscal_quarter" if "bh" in (joins or []) else "period_name"
    elif dimension == "year":
        group_by = "EXTRACT(YEAR FROM {date_col})"
        if metric_table and metric_table != "fin_budget_lines":
            date_col = TABLE_DATE_COLUMNS.get(metric_table, "created_at")
            group_by = group_by.replace("{date_col}", date_col)
        elif metric_table == "fin_budget_lines":
            group_by = "bh.fiscal_year"  # budget uses fiscal_year on the joined header
    elif dimension:
        group_by = dimension

    # ── Join path ──
    joins: list[str] = []
    if metric_table and dimension:
        join_key = f"{metric_table}→{dimension}"
        if join_key in JOIN_PATHS:
            joins = JOIN_PATHS[join_key]

    # ── Time filter SQL ──
    time_filter_sql: Optional[str] = None
    if time_filter and metric_table:
        time_filter_sql = get_time_filter_sql(time_filter, metric_table)

    # ── Cross-domain detection ──
    q_lower = (intent.get("normalised_query") or query).lower()
    detected_domains = _detect_domains_from_query(q_lower)
    is_cross_domain = (
        len(detected_domains) >= 2
        or (domain == "CROSS_DOMAIN" and len(detected_domains) >= 1)
    )
    cte_domains = detected_domains if is_cross_domain else []

    # ── Schema notes (critical rules to inject into LLM prompt) ──
    plan_notes: list[str] = []
    if metric_table and semantic:
        if semantic.get("notes"):
            plan_notes.append(semantic["notes"])

    # Add critical cross-join rules
    if "department" in (dimension or ""):
        plan_notes.append(
            "ALWAYS join finance/procurement tables to departments via fin_cost_centres "
            "(dept_id FK). Do NOT join directly to hcm_departments."
        )
    if metric == "budget":
        plan_notes.append(
            "CRITICAL: Budget monetary values are in fin_budget_lines.amount. "
            "fin_budget_lines has NO date column (no start_date, no end_date). "
            "To filter by year: JOIN fin_budget_lines bl ON bl.budget_header_id = bh.budget_header_id "
            "then WHERE bh.fiscal_year = <year>. "
            "NEVER use EXTRACT(YEAR FROM bl.start_date) — start_date does not exist. "
            "fin_budget_headers has NO period_name column; period_name is on fin_budget_lines."
        )
    if metric == "spend":
        plan_notes.append(
            "CRITICAL: PO spend/cost must come from proc_po_distributions.amount — "
            "NOT proc_po_headers.total_amount (use that for header-level lookups only)."
        )
    if metric in {"gl_actual", "gl_variance"}:
        plan_notes.append(
            "Actual GL amounts are in fin_gl_balances.actual_amount. "
            "Budget GL amounts are in fin_gl_balances.budget_amount. "
            "Variance = actual_amount - budget_amount."
        )

    plan = {
        "metric": metric,
        "metric_table": metric_table,
        "metric_column": metric_column,
        "aggregation": aggregation,
        "agg_expression": agg_expression,
        "dimension": dimension,
        "joins": joins,
        "group_by": group_by,
        "time_filter": time_filter,
        "time_filter_sql": time_filter_sql,
        "entity_filter": entity_filter,
        "is_cross_domain": is_cross_domain,
        "cte_domains": cte_domains,
        "intent": intent,
        "plan_notes": plan_notes,
    }

    logger.debug("Query plan: table=%s col=%s agg=%s group=%s time_sql=%s",
                 metric_table, metric_column, agg_expression, group_by, time_filter_sql)
    return plan


def format_plan_for_prompt(plan: dict) -> str:
    """Format a query plan as a human-readable block for injection into the LLM prompt.

    Returns a string that is prepended to the user query in the SQL generator.
    """
    if not plan.get("metric_table"):
        # No useful plan — don't add noise to the prompt
        return ""

    lines = ["QUERY PLAN — use these exact table/column mappings:"]

    if plan.get("metric_table"):
        lines.append(f"  Primary table  : {plan['metric_table']}")
    if plan.get("metric_column"):
        lines.append(f"  Primary column : {plan['metric_column']}")
    if plan.get("agg_expression"):
        lines.append(f"  Aggregation    : {plan['agg_expression']}")
    if plan.get("group_by"):
        lines.append(f"  GROUP BY       : {plan['group_by']}")
    if plan.get("time_filter_sql"):
        lines.append(f"  Time filter    : WHERE {plan['time_filter_sql']}")
    if plan.get("entity_filter"):
        lines.append(f"  Entity filter  : {plan['entity_filter']}")
    if plan.get("joins"):
        lines.append("  Join path      :")
        for j in plan["joins"]:
            lines.append(f"    {j}")
    if plan.get("is_cross_domain") and plan.get("cte_domains"):
        lines.append(f"  Cross-domain   : Use CTEs for domains: {', '.join(plan['cte_domains'])}")
    if plan.get("plan_notes"):
        lines.append("  Schema rules   :")
        for note in plan["plan_notes"]:
            lines.append(f"    ⚠ {note}")

    return "\n".join(lines)
