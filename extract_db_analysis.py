"""
Database Analysis Extractor — queries live PostgreSQL and writes database_analysis.md
Uses correct column names from schema.sql
"""
import os, sys
sys.path.insert(0, '.')
import psycopg2
from dotenv import load_dotenv

load_dotenv()
URL = os.environ.get('POSTGRES_URL', 'postgresql://poc_user:poc_pass_2025@localhost:5432/oracle_fusion_poc')

conn = psycopg2.connect(URL)
cur = conn.cursor()

out = []
def w(s=""): out.append(str(s))

def q(sql, p=None):
    cur.execute(sql, p)
    return cur.fetchall()

def q1(sql, p=None):
    cur.execute(sql, p)
    r = cur.fetchone()
    return r[0] if r else None

def safe(sql):
    try:
        cur.execute(sql)
        return cur.fetchall(), [d[0] for d in cur.description]
    except Exception as e:
        conn.rollback()
        return [], []

# ── DB overview ───────────────────────────────────────────────────────────────
db_version = q1("SELECT version()")
db_name    = q1("SELECT current_database()")

tables_raw = q("""
    SELECT t.table_name
    FROM information_schema.tables t
    WHERE t.table_schema='public' AND t.table_type='BASE TABLE'
    ORDER BY t.table_name
""")
table_names = [r[0] for r in tables_raw]

# Accurate row counts
row_counts = {}
for tname in table_names:
    try:
        row_counts[tname] = q1(f"SELECT COUNT(*) FROM {tname}")
    except:
        conn.rollback()
        row_counts[tname] = -1

total_rows = sum(v for v in row_counts.values() if v >= 0)

# ── Columns ───────────────────────────────────────────────────────────────────
all_cols = q("""
    SELECT c.table_name, c.column_name, c.data_type,
           c.character_maximum_length, c.numeric_precision, c.numeric_scale,
           c.is_nullable, c.column_default, c.ordinal_position
    FROM information_schema.columns c
    WHERE c.table_schema='public'
    ORDER BY c.table_name, c.ordinal_position
""")
cols_by_table = {}
for row in all_cols:
    cols_by_table.setdefault(row[0], []).append(row)

# ── Primary keys ──────────────────────────────────────────────────────────────
pks = q("""
    SELECT tc.table_name, kc.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kc
         ON tc.constraint_name=kc.constraint_name AND tc.table_schema=kc.table_schema
    WHERE tc.constraint_type='PRIMARY KEY' AND tc.table_schema='public'
    ORDER BY tc.table_name
""")
pk_by_table = {}
for t, c in pks:
    pk_by_table.setdefault(t, []).append(c)

# ── Foreign keys ──────────────────────────────────────────────────────────────
fks = q("""
    SELECT tc.table_name, kcu.column_name, ccu.table_name, ccu.column_name, tc.constraint_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
         ON tc.constraint_name=kcu.constraint_name AND tc.table_schema=kcu.table_schema
    JOIN information_schema.constraint_column_usage ccu
         ON ccu.constraint_name=tc.constraint_name AND ccu.table_schema=tc.table_schema
    WHERE tc.constraint_type='FOREIGN KEY' AND tc.table_schema='public'
    ORDER BY tc.table_name, kcu.column_name
""")

fk_lookup = {}
for child_t, child_col, parent_t, parent_col, _ in fks:
    fk_lookup[(child_t, child_col)] = f"FK -> {parent_t}.{parent_col}"

