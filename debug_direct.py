"""Direct debug: call the tool directly and see what error occurs."""
import traceback
import sys
import os

# Set up env
os.environ.setdefault("GROQ_API_KEY", open(".env").read().split("GROQ_API_KEY=")[1].split("\n")[0].strip().strip('"'))

sys.path.insert(0, ".")

try:
    from backend.agent.tools.hcm_tool import hcm_query_tool
    print("1. Testing HCM tool directly...")
    result = hcm_query_tool.invoke("How many employees are in Engineering department?")
    import json
    d = json.loads(result)
    print(f"   Rows: {d.get('row_count', 0)}")
    print(f"   SQL: {d.get('sql_used', '')[:200]}")
    print(f"   Data: {str(d.get('data', []))[:200]}")
    print(f"   Chart: {'YES' if d.get('chart_data') else 'NO'}")
except Exception as e:
    traceback.print_exc()

print()

try:
    from backend.agent.orchestrator import Orchestrator
    print("2. Testing Orchestrator...")
    orch = Orchestrator()
    result = orch.run("How many employees are in Engineering department?", session_id="debug1")
    print(f"   Answer: {result.answer[:200]}")
    print(f"   Rows: {result.row_count}")
    print(f"   Chart: {'YES' if result.chart_data else 'NO'}")
    print(f"   SQL: {result.sql_used[:200]}")
except Exception as e:
    traceback.print_exc()
