"""Quick test: run 5 queries and print results unbuffered."""
import sys
import requests
import time

sys.stdout.reconfigure(line_buffering=True)

URL = "http://localhost:8000/chat"

QUERIES = [
    ("Q1-HCM", "How many employees are there in the Engineering department?"),
    ("Q2-FIN", "Show total AP invoice amount by supplier for top 5 suppliers"),
    ("Q3-PROC", "Show purchase orders by status"),
    ("Q4-CHART", "Show budget amount vs actual amount for all cost centres"),
    ("Q5-COMPLEX", "Show average salary by department with headcount"),
]

for label, query in QUERIES:
    print(f"\n[{label}] {query}", flush=True)
    t0 = time.time()
    try:
        r = requests.post(URL, json={"query": query, "session_id": label}, timeout=180)
        elapsed = time.time() - t0
        d = r.json()
        chart = "YES" if d.get("chart_data") else "NO"
        rows = d.get("row_count", 0)
        domain = d.get("domain", "?")
        ms = d.get("execution_time_ms", 0)
        ans = d.get("answer", "")[:250].replace("\n", " ")
        sql = d.get("sql_used", "")[:200]
        print(f"  -> {elapsed:.1f}s | Rows:{rows} | Chart:{chart} | Domain:{domain} | Backend:{ms}ms", flush=True)
        print(f"  SQL: {sql}", flush=True)
        print(f"  Ans: {ans}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e} ({time.time()-t0:.1f}s)", flush=True)

print("\nDone!", flush=True)