# ── Data coverage ─────────────────────────────────────────────────────────────
# Budget years (from budget headers)
bh_years,  _ = safe("SELECT DISTINCT fiscal_year FROM fin_budget_headers ORDER BY fiscal_year")
# GL years (fiscal_year column)
gl_years,  _ = safe("SELECT DISTINCT fiscal_year FROM fin_gl_balances WHERE fiscal_year IS NOT NULL ORDER BY fiscal_year")
# Budget periods
bh_periods,_ = safe("SELECT DISTINCT period_name FROM fin_budget_headers ORDER BY period_name")
bl_periods,_ = safe("SELECT DISTINCT period_name FROM fin_budget_lines ORDER BY period_name LIMIT 20")
gl_periods,_ = safe("SELECT DISTINCT period_name FROM fin_gl_balances ORDER BY period_name LIMIT 20")
# Departments
depts,     _ = safe("SELECT dept_id, dept_name FROM hcm_departments ORDER BY dept_id LIMIT 20")
# Cost centres
ccs,       _ = safe("SELECT cost_centre_id, cost_centre_code, cost_centre_name, dept_id FROM fin_cost_centres ORDER BY cost_centre_id")
# Assignment statuses
asgn_stat, _ = safe("SELECT assignment_status, COUNT(*) FROM hcm_assignments GROUP BY assignment_status ORDER BY assignment_status")
# Amount ranges
bl_range,  _ = safe("SELECT MIN(amount), MAX(amount), AVG(amount), COUNT(*) FROM fin_budget_lines")
gl_range,  _ = safe("SELECT MIN(period_net), MAX(period_net), MIN(end_balance), MAX(end_balance) FROM fin_gl_balances")
po_range,  _ = safe("SELECT MIN(total_amount), MAX(total_amount), COUNT(*) FROM proc_po_headers")
inv_range, _ = safe("SELECT MIN(invoice_amount), MAX(invoice_amount), COUNT(*) FROM fin_ap_invoices")

# ── Sample data ───────────────────────────────────────────────────────────────
sample_tables = [
    "hcm_persons","hcm_assignments","hcm_departments",
    "fin_cost_centres","fin_budget_headers","fin_budget_lines",
    "fin_gl_balances","proc_po_headers","proc_po_lines",
    "proc_po_distributions","fin_ap_invoices","fin_ap_payments","sup_suppliers"
]
samples = {}
for tbl in sample_tables:
    if tbl in table_names:
        rows, hdrs = safe(f"SELECT * FROM {tbl} LIMIT 5")
        if hdrs:
            samples[tbl] = (hdrs, rows)

# ── Integrity checks ─────────────────────────────────────────────────────────
def icheck(label, sql):
    rows, _ = safe(sql)
    val = rows[0][0] if rows else "?"
    return label, val

checks = [
    icheck("Cost centres with no matching dept",
           "SELECT COUNT(*) FROM fin_cost_centres cc LEFT JOIN hcm_departments d ON d.dept_id=cc.dept_id WHERE d.dept_id IS NULL"),
    icheck("Budget lines with orphan budget_header_id",
           "SELECT COUNT(*) FROM fin_budget_lines bl LEFT JOIN fin_budget_headers bh ON bh.budget_header_id=bl.budget_header_id WHERE bh.budget_header_id IS NULL"),
    icheck("Budget lines with orphan cost_centre_id",
           "SELECT COUNT(*) FROM fin_budget_lines bl LEFT JOIN fin_cost_centres cc ON cc.cost_centre_id=bl.cost_centre_id WHERE cc.cost_centre_id IS NULL"),
    icheck("GL balances with orphan cost_centre_id",
           "SELECT COUNT(*) FROM fin_gl_balances gl LEFT JOIN fin_cost_centres cc ON cc.cost_centre_id=gl.cost_centre_id WHERE cc.cost_centre_id IS NULL"),
    icheck("Assignments with missing person_id",
           "SELECT COUNT(*) FROM hcm_assignments a LEFT JOIN hcm_persons p ON p.person_id=a.person_id WHERE p.person_id IS NULL"),
    icheck("PO distributions with missing po_line_id",
           "SELECT COUNT(*) FROM proc_po_distributions pod LEFT JOIN proc_po_lines pol ON pol.po_line_id=pod.po_line_id WHERE pol.po_line_id IS NULL"),
    icheck("Budget lines where amount IS NULL or 0",
           "SELECT COUNT(*) FROM fin_budget_lines WHERE amount IS NULL OR amount=0"),
    icheck("GL balances where period_net IS NULL",
           "SELECT COUNT(*) FROM fin_gl_balances WHERE period_net IS NULL"),
    icheck("AP invoices where invoice_amount IS NULL",
           "SELECT COUNT(*) FROM fin_ap_invoices WHERE invoice_amount IS NULL"),
    icheck("PO distributions where amount IS NULL",
           "SELECT COUNT(*) FROM proc_po_distributions WHERE amount IS NULL"),
]

