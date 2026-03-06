"""Schema Semantics — authoritative mapping from business terms to DB schema elements.

Maps canonical metric/entity names → exact PostgreSQL table and column names.
This is the single source of truth that prevents the LLM from guessing wrong
table/column combinations.
"""

from typing import Optional

# ── Primary semantic map: business term → DB table + column ───────────────────
# Each entry:
#   table   (str)          - exact table name in Postgres
#   column  (str|None)     - the primary value column (None if metric is row-count)
#   agg_column (str|None)  - column used for aggregation (may differ from column)
#   pk      (str)          - primary key column (for COUNT DISTINCT)
#   domain  (str)          - HCM | FINANCE | PROCUREMENT | ALL

SEMANTIC_MAP: dict[str, dict] = {
    # ── Finance ─────────────────────────────────────────────────────────────
    "budget": {
        "table": "fin_budget_lines",
        "column": "amount",
        "agg_column": "amount",
        "pk": "budget_line_id",
        "domain": "FINANCE",
        "notes": "Budget monetary values are in fin_budget_lines.amount — NOT fin_budget_headers.budget_amount",
    },
    "gl_actual": {
        "table": "fin_gl_balances",
        "column": "actual_amount",
        "agg_column": "actual_amount",
        "pk": "balance_id",
        "domain": "FINANCE",
        "notes": "Actual GL posted amounts come from fin_gl_balances.actual_amount",
    },
    "gl_budget": {
        "table": "fin_gl_balances",
        "column": "budget_amount",
        "agg_column": "budget_amount",
        "pk": "balance_id",
        "domain": "FINANCE",
        "notes": "GL budget figures come from fin_gl_balances.budget_amount (for variance queries against actuals)",
    },
    "gl_variance": {
        "table": "fin_gl_balances",
        "column": "actual_amount",        # variance = actual_amount - budget_amount
        "agg_column": "actual_amount - budget_amount",
        "pk": "balance_id",
        "domain": "FINANCE",
        "notes": "Budget variance = fin_gl_balances.actual_amount - fin_gl_balances.budget_amount",
    },
    "invoice": {
        "table": "fin_ap_invoices",
        "column": "invoice_amount",        # CORRECT column name — NOT 'amount'
        "agg_column": "invoice_amount",
        "pk": "invoice_id",
        "domain": "FINANCE",
        "notes": "AP invoice amounts in fin_ap_invoices.invoice_amount — the column is NOT called 'amount'",
    },
    "payment": {
        "table": "fin_ap_payments",
        "column": "payment_amount",
        "agg_column": "payment_amount",
        "pk": "payment_id",
        "domain": "FINANCE",
        "notes": "AP payment amounts in fin_ap_payments.payment_amount. Joins to sup_suppliers via supplier_id.",
    },
    "cost_centre": {
        "table": "fin_cost_centres",
        "column": "cost_centre_name",
        "agg_column": None,
        "pk": "cost_centre_id",
        "domain": "FINANCE",
        "notes": "fin_cost_centres is the bridge between finance tables and hcm_departments via dept_id",
    },
    "ar_invoice": {
        "table": "fin_ar_invoices",
        "column": "amount",
        "agg_column": "amount",
        "pk": "ar_invoice_id",
        "domain": "FINANCE",
    },

    # ── HCM ─────────────────────────────────────────────────────────────────
    "salary": {
        "table": "hcm_assignments",
        "column": "salary",
        "agg_column": "salary",
        "pk": "assignment_id",
        "domain": "HCM",
        "notes": "Salary is in hcm_assignments.salary — hcm_persons does NOT have a salary column",
    },
    "headcount": {
        "table": "hcm_assignments",
        "column": "person_id",
        "agg_column": "person_id",       # used with COUNT(DISTINCT person_id)
        "pk": "assignment_id",
        "domain": "HCM",
        "notes": "Active headcount: COUNT(DISTINCT person_id) FROM hcm_assignments WHERE assignment_status='ACTIVE'",
    },
    "employee": {
        "table": "hcm_persons",
        "column": "person_id",
        "agg_column": "person_id",
        "pk": "person_id",
        "domain": "HCM",
        "notes": "Employee identities in hcm_persons; salary/department in hcm_assignments",
    },
    "department": {
        "table": "hcm_departments",
        "column": "dept_name",
        "agg_column": None,
        "pk": "dept_id",
        "domain": "HCM",
        "notes": "Always join hcm_departments to finance tables via fin_cost_centres (dept_id FK)",
    },
    "grade": {
        "table": "hcm_assignments",
        "column": "grade_code",
        "agg_column": None,
        "pk": "assignment_id",
        "domain": "HCM",
    },
    "attrition": {
        "table": "hcm_assignments",
        "column": "assignment_status",
        "agg_column": "person_id",
        "pk": "assignment_id",
        "domain": "HCM",
        "notes": "Attrition: COUNT of assignments where assignment_status IN ('TERMINATED','RESIGNED')",
    },
    "performance": {
        "table": "hcm_performance_reviews",
        "column": "overall_rating",
        "agg_column": "overall_rating",
        "pk": "review_id",
        "domain": "HCM",
    },
    "training": {
        "table": "hcm_training_completions",
        "column": "completion_status",
        "agg_column": "person_id",
        "pk": "completion_id",
        "domain": "HCM",
    },
    "absence": {
        "table": "hcm_absences",
        "column": "absence_days",
        "agg_column": "absence_days",
        "pk": "absence_id",
        "domain": "HCM",
    },

    # ── Procurement ──────────────────────────────────────────────────────────
    "spend": {
        "table": "proc_po_distributions",
        "column": "amount",
        "agg_column": "amount",
        "pk": "distribution_id",
        "domain": "PROCUREMENT",
        "notes": (
            "PO spend/cost must be aggregated from proc_po_distributions.amount. "
            "Join path for dept-level: proc_po_distributions → fin_cost_centres → hcm_departments. "
            "Join path for PO details: proc_po_distributions → proc_po_lines → proc_po_headers."
        ),
    },
    "purchase_order": {
        "table": "proc_po_headers",
        "column": "total_amount",
        "agg_column": "total_amount",
        "pk": "po_header_id",
        "domain": "PROCUREMENT",
        "notes": (
            "proc_po_headers does NOT have cost_centre_id. "
            "proc_po_distributions does NOT have po_header_id. "
            "Only correct PO chain: proc_po_headers → proc_po_lines (po_header_id) → proc_po_distributions (po_line_id)."
        ),
    },
    "requisition": {
        "table": "proc_requisition_headers",
        "column": "total_amount",
        "agg_column": "total_amount",
        "pk": "requisition_id",
        "domain": "PROCUREMENT",
    },
    "contract": {
        "table": "proc_contracts",
        "column": "contract_value",
        "agg_column": "contract_value",
        "pk": "contract_id",
        "domain": "PROCUREMENT",
    },
    "supplier": {
        "table": "sup_suppliers",
        "column": "supplier_name",
        "agg_column": None,
        "pk": "supplier_id",
        "domain": "PROCUREMENT",
        "notes": "Always use ILIKE '%%name%%' for supplier name lookups — never exact match.",
    },
}

