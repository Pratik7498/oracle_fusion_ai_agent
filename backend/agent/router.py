"""Intent classification using Groq (Llama 3.3 70B).

Switched from OpenAI GPT-4o to Groq Llama 3.3 70B Versatile.
"""

import json
import logging
# from openai import OpenAI  # commented out -- switched to Groq
from groq import Groq
from config.settings import get_settings

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are an intent classifier for an Oracle Fusion ERP AI agent. Analyse the user query and classify it.

Domains:
- HCM: employee headcount, attrition rate, salary analysis, grade distribution, HR metrics, workforce data
- FINANCE: GL balances, budget vs actual, AP invoices, payment aging, cost centre variance, spend analysis
- PROCUREMENT: purchase orders, supplier quotations, engagement deltas, PO approval status, supplier spend
- CROSS_DOMAIN: queries spanning multiple domains

Query types:
- lookup: retrieve specific record(s)
- aggregation: count, sum, average, group by
- delta: calculate change/difference between two values (e.g. original vs revised quotation)
- trend: change over time periods

Respond in valid JSON ONLY, no other text:
{
  "domain": "HCM|FINANCE|PROCUREMENT|CROSS_DOMAIN",
  "query_type": "lookup|aggregation|delta|trend",
  "needs_calculation": true|false,
  "calculation_type": "attrition_rate|delta|budget_variance|ap_aging|headcount|none",
  "confidence": 0.0-1.0
}"""

_DEFAULT_INTENT: dict = {
    "domain": "CROSS_DOMAIN",
    "query_type": "lookup",
    "needs_calculation": False,
    "calculation_type": "none",
    "confidence": 0.5,
}


def classify_intent(query: str) -> dict:
    """Classify user query into domain, query_type, and calculation needs.

    Returns a safe default on any failure.
    """
    try:
        settings = get_settings()
        # OpenAI version (commented out):
        # client = OpenAI(api_key=settings.openai_api_key)
        client = Groq(api_key=settings.groq_api_key)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # was "gpt-4o"
            temperature=0,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            max_tokens=200,
        )

        raw = response.choices[0].message.content.strip()
        # Strip markdown fences if the model wraps output
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()

        intent = json.loads(raw)
        # Ensure all keys exist
        for key in _DEFAULT_INTENT:
            intent.setdefault(key, _DEFAULT_INTENT[key])
        return intent

    except (json.JSONDecodeError, Exception) as exc:
        logger.warning("Intent classification failed (%s), using default.", exc)
        return dict(_DEFAULT_INTENT)