zero_tables = [(t, c) for t, c in row_counts.items() if c == 0]

domain_map = {
    "HCM":          [t for t in table_names if t.startswith("hcm_")],
    "Finance":      [t for t in table_names if t.startswith("fin_")],
    "Procurement":  [t for t in table_names if t.startswith("proc_") or t.startswith("sup_")],
    "System":       [t for t in table_names if not any(t.startswith(p) for p in ["hcm_","fin_","proc_","sup_"])],
}

table_desc = {
    "ai_query_log":"AI agent query audit log",
    "hcm_persons":"Employee master: identity (no salary, no org context)",
    "hcm_person_names":"Legal name change history",
    "hcm_person_emails":"Employee email addresses",
    "hcm_organizations":"Business units and legal entities",
    "hcm_locations":"Office and work locations",
    "hcm_departments":"Department master — has cost_centre_code VARCHAR (not FK to fin_cost_centres)",
    "hcm_jobs":"Job catalog and job families",
    "hcm_grades":"Grade salary bands (min/mid/max)",
    "hcm_positions":"Position definitions (slot in org chart)",
    "hcm_assignments":"ALL org context: dept, grade, salary, job — primary HCM table",
    "hcm_employment_periods":"Hire to terminate date spans",
    "hcm_termination_reasons":"Termination reason lookup",
    "hcm_workforce_actions":"Hire/transfer/promote/terminate lifecycle actions",
    "hcm_promotions":"Promotion history per assignment",
    "hcm_transfers":"Transfer history per assignment",
    "hcm_salary_history":"Salary change history per assignment",
    "hcm_compensation_elements":"Base/bonus/allowance pay components",
    "hcm_payroll_runs":"Payroll batch run headers",
    "hcm_payroll_results":"Individual payroll results per assignment",
    "hcm_cost_allocations":"Assignment cost allocation to fin_cost_centres (cross-domain bridge)",
    "hcm_performance_reviews":"Performance reviews linked to person",
    "hcm_training_records":"Training and certification records",
    "fin_ledgers":"General ledger definitions",
    "fin_chart_of_accounts":"Chart of accounts structure",
    "fin_coa_segments":"COA segment definitions",
    "fin_cost_centres":"Cost centre master — bridge between HCM and Finance",
    "fin_account_codes":"Account code master",
    "fin_reporting_periods":"Fiscal reporting periods with fiscal_year and dates",
    "fin_currency_rates":"Currency exchange rates",
    "fin_gl_journal_headers":"GL journal entry headers",
    "fin_gl_journal_lines":"GL journal line items with account + cost centre",
    "fin_gl_balances":"GL summary balances: period_debit/credit/net, begin/end_balance, fiscal_year",
    "fin_budget_versions":"Budget version control (original/revised/forecast)",
    "fin_budget_headers":"Budget header per ledger — fiscal_year and total_amount only",
    "fin_budget_lines":"Budget line amounts at cost centre + account level — PRIMARY budget table",
    "fin_ap_invoices":"AP invoices with invoice_amount, supplier_id, status, due_date",
    "fin_ap_invoice_lines":"AP invoice line items with po_line_id (3-way match)",
    "fin_ap_invoice_distributions":"AP invoice accounting distributions to cost centres",
    "fin_ap_payment_schedules":"AP payment schedules per invoice",
    "fin_ap_payments":"AP payment records — payment_amount, supplier_id (NO invoice_id FK)",
    "fin_ar_customers":"Accounts receivable customer master",
    "fin_ar_invoices":"AR invoices with invoice_amount, customer_id, outstanding",
    "fin_ar_receipts":"AR customer payment receipts",
    "sup_suppliers":"Unified supplier/vendor master for AP and Procurement",
    "sup_supplier_sites":"Supplier site addresses",
    "sup_supplier_contacts":"Supplier contact persons",
    "proc_item_categories":"Item category hierarchy (self-referencing)",
    "proc_items":"Item/service catalog with unit_price",
    "proc_requisition_headers":"Purchase requisition headers with total_amount",
    "proc_requisition_lines":"Requisition line items",
    "proc_requisition_distributions":"Requisition accounting distributions to cost centres",
    "proc_quotation_headers":"Supplier quotation (RFQ) headers with engagement_id",
    "proc_quotation_lines":"Quotation line items",
    "proc_quote_versions":"Quotation version history (audit trail)",
    "proc_po_headers":"PO headers: supplier_id, total_amount, status — NO cost_centre_id",
    "proc_po_lines":"PO line items: quantity, unit_price, line_amount",
    "proc_po_distributions":"PO accounting distributions: amount, cost_centre_id — PRIMARY spend table",
    "proc_po_approvals":"PO approval workflow",
    "proc_receipt_headers":"Goods receipt headers linked to PO",
    "proc_receipt_lines":"Goods receipt lines matched to PO lines",
    "proc_contract_headers":"Blanket purchase contracts with supplier",
    "proc_contract_lines":"Contract line items",
    "schema_embeddings":"PGVector embeddings of schema documentation (AI RAG)",
}

