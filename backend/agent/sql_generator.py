"""SQL generation and validation using Groq (Llama 3.3 70B) with schema context.

Switched from OpenAI GPT-4o to Groq Llama 3.3 70B Versatile.
Now integrates the query planner for schema-accurate table/column guidance.
"""

import logging
import re
# from openai import OpenAI  # commented out -- switched to Groq
from groq import Groq
from config.settings import get_settings

logger = logging.getLogger(__name__)

# ── Module-level cached Groq client (avoid re-creating per call) ──
_groq_client = None

def _get_groq_client() -> Groq:
    global _groq_client
    if _groq_client is None:
        settings = get_settings()
        _groq_client = Groq(api_key=settings.groq_api_key)
    return _groq_client

_BLOCKED_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE",
    "CREATE", "ALTER", "EXEC", "EXECUTE",
}

_SQL_SYSTEM_PROMPT = """You are an expert PostgreSQL 15 SQL generator for an Oracle Fusion ERP data replica.
Rules you MUST follow:
1. Generate ONLY a SELECT statement -- never INSERT, UPDATE, DELETE, DROP, or any DDL
2. Return ONLY the raw SQL -- no markdown, no code blocks, no explanation, no semicolons
3. Use exact column and table names from the schema provided
4. DO NOT automatically add LIMIT. Only add LIMIT if the user explicitly requests a limit (e.g. "top 10", "first 20", etc.)
5. Use ILIKE for case-insensitive text matching
6. For date comparisons use CURRENT_DATE
7. For fiscal quarters: Q1=JAN-MAR, Q2=APR-JUN, Q3=JUL-SEP, Q4=OCT-DEC
8. Never put user values directly in SQL -- but for this POC, string interpolation is acceptable
9. Return only the SQL query, starting with SELECT
10. When query mentions 'budget' AND 'actual' together, ALWAYS use fin_gl_balances with balance_id as the primary key -- NEVER use fin_ap_invoices for budget queries.
11. proc_po_headers does NOT have a cost_centre_id column AND proc_po_distributions does NOT have a po_header_id column.
    The ONLY correct path to reach distributions from a PO header is:
    proc_po_headers → proc_po_lines (po_header_id) → proc_po_distributions (po_line_id) → fin_cost_centres (cost_centre_id) → hcm_departments (dept_id).
12. For ANY supplier name lookup, ALWAYS use ILIKE '%%<name>%%' with wildcard percent signs on both sides. NEVER use exact string match.
13. For monthly invoice aggregations, ALWAYS use EXTRACT(YEAR FROM i.invoice_date) and EXTRACT(MONTH FROM i.invoice_date).
    NEVER compute months from CURRENT_DATE or intervals. The column is fin_ap_invoices.invoice_date.
14. When combining salary cost and PO spend (or any two domain aggregates), ALWAYS use separate CTEs for each domain then
    JOIN them. Use COALESCE(value, 0) to handle NULLs. NEVER compute salary + po_spend in a single flat JOIN.

CRITICAL COLUMN RULES -- these override any other assumptions:
15. BUDGET TIME FILTERING: fin_budget_lines has NO start_date, end_date, or any date column.
    To filter budget by year: JOIN fin_budget_lines bl TO fin_budget_headers bh ON bl.budget_header_id = bh.budget_header_id
    and use WHERE bh.fiscal_year = <year> (integer, e.g. 2024).
    CORRECT example -- last year budget:
      SELECT SUM(bl.amount) FROM fin_budget_lines bl
      JOIN fin_budget_headers bh ON bh.budget_header_id = bl.budget_header_id
      WHERE bh.fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int - 1
    WRONG (will always return 0 rows): WHERE EXTRACT(YEAR FROM bl.start_date) = ...

16. BUDGET PERIOD FILTERING: fin_budget_headers does NOT have a period_name column.
    Period names (e.g. 'JAN-2025') exist ONLY on fin_budget_lines.period_name.
    CORRECT: WHERE bl.period_name = 'JAN-2025' AND bh.fiscal_year = 2025
    WRONG: WHERE bh.period_name = 'JAN-2025'

17. AP INVOICE AMOUNT: The amount column on fin_ap_invoices is named invoice_amount, NOT amount.
    CORRECT: SELECT SUM(i.invoice_amount) FROM fin_ap_invoices i
    WRONG: SELECT SUM(i.amount) FROM fin_ap_invoices i

18. GL BALANCES TIME FILTERING: fin_gl_balances has NO period_date column.
    It has fiscal_year (INTEGER) and period_name (VARCHAR, e.g. 'JAN-2025') and fiscal_quarter (INTEGER).
    CORRECT last year filter: WHERE gl.fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int - 1
    WRONG: WHERE EXTRACT(YEAR FROM gl.period_date) = ...

19. COST CENTRE / DEPARTMENT NAME MATCHING: ALWAYS use ILIKE '%%<name>%%' for cost_centre_name and dept_name.
    NEVER use exact string match (= 'Engineering').
    CORRECT: WHERE cc.cost_centre_name ILIKE '%%Engineering%%'
    WRONG: WHERE cc.cost_centre_name = 'Engineering'

20. hcm_assignments uses effective_from (DATE), not start_date.
    CORRECT: WHERE a.effective_from >= '2024-01-01'
    WRONG: WHERE a.start_date >= '2024-01-01'

CRITICAL JOIN RULES -- these override any other assumptions:
- hcm_persons does NOT have cost_centre_id or salary columns
- Salary is in hcm_assignments.salary
- fin_ap_payments has NO invoice_id and NO schedule_id -- it joins ONLY to sup_suppliers via supplier_id
- fin_ap_payment_schedules has NO payment_id -- it joins ONLY to fin_ap_invoices via invoice_id
- Always anchor department queries through fin_cost_centres (10 real cost centres) not directly from hcm_departments (4000+ seeded rows)
- ALWAYS join fin_cost_centres to hcm_departments via dept_id (e.g. `cc.dept_id = d.dept_id`). NEVER join on cost_centre_code.
- NEVER join POs, Invoices, and Payments in a flat SELECT on supplier_id independently, as this causes a Cartesian product row explosion. Join POs to Invoices explicitly via PO Lines and Invoice Lines (3-way match).

CROSS-DOMAIN JOIN PATHS -- use these EXACTLY via CTEs:
- Headcount by dept (CTE 1): fin_cost_centres → hcm_departments (dept_id) → hcm_assignments (dept_id, WHERE assignment_status='ACTIVE') → COUNT(DISTINCT person_id)
- Budget variance (CTE 2): fin_cost_centres → fin_gl_balances (cost_centre_id) → SUM(actual_amount - budget_amount)
- PO spend by dept (CTE 3): fin_cost_centres → proc_po_distributions (cost_centre_id) → proc_po_lines (po_line_id) → proc_po_headers (po_header_id)
- Requisition → PO → Invoice chain: proc_requisition_headers → proc_po_headers (requisition_id) → proc_po_lines (po_header_id) → fin_ap_invoice_lines (po_line_id)
- Payment trail for supplier: sup_suppliers → proc_po_headers + fin_ap_invoices + fin_ap_payments (all via supplier_id)

Q: 'Which departments have employees raising requisitions that resulted in approved POs with invoices?'
A: SELECT d.dept_name, COUNT(DISTINCT a.person_id) AS employees
   FROM fin_cost_centres cc
   JOIN hcm_departments d ON d.dept_id = cc.dept_id
   JOIN hcm_assignments a ON a.dept_id = d.dept_id AND a.assignment_status = 'ACTIVE'
   JOIN proc_requisition_headers rh ON rh.requester_id = a.person_id
   JOIN proc_po_headers po ON po.requisition_id = rh.requisition_id AND po.status = 'APPROVED'
   JOIN proc_po_lines pol ON pol.po_header_id = po.po_header_id
   JOIN fin_ap_invoice_lines il ON il.po_line_id = pol.po_line_id
   GROUP BY d.dept_name

Q: 'Show approved purchase orders that have been received, grouped by cost centre with total value'
A: SELECT cc.cost_centre_name, SUM(pod.amount) as total_value
   FROM fin_cost_centres cc
   JOIN proc_po_distributions pod ON pod.cost_centre_id = cc.cost_centre_id
   JOIN proc_po_lines pol ON pol.po_line_id = pod.po_line_id
   JOIN proc_po_headers po ON po.po_header_id = pol.po_header_id
   JOIN proc_receipt_lines rl ON rl.po_line_id = pol.po_line_id
   WHERE po.status = 'APPROVED' AND rl.quantity_received > 0
   GROUP BY cc.cost_centre_name

Q: 'What was the last year budget amount?'
A: SELECT SUM(bl.amount) AS last_year_budget
   FROM fin_budget_lines bl
   JOIN fin_budget_headers bh ON bh.budget_header_id = bl.budget_header_id
   WHERE bh.fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int - 1

Q: 'What is the budget for Engineering cost centre last year?'
A: SELECT SUM(bl.amount) AS budget_amount
   FROM fin_budget_lines bl
   JOIN fin_budget_headers bh ON bh.budget_header_id = bl.budget_header_id
   JOIN fin_cost_centres cc ON cc.cost_centre_id = bl.cost_centre_id
   WHERE bh.fiscal_year = EXTRACT(YEAR FROM CURRENT_DATE)::int - 1
   AND cc.cost_centre_name ILIKE '%%Engineering%%'

Q: 'What is the budget for January 2025 for cost centre id 1?'
A: SELECT SUM(bl.amount) AS budget_total
   FROM fin_budget_lines bl
   JOIN fin_budget_headers bh ON bh.budget_header_id = bl.budget_header_id
   WHERE bh.fiscal_year = 2025
   AND bl.period_name = 'JAN-2025'
   AND bl.cost_centre_id = 1

21. THREE-WAY MATCH WARNING: fin_ap_invoice_lines.po_line_id is NULL for most invoices.
    Do NOT use INNER JOIN through fin_ap_invoice_lines to proc_po_lines to count POs.
    This will always return 0 rows.
    For cross-domain supplier queries (invoices + POs + employees):
    ALWAYS use supplier-anchored CTEs where each metric is aggregated INDEPENDENTLY by supplier_id,
    then LEFT JOIN the CTEs together on supplier_id or supplier_name.
    NEVER chain invoice_lines → po_lines → po_headers as the primary join path for aggregation.

Q: 'For each supplier show total invoice amount, number of POs, and employees in departments that issued those POs'
A: WITH supplier_invoices AS (
     SELECT s.supplier_id, s.supplier_name,
            SUM(i.invoice_amount) AS total_invoice_amount
     FROM fin_ap_invoices i
     JOIN sup_suppliers s ON s.supplier_id = i.supplier_id
     GROUP BY s.supplier_id, s.supplier_name
   ),
   supplier_pos AS (
     SELECT s.supplier_id,
            COUNT(DISTINCT po.po_header_id) AS num_pos
     FROM proc_po_headers po
     JOIN sup_suppliers s ON s.supplier_id = po.supplier_id
     GROUP BY s.supplier_id
   ),
   supplier_employees AS (
     SELECT s.supplier_id,
            COUNT(DISTINCT a.person_id) AS employee_count
     FROM proc_po_headers po
     JOIN sup_suppliers s ON s.supplier_id = po.supplier_id
     JOIN proc_po_lines pol ON pol.po_header_id = po.po_header_id
     JOIN proc_po_distributions pod ON pod.po_line_id = pol.po_line_id
     JOIN fin_cost_centres cc ON cc.cost_centre_id = pod.cost_centre_id
     JOIN hcm_departments d ON d.dept_id = cc.dept_id
     JOIN hcm_assignments a ON a.dept_id = d.dept_id AND a.assignment_status = 'ACTIVE'
     GROUP BY s.supplier_id
   )
   SELECT si.supplier_name,
          si.total_invoice_amount,
          COALESCE(sp.num_pos, 0) AS num_pos,
          COALESCE(se.employee_count, 0) AS employee_count
   FROM supplier_invoices si
   LEFT JOIN supplier_pos sp ON sp.supplier_id = si.supplier_id
   LEFT JOIN supplier_employees se ON se.supplier_id = si.supplier_id
   ORDER BY si.total_invoice_amount DESC

Important rule:
WHEN combining HR + Finance + Procurement metrics (e.g., headcount, budget, PO spend), you MUST prevent Cartesian products by using CTEs for each domain separately, then joining them:

WITH hr_stats AS (
  SELECT d.dept_name, COUNT(DISTINCT a.person_id) as headcount 
  FROM fin_cost_centres cc
  JOIN hcm_departments d ON cc.dept_id = d.dept_id
  LEFT JOIN hcm_assignments a ON a.dept_id = d.dept_id AND a.assignment_status = 'ACTIVE'
  GROUP BY d.dept_name
),
fin_stats AS (
  SELECT d.dept_name, SUM(gb.actual_amount - gb.budget_amount) as budget_variance
  FROM fin_cost_centres cc
  JOIN hcm_departments d ON cc.dept_id = d.dept_id
  JOIN fin_gl_balances gb ON gb.cost_centre_id = cc.cost_centre_id
  GROUP BY d.dept_name
),
proc_stats AS (
  SELECT d.dept_name, SUM(pod.amount) as total_po_spend
  FROM fin_cost_centres cc
  JOIN hcm_departments d ON cc.dept_id = d.dept_id
  JOIN proc_po_distributions pod ON pod.cost_centre_id = cc.cost_centre_id
  GROUP BY d.dept_name
)
SELECT hr_stats.dept_name, hr_stats.headcount, fin_stats.budget_variance, proc_stats.total_po_spend
FROM hr_stats
LEFT JOIN fin_stats ON hr_stats.dept_name = fin_stats.dept_name
LEFT JOIN proc_stats ON hr_stats.dept_name = proc_stats.dept_name
"""


