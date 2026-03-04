"""Debug: test tool output directly to see if chart_data is generated."""
import json
from backend.agent.tools.finance_tool import finance_query_tool

result = finance_query_tool.invoke("Show me all suppliers and their invoice count")
data = json.loads(result)
print("Keys:", list(data.keys()))
print("Row count:", data.get("row_count", 0))
print("Has chart:", "YES" if data.get("chart_data") else "NO")
print("Has metrics:", "YES" if data.get("metrics") else "NO")
if data.get("data"):
    print("First 2 rows:", data["data"][:2])
if data.get("chart_data"):
    chart = data["chart_data"]
    print("Chart type:", chart.get("data", [{}])[0].get("type", "unknown"))
