"""Fast keyword-based intent classification — no LLM call needed.

Replaces the previous Groq-based router to save ~3-5 seconds per query.
"""

import logging

logger = logging.getLogger(__name__)

# ── Keyword sets for domain classification ──
_HCM_KEYWORDS = {
    "employee", "employees", "headcount", "attrition", "turnover", "salary",
    "salaries", "grade", "grades", "department", "departments", "hr",
    "human resource", "workforce", "payroll", "compensation", "promotion",
    "promotions", "transfer", "transfers", "training", "performance review",
    "performance", "absence", "leave", "hire", "hiring", "person",
    "worker", "workers", "people", "staff", "designation", "job",
    "hcm", "termination", "terminated", "resigned", "joining",
}

_FINANCE_KEYWORDS = {
    "budget", "actual", "variance", "gl", "general ledger", "journal",
    "ap invoice", "ap invoices", "accounts payable", "payment", "payments",
    "aging", "overdue", "cost centre", "cost center", "finance",
    "financial", "ledger", "ar invoice", "ar invoices", "accounts receivable",
    "receipt", "receipts", "balance", "balances", "invoice", "invoices",
    "spend", "expenditure", "revenue", "outstanding", "paid", "unpaid",
    "fiscal", "fy", "quarter",
}

_PROCUREMENT_KEYWORDS = {
    "purchase order", "po ", "pos ", "procurement", "supplier", "suppliers",
    "quotation", "quotations", "requisition", "requisitions", "contract",
    "contracts", "engagement", "delta", "revised", "goods receipt",
    "item catalog", "catalog", "tender", "bid", "rfq", "vendor",
    "vendors", "sourcing", "award",
}

_OUT_OF_SCOPE_KEYWORDS = {
    "weather", "news", "coding", "python tutorial", "recipe", "movie",
    "sports", "politics", "stock market", "crypto", "bitcoin",
    "write code", "help me code", "translate", "wikipedia",
    "who is", "what is the capital", "how to cook",
}

_QUERY_TYPE_KEYWORDS = {
    "aggregation": ["count", "total", "sum", "average", "avg", "how many", "group by", "top", "highest", "lowest", "max", "min"],
    "delta": ["delta", "difference", "change", "revised", "variance", "vs", "versus", "compared"],
    "trend": ["trend", "over time", "monthly", "quarterly", "yearly", "by month", "by quarter", "by year", "growth"],
}

_CALC_KEYWORDS = {
    "attrition_rate": ["attrition", "turnover"],
    "delta": ["delta", "revised", "change"],
    "budget_variance": ["budget", "variance", "over budget"],
    "ap_aging": ["aging", "overdue"],
    "headcount": ["headcount", "how many employees", "employee count"],
}


def classify_intent(query: str) -> dict:
    """Classify user query into domain, query_type, and calculation needs.

    Uses fast keyword matching instead of an LLM call (~0ms vs ~3-5s).
    """
    q = query.lower()

    # ── Check out-of-scope first ──
    if any(kw in q for kw in _OUT_OF_SCOPE_KEYWORDS):
        return {
            "domain": "OUT_OF_SCOPE",
            "query_type": "lookup",
            "needs_calculation": False,
            "calculation_type": "none",
            "confidence": 0.9,
        }

    # ── Score each domain ──
    hcm_score = sum(1 for kw in _HCM_KEYWORDS if kw in q)
    fin_score = sum(1 for kw in _FINANCE_KEYWORDS if kw in q)
    proc_score = sum(1 for kw in _PROCUREMENT_KEYWORDS if kw in q)

    scores = {"HCM": hcm_score, "FINANCE": fin_score, "PROCUREMENT": proc_score}
    max_score = max(scores.values())

    if max_score == 0:
        domain = "CROSS_DOMAIN"
        confidence = 0.4
    else:
        # Check if multiple domains scored equally high
        top_domains = [d for d, s in scores.items() if s == max_score]
        if len(top_domains) > 1:
            domain = "CROSS_DOMAIN"
            confidence = 0.6
        else:
            domain = top_domains[0]
            confidence = min(0.95, 0.5 + max_score * 0.1)

    # ── Determine query type ──
    query_type = "lookup"
    for qt, keywords in _QUERY_TYPE_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            query_type = qt
            break

    # ── Determine calculation type ──
    calc_type = "none"
    needs_calc = False
    for ct, keywords in _CALC_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            calc_type = ct
            needs_calc = True
            break

    return {
        "domain": domain,
        "query_type": query_type,
        "needs_calculation": needs_calc,
        "calculation_type": calc_type,
        "confidence": confidence,
    }

