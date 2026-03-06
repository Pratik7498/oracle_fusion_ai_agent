"""
Comprehensive test suite - Oracle Fusion AI Agent
38 queries across 7 domain combinations
ASCII-only output (Windows cp1252 safe)
"""
import requests, json, time, sys
from datetime import datetime

BASE_URL = "http://localhost:8000"
TIMEOUT = 90

TEST_CATEGORIES = {
    "ALL THREE DOMAINS": [
        "For each cost centre show total budget, GL actual spend, PO spend, and active employee headcount",
        "Show department salary totals vs PO spend vs budget allocation side by side",
        "Which departments are over budget and also have the highest attrition rate?",
        "Show supplier invoice totals, PO count, and employee headcount for departments that raised those POs",
        "List cost centres with budget utilization above 80% alongside active headcount and total requisition value",
        "Show total payroll cost vs total PO spend vs total GL actual by department",
        "Which suppliers have the highest invoice amounts from departments with more than 50 employees?",
        "Show a breakdown of finance spend, HR costs, and procurement spend by cost centre",
    ],
    "HCM + FINANCE": [
        "Show department headcount alongside average salary and budget variance",
        "Which departments have the highest salary cost and are also over budget?",
        "Show payroll expense by cost centre compared to GL actual amount",
        "What is the average salary for employees in departments with budget above 500000?",
        "Show employee count and total salary vs budget amount for each department",
    ],
    "HCM + PROCUREMENT": [
        "Which employees raised the most requisitions this year?",
        "Show headcount per department alongside total PO spend raised by that department",
        "List departments where employees have raised approved POs with total value above 100000",
        "Which departments have active employees who submitted requisitions that became approved POs?",
        "Show average salary vs total requisition value raised by each department",
    ],
    "FINANCE + PROCUREMENT": [
        "Show total invoice amount and total PO value per supplier",
        "Which cost centres have the highest AP invoice spend and PO commitments?",
        "Show budget vs actual vs PO spend commitment for each cost centre",
        "List suppliers with invoices over 50000 and their corresponding approved PO count",
        "Show AP payment totals alongside open PO commitments by cost centre",
    ],
    "PROCUREMENT DOMAIN": [
        "Show top 10 suppliers by total PO amount",
        "List all purchase orders with status APPROVED grouped by cost centre",
        "What is the total value of pending requisitions by department?",
        "Show PO spend by category",
        "Which suppliers have contracts expiring this year?",
    ],
    "FINANCE DOMAIN": [
        "What was the last year budget amount?",
        "Show budget vs actual variance for each cost centre",
        "What is the total outstanding AP invoice amount?",
        "Show AP invoice amounts by month for the current year",
        "Show GL actual amounts vs budget by cost centre for fiscal year 2024",
    ],
    "HCM DOMAIN": [
        "How many active employees are there by department?",
        "Show average salary by department",
        "What is the attrition rate by department?",
        "List the top 10 highest paid employees with their grade and department",
        "Show headcount breakdown by grade code",
    ],
}