def validate_sql(sql: str) -> tuple[bool, str]:
    """Validate SQL for safety and correctness.

    Returns (is_valid, cleaned_sql_or_error_message).
    """
    if not sql or not sql.strip():
        return False, "Empty SQL statement"

    cleaned = sql.strip().rstrip(";").strip()

    # Remove markdown code fences if present
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()

    # Remove inline comments at the start
    while cleaned.startswith("--"):
        cleaned = cleaned.split("\n", 1)[1].strip() if "\n" in cleaned else ""

    upper = cleaned.upper().strip()

    # Must start with SELECT
    if not upper.startswith("SELECT"):
        return False, f"SQL must start with SELECT, got: {upper[:30]}"

    # Block dangerous keywords -- check whole tokens
    for kw in _BLOCKED_KEYWORDS:
        # Use word boundary check to avoid false positives (e.g. "SELECTION")
        pattern = r'\b' + kw + r'\b'
        if re.search(pattern, upper):
            return False, f"Blocked keyword detected: {kw}"

    # # Add LIMIT if not present
    # if "LIMIT" not in upper:
    #     cleaned = cleaned + "\nLIMIT 100"

    return True, cleaned


def generate_sql(
    query: str,
    schema_context: list[dict],
    domain: str,
    retry_reason: str | None = None,
    query_plan: dict | None = None,
) -> str:
    """Generate parameterised PostgreSQL SQL from natural language query.

    Uses Groq Llama 3.3 70B with schema context as few-shot examples.
    When a query_plan is provided, injects it as an authoritative instruction
    block into the LLM prompt so the model uses the correct table/column instead
    of inferring from context.

    Validates output and retries once on failure.
    """
    client = _get_groq_client()

    context_text = "\n\nAvailable schema and examples:\n" + "\n\n".join(
        [f"=== {doc['title']} ===\n{doc['content']}" for doc in schema_context]
    )

    # ── Build user prompt: optionally prepend the structured query plan ──
    plan_block = ""
    if query_plan:
        try:
            from backend.query_planner import format_plan_for_prompt
            plan_text = format_plan_for_prompt(query_plan)
            if plan_text:
                plan_block = plan_text + "\n\n"
        except Exception as _e:
            logger.warning("Could not format query plan for prompt: %s", _e)

    user_prompt = plan_block + query
    if retry_reason:
        user_prompt = (
            f"Your previous SQL was rejected because: {retry_reason}\n"
            f"Generate a corrected version.\n\n"
        ) + plan_block + query

    # Use 8b for single-domain (fast), 70b for cross-domain (accurate complex joins)
    model = "llama-3.3-70b-versatile" if domain == "CROSS_DOMAIN" else "llama-3.1-8b-instant"

    # Token budget: cross-domain CTEs need much more room than single-domain.
    # 400 tokens is NOT enough for 3-4 CTE blocks -- it truncates mid-query.
    # Single domain (8b):  700 tokens  -- simple SELECTs, 1-2 JOINs
    # Cross domain (70b): 1600 tokens  -- 3-4 CTE blocks with multiple JOINs
    # Retry (any model):  1800 tokens  -- needs full corrected rewrite
    if retry_reason:
        max_tok = 1800
    elif domain == "CROSS_DOMAIN":
        max_tok = 1600
    else:
        max_tok = 700

    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": _SQL_SYSTEM_PROMPT + context_text},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tok,
    )

    raw_sql = response.choices[0].message.content.strip()

    is_valid, result = validate_sql(raw_sql)
    if is_valid:
        return result

    # Retry once
    if not retry_reason:
        logger.warning("SQL validation failed (%s), retrying once.", result)
        return generate_sql(query, schema_context, domain, retry_reason=result, query_plan=query_plan)

    raise ValueError(f"SQL generation failed after retry: {result}")
