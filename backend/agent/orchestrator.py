"""LangChain agent orchestrator -- ties tools, memory, and Llama 3.3 70B together.

Switched from OpenAI GPT-4o (ChatOpenAI) to Groq Llama 3.3 70B (ChatGroq).
"""

from dataclasses import dataclass, field
from typing import Optional
import time
import json
import logging

# from langchain_openai import ChatOpenAI  # commented out -- switched to Groq
from langchain_groq import ChatGroq
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory

from backend.agent.tools.hcm_tool import hcm_query_tool
from backend.agent.tools.finance_tool import finance_query_tool
from backend.agent.tools.procurement_tool import procurement_query_tool
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
            model="llama-3.3-70b-versatile",
            temperature=0,
            groq_api_key=settings.groq_api_key,
        )
        self.tools = [hcm_query_tool, finance_query_tool, procurement_query_tool]
        self.memories: dict[str, ConversationBufferWindowMemory] = {}

        self.system_prompt = (
            "You are an intelligent AI assistant for Oracle Fusion ERP data.\n"
            "You have access to three tools that query real database tables:\n"
            "- hcm_query_tool: for HR, headcount, attrition, salary, employee data\n"
            "- finance_query_tool: for GL balances, budget vs actual, AP invoices, payment aging\n"
            "- procurement_query_tool: for purchase orders, quotations, supplier spend, engagement deltas\n\n"
            "Rules:\n"
            "1. ALWAYS use the appropriate tool to fetch real data -- never make up numbers\n"
            "2. After getting tool results, provide a clear, concise business-focused answer\n"
            "3. Highlight key numbers prominently (e.g. \"47 employees\", \"+12.4% delta\")\n"
            "4. If the tool returns chart_data or metrics, acknowledge them in your answer\n"
            "5. Keep answers professional and to the point -- max 4 sentences for simple queries\n"
            "6. If a query spans multiple domains, use multiple tools\n"
            "7. Never reveal raw SQL to the user unless they ask -- the UI shows it separately\n"
            "8. You MUST ONLY answer questions about Oracle Fusion ERP data (HCM, Finance, Procurement). "
            "If a question is about general knowledge, internet search, weather, news, coding help, "
            "or anything NOT related to the ERP database, politely decline and explain that you can "
            "only assist with ERP-related queries.\n"
            "9. NEVER answer from your general knowledge. ALL answers MUST come from tool results. "
            "If no tool can answer the question, say so."
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
            return_intermediate_steps=True,
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
        }

        try:
            # ── FAST PATH: single-domain → call tool directly, skip agent ──
            if domain in _TOOL_MAP:
                tool_fn = _TOOL_MAP[domain]
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

                if error_msg:
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

            # ── FULL PATH: cross-domain → use agent executor (needs tool selection) ──
            else:
                result = self.agent_executor.invoke(
                    {
                        "input": query,
                        "chat_history": memory.chat_memory.messages,
                    }
                )

                answer = result.get("output", "I could not generate a response.")

                # Extract structured data from tool outputs
                for step in result.get("intermediate_steps", []):
                    if len(step) >= 2:
                        tool_output = step[1]
                        raw_str = None
                        if isinstance(tool_output, str):
                            raw_str = tool_output
                        elif hasattr(tool_output, "content"):
                            raw_str = tool_output.content
                        elif hasattr(tool_output, "__str__"):
                            raw_str = str(tool_output)

                        if raw_str:
                            try:
                                tool_data = json.loads(raw_str)
                                if tool_data.get("sql_used"):
                                    sql_used = tool_data["sql_used"]
                                if tool_data.get("chart_data"):
                                    chart_data = tool_data["chart_data"]
                                if tool_data.get("metrics"):
                                    metrics = tool_data["metrics"]
                                if "row_count" in tool_data:
                                    row_count = tool_data["row_count"]
                            except (json.JSONDecodeError, TypeError):
                                pass

            # Update memory
            memory.chat_memory.add_user_message(query)
            memory.chat_memory.add_ai_message(answer)

            execution_time = int((time.time() - start_time) * 1000)

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