type_abbrev = {
    "character varying":"varchar","integer":"integer","bigint":"bigint",
    "numeric":"numeric","boolean":"boolean","text":"text",
    "timestamp without time zone":"timestamp","timestamp with time zone":"timestamptz",
    "date":"date","double precision":"float8","USER-DEFINED":"vector","ARRAY":"array",
}

# ═════════════════════════════════════════════════════════════════════════════
# BUILD MARKDOWN
# ═════════════════════════════════════════════════════════════════════════════

w("# Database Analysis — Oracle Fusion AI Agent POC")
w()
w("> Generated from live PostgreSQL database on 2026-03-06 (IST)")
w()
w("---")
w()

# ── DATABASE OVERVIEW ─────────────────────────────────────────────────────────
w("# DATABASE OVERVIEW")
w()
w(f"| Property | Value |")
w(f"|---|---|")
w(f"| Database name | `{db_name}` |")
w(f"| PostgreSQL version | {db_version.split('(')[0].strip()} |")
w(f"| Total tables | {len(table_names)} |")
w(f"| Total rows (all tables) | {total_rows:,} |")
w(f"| Domains | HCM (22), Finance (23+), Procurement (17), Supplier (3) |")
w()

# ── TABLE INVENTORY ───────────────────────────────────────────────────────────
w("---")
w()
w("# TABLE INVENTORY")
w()
w("| Table | Rows | Domain | Description |")
w("|---|---|---|---|")
for tname in table_names:
    dom = next((d for d, ts in domain_map.items() if tname in ts), "System")
    desc = table_desc.get(tname, "")
    cnt = row_counts[tname]
    w(f"| `{tname}` | {cnt:,} | {dom} | {desc} |")
w()

# ── FULL TABLE STRUCTURE ──────────────────────────────────────────────────────
w("---")
w()
w("# FULL TABLE STRUCTURE")
w()

for tname in table_names:
    w(f"## `{tname}`")
    w()
    w(f"**Rows:** {row_counts[tname]:,}  |  **Purpose:** {table_desc.get(tname,'N/A')}")
    w()
    w("| Column | Type | Nullable | Default | Notes |")
    w("|---|---|---|---|---|")
    pk_cols = pk_by_table.get(tname, [])
    for row in cols_by_table.get(tname, []):
        _, col_name, data_type, char_max, num_prec, num_scale, nullable, default, _ = row
        dtype = type_abbrev.get(data_type, data_type)
        if char_max:
            dtype += f"({char_max})"
        elif data_type == "numeric" and num_prec:
            dtype += f"({num_prec},{num_scale or 0})"
        null_str = "YES" if nullable == "YES" else "NO"
        def_str = str(default)[:30] if default else ""
        notes = []
        if col_name in pk_cols:
            notes.append("**PK**")
        fk_note = fk_lookup.get((tname, col_name))
        if fk_note:
            notes.append(fk_note)
        w(f"| `{col_name}` | {dtype} | {null_str} | {def_str} | {' | '.join(notes)} |")
    w()

