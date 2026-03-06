"""Intent Parser — extracts structured intent from natural language ERP queries.

Zero LLM calls. Pure keyword + pattern matching.
Resolves synonyms, extracts metric, aggregation, dimension, time filters.
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ── Synonym normalisation ──────────────────────────────────────────────────────
# Maps various user phrasings to a canonical internal term.
SYNONYM_MAP: dict[str, str] = {
    # Employee / HR synonyms
    "staff": "employee",
    "staffs": "employee",
    "people": "employee",
    "person": "employee",
    "persons": "employee",
    "worker": "employee",
    "workers": "employee",
    "workforce": "employee",
    "headcount": "employee",
    "head count": "employee",
    "human resource": "employee",
    "hr": "employee",
    "personnel": "employee",
    "team member": "employee",
    "team members": "employee",

    # Budget / spend synonyms
    "spend": "spend",
    "spending": "spend",
    "expenditure": "spend",
    "outgoing": "spend",
    "outgoings": "spend",
    # NOTE: 'cost'/'costs' intentionally excluded — too broad, breaks 'cost centre' parsing
    "po spend": "spend",
    "purchase spend": "spend",

    # Budget (finance) synonyms
    "budget amount": "budget",
    "budgeted": "budget",
    "budgets": "budget",
    "budget figure": "budget",
    "planned amount": "budget",
    "planned budget": "budget",
    "allocated budget": "budget",
    "allocation": "budget",

    # Actual (finance GL) synonyms
    "actuals": "gl_actual",
    "actual amount": "gl_actual",
    "actual spend": "gl_actual",
    "realized": "gl_actual",
    "realised": "gl_actual",
    "posted amount": "gl_actual",

    # Invoice synonyms
    "bill": "invoice",
    "bills": "invoice",
    "ap invoice": "invoice",
    "ap invoices": "invoice",
    "payable": "invoice",
    "payables": "invoice",

    # Payment synonyms
    "paid": "payment",
    "payments": "payment",
    "disbursement": "payment",
    "disbursements": "payment",
    "ap payment": "payment",

    # Salary synonyms
    # NOTE: 'pay' intentionally excluded — appears in 'payment' causing false matches
    "wage": "salary",
    "wages": "salary",
    "compensation": "salary",
    "remuneration": "salary",
    "payroll": "salary",
    "earnings": "salary",
    "package": "salary",

    # Supplier synonyms
    "vendor": "supplier",
    "vendors": "supplier",
    "suppliers": "supplier",
    "contractor": "supplier",
    "contractors": "supplier",

    # Department synonyms
    "dept": "department",
    "depts": "department",
    "division": "department",
    "divisions": "department",
    "team": "department",

    # Cost centre synonyms
    "cost center": "cost_centre",
    "costcenter": "cost_centre",
    "cost centres": "cost_centre",
    "cost centers": "cost_centre",
    "cc": "cost_centre",

    # Purchase order synonyms
    "purchase order": "purchase_order",
    "purchase orders": "purchase_order",
    "po ": "purchase_order",
    "pos ": "purchase_order",

    # Contract synonyms
    "contracts": "contract",
    "agreement": "contract",
    "agreements": "contract",

    # Requisition synonyms
    "requisitions": "requisition",
    "req ": "requisition",
    "reqs ": "requisition",
    "purchase request": "requisition",
}

# ── Metric detection patterns ──────────────────────────────────────────────────
# Ordered list: (canonical_metric, [keywords that indicate this metric])
# ORDER MATTERS — more specific / higher-priority metrics first.
METRIC_PATTERNS: list[tuple[str, list[str]]] = [
    ("gl_variance",     ["variance", "over budget", "under budget", "budget variance"]),
    ("gl_actual",       ["actual", "gl_actual", "posted"]),
    ("budget",          ["budget"]),
    ("payment",         ["payment", "paid", "disbursement"]),
    ("invoice",         ["invoice", "ap invoice", "bill", "payable"]),
    ("spend",           ["spend", "spending", "expenditure", "outgoing", "po spend", "purchase spend"]),
    ("purchase_order",  ["purchase order", "po ", "po,", "pos ", "purchase_order"]),
    ("requisition",     ["requisition", "req ", "purchase request"]),
    ("contract",        ["contract", "agreement"]),
    ("supplier",        ["supplier", "vendor"]),
    ("headcount",       ["headcount", "head count", "employee count", "how many employee", "how many staff",
                         "how many people", "how many worker", "number of employee", "number of staff"]),
    ("salary",          ["salary", "wage", "wages", "payroll", "compensation", "remuneration", "earnings"]),
    ("attrition",       ["attrition", "turnover", "attrition rate", "turnover rate"]),
    ("employee",        ["employee", "staff", "workers", "people", "person", "persons", "workforce"]),
    ("performance",     ["performance", "performance review", "appraisal", "rating"]),
    ("training",        ["training", "learning", "course", "certification"]),
    ("absence",         ["absence", "leave", "sick", "holiday", "vacation"]),
    ("grade",           ["grade", "job grade", "band"]),
    ("department",      ["department", "dept"]),
    ("cost_centre",     ["cost centre", "cost_centre", "cost center"]),
    ("ar_invoice",      ["accounts receivable", "ar invoice", "ar invoices"]),
]

# ── Aggregation detection ──────────────────────────────────────────────────────
AGG_PATTERNS: list[tuple[str, list[str]]] = [
    ("COUNT", ["how many", "count", "number of", "total number", "headcount"]),
    ("SUM",   ["total", "sum", "overall", "aggregate", "how much", "amount"]),
    ("AVG",   ["average", "avg", "mean", "typical"]),
    ("MAX",   ["maximum", "max", "highest", "largest", "biggest", "top"]),
    ("MIN",   ["minimum", "min", "lowest", "smallest", "least"]),
]

# ── Dimension detection ────────────────────────────────────────────────────────
DIMENSION_PATTERNS: list[tuple[str, list[str]]] = [
    ("department",    ["by department", "per department", "by dept", "for each department",
                       "across department", "breakdown by department", "by division"]),
    # Note: both raw form and post-synonym-replacement form are included
    ("cost_centre",   ["by cost centre", "per cost centre", "by cost center", "for each cost centre",
                       "across cost centre", "by cc",
                       "by cost_centre", "per cost_centre",  # after synonym resolution
                       "cost centre", "cost_centre", "cost center"]),
    ("supplier",      ["by supplier", "per supplier", "for each supplier", "across supplier"]),
    ("month",         ["by month", "monthly", "per month", "month by month", "each month"]),
    ("quarter",       ["by quarter", "quarterly", "per quarter", "each quarter"]),
    ("year",          ["by year", "yearly", "annual", "annually", "per year", "each year"]),
    ("grade",         ["by grade", "per grade", "by band", "each grade"]),
    ("status",        ["by status", "per status"]),
    ("category",      ["by category", "per category"]),
    ("job",           ["by job", "by role", "by position"]),
]

# ── Time filter detection ──────────────────────────────────────────────────────
def _extract_time_filter(q: str) -> Optional[str]:
    """Return a canonical time filter token from the query, or None."""
    # Explicit fiscal year: FY2024, FY24, fiscal year 2024, 2024-25
    fy_match = re.search(
        r'\b(?:fiscal year|fy)\s*(\d{2,4})\b|\b(20\d{2})[/-](\d{2,4})\b',
        q, re.IGNORECASE
    )
    if fy_match:
        year = fy_match.group(1) or fy_match.group(2)
        if year and len(year) == 2:
            year = "20" + year
        return f"fiscal_year_{year}" if year else "current_year"

    # Relative time patterns (ordered from most specific to least)
    time_rules: list[tuple[str, list[str]]] = [
        ("last_year",       ["last year", "previous year", "prior year", "last fiscal year",
                             "previous fiscal year", "last fy", "prior fy"]),
        ("last_quarter",    ["last quarter", "previous quarter", "prior quarter"]),
        ("last_month",      ["last month", "previous month", "prior month"]),
        ("current_year",    ["this year", "current year", "ytd", "year to date",
                             "this fiscal year", "current fy"]),
        ("current_quarter", ["this quarter", "current quarter", "qtd", "quarter to date"]),
        ("current_month",   ["this month", "current month", "mtd", "month to date"]),
        ("q1",              ["q1", "first quarter", "jan-mar", "january to march"]),
        ("q2",              ["q2", "second quarter", "apr-jun", "april to june"]),
        ("q3",              ["q3", "third quarter", "jul-sep", "july to september"]),
        ("q4",              ["q4", "fourth quarter", "oct-dec", "october to december"]),
    ]
    for token, patterns in time_rules:
        if any(p in q for p in patterns):
            return token
    return None


# ── Entity filter detection ────────────────────────────────────────────────────
def _extract_entity_filter(q: str) -> Optional[str]:
    """Try to detect a named entity (department name, supplier name, etc.)."""
    # Patterns like: "for Engineering", "in Engineering", "of Engineering"
    m = re.search(
        r'\b(?:for|in|of|from|about|regarding)\s+([A-Z][a-zA-Z &\-]+)(?:\s+department|\s+dept|\s+division)?\b',
        q
    )
    if m:
        candidate = m.group(1).strip()
        # Skip time words caught by accident
        skip = {"last", "previous", "this", "current", "the", "all", "each", "every", "which", "what"}
        if candidate.lower() not in skip and len(candidate) > 2:
            return candidate
    return None


# ── Synonym resolution ─────────────────────────────────────────────────────────
def _resolve_synonyms(q: str) -> tuple[str, list[str]]:
    """Apply synonym map and return (normalised_query, list_of_substitutions_made)."""
    normalised = q
    applied: list[str] = []
    # Sort by length descending so longer phrases match first
    for src, canonical in sorted(SYNONYM_MAP.items(), key=lambda x: -len(x[0])):
        if src in normalised and src != canonical:
            normalised = normalised.replace(src, canonical)
            applied.append(f"{src}→{canonical}")
    return normalised, applied


def parse_intent(query: str) -> dict:
    """Extract structured intent from a natural language ERP query.

    Args:
        query: Raw user query string.

    Returns:
        Dict with keys:
            metric (str|None): primary metric the user wants
            aggregation (str|None): SUM, COUNT, AVG, MAX, MIN
            dimension (str|None): grouping dimension
            time_filter (str|None): temporal scope
            entity_filter (str|None): named entity (dept name, supplier, etc.)
            synonyms_resolved (list[str]): synonym substitutions applied
            normalised_query (str): query after synonym resolution
    """
    q_original = query.strip()
    q, synonyms_resolved = _resolve_synonyms(q_original.lower())

    # ── Metric ──
    metric: Optional[str] = None
    for canonical, keywords in METRIC_PATTERNS:
        if any(kw in q for kw in keywords):
            metric = canonical
            break

    # ── Aggregation ──
    aggregation: Optional[str] = None
    for agg, keywords in AGG_PATTERNS:
        if any(kw in q for kw in keywords):
            aggregation = agg
            break

    # Default aggregation based on metric if not detected
    if aggregation is None and metric:
        _default_aggs: dict[str, str] = {
            "budget": "SUM",
            "gl_actual": "SUM",
            "gl_variance": "SUM",
            "salary": "AVG",
            "headcount": "COUNT",
            "employee": "COUNT",
            "invoice": "SUM",
            "payment": "SUM",
            "spend": "SUM",
        }
        aggregation = _default_aggs.get(metric)

    # ── Dimension ──
    dimension: Optional[str] = None
    for dim, patterns in DIMENSION_PATTERNS:
        if any(p in q for p in patterns):
            dimension = dim
            break

    # ── Time filter ──
    time_filter = _extract_time_filter(q)

    # ── Entity filter (use original-cased query for proper noun detection) ──
    entity_filter = _extract_entity_filter(q_original)

    intent = {
        "metric": metric,
        "aggregation": aggregation,
        "dimension": dimension,
        "time_filter": time_filter,
        "entity_filter": entity_filter,
        "synonyms_resolved": synonyms_resolved,
        "normalised_query": q,
    }

    logger.debug("Intent parsed: %s", intent)
    return intent