# ── Canonical join paths ───────────────────────────────────────────────────────
# Describes how to connect key table pairs when planning joins.
JOIN_PATHS: dict[str, list[str]] = {
    # Finance ↔ HCM bridge (ALWAYS via fin_cost_centres)
    "fin_budget_lines→department": [
        "fin_budget_lines JOIN fin_cost_centres ON fin_cost_centres.cost_centre_id = fin_budget_lines.cost_centre_id",
        "JOIN hcm_departments ON hcm_departments.dept_id = fin_cost_centres.dept_id",
    ],
    "fin_gl_balances→department": [
        "fin_gl_balances JOIN fin_cost_centres ON fin_cost_centres.cost_centre_id = fin_gl_balances.cost_centre_id",
        "JOIN hcm_departments ON hcm_departments.dept_id = fin_cost_centres.dept_id",
    ],
    "hcm_assignments→cost_centre": [
        "hcm_assignments JOIN hcm_departments ON hcm_departments.dept_id = hcm_assignments.dept_id",
        "JOIN fin_cost_centres ON fin_cost_centres.dept_id = hcm_departments.dept_id",
    ],

    # Procurement full chain
    "proc_po_distributions→department": [
        "proc_po_distributions JOIN fin_cost_centres ON fin_cost_centres.cost_centre_id = proc_po_distributions.cost_centre_id",
        "JOIN hcm_departments ON hcm_departments.dept_id = fin_cost_centres.dept_id",
    ],
    "proc_po_headers→proc_po_distributions": [
        "proc_po_headers JOIN proc_po_lines ON proc_po_lines.po_header_id = proc_po_headers.po_header_id",
        "JOIN proc_po_distributions ON proc_po_distributions.po_line_id = proc_po_lines.po_line_id",
    ],
    "proc_po_distributions→supplier": [
        "proc_po_distributions JOIN proc_po_lines ON proc_po_lines.po_line_id = proc_po_distributions.po_line_id",
        "JOIN proc_po_headers ON proc_po_headers.po_header_id = proc_po_lines.po_header_id",
        "JOIN sup_suppliers ON sup_suppliers.supplier_id = proc_po_headers.supplier_id",
    ],

    # Finance ↔ Supplier
    "fin_ap_invoices→supplier": [
        "fin_ap_invoices JOIN sup_suppliers ON sup_suppliers.supplier_id = fin_ap_invoices.supplier_id",
    ],
    "fin_ap_payments→supplier": [
        "fin_ap_payments JOIN sup_suppliers ON sup_suppliers.supplier_id = fin_ap_payments.supplier_id",
    ],
}

