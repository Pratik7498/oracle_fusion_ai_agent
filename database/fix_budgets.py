"""Fix budget_amount in fin_gl_balances - populate with correct budget data."""
import psycopg2

# Budget data per cost centre (from generate_seed.py cc_data arrays)
# Format: (cost_centre_code, [13 budget values for JAN-2025 through JAN-2026])
BUDGETS = [
    ("CC001", [430000,430000,430000,435000,435000,435000,440000,440000,440000,445000,445000,450000,450000]),
    ("CC002", [90000,90000,90000,90000,90000,90000,90000,90000,90000,90000,90000,90000,92000]),
    ("CC003", [150000,150000,150000,150000,150000,150000,150000,150000,150000,150000,150000,155000,155000]),
    ("CC004", [65000,65000,65000,65000,65000,65000,65000,65000,65000,65000,65000,65000,66000]),
    ("CC005", [55000,55000,55000,55000,55000,55000,55000,55000,55000,55000,55000,55000,56000]),
    ("CC006", [185000,185000,185000,185000,185000,185000,185000,185000,185000,188000,188000,190000,190000]),
    ("CC007", [100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,102000]),
    ("CC008", [210000,210000,210000,215000,215000,215000,215000,215000,215000,215000,215000,220000,220000]),
    ("CC009", [75000,75000,75000,75000,75000,75000,75000,75000,75000,75000,75000,75000,76000]),
    ("CC010", [320000,320000,320000,320000,320000,320000,320000,320000,320000,325000,325000,330000,330000]),
]

MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
PERIODS = [f"{m}-2025" for m in MONTHS] + ["JAN-2026"]

conn = psycopg2.connect(dbname="oracle_fusion_poc", user="postgres", password="12345", host="localhost")
conn.autocommit = True
cur = conn.cursor()

updated = 0
for cc_code, budgets in BUDGETS:
    # Get cost_centre_id
    cur.execute("SELECT cost_centre_id FROM fin_cost_centres WHERE cost_centre_code=%s", (cc_code,))
    row = cur.fetchone()
    if not row:
        print(f"  WARN: {cc_code} not found")
        continue
    cc_id = row[0]
    for i, period in enumerate(PERIODS):
        cur.execute(
            "UPDATE fin_gl_balances SET budget_amount=%s WHERE cost_centre_id=%s AND period_name=%s",
            (budgets[i], cc_id, period)
        )
        updated += cur.rowcount

# Also update the finance_gl_balances view (it auto-refreshes since it reads from fin_gl_balances)
# Verify
cur.execute("SELECT balance_id, cost_centre_id, period_name, actual_amount, budget_amount FROM fin_gl_balances WHERE balance_id BETWEEN 38 AND 47")
rows = cur.fetchall()
print(f"Updated {updated} rows")
print(f"\nVerification (balance_id 38-47):")
for r in rows:
    pct = round(((r[3]-r[4])/r[4])*100, 2) if r[4] and r[4] != 0 else None
    print(f"  id={r[0]} cc={r[1]} period={r[2]} actual={r[3]} budget={r[4]} pct={pct}%")

cur.close()
conn.close()
print("\nDone!")