# ── PRIMARY KEYS ──────────────────────────────────────────────────────────────
w("---")
w()
w("# PRIMARY KEYS")
w()
w("| Table | Primary Key |")
w("|---|---|")
for tname in table_names:
    pks_list = pk_by_table.get(tname, [])
    if pks_list:
        w(f"| `{tname}` | `{'`, `'.join(pks_list)}` |")
w()

# ── FOREIGN KEY RELATIONSHIPS ─────────────────────────────────────────────────
w("---")
w()
w("# FOREIGN KEY RELATIONSHIPS")
w()
w("| Child Table | Child Column | Referenced Table | Referenced Column |")
w("|---|---|---|---|")
for child_t, child_col, parent_t, parent_col, _ in fks:
    w(f"| `{child_t}` | `{child_col}` | `{parent_t}` | `{parent_col}` |")
w()

# ── DOMAIN GROUPING ───────────────────────────────────────────────────────────
w("---")
w()
w("# DOMAIN GROUPING")
w()
for domain, t_list in domain_map.items():
    if not t_list:
        continue
    w(f"## {domain}")
    w()
    w("| Table | Rows | Purpose |")
    w("|---|---|---|")
    for t in t_list:
        w(f"| `{t}` | {row_counts[t]:,} | {table_desc.get(t,'')} |")
    w()

# ── DATA COVERAGE ─────────────────────────────────────────────────────────────
w("---")
w()
w("# DATA COVERAGE ANALYSIS")
w()

w("## Fiscal Years Available")
w()
w("| Source Table | Fiscal Years |")
w("|---|---|")

fy_bh = ", ".join(str(r[0]) for r in bh_years if r[0] is not None) or "(none)"
fy_gl_str = ", ".join(str(r[0]) for r in gl_years if r[0] is not None) or "(none)"
w(f"| `fin_budget_headers.fiscal_year` | {fy_bh} |")
w(f"| `fin_gl_balances.fiscal_year` | {fy_gl_str} |")
w()

w("## Accounting Periods Available")
w()
w("**fin_budget_headers.period_name:**")
w()
w(", ".join(str(r[0]) for r in bh_periods if r and r[0]) or "(none)")
w()
w("**fin_budget_lines.period_name:**")
w()
w(", ".join(str(r[0]) for r in bl_periods if r and r[0]) or "(none)")
w()
w("**fin_gl_balances.period_name:**")
w()
w(", ".join(str(r[0]) for r in gl_periods if r and r[0]) or "(none)")
w()

w("## Departments (first 20 from hcm_departments)")
w()
w("| dept_id | dept_name |")
w("|---|---|")
for r in depts:
    w(f"| {r[0]} | {r[1]} |")
w()