# ── Time filter → SQL WHERE snippets ─────────────────────────────────────────
TIME_FILTER_SQL: dict[str, str] = {
    "last_year":       "EXTRACT(YEAR FROM {date_col}) = EXTRACT(YEAR FROM CURRENT_DATE) - 1",
    "current_year":    "EXTRACT(YEAR FROM {date_col}) = EXTRACT(YEAR FROM CURRENT_DATE)",
    "last_quarter":    (
        "({date_col} >= DATE_TRUNC('quarter', CURRENT_DATE - INTERVAL '3 months') "
        "AND {date_col} < DATE_TRUNC('quarter', CURRENT_DATE))"
    ),
    "current_quarter": (
        "{date_col} >= DATE_TRUNC('quarter', CURRENT_DATE) "
        "AND {date_col} < DATE_TRUNC('quarter', CURRENT_DATE) + INTERVAL '3 months'"
    ),
    "last_month":      (
        "EXTRACT(YEAR FROM {date_col}) = EXTRACT(YEAR FROM CURRENT_DATE - INTERVAL '1 month') "
        "AND EXTRACT(MONTH FROM {date_col}) = EXTRACT(MONTH FROM CURRENT_DATE - INTERVAL '1 month')"
    ),
    "current_month":   (
        "EXTRACT(YEAR FROM {date_col}) = EXTRACT(YEAR FROM CURRENT_DATE) "
        "AND EXTRACT(MONTH FROM {date_col}) = EXTRACT(MONTH FROM CURRENT_DATE)"
    ),
    "q1":  "EXTRACT(MONTH FROM {date_col}) IN (1, 2, 3)",
    "q2":  "EXTRACT(MONTH FROM {date_col}) IN (4, 5, 6)",
    "q3":  "EXTRACT(MONTH FROM {date_col}) IN (7, 8, 9)",
    "q4":  "EXTRACT(MONTH FROM {date_col}) IN (10, 11, 12)",
}

