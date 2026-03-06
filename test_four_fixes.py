#!/usr/bin/env python3
"""Verify all 4 fixed query patterns return real data (not empty/NaN)."""

import requests, json, time

URL = "http://localhost:8000/chat"

TESTS = [
    ("Q1 Supplier+Invoice+Headcount",
     "For each supplier, show total invoice amount, number of POs, and how many employees work in the departments that issued those POs"),
    ("Q2 Salary+PO combined cost",
     "Which departments have the highest combined employee salary cost and PO spend?"),
    ("Q3 Deloitte UK ERP summary",
     "Show full ERP summary for supplier Deloitte UK: POs, invoices, payments, and which departments ordered from them"),
    ("Q4 Monthly invoices 2025",
     "Show total invoiced amount by month for the year 2025 as a line chart"),
]

for label, query in TESTS:
    print(f"\n{'='*70}")
    print(f"[{label}]")
    print(f"Query: {query}")
    print("-" * 70)
    try:
        r = requests.post(URL, json={"query": query, "session_id": f"fix_test"}, timeout=120)
        d = r.json()
        rows      = d.get("row_count", 0)
        has_chart = bool(d.get("chart_data"))
        sql       = d.get("sql_used", "")[:400]
        answer    = d.get("answer", "")[:300]
        domain    = d.get("domain", "?")
        error     = d.get("error", None)

        print(f"  Domain:  {domain}")
        print(f"  Rows:    {rows}")
        print(f"  Chart:   {'YES' if has_chart else 'NO'}")
        print(f"  Error:   {error}")
        print(f"  SQL:     {sql}")
        print(f"  Answer:  {answer}")

        # Quick checks
        issues = []
        if rows == 0:
            issues.append("EMPTY RESULT")
        if error:
            issues.append(f"ERROR: {error}")
        # Check NaN in data rows
        data = d.get("data", []) or []
        nan_count = sum(1 for row in data[:5]
                        for v in row.values()
                        if isinstance(v, float) and v != v)  # NaN check
        if nan_count > 0:
            issues.append(f"NaN VALUES in {nan_count} cells")

        if issues:
            print(f"\n  *** ISSUES: {', '.join(issues)} ***")
        else:
            print(f"\n  ✓ OK - {rows} rows returned")

    except Exception as e:
        print(f"  EXCEPTION: {e}")

print("\n\nDone.")