def post_query(query, session_id):
    try:
        r = requests.post(f"{BASE_URL}/chat",
                          json={"query": query, "session_id": session_id},
                          timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        return {"error": f"TIMEOUT {TIMEOUT}s", "row_count": 0, "sql_used": "", "domain": "?"}
    except Exception as e:
        return {"error": str(e)[:120], "row_count": 0, "sql_used": "", "domain": "?"}


def clip(s, n=160):
    s = (s or "").strip().replace("\n", " ")
    return s[:n] + ("..." if len(s) > n else "")


def run():
    W = 76
    print("=" * W)
    print("  ORACLE FUSION AI AGENT - COMPREHENSIVE TEST SUITE")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * W)

    try:
        h = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"\n[HEALTH OK] {h.json()}\n")
    except Exception as e:
        print(f"\n[HEALTH FAIL] {e}\n")
        return

    results = []
    cat_summary = []
    session = f"test-{int(time.time())}"
    total_q = sum(len(v) for v in TEST_CATEGORIES.values())
    q_num = 0

    for cat, queries in TEST_CATEGORIES.items():
        print(f"\n{'-' * W}")
        print(f"  {cat}  ({len(queries)} queries)")
        print(f"{'-' * W}")
        cp = cw = cf = 0

        for q in queries:
            q_num += 1
            print(f"\n  [{q_num}/{total_q}] {q}")
            t0 = time.time()
            resp = post_query(q, session)
            elapsed = time.time() - t0

            # Rate-limit guard: sleep between queries to avoid Groq 429
            # Cross-domain queries use 70b model which has tighter RPM limits
            inter_delay = 8 if cat.startswith("ALL THREE") or "+" in cat else 4
            time.sleep(inter_delay)

            err       = resp.get("error") or ""
            rows      = resp.get("row_count", 0)
            sql       = resp.get("sql_used") or ""
            domain    = resp.get("domain") or "?"
            chart     = bool(resp.get("chart_data"))
            fixes     = resp.get("sql_corrections") or []
            sample    = (resp.get("data") or [])[:1]

            is_err = bool(err) and "no data" not in err.lower() and "no records" not in err.lower()
            if is_err:
                status = "FAIL"; cf += 1
                results.append(("FAIL", cat, q, err, sql))
            elif rows == 0:
                status = "ZERO"; cw += 1
                results.append(("ZERO", cat, q, "0 rows", sql))
            else:
                status = "PASS"; cp += 1
                results.append(("PASS", cat, q, "", sql))

            chart_s = " [CHART]" if chart else ""
            fix_s   = f" [{len(fixes)} fix(es)]" if fixes else ""
            print(f"    [{status}] {domain}  rows={rows}  {elapsed:.1f}s{chart_s}{fix_s}")
            print(f"    SQL: {clip(sql, 160)}")
            if is_err:
                print(f"    ERR: {clip(err, 120)}")
            if fixes:
                for fx in fixes[:2]:
                    print(f"    FIX: {clip(str(fx), 100)}")
            if sample:
                print(f"    SAMPLE cols: {list(sample[0].keys())[:6]}")

        ct = cp + cw + cf
        cat_summary.append((cat, cp, cw, cf, ct))
        print(f"\n  -> {cp}/{ct} PASS | {cw} ZERO-ROW | {cf} FAIL")

    # Summary
    all_p = sum(1 for r in results if r[0] == "PASS")
    all_w = sum(1 for r in results if r[0] == "ZERO")
    all_f = sum(1 for r in results if r[0] == "FAIL")
    total = len(results)

    print(f"\n\n{'=' * W}")
    print("  FINAL SUMMARY")
    print(f"{'=' * W}")
    print(f"\n  {'Category':<35} {'PASS':>5} {'ZERO':>5} {'FAIL':>5} {'TOT':>5}")
    print(f"  {'-'*35} {'-'*5} {'-'*5} {'-'*5} {'-'*5}")
    for nm, p, w, f, t in cat_summary:
        print(f"  {nm:<35} {p:>5} {w:>5} {f:>5} {t:>5}")
    print(f"  {'-'*55}")
    print(f"  {'TOTAL':<35} {all_p:>5} {all_w:>5} {all_f:>5} {total:>5}")
    pct = int(all_p/total*100) if total else 0
    print(f"\n  SCORE: {pct}%  ({all_p}/{total})")

    if all_f:
        print(f"\n  FAILURES ({all_f}):")
        for s, c, q, e, sq in results:
            if s == "FAIL":
                print(f"    [{c}] {q[:65]}")
                print(f"      ERROR: {e[:110]}")

    if all_w:
        print(f"\n  ZERO-ROW ({all_w}):")
        for s, c, q, e, sq in results:
            if s == "ZERO":
                print(f"    [{c}] {q[:65]}")
                print(f"      SQL: {clip(sq, 120)}")

    print(f"\n{'=' * W}")

    # Save JSON
    out = {
        "timestamp": datetime.now().isoformat(),
        "summary": {"total": total, "pass": all_p, "zero_row": all_w,
                    "fail": all_f, "score_pct": pct},
        "categories": [{"name": n, "pass": p, "zero": w, "fail": f, "total": t}
                       for n, p, w, f, t in cat_summary],
        "results": [{"status": r[0], "category": r[1], "query": r[2],
                     "error": r[3], "sql": r[4]} for r in results],
    }
    with open("test_results.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print("  Saved: test_results.json")
    print()


if __name__ == "__main__":
    run()
