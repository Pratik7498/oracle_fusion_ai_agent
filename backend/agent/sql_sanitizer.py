"""SQL Sanitizer + Schema Validator — dynamic SQL correction before execution.

Layer 1: regex-based structural fixes for known wrong pattern families
         (applies to ANY query, not just the 3 known cases)

Layer 2: PostgreSQL EXPLAIN-based pre-validator that runs the SQL against
         the actual DB schema to catch any column/table error. Returns the
         exact PostgreSQL error message so the LLM can self-correct.

This module is the single chokepoint for ALL generated SQL before it
touches the database.  No hand-coding per query is needed — the DB itself
acts as the schema oracle.
"""

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# LAYER 1: Pattern-based structural sanitiser
# Each rule: (compiled_regex, replacement, description)
# Applied in order; earlier rules take priority.
# ─────────────────────────────────────────────────────────────────────────────
_SANITIZE_RULES: list[tuple] = [

    # ── Budget: fix EXTRACT(YEAR FROM bl.start_date) pattern ──────────────────
    # fin_budget_lines has NO start_date. Correct approach: bh.fiscal_year
    (
        re.compile(
            r"EXTRACT\s*\(\s*YEAR\s+FROM\s+\w*\.?start_date\s*\)"
            r"\s*=\s*EXTRACT\s*\(\s*YEAR\s+FROM\s+CURRENT_DATE\s*\)\s*-\s*1",
            re.IGNORECASE,
        ),
        "bh.fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int - 1",
        "budget start_date→bh.fiscal_year (last_year)",
    ),
    (
        re.compile(
            r"EXTRACT\s*\(\s*YEAR\s+FROM\s+\w*\.?start_date\s*\)"
            r"\s*=\s*EXTRACT\s*\(\s*YEAR\s+FROM\s+CURRENT_DATE\s*\)",
            re.IGNORECASE,
        ),
        "bh.fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int",
        "budget start_date→bh.fiscal_year (current_year)",
    ),
    (
        re.compile(
            r"EXTRACT\s*\(\s*YEAR\s+FROM\s+bl\.start_date\s*\)\s*=\s*(\d{4})",
            re.IGNORECASE,
        ),
        lambda m: f"bh.fiscal_year = {m.group(1)}",
        "budget bl.start_date→bh.fiscal_year (explicit year)",
    ),

    # ── GL: fix EXTRACT(YEAR FROM gl.period_date) — period_date doesn't exist ─
    (
        re.compile(
            r"EXTRACT\s*\(\s*YEAR\s+FROM\s+\w*\.?period_date\s*\)"
            r"\s*=\s*EXTRACT\s*\(\s*YEAR\s+FROM\s+CURRENT_DATE\s*\)\s*-\s*1",
            re.IGNORECASE,
        ),
        "fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int - 1",
        "GL period_date→fiscal_year (last_year)",
    ),
    (
        re.compile(
            r"EXTRACT\s*\(\s*YEAR\s+FROM\s+\w*\.?period_date\s*\)"
            r"\s*=\s*EXTRACT\s*\(\s*YEAR\s+FROM\s+CURRENT_DATE\s*\)",
            re.IGNORECASE,
        ),
        "fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int",
        "GL period_date→fiscal_year (current_year)",
    ),
    (
        re.compile(
            r"EXTRACT\s*\(\s*YEAR\s+FROM\s+\w+\.period_date\s*\)\s*=\s*(\d{4})",
            re.IGNORECASE,
        ),
        lambda m: f"fiscal_year = {m.group(1)}",
        "GL period_date→fiscal_year (explicit year)",
    ),

    # ── AP Invoice: fix .amount → .invoice_amount ──────────────────────────────
    # Only on fin_ap_invoices alias references (i.amount, inv.amount, invoice.amount)
    (
        re.compile(
            r"\b(i|inv|invoice|ap_inv|api)\s*\.\s*(?<!\w)(amount)(?!\w)",
            re.IGNORECASE,
        ),
        lambda m: f"{m.group(1)}.invoice_amount",
        "AP invoice alias.amount → alias.invoice_amount",
    ),
    # Direct table-qualified fin_ap_invoices.amount
    (
        re.compile(
            r"\bfin_ap_invoices\s*\.\s*amount\b",
            re.IGNORECASE,
        ),
        "fin_ap_invoices.invoice_amount",
        "fin_ap_invoices.amount → fin_ap_invoices.invoice_amount",
    ),

    # ── fin_budget_headers.period_name: doesn't exist on headers ──────────────
    # Remove or convert to bl.period_name
    (
        re.compile(
            r"\bbh\s*\.\s*period_name\b",
            re.IGNORECASE,
        ),
        "bl.period_name",
        "bh.period_name → bl.period_name",
    ),
    (
        re.compile(
            r"\bfin_budget_headers\s*\.\s*period_name\b",
            re.IGNORECASE,
        ),
        "fin_budget_lines.period_name",
        "fin_budget_headers.period_name → fin_budget_lines.period_name",
    ),

    # ── hcm_assignments.start_date doesn't exist → effective_from ─────────────
    (
        re.compile(
            r"\b(a|asgn|assign|assignment)\s*\.\s*start_date\b",
            re.IGNORECASE,
        ),
        lambda m: f"{m.group(1)}.effective_from",
        "hcm_assignments alias.start_date → alias.effective_from",
    ),

    # ── proc_po_headers date columns ──────────────────────────────────────────
    # po_date doesn't exist, it's created_date
    (
        re.compile(r"\b(po|ph)\s*\.\s*po_date\b", re.IGNORECASE),
        lambda m: f"{m.group(1)}.created_date",
        "po_headers po.po_date → po.created_date",
    ),

    # ── Exact name match on cost_centre → ILIKE ──────────────────────────────
    # e.g. cc.cost_centre_name = 'Engineering'  →  ILIKE '%Engineering%'
    (
        re.compile(
            r"\b(\w+)\s*\.\s*cost_centre_name\s*=\s*'([^']+)'",
            re.IGNORECASE,
        ),
        lambda m: f"{m.group(1)}.cost_centre_name ILIKE '%{m.group(2)}%'",
        "cost_centre_name exact match → ILIKE",
    ),
    (
        re.compile(
            r"\b(\w+)\s*\.\s*dept_name\s*=\s*'([^']+)'",
            re.IGNORECASE,
        ),
        lambda m: f"{m.group(1)}.dept_name ILIKE '%{m.group(2)}%'",
        "dept_name exact match → ILIKE",
    ),
    (
        re.compile(
            r"\b(\w+)\s*\.\s*supplier_name\s*=\s*'([^']+)'",
            re.IGNORECASE,
        ),
        lambda m: f"{m.group(1)}.supplier_name ILIKE '%{m.group(2)}%'",
        "supplier_name exact match → ILIKE",
    ),

    # ── int cast for fiscal_year arithmetic ───────────────────────────────────
    # EXTRACT(YEAR FROM CURRENT_DATE) - 1 → need ::int cast to avoid type error
    (
        re.compile(
            r"fiscal_year\s*=\s*EXTRACT\s*\(\s*YEAR\s+FROM\s+CURRENT_DATE\s*\)\s*-\s*1(?!::int)",
            re.IGNORECASE,
        ),
        "fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int - 1",
        "fiscal_year EXTRACT cast missing ::int (last_year)",
    ),
    (
        re.compile(
            r"fiscal_year\s*=\s*EXTRACT\s*\(\s*YEAR\s+FROM\s+CURRENT_DATE\s*\)(?!\s*::int)(?!\s*-)",
            re.IGNORECASE,
        ),
        "fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int",
        "fiscal_year EXTRACT cast missing ::int (current_year)",
    ),

    # ── 3-way match: INNER JOIN proc_po_lines ON po_line_id after invoice_lines ─
    # fin_ap_invoice_lines.po_line_id is NULL for most rows in seeded data.
    # Converting INNER JOIN → LEFT JOIN prevents the whole query returning 0 rows.
    (
        re.compile(
            r"\bJOIN\s+proc_po_lines\s+(\w+)\s+ON\s+\1\.po_line_id\s*=\s*il\.po_line_id",
            re.IGNORECASE,
        ),
        lambda m: f"LEFT JOIN proc_po_lines {m.group(1)} ON {m.group(1)}.po_line_id = il.po_line_id",
        "INNER JOIN proc_po_lines ON il.po_line_id converted to LEFT JOIN (il.po_line_id is often NULL)",
    ),
    (
        re.compile(
            r"\bJOIN\s+proc_po_lines\s+(\w+)\s+ON\s+il\.po_line_id\s*=\s*\1\.po_line_id",
            re.IGNORECASE,
        ),
        lambda m: f"LEFT JOIN proc_po_lines {m.group(1)} ON il.po_line_id = {m.group(1)}.po_line_id",
        "INNER JOIN proc_po_lines ON il.po_line_id (reversed) converted to LEFT JOIN",
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# SEMANTIC RISK DETECTOR — flags patterns that are syntactically valid but
# semantically broken (e.g. will always return 0 rows due to NULL foreign keys)
# ─────────────────────────────────────────────────────────────────────────────
_ZERO_ROW_RISK_PATTERNS: list[tuple] = [
    (
        # Supplier cross-domain query that does NOT use CTEs (all in flat SELECT)
        # Risk: Cartesian product or 0-row result from missing 3-way match
        re.compile(
            r"fin_ap_invoices.*proc_po_(?:headers|lines|distributions).*hcm_assignments",
            re.IGNORECASE | re.DOTALL,
        ),
        "Cross-domain supplier query uses flat JOINs (invoices+POs+employees) without CTEs — "
        "risk of 0-row result. Use supplier-anchored CTEs aggregating each domain independently.",
    ),
    (
        # Using MAX(invoice_amount) or SUM(invoice_amount) directly joined to proc_po_lines
        # without LEFT JOIN — almost certainly returns 0 due to NULL po_line_id
        re.compile(
            r"fin_ap_invoice_lines.*JOIN\s+proc_po_lines(?!.*LEFT\s+JOIN\s+proc_po_lines)",
            re.IGNORECASE | re.DOTALL,
        ),
        "fin_ap_invoice_lines INNER-JOINed to proc_po_lines — po_line_id is often NULL, use LEFT JOIN.",
    ),
    (
        # Direct hcm_assignments join with no assignment_status filter
        re.compile(
            r"JOIN\s+hcm_assignments\s+\w+\s+ON[^W]*(?!WHERE|AND)[^;]*GROUP BY",
            re.IGNORECASE | re.DOTALL,
        ),
        "hcm_assignments joined without assignment_status='ACTIVE' filter — may count terminated employees.",
    ),
]


def detect_zero_row_risk(sql: str) -> list[str]:
    """Detect SQL patterns that are syntactically valid but likely to return 0 rows.

    Returns list of risk descriptions (empty list = no risks detected).
    These are NOT auto-fixed but are logged and bubbled up in corrections
    so the caller knows to flag them or trigger a targeted LLM retry.
    """
    risks: list[str] = []
    for pattern, description in _ZERO_ROW_RISK_PATTERNS:
        if pattern.search(sql):
            risks.append(description)
            logger.warning("Zero-row risk detected: %s", description[:100])
    return risks


def sanitize_sql(sql: str) -> tuple[str, list[str]]:
    """Apply all structural sanitisation rules to the SQL.

    Returns:
        (sanitized_sql, list_of_applied_rule_descriptions)
    """
    applied: list[str] = []
    for pattern, replacement, description in _SANITIZE_RULES:
        if isinstance(replacement, str):
            new_sql, n = pattern.subn(replacement, sql)
        else:
            # callable replacement (lambda)
            new_sql, n = pattern.subn(replacement, sql)
        if n > 0:
            applied.append(description)
            sql = new_sql

    # Also run zero-row risk detection (logs warnings, returns descriptions)
    risks = detect_zero_row_risk(sql)
    if risks:
        applied.extend([f"RISK_DETECTED: {r}" for r in risks])

    if applied:
        logger.info("SQL sanitiser applied %d fix(es)/warnings: %s", len(applied), applied)
    return sql, applied


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 2: PostgreSQL EXPLAIN-based pre-validator
# ─────────────────────────────────────────────────────────────────────────────
def validate_sql_with_explain(sql: str) -> tuple[bool, Optional[str]]:
    """Validate SQL by running EXPLAIN against the live PostgreSQL DB.

    Uses EXPLAIN (not EXECUTE) so no data is touched and it's safe for SELECTs.

    Returns:
        (is_valid: bool, error_message: str | None)
        error_message is the raw PostgreSQL error, stripped of noise, ready
        to feed back into the LLM retry prompt.
    """
    try:
        from sqlalchemy import text as sa_text
        from backend.db.connection import get_engine

        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(sa_text(f"EXPLAIN {sql}"))
        return True, None

    except Exception as exc:
        # Extract the most useful part of the PostgreSQL error
        raw = str(exc)
        # Truncate very long errors (some include the full SQL plan)
        error_msg = raw[:400] if len(raw) > 400 else raw
        logger.warning("EXPLAIN validation failed: %s", error_msg)
        return False, error_msg


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 3: Combined entry point used by all domain tools
# ─────────────────────────────────────────────────────────────────────────────
def validate_and_fix_sql(
    sql: str,
    query: str,
    schema_context: list[dict],
    domain: str,
    query_plan: dict | None = None,
    max_retries: int = 2,
) -> tuple[str, list[str]]:
    """Full pipeline: sanitise → EXPLAIN validate → LLM retry on failure.

    Args:
        sql:            LLM-generated SQL string.
        query:          Original user query (needed for LLM retry).
        schema_context: Vector-store schema docs (needed for LLM retry).
        domain:         HCM | FINANCE | PROCUREMENT | CROSS_DOMAIN.
        query_plan:     Optional structured query plan dict.
        max_retries:    How many EXPLAIN-fail → LLM-retry loops to allow.

    Returns:
        (final_sql, list_of_all_corrections_applied)
    """
    from backend.agent.sql_generator import generate_sql

    corrections: list[str] = []

    # Step A: structural sanitise
    sql, sanitise_fixes = sanitize_sql(sql)
    corrections.extend(sanitise_fixes)

    # Step B: EXPLAIN validate → retry loop
    for attempt in range(max_retries + 1):
        is_valid, error = validate_sql_with_explain(sql)
        if is_valid:
            break

        if attempt >= max_retries:
            logger.error(
                "SQL failed EXPLAIN after %d sanitise+retry attempt(s). "
                "Proceeding with last SQL and relying on execute_query error handling. "
                "Error was: %s", max_retries, error
            )
            break

        # Build a targeted retry instruction from the DB error
        retry_reason = (
            f"PostgreSQL rejected your SQL with this error:\n{error}\n\n"
            "Fix ONLY the column/table reference that caused this error. "
            "Do not change anything else. "
            "Return the corrected SELECT statement."
        )
        logger.info(
            "EXPLAIN failed (attempt %d/%d), sending DB error to LLM for self-correction. "
            "Error: %s", attempt + 1, max_retries, error[:150]
        )

        # Ask LLM to self-correct using the actual DB error
        try:
            corrected_sql = generate_sql(
                query,
                schema_context,
                domain,
                retry_reason=retry_reason,
                query_plan=query_plan,
            )
            # Re-sanitise the corrected SQL
            corrected_sql, new_fixes = sanitize_sql(corrected_sql)
            corrections.extend(new_fixes)
            corrections.append(f"LLM self-correction (attempt {attempt + 1}): {error[:120]}")
            sql = corrected_sql
        except Exception as gen_exc:
            logger.error("LLM self-correction failed: %s", gen_exc)
            break

    return sql, corrections
