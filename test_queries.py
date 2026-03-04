#!/usr/bin/env python3
"""Battery test: 10 queries across domains — checks answer quality, chart, and speed."""

import requests
import time
import json

URL = "http://localhost:8000/chat"

QUERIES = [
    # Simple lookups
    ("HCM Simple", "How many employees are there in the Engineering department?"),
    ("HCM Complex", "Show average salary by department with headcount for top 5 departments"),
    ("Finance Simple", "Show total AP invoice amount by supplier"),
    ("Finance Complex", "What is the budget vs actual variance for each cost centre in FY2025?"),
    ("Procurement Simple", "Show purchase orders by status"),
    ("Procurement Complex", "Show top 10 suppliers by total PO amount with their approval rate"),
    # Chart-specific
    ("Chart Bar", "Show headcount breakdown by department"),
    ("Chart Grouped", "Show budget amount vs actual amount for all cost centres"),
    ("Chart Time", "Show GL balance trend by period for Engineering"),
    # Cross-domain
    ("Cross Domain", "Which departments have the highest procurement spend and most employees?"),
]

results = []
for label, query in QUERIES:
    print(f"\n{'='*60}")
    print(f"[{label}] {query}")
    print("-" * 60)
    t0 = time.time()
    try:
        r = requests.post(URL, json={"query": query, "session_id": f"test_{label}"}, timeout=180)
        elapsed = time.time() - t0
        d = r.json()
        answer = d.get("answer", "")[:200]
        has_chart = "YES" if d.get("chart_data") else "NO"
        rows = d.get("row_count", 0)
        sql = d.get("sql_used", "")[:150]
        domain = d.get("domain", "?")
        exec_ms = d.get("execution_time_ms", 0)

        print(f"  Domain: {domain} | Rows: {rows} | Chart: {has_chart}")
        print(f"  Time: {elapsed:.1f}s (backend: {exec_ms}ms)")
        print(f"  SQL: {sql}")
        print(f"  Answer: {answer}")

        results.append({
            "label": label, "elapsed": round(elapsed, 1), "rows": rows,
            "chart": has_chart, "domain": domain, "exec_ms": exec_ms,
            "answer_len": len(d.get("answer", "")),
            "has_data": rows > 0 or "no data" not in answer.lower()
        })
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ERROR: {e} ({elapsed:.1f}s)")
        results.append({"label": label, "elapsed": round(elapsed, 1), "error": str(e)})

# Summary
print(f"\n\n{'='*60}")
print("SUMMARY")
print("=" * 60)
print(f"{'Query':<25} {'Time':>6} {'Rows':>6} {'Chart':>6} {'Data':>5}")
print("-" * 60)
for r in results:
    if "error" in r:
        print(f"{r['label']:<25} {r['elapsed']:>5.1f}s {'ERR':>6} {'ERR':>6} {'ERR':>5}")
    else:
        print(f"{r['label']:<25} {r['elapsed']:>5.1f}s {r['rows']:>6} {r['chart']:>6} {'OK' if r['has_data'] else 'EMPTY':>5}")

avg_time = sum(r["elapsed"] for r in results) / len(results)
charts_ok = sum(1 for r in results if r.get("chart") == "YES")
data_ok = sum(1 for r in results if r.get("has_data"))
print(f"\nAvg response: {avg_time:.1f}s | Charts: {charts_ok}/{len(results)} | Data: {data_ok}/{len(results)}")