# ── Budget notes: time filtering rules (injected into plan notes) ────────────
# fin_budget_lines has NO start_date or end_date column.
# Time filtering for budget MUST go via fin_budget_headers.fiscal_year JOIN.
# Period filtering uses fin_budget_lines.period_name (e.g. 'JAN-2025')
# and can also JOIN fin_reporting_periods via period_name for date range queries.
BUDGET_TIME_FILTER_NOTE = (
    "CRITICAL: fin_budget_lines has NO start_date, end_date, or date column. "
    "To filter by year, JOIN fin_budget_lines to fin_budget_headers on budget_header_id "
    "and filter on fin_budget_headers.fiscal_year. "
    "To filter by period, use fin_budget_lines.period_name (e.g. period_name='JAN-2025'). "
    "NEVER use EXTRACT(YEAR FROM bl.start_date) — start_date does not exist on fin_budget_lines."
)

# ── Date column for each primary table used in TIME_FILTER_SQL ────────────────
# IMPORTANT: Only tables that actually HAVE a date column are listed here.
# fin_budget_lines is intentionally omitted — use BUDGET_TIME_FILTER_NOTE instead.
TABLE_DATE_COLUMNS: dict[str, str] = {
    # fin_budget_lines: NO date column — filter via fin_budget_headers.fiscal_year JOIN
    # fin_gl_balances:  has fiscal_year (integer) and period_name (VARCHAR) — NO period_date
    "fin_gl_balances":          "fiscal_year",   # used as integer, not DATE
    "fin_ap_invoices":          "invoice_date",
    "fin_ap_payments":          "payment_date",
    "fin_ar_invoices":          "invoice_date",
    "hcm_assignments":          "effective_from",
    "hcm_employment_periods":   "start_date",
    "hcm_performance_reviews":  "review_date",
    "hcm_training_records":     "completion_date",
    "proc_po_headers":          "created_date",
    "proc_requisition_headers": "submitted_date",
    "proc_contract_headers":    "start_date",
}


def get_semantic_entry(metric: str) -> Optional[dict]:
    """Return the semantic map entry for a canonical metric name, or None."""
    return SEMANTIC_MAP.get(metric)


def get_time_filter_sql(time_filter: str, table: str) -> Optional[str]:
    """Return a SQL WHERE clause snippet for the given time filter and table.

    For fin_budget_lines, returns the BUDGET_TIME_FILTER_NOTE string instead
    of a raw SQL snippet because budget lines use fiscal_year on the JOIN table.
    """
    # Budget lines have no date column — caller should inject BUDGET_TIME_FILTER_NOTE
    if table == "fin_budget_lines":
        return BUDGET_TIME_FILTER_NOTE

    # fin_gl_balances uses fiscal_year (integer), not a date column
    if table == "fin_gl_balances":
        if time_filter == "last_year":
            return "fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int - 1"
        if time_filter == "current_year":
            return "fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int"
        if time_filter.startswith("fiscal_year_"):
            year = time_filter.split("_")[-1]
            return f"fiscal_year = {year}"
        if time_filter in ("q1", "q2", "q3", "q4"):
            q_map = {"q1": 1, "q2": 2, "q3": 3, "q4": 4}
            return f"fiscal_quarter = {q_map[time_filter]}"
        return None

    template = TIME_FILTER_SQL.get(time_filter)
    if not template:
        if time_filter.startswith("fiscal_year_"):
            year = time_filter.split("_")[-1]
            date_col = TABLE_DATE_COLUMNS.get(table, "created_at")
            return f"EXTRACT(YEAR FROM {date_col}) = {year}"
        return None

    date_col = TABLE_DATE_COLUMNS.get(table, "created_at")
    return template.replace("{date_col}", date_col)
