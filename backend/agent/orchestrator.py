"""LangChain agent orchestrator — ties tools, memory, and GPT-4o together."""

from dataclasses import dataclass, field
from typing import Optional
import time
import json
import logging

from langchain_openai import ChatOpenAI
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
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=settings.openai_api_key,
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
            "1. ALWAYS use the appropriate tool to fetch real data — never make up numbers\n"
            "2. After getting tool results, provide a clear, concise business-focused answer\n"
            "3. Highlight key numbers prominently (e.g. \"47 employees\", \"+12.4% delta\")\n"
            "4. If the tool returns chart_data or metrics, acknowledge them in your answer\n"
            "5. Keep answers professional and to the point — max 4 sentences for simple queries\n"
            "6. If a query spans multiple domains, use multiple tools\n"
            "7. Never reveal raw SQL to the user unless they ask — the UI shows it separately"
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
            max_iterations=3,
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

        # Classify intent first
        intent = classify_intent(query)
        domain = intent.get("domain", "CROSS_DOMAIN")
        query_type = intent.get("query_type", "lookup")

        sql_used = ""
        chart_data = None
        metrics = None
        row_count = 0

        try:
            result = self.agent_executor.invoke(
                {
                    "input": query,
                    "chat_history": memory.chat_memory.messages,
                }
            )

            answer = result.get("output", "I could not generate a response.")

            # Extract structured data from tool outputs if available
            for step in result.get("intermediate_steps", []):
                if len(step) >= 2:
                    tool_output = step[1]
                    if isinstance(tool_output, str):
                        try:
                            tool_data = json.loads(tool_output)
                            if tool_data.get("sql_used"):
                                sql_used = tool_data["sql_used"]
                            if tool_data.get("chart_data"):
                                chart_data = tool_data["chart_data"]
                            if tool_data.get("metrics"):
                                metrics = tool_data["metrics"]
                            if "row_count" in tool_data:
                                row_count = tool_data["row_count"]
                        except json.JSONDecodeError:
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
