"""Minimal test: single API call to running server."""
import requests, time, sys
sys.stdout.reconfigure(line_buffering=True)

print("Testing server...", flush=True)
t0 = time.time()
try:
    r = requests.post("http://localhost:8000/chat", 
                      json={"query": "How many total employees are there?", "session_id": "minimal_test"},
                      timeout=120)
    elapsed = time.time() - t0
    print(f"Status: {r.status_code}", flush=True)
    d = r.json()
    print(f"Time: {elapsed:.1f}s", flush=True)
    print(f"Domain: {d.get('domain')}", flush=True)
    print(f"Rows: {d.get('row_count', 0)}", flush=True)
    print(f"Chart: {'YES' if d.get('chart_data') else 'NO'}", flush=True)
    print(f"SQL: {d.get('sql_used', '')[:200]}", flush=True)
    answer = d.get("answer", "")[:400]
    print(f"Answer: {answer}", flush=True)
    if d.get("error"):
        print(f"Error: {d.get('error')}", flush=True)
except Exception as e:
    print(f"Error: {e} ({time.time()-t0:.1f}s)", flush=True)
