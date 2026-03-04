"""SQL generation and validation using Groq (Llama 3.3 70B) with schema context.

Switched from OpenAI GPT-4o to Groq Llama 3.3 70B Versatile.
"""

import logging
import re
# from openai import OpenAI  # commented out -- switched to Groq
from groq import Groq
from config.settings import get_settings

logger = logging.getLogger(__name__)

_BLOCKED_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE",
    "CREATE", "ALTER", "EXEC", "EXECUTE",
}

_SQL_SYSTEM_PROMPT = """You are an expert PostgreSQL 15 SQL generator for an Oracle Fusion ERP data replica.
Rules you MUST follow:
1. Generate ONLY a SELECT statement -- never INSERT, UPDATE, DELETE, DROP, or any DDL
2. Return ONLY the raw SQL -- no markdown, no code blocks, no explanation, no semicolons
3. Use exact column and table names from the schema provided
4. Always add LIMIT 100 unless the query specifically requests all records or a different limit
5. Use ILIKE for case-insensitive text matching
6. For date comparisons use CURRENT_DATE
7. For fiscal quarters: Q1=JAN-MAR, Q2=APR-JUN, Q3=JUL-SEP, Q4=OCT-DEC
8. Never put user values directly in SQL -- but for this POC, string interpolation is acceptable
9. Return only the SQL query, starting with SELECT
10. When query mentions 'budget' AND 'actual' together (budget vs actual, actual vs budget, percentage difference between actual and budget), ALWAYS use the finance_gl_balances view with balance_id as the primary key -- NEVER use fin_ap_invoices for budget queries (AP invoices have no budget_amount column). If user says 'invoice id' but asks about budget, treat it as balance_id in finance_gl_balances."""


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

    # Add LIMIT if not present
    if "LIMIT" not in upper:
        cleaned = cleaned + "\nLIMIT 100"

    return True, cleaned


def generate_sql(
    query: str,
    schema_context: list[dict],
    domain: str,
    retry_reason: str | None = None,
) -> str:
    """Generate parameterised PostgreSQL SQL from natural language query.

    Uses Groq Llama 3.3 70B with schema context as few-shot examples.
    Validates output and retries once on failure.
    """
    settings = get_settings()
    # OpenAI version (commented out):
    # client = OpenAI(api_key=settings.openai_api_key)
    client = Groq(api_key=settings.groq_api_key)

    context_text = "\n\nAvailable schema and examples:\n" + "\n\n".join(
        [f"=== {doc['title']} ===\n{doc['content']}" for doc in schema_context]
    )

    user_prompt = query
    if retry_reason:
        user_prompt = (
            f"Your previous SQL was rejected because: {retry_reason}\n"
            f"Generate a corrected version.\n\n{query}"
        )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # was "gpt-4o"
        temperature=0,
        messages=[
            {"role": "system", "content": _SQL_SYSTEM_PROMPT + context_text},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=400,
    )

    raw_sql = response.choices[0].message.content.strip()

    is_valid, result = validate_sql(raw_sql)
    if is_valid:
        return result

    # Retry once
    if not retry_reason:
        logger.warning("SQL validation failed (%s), retrying once.", result)
        return generate_sql(query, schema_context, domain, retry_reason=result)

    raise ValueError(f"SQL generation failed after retry: {result}")
