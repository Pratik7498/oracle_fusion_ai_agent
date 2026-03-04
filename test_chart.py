"""Test chart generation with 3 key queries."""
import sys, requests, time, json
sys.stdout.reconfigure(line_buffering=True)

URL = "http://localhost:8000/chat"

QUERIES = [
    ("Headcount Chart", "Show headcount breakdown by department"),
    ("AP by Supplier", "Show total AP invoice amount by supplier for top 5 suppliers"),
    ("PO by Status", "Show purchase orders breakdown by status"),
]

for label, query in QUERIES:
    print(f"\n{'='*60}", flush=True)
    print(f"[{label}] {query}", flush=True)
    t0 = time.time()
    try:
        r = requests.post(URL, json={"query": query, "session_id": label}, timeout=120)
        elapsed = time.time() - t0
        d = r.json()
        chart = d.get("chart_data")
        has_chart = "YES" if chart else "NO"
        rows = d.get("row_count", 0)
        domain = d.get("domain", "?")
        sql = d.get("sql_used", "")[:200]
        ans = d.get("answer", "")[:300].replace("\n", " ")
        err = d.get("error", "")

        print(f"  Time: {elapsed:.1f}s | Rows: {rows} | Chart: {has_chart} | Domain: {domain}", flush=True)
        print(f"  SQL: {sql}", flush=True)
        print(f"  Answer: {ans}", flush=True)
        if err:
            print(f"  Error: {err}", flush=True)
        if chart:
            chart_type = chart.get("data", [{}])
            if chart_type:
                trace_type = chart_type[0].get("type", "unknown") if isinstance(chart_type, list) and chart_type else "unknown"
                print(f"  Chart Type: {trace_type}", flush=True)
                title = chart.get("layout", {}).get("title", {})
                if isinstance(title, dict):
                    print(f"  Chart Title: {title.get('text', 'N/A')}", flush=True)
                else:
                    print(f"  Chart Title: {title}", flush=True)
    except Exception as e:
        print(f"  ERROR: {e} ({time.time()-t0:.1f}s)", flush=True)

print(f"\n{'='*60}", flush=True)
print("Done!", flush=True)