w("## Cost Centres (fin_cost_centres — all rows)")
w()
w("| cost_centre_id | code | name | dept_id |")
w("|---|---|---|---|")
for r in ccs:
    w(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
w()

w("## Assignment Status Breakdown (hcm_assignments)")
w()
w("| Status | Count |")
w("|---|---|")
for r in asgn_stat:
    w(f"| {r[0]} | {r[1]:,} |")
w()

w("## Key Amount Ranges")
w()
if bl_range and bl_range[0][0] is not None:
    r = bl_range[0]
    w(f"- **fin_budget_lines.amount**: min={float(r[0]):,.2f}, max={float(r[1]):,.2f}, avg={float(r[2]):,.2f}, count={r[3]:,}")
if gl_range and gl_range[0][0] is not None:
    r = gl_range[0]
    w(f"- **fin_gl_balances.period_net**: min={float(r[0]):,.2f}, max={float(r[1]):,.2f}")
    w(f"- **fin_gl_balances.end_balance**: min={float(r[2]):,.2f}, max={float(r[3]):,.2f}")
if po_range and po_range[0][0] is not None:
    r = po_range[0]
    w(f"- **proc_po_headers.total_amount**: min={float(r[0]):,.2f}, max={float(r[1]):,.2f}, count={r[2]:,}")
if inv_range and inv_range[0][0] is not None:
    r = inv_range[0]
    w(f"- **fin_ap_invoices.invoice_amount**: min={float(r[0]):,.2f}, max={float(r[1]):,.2f}, count={r[2]:,}")
w()

# ── SAMPLE DATA ───────────────────────────────────────────────────────────────
w("---")
w()
w("# SAMPLE DATA")
w()

for tbl, (header, rows) in samples.items():
    w(f"## `{tbl}` — sample rows")
    w()
    w("| " + " | ".join(str(h) for h in header) + " |")
    w("|" + "|".join(["---"] * len(header)) + "|")
    for row in rows[:5]:
        cells = []
        for v in row:
            sv = str(v) if v is not None else "NULL"
            if len(sv) > 35:
                sv = sv[:32] + "..."
            cells.append(sv)
        w("| " + " | ".join(cells) + " |")
    w()

# ── JOIN PATH ANALYSIS ────────────────────────────────────────────────────────
w("---")
w()
w("# JOIN PATH ANALYSIS")
w()
w("""## Core Join Paths

### 1. Headcount by Department

```sql
hcm_assignments a
JOIN hcm_departments d ON d.dept_id = a.dept_id
WHERE a.assignment_status = 'ACTIVE'
GROUP BY d.dept_name
```

> hcm_assignments is the single source of all org context (department, salary, grade).
> hcm_persons contains identity only — it has NO dept_id.

---

### 2. Budget by Cost Centre (correct path)

```sql
fin_budget_lines bl
JOIN fin_budget_headers bh   ON bh.budget_header_id = bl.budget_header_id
JOIN fin_cost_centres   cc   ON cc.cost_centre_id    = bl.cost_centre_id
WHERE bh.fiscal_year = 2024
GROUP BY cc.cost_centre_name
-- VALUE COLUMN: bl.amount
```

> fin_budget_headers has only metadata (fiscal_year, total_amount for the whole budget).
> NEVER use fin_budget_headers.total_amount for per-cost-centre budget amounts.

---

### 3. GL Actuals by Cost Centre

```sql
SELECT cc.cost_centre_name,
       SUM(gl.period_net) AS net_activity,
       SUM(gl.end_balance) AS closing_balance
FROM fin_gl_balances gl
JOIN fin_cost_centres cc ON cc.cost_centre_id = gl.cost_centre_id
WHERE gl.fiscal_year = 2024
GROUP BY cc.cost_centre_name
```

> fin_gl_balances does NOT have actual_amount or budget_amount columns.
> Use period_net for the net movement and end_balance for the period-end balance.

---

### 4. PO Spend by Department (full traversal required)

```sql
SELECT d.dept_name, SUM(pod.amount) AS total_spend
FROM proc_po_distributions pod
JOIN fin_cost_centres     cc  ON cc.cost_centre_id    = pod.cost_centre_id
JOIN hcm_departments      d   ON d.dept_id            = cc.dept_id
GROUP BY d.dept_name
-- Optionally JOIN proc_po_lines / proc_po_headers for date/supplier filtering
```

> proc_po_headers has NO cost_centre_id.
> proc_po_distributions has NO po_header_id.
> Must traverse: distributions -> po_lines -> po_headers.

---

### 5. AP Invoice by Supplier

```sql
SELECT s.supplier_name, SUM(i.invoice_amount) AS total_invoiced
FROM fin_ap_invoices i
JOIN sup_suppliers s ON s.supplier_id = i.supplier_id
GROUP BY s.supplier_name
-- Column: invoice_amount (NOT amount)
```

---

### 6. AP Payments by Supplier

```sql
SELECT s.supplier_name, SUM(p.payment_amount) AS total_paid
FROM fin_ap_payments p
JOIN sup_suppliers s ON s.supplier_id = p.supplier_id
GROUP BY s.supplier_name
-- fin_ap_payments has NO invoice_id column
```

---

### 7. Budget vs GL Comparison (cross-table — requires CTE or subquery)

```sql
WITH budget AS (
    SELECT cc.cost_centre_name, SUM(bl.amount) AS budget_amount
    FROM fin_budget_lines bl
    JOIN fin_cost_centres cc ON cc.cost_centre_id = bl.cost_centre_id
    JOIN fin_budget_headers bh ON bh.budget_header_id = bl.budget_header_id
    WHERE bh.fiscal_year = 2024
    GROUP BY cc.cost_centre_name
),
actuals AS (
    SELECT cc.cost_centre_name, SUM(gl.period_net) AS actual_amount
    FROM fin_gl_balances gl
    JOIN fin_cost_centres cc ON cc.cost_centre_id = gl.cost_centre_id
    WHERE gl.fiscal_year = 2024
    GROUP BY cc.cost_centre_name
)
SELECT b.cost_centre_name,
       b.budget_amount,
       a.actual_amount,
       a.actual_amount - b.budget_amount AS variance
FROM budget b
LEFT JOIN actuals a ON a.cost_centre_name = b.cost_centre_name
```

---

### 8. Employee → Cost Centre Bridge (via hcm_cost_allocations)

```sql
hcm_assignments a
JOIN hcm_cost_allocations ca ON ca.assignment_id = a.assignment_id
JOIN fin_cost_centres cc     ON cc.cost_centre_id = ca.cost_centre_id
WHERE ca.effective_to IS NULL
```
""")

# ── POTENTIAL DATA ISSUES ─────────────────────────────────────────────────────
w("---")
w()
w("# POTENTIAL DATA ISSUES")
w()
w("## Integrity Check Results")
w()
w("| Check | Orphan Count | Status |")
w("|---|---|---|")
for label, count in checks:
    try:
        n = int(count)
        status = "OK" if n == 0 else "ISSUE"
    except:
        status = "WARN"
    w(f"| {label} | {count} | {status} |")
w()

if zero_tables:
    w("## Tables With Zero Rows")
    w()
    w("| Table | Rows |")
    w("|---|---|")
    for tname, cnt in sorted(zero_tables):
        w(f"| `{tname}` | {cnt} |")
    w()
else:
    w("## Tables With Zero Rows")
    w()
    w("All tables have at least 1 row.")
    w()

w("## Critical Schema Gotchas")
w()
w("""
| Issue | Incorrect Assumption | Correct Fact |
|---|---|---|
| Budget values | `fin_budget_headers.budget_amount` | `fin_budget_lines.amount` |
| GL actuals | `fin_gl_balances.actual_amount` | `fin_gl_balances.period_net` or `end_balance` |
| AP invoice amount column | `fin_ap_invoices.amount` | `fin_ap_invoices.invoice_amount` |
| Cost centre on PO | `proc_po_headers.cost_centre_id` | Does not exist — use `proc_po_distributions.cost_centre_id` |
| PO header from distribution | `proc_po_distributions.po_header_id` | Does not exist — traverse via `proc_po_lines` |
| Salary location | `hcm_persons.salary` | `hcm_assignments.salary` |
| Department on person | `hcm_persons.dept_id` | Does not exist — use `hcm_assignments.dept_id` |
| Payment → Invoice FK | `fin_ap_payments.invoice_id` | Does not exist — join only via `supplier_id` |
| GL budget_amount column | `fin_gl_balances.budget_amount` | Does not exist in this schema |
| GL actual_amount column | `fin_gl_balances.actual_amount` | Does not exist — use `period_net` or `end_balance` |
| fin_budget_lines date | `fin_budget_lines.start_date` | Does not exist — use `period_name` + JOIN to `fin_reporting_periods` |
""")

# ── SQL AGENT RISK AREAS ──────────────────────────────────────────────────────
w("---")
w()
w("# SQL AGENT RISK AREAS")
w()
w("""
| Risk | Root Cause | Fix |
|---|---|---|
| Budget query returns 0 rows | Querying `fin_budget_headers.budget_amount` (budget_version total, not per cost centre) | Always use `fin_budget_lines.amount` |
| GL actual query fails | LLM generates `fin_gl_balances.actual_amount` — column does not exist | Use `period_net` (activity) or `end_balance` (balance) |
| AP invoice query fails | LLM uses `fin_ap_invoices.amount` — column does not exist | Use `invoice_amount` |
| PO spend wrong level | LLM sums `proc_po_headers.total_amount` giving org-level, not dept-level | Must use `proc_po_distributions.amount` |
| No dept-level finance data | LLM joins HCM departments directly to finance tables | Route through `fin_cost_centres.dept_id` |
| Time filter broken | LLM uses `fin_budget_lines.start_date` — column does not exist | Join `fin_budget_lines` to `fin_reporting_periods` via `period_name` |
| Budget vs actual comparison fails | LLM attempts single table join — tables have no common amount columns | Use CTE: budget from `fin_budget_lines`, actuals from `fin_gl_balances` |
| Cross-domain Cartesian explosion | Flat JOIN of 3 domains without aggregation anchor | Use CTEs per domain, then LEFT JOIN on cost_centre_name |
| Supplier name no match | LLM uses exact string match | Use `ILIKE '%%name%%'` |
| Payment not linked to invoice | LLM tries JOIN on invoice_id | `fin_ap_payments` has no `invoice_id`; use `fin_ap_payment_schedules` → `fin_ap_invoices` |
""")

# ── SUMMARY ───────────────────────────────────────────────────────────────────
w("---")
w()
w("# SUMMARY")
w()
w("## Key Tables by Use Case")
w()
w("""
| Use Case | Primary Table | Value Column | Critical Join |
|---|---|---|---|
| Budget by cost centre | `fin_budget_lines` | `amount` | JOIN `fin_budget_headers` (fiscal_year), `fin_cost_centres` |
| GL net activity | `fin_gl_balances` | `period_net` | JOIN `fin_cost_centres` |
| GL closing balance | `fin_gl_balances` | `end_balance` | JOIN `fin_cost_centres` |
| PO spend by dept | `proc_po_distributions` | `amount` | JOIN `proc_po_lines`, `fin_cost_centres`, `hcm_departments` |
| AP invoices | `fin_ap_invoices` | `invoice_amount` | JOIN `sup_suppliers` |
| AP payments | `fin_ap_payments` | `payment_amount` | JOIN `sup_suppliers` |
| Employee salary | `hcm_assignments` | `salary` | JOIN `hcm_departments`, `hcm_persons` |
| Headcount | `hcm_assignments` | COUNT(DISTINCT person_id) | WHERE assignment_status='ACTIVE' |
""")

w()
w("## Mandatory AI SQL Agent Rules")
w()
w("""
1. **NEVER** use `fin_budget_headers.budget_amount` — always `fin_budget_lines.amount`
2. **NEVER** use `fin_gl_balances.actual_amount` — always `period_net` or `end_balance`
3. **NEVER** use `fin_ap_invoices.amount` — always `invoice_amount`
4. **NEVER** put `cost_centre_id` on `proc_po_headers` — it's on `proc_po_distributions`
5. **NEVER** put `po_header_id` on `proc_po_distributions` — traverse via `proc_po_lines`
6. **NEVER** access `fin_budget_lines.start_date` — it doesn't exist; use `period_name`
7. **NEVER** put `dept_id` or `salary` on `hcm_persons` — they're on `hcm_assignments`
8. **ALWAYS** filter headcount with `WHERE assignment_status='ACTIVE'`
9. **ALWAYS** use `ILIKE '%%name%%'` for supplier/department name lookups
10. **ALWAYS** use CTEs for cross-domain queries (HCM + Finance + Procurement)
""")

conn.close()

# Write output
out_lines = "\n".join(out)
with open("database_analysis.md", "w", encoding="utf-8") as f:
    f.write(out_lines)

print(f"Wrote database_analysis.md ({len(out)} lines, {len(out_lines):,} bytes)")
