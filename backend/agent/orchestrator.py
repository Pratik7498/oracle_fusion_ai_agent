"""Orchestrator — ties tools, memory, and Llama 3.1 8B together.

Switched from Groq Llama 3.3 70B to 3.1 8B Instant for speed.
"""

from dataclasses import dataclass, field
from typing import Optional
import time
import json
import logging

# from langchain_openai import ChatOpenAI  # commented out -- switched to Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from backend.agent.tools.hcm_tool import hcm_query_tool
from backend.agent.tools.finance_tool import finance_query_tool
from backend.agent.tools.procurement_tool import procurement_query_tool
from backend.agent.tools.cross_domain_tool import cross_domain_query_tool
from backend.agent.router import classify_intent
from backend.db.connection import log_query
from config.settings import get_settings

logger = logging.getLogger(__name__)


@dataclass
class AgentResponse:
    """Structured response from the agent."""

    answer: str
    domain: str
    query_type: str
    sql_used: str
    chart_data: Optional[dict]
    metrics: Optional[dict]
    execution_time_ms: int
    row_count: int = 0
    data: Optional[list] = None
    error: Optional[str] = None


class OracleFusionAgent:
    """Main agent that handles user queries via LangChain tool-calling."""

    def __init__(self) -> None:
        settings = get_settings()
        # OpenAI version (commented out):
        # self.llm = ChatOpenAI(
        #     model="gpt-4o",
        #     temperature=0,
        #     api_key=settings.openai_api_key,
        # )
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",  # 8b for speed (~1-2s vs ~8-12s for 70b)
            temperature=0,
            groq_api_key=settings.groq_api_key,
        )
        self.memories: dict[str, ConversationBufferWindowMemory] = {}

        self.system_prompt = (
            "You are an intelligent AI assistant for Oracle Fusion ERP data.\n"
            "Rules:\n"
            "1. Provide a clear, concise business-focused answer from the data provided\n"
            "2. Highlight key numbers prominently (e.g. \"47 employees\", \"+12.4% delta\")\n"
            "3. Keep answers professional and to the point -- max 4 sentences for simple queries\n"
            "4. Never reveal raw SQL to the user unless they ask\n"
            "5. You MUST ONLY answer questions about Oracle Fusion ERP data.\n"
            "6. NEVER answer from your general knowledge. ALL answers MUST come from tool results."
        )

    def _get_memory(self, session_id: str) -> ConversationBufferWindowMemory:
        if session_id not in self.memories:
            self.memories[session_id] = ConversationBufferWindowMemory(
                k=10,
                memory_key="chat_history",
                return_messages=True,
            )
        return self.memories[session_id]

    def run(self, query: str, session_id: str = "default") -> AgentResponse:
        """Process a user query end-to-end and return a structured response."""
        start_time = time.time()
        memory = self._get_memory(session_id)

        # Classify intent first (keyword-based, ~0ms)
        intent = classify_intent(query)
        domain = intent.get("domain", "CROSS_DOMAIN")
        query_type = intent.get("query_type", "lookup")

        sql_used = ""
        chart_data = None
        metrics = None
        row_count = 0

        # ── Guard: block out-of-scope queries ──
        if domain == "OUT_OF_SCOPE":
            execution_time = int((time.time() - start_time) * 1000)
            out_of_scope_msg = (
                "I'm designed to assist only with **Oracle Fusion ERP data** — "
                "including HCM (employees, payroll, performance), Finance (GL, AP, AR, budgets), "
                "and Procurement (POs, requisitions, suppliers, contracts).\n\n"
                "Your question appears to be outside this scope. "
                "Please ask something related to the ERP database and I'll be happy to help! 🔮"
            )
            return AgentResponse(
                answer=out_of_scope_msg,
                domain="OUT_OF_SCOPE",
                query_type=query_type,
                sql_used="",
                chart_data=None,
                metrics=None,
                execution_time_ms=execution_time,
                row_count=0,
            )

        # ── Map domain → tool for direct-call path ──
        _TOOL_MAP = {
            "HCM": hcm_query_tool,
            "FINANCE": finance_query_tool,
            "PROCUREMENT": procurement_query_tool,
            "CROSS_DOMAIN": cross_domain_query_tool,  # single tool with full multi-domain schema
        }

        try:
            # ── FAST PATH: single-domain → call tool directly, skip agent ──
            if domain in _TOOL_MAP:
                tool_fn = _TOOL_MAP[domain]
                logger.info("[%s] query=%r → %s", domain, query[:80], tool_fn.name)
                raw_output = tool_fn.invoke(query)

                # Parse tool output
                try:
                    tool_data = json.loads(raw_output)
                except (json.JSONDecodeError, TypeError):
                    tool_data = {}

                sql_used = tool_data.get("sql_used", "")
                chart_data = tool_data.get("chart_data")
                metrics = tool_data.get("metrics")
                row_count = tool_data.get("row_count", 0)
                data_rows = tool_data.get("data", [])
                error_msg = tool_data.get("error")

                logger.info("[%s] SQL: %s", domain, sql_used[:200] if sql_used else "none")
                logger.info("[%s] rows=%d  chart=%s", domain, row_count, "yes" if chart_data else "no")

                if error_msg:
                    logger.warning("[%s] tool error: %s", domain, error_msg)
                    raise ValueError(error_msg)

                # Format answer with a single LLM call
                data_preview = str(data_rows[:15]) if data_rows else "No data"
                metrics_str = json.dumps(metrics, default=str) if metrics else "None"

                format_prompt = (
                    f"User asked: {query}\n\n"
                    f"Data returned ({row_count} rows, first 15 shown):\n{data_preview}\n\n"
                    f"Metrics: {metrics_str}\n\n"
                    f"Give a clear, concise business-focused answer. "
                    f"Highlight key numbers prominently. Max 4 sentences for simple queries. "
                    f"Do NOT reveal SQL. Do NOT make up data — only use what is shown above."
                )

                llm_response = self.llm.invoke(format_prompt)
                answer = llm_response.content

            # Update memory
            memory.chat_memory.add_user_message(query)
            memory.chat_memory.add_ai_message(answer)

            execution_time = int((time.time() - start_time) * 1000)
            logger.info("[%s] DONE in %dms | rows=%d", domain, execution_time, row_count)

            # Log to DB (fire-and-forget)
            try:
                log_query(query, domain, sql_used, answer[:500], execution_time)
            except Exception:
                pass

            return AgentResponse(
                answer=answer,
                domain=domain,
                query_type=query_type,
                sql_used=sql_used,
                chart_data=chart_data,
                metrics=metrics,
                execution_time_ms=execution_time,
                row_count=row_count,
                data=data_rows[:100] if data_rows else None,
            )

        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            logger.error("Agent run failed: %s", e)
            return AgentResponse(
                answer="I encountered an issue processing your query. Please try rephrasing it.",
                domain=domain,
                query_type=query_type,
                sql_used=sql_used,
                chart_data=None,
                metrics=None,
                execution_time_ms=execution_time,
                error=str(e),
            )

