#!/usr/bin/env python3
"""Generate 4000 rows per table across all 63 tables (~250K total).

Uses psycopg2.extras.execute_values for fast bulk inserts.
Maintains FK integrity by inserting in dependency order.
Run: python database/expand_seed.py
"""

import random
import psycopg2
from psycopg2.extras import execute_values
from datetime import date, timedelta
import time as _time

random.seed(99)
CONN = dict(dbname="oracle_fusion_poc", user="postgres", password="12345", host="localhost")
TARGET = 4000  # rows per table

# ── Name pools ──
FN = ["James","Emma","Oliver","Sophia","William","Ava","Benjamin","Isabella","Lucas","Mia",
      "Henry","Charlotte","Alexander","Amelia","Daniel","Harper","Matthew","Evelyn","Jack","Abigail",
      "Liam","Emily","Noah","Ella","Ethan","Chloe","Mason","Victoria","Logan","Grace",
      "Thomas","Eleanor","Leo","Penelope","Sebastian","Layla","Gabriel","Riley","Adrian","Aria",
      "Caleb","Aurora","Isaac","Savannah","Joshua","Brooklyn","Andrew","Stella","Dylan","Hazel"]
LN = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
      "Anderson","Taylor","Thomas","Jackson","White","Harris","Martin","Thompson","Moore","Young",
      "Allen","King","Wright","Scott","Torres","Hill","Green","Adams","Baker","Nelson",
      "Hall","Rivera","Campbell","Mitchell","Carter","Reed","Phillips","Evans","Turner","Collins"]
NAT = ["British","Irish","Indian","Polish","Nigerian","Pakistani","Chinese","French","German","Italian"]
GRADES = ["G3","G4","G5","G6","G7","G8"]
CITIES = ["London","Manchester","Birmingham","Leeds","Bristol","Edinburgh","Glasgow","Cardiff","Belfast","Liverpool",
          "Sheffield","Oxford","Cambridge","Brighton","Nottingham","York","Bath","Reading","Plymouth","Exeter"]
JOB_TITLES = ["Software Engineer","Senior Developer","Data Analyst","Business Analyst","Project Manager",
              "Financial Analyst","HR Coordinator","Procurement Officer","IT Support","Operations Manager",
              "Marketing Executive","Sales Representative","Legal Counsel","Architect","DevOps Engineer",
              "QA Engineer","UX Designer","Product Manager","Security Analyst","Cloud Engineer"]
COURSES = ["Leadership","Data Analytics","Cloud Architecture","Agile","Financial Reporting","HR Compliance",
           "Procurement","Cybersecurity","PMP","Advanced Excel","Python","ML Basics","Communication","Negotiation"]
PROVIDERS = ["Coursera","LinkedIn Learning","PwC Academy","Internal L&D","Deloitte Academy","CIPD"]
ITEMS = ["Laptop","Monitor","Keyboard","Mouse","Headset","Dock","Webcam","Desk","Chair","Printer",
         "Server","UPS","Switch","Firewall","SSD","RAM","Cable","License","Cloud Credits","Consulting"]
PAY_METHODS = ["BACS","CHAPS","Wire Transfer","Direct Debit"]
GL_DESC = ["Salary accrual","IT expense","Marketing cost","Travel","Consulting","Software","Supplies","Training"]
MONTHS = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

def rd(sy=2023, ey=2025):
    s = date(sy,1,1); e = date(ey,12,31)
    return s + timedelta(days=random.randint(0,(e-s).days))

def bulk(cur, sql, rows, label):
    if not rows: return 0
    t0 = _time.time()
    # Add ON CONFLICT DO NOTHING for tables with unique constraints
    sql_safe = sql.rstrip() 
    if sql_safe.endswith('VALUES %s'):
        sql_safe = sql_safe + ' ON CONFLICT DO NOTHING'
    try:
        execute_values(cur, sql_safe, rows, page_size=500)
    except Exception as e:
        print(f"  ⚠️ {label}: ERROR - {e}")
        return 0
    dt = _time.time() - t0
    print(f"  {label}: {len(rows)} rows ({dt:.1f}s)")
    return len(rows)


def run():
    conn = psycopg2.connect(**CONN)
    conn.autocommit = True
    cur = conn.cursor()
    grand_total = 0

    def get_ids(t, c):
        cur.execute(f"SELECT {c} FROM {t}"); return [r[0] for r in cur.fetchall()]
    def get_max(t, c):
        cur.execute(f"SELECT COALESCE(MAX({c}),0) FROM {t}"); return cur.fetchone()[0]
    def need(t, c):
        existing = len(get_ids(t, c))
        return max(0, TARGET - existing)

    # ══════════════════════════════════════════
    # PHASE 1: Reference / lookup tables
    # ══════════════════════════════════════════
    print("=" * 60)
    print("PHASE 1: Reference tables")
    print("=" * 60)

    # H1: Organizations
    n = need("hcm_organizations", "org_id")
    if n > 0:
        base = get_max("hcm_organizations", "org_id")
        rows = [(f"ORG-{base+i+1:04d}", f"Organization {base+i+1}", random.choice(["OPERATING","HOLDING","SUBSIDIARY"]),
                 f"LE-{(base+i+1)%50+1:03d}") for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_organizations (org_code,org_name,org_type,legal_entity) VALUES %s", rows, "hcm_organizations")

    # H2: Departments
    n = need("hcm_departments", "dept_id")
    org_ids = get_ids("hcm_organizations", "org_id")
    if n > 0:
        base = get_max("hcm_departments", "dept_id")
        dept_names = ["Engineering","Finance","Marketing","HR","Procurement","Sales","Operations","IT","Legal","Executive",
                      "R&D","Customer Support","Quality","Logistics","Strategy","Analytics","Compliance","Risk","Audit","Treasury"]
        rows = [(f"DEPT-{base+i+1:04d}", f"{random.choice(dept_names)} {base+i+1}", random.choice(org_ids)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_departments (dept_code,dept_name,org_id) VALUES %s", rows, "hcm_departments")

    # H3: Locations
    n = need("hcm_locations", "location_id")
    if n > 0:
        base = get_max("hcm_locations", "location_id")
        rows = [(f"LOC-{base+i+1:04d}", f"{random.choice(CITIES)} Office {base+i+1}",
                 f"{random.randint(1,300)} {random.choice(['High St','Park Rd','Mill Lane','King St'])}",
                 random.choice(CITIES), f"{random.choice(['SW','EC','W','N','SE'])}{random.randint(1,20)} {random.randint(1,9)}{random.choice('ABCDEFGH')}{random.choice('ABCDEFGH')}",
                 "United Kingdom") for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_locations (location_code,location_name,address_line1,city,postal_code,country) VALUES %s", rows, "hcm_locations")

    # H4: Jobs
    n = need("hcm_jobs", "job_id")
    if n > 0:
        base = get_max("hcm_jobs", "job_id")
        families = ["ENGINEERING","FINANCE","HR","PROCUREMENT","IT","SALES","OPERATIONS","LEGAL","MARKETING","EXECUTIVE"]
        rows = [(f"JOB-{base+i+1:04d}", f"{random.choice(JOB_TITLES)} {base+i+1}", random.choice(families)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_jobs (job_code,job_name,job_family) VALUES %s", rows, "hcm_jobs")

    # H5: Grades
    n = need("hcm_grades", "grade_id")
    if n > 0:
        base = get_max("hcm_grades", "grade_id")
        rows = [(f"GRD-{base+i+1:04d}", f"Grade Level {base+i+1}", random.randint(25,40)*1000, random.randint(60,120)*1000) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_grades (grade_code,grade_name,min_salary,max_salary) VALUES %s", rows, "hcm_grades")

    # H6: Positions
    n = need("hcm_positions", "position_id")
    dept_ids = get_ids("hcm_departments", "dept_id")
    job_ids = get_ids("hcm_jobs", "job_id")
    grade_ids = get_ids("hcm_grades", "grade_id")
    loc_ids = get_ids("hcm_locations", "location_id")
    if n > 0:
        base = get_max("hcm_positions", "position_id")
        rows = [(f"POS-{base+i+1:04d}", f"{random.choice(JOB_TITLES)} Position {base+i+1}",
                 random.choice(dept_ids), random.choice(job_ids), random.choice(grade_ids),
                 random.choice(loc_ids), random.randint(1,5)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_positions (position_code,position_name,dept_id,job_id,grade_id,location_id,headcount) VALUES %s", rows, "hcm_positions")

    # H12: Termination reasons
    n = need("hcm_termination_reasons", "reason_id")
    if n > 0:
        base = get_max("hcm_termination_reasons", "reason_id")
        reasons = ["Resignation","Retirement","Redundancy","Misconduct","Performance","End of Contract",
                    "Career Change","Relocation","Health","Better Offer"]
        rows = [(f"TR-{base+i+1:04d}", f"{random.choice(reasons)} {base+i+1}", random.choice(["VOLUNTARY","INVOLUNTARY"]),
                 random.random() > 0.4) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_termination_reasons (reason_code,reason_name,reason_category,is_voluntary) VALUES %s", rows, "hcm_termination_reasons")

    # H18: Payroll runs
    n = need("hcm_payroll_runs", "payroll_run_id")
    if n > 0:
        base = get_max("hcm_payroll_runs", "payroll_run_id")
        rows = []
        for i in range(n):
            m = MONTHS[i % 12]; yr = 2023 + i // 12
            gross = random.randint(500,2000)*1000
            ded = int(gross*0.35); net = gross - ded
            rows.append((f"Payroll {m}-{yr} Batch {base+i+1}", f"{m}-{yr}", date(yr,i%12+1,28),
                         gross, ded, net, random.randint(50,300)))
        grand_total += bulk(cur, "INSERT INTO hcm_payroll_runs (run_name,period_name,run_date,total_gross,total_deductions,total_net,employee_count) VALUES %s", rows, "hcm_payroll_runs")

    # Finance reference tables
    # F1: Ledgers
    n = need("fin_ledgers", "ledger_id")
    if n > 0:
        base = get_max("fin_ledgers", "ledger_id")
        rows = [(f"LED-{base+i+1:04d}", f"Ledger {base+i+1}", random.choice(["GBP","USD","EUR"])) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_ledgers (ledger_code,ledger_name,currency) VALUES %s", rows, "fin_ledgers")

    # F2: Chart of accounts
    ledger_ids = get_ids("fin_ledgers", "ledger_id")
    n = need("fin_chart_of_accounts", "coa_id")
    if n > 0:
        base = get_max("fin_chart_of_accounts", "coa_id")
        rows = [(f"COA-{base+i+1:04d}", f"Chart {base+i+1}", random.choice(ledger_ids)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_chart_of_accounts (coa_code,coa_name,ledger_id) VALUES %s", rows, "fin_chart_of_accounts")

    # F3: COA segments
    coa_ids = get_ids("fin_chart_of_accounts", "coa_id")
    n = need("fin_coa_segments", "segment_id")
    if n > 0:
        segs = ["Company","Cost Centre","Account","Project","Intercompany","Future"]
        rows = [(random.choice(coa_ids), random.choice(segs), random.randint(1,6), random.choice(["NATURAL","BALANCING"])) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_coa_segments (coa_id,segment_name,segment_number,segment_type) VALUES %s", rows, "fin_coa_segments")

    # F4: Cost centres
    n = need("fin_cost_centres", "cost_centre_id")
    if n > 0:
        base = get_max("fin_cost_centres", "cost_centre_id")
        names = ["Engineering","Finance","Marketing","HR","Procurement","Sales","Operations","IT","Legal","Executive",
                 "R&D","Support","Quality","Logistics","Strategy","Analytics","Compliance","Risk","Audit","Treasury"]
        rows = [(f"CC{base+i+1:04d}", f"{random.choice(names)} CC{base+i+1}", random.choice(dept_ids)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_cost_centres (cost_centre_code,cost_centre_name,dept_id) VALUES %s", rows, "fin_cost_centres")

    # F5: Account codes
    n = need("fin_account_codes", "account_code_id")
    if n > 0:
        base = get_max("fin_account_codes", "account_code_id")
        types = ["EXPENSE","REVENUE","ASSET","LIABILITY","EQUITY"]
        rows = [(f"{5000+base+i+1}", f"Account {5000+base+i+1}", random.choice(types), random.choice(coa_ids)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_account_codes (account_code,account_name,account_type,coa_id) VALUES %s", rows, "fin_account_codes")

    # F6: Reporting periods
    n = need("fin_reporting_periods", "period_id")
    if n > 0:
        base = get_max("fin_reporting_periods", "period_id")
        rows = []
        for i in range(n):
            yr = 2020 + i // 12; m = i % 12 + 1
            pname = f"{MONTHS[m-1]}-{yr}"
            rows.append((f"{pname}-{base+i+1}", yr, (m-1)//3+1, m, date(yr,m,1), date(yr,m,28)))
        grand_total += bulk(cur, "INSERT INTO fin_reporting_periods (period_name,fiscal_year,fiscal_quarter,period_number,start_date,end_date) VALUES %s", rows, "fin_reporting_periods")

    # F7: Currency rates
    n = need("fin_currency_rates", "rate_id")
    if n > 0:
        pairs = [("GBP","USD"),("GBP","EUR"),("USD","GBP"),("USD","EUR"),("EUR","GBP"),("EUR","USD")]
        rows = [(p[0], p[1], round(random.uniform(0.7,1.5),6), "SPOT", rd()) for p in pairs for _ in range(n//6+1)][:n]
        grand_total += bulk(cur, "INSERT INTO fin_currency_rates (from_currency,to_currency,exchange_rate,rate_type,effective_date) VALUES %s", rows, "fin_currency_rates")

    # F11: Budget versions
    n = need("fin_budget_versions", "budget_version_id")
    if n > 0:
        rows = [(f"Budget {random.choice(['Original','Revised','Forecast'])} v{i+1}",
                 random.choice(["ORIGINAL","REVISED","FORECAST"]), random.randint(2023,2026)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_budget_versions (version_name,version_type,fiscal_year) VALUES %s", rows, "fin_budget_versions")

    # F12: Budget headers
    bv_ids = get_ids("fin_budget_versions", "budget_version_id")
    n = need("fin_budget_headers", "budget_header_id")
    if n > 0:
        rows = [(f"Budget {i+1}", random.choice(ledger_ids), random.choice(bv_ids),
                 random.randint(2023,2026), random.randint(100,5000)*1000) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_budget_headers (budget_name,ledger_id,budget_version_id,fiscal_year,total_amount) VALUES %s", rows, "fin_budget_headers")

    # Suppliers
    n = need("sup_suppliers", "supplier_id")
    if n > 0:
        base = get_max("sup_suppliers", "supplier_id")
        stypes = ["IT_SERVICES","HARDWARE","CONSULTING","FACILITIES","LEGAL","FINANCIAL","MANUFACTURING","LOGISTICS"]
        rows = [(f"SUP-{base+i+1:04d}", f"{random.choice(FN)} {random.choice(LN)} Ltd #{base+i+1}",
                 random.choice(["NET30","NET60","NET90"]), random.choice(stypes),
                 random.choice(["LOW","MEDIUM","HIGH"])) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO sup_suppliers (supplier_number,supplier_name,payment_terms,supplier_type,risk_rating) VALUES %s", rows, "sup_suppliers")

    # AR Customers
    n = need("fin_ar_customers", "customer_id")
    if n > 0:
        base = get_max("fin_ar_customers", "customer_id")
        rows = [(f"CUST-{base+i+1:04d}", f"{random.choice(FN)} {random.choice(LN)} Corp {base+i+1}",
                 random.choice(["CORPORATE","SME","PUBLIC_SECTOR"]), random.choice(["NET30","NET60"]),
                 random.randint(50,2000)*1000) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_ar_customers (customer_number,customer_name,customer_type,payment_terms,credit_limit) VALUES %s", rows, "fin_ar_customers")

    # Proc: Item categories
    n = need("proc_item_categories", "category_id")
    if n > 0:
        base = get_max("proc_item_categories", "category_id")
        cat_names = ["IT Equipment","Office Supplies","Consulting","Software","Hardware","Facilities","Travel","Training"]
        rows = [(f"CAT-{base+i+1:04d}", f"{random.choice(cat_names)} {base+i+1}") for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_item_categories (category_code,category_name) VALUES %s", rows, "proc_item_categories")

    # Proc: Items
    cat_ids = get_ids("proc_item_categories", "category_id")
    n = need("proc_items", "item_id")
    if n > 0:
        base = get_max("proc_items", "item_id")
        rows = [(f"ITM-{base+i+1:05d}", f"{random.choice(ITEMS)} Model-{base+i+1}", "Catalog item",
                 random.choice(cat_ids), round(random.uniform(50,10000),2), random.choice(["GOODS","SERVICES"])) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_items (item_code,item_name,description,category_id,unit_price,item_type) VALUES %s", rows, "proc_items")

    # Refresh all reference IDs
    org_ids = get_ids("hcm_organizations", "org_id")
    dept_ids = get_ids("hcm_departments", "dept_id")
    loc_ids = get_ids("hcm_locations", "location_id")
    job_ids = get_ids("hcm_jobs", "job_id")
    grade_ids = get_ids("hcm_grades", "grade_id")
    position_ids = get_ids("hcm_positions", "position_id")
    cc_ids = get_ids("fin_cost_centres", "cost_centre_id")
    ac_ids = get_ids("fin_account_codes", "account_code_id")
    ledger_ids = get_ids("fin_ledgers", "ledger_id")
    period_ids = get_ids("fin_reporting_periods", "period_id")
    supplier_ids = get_ids("sup_suppliers", "supplier_id")
    customer_ids = get_ids("fin_ar_customers", "customer_id")
    cat_ids = get_ids("proc_item_categories", "category_id")
    item_ids = get_ids("proc_items", "item_id")
    bh_ids = get_ids("fin_budget_headers", "budget_header_id")
    payroll_ids = get_ids("hcm_payroll_runs", "payroll_run_id")
    reason_ids = get_ids("hcm_termination_reasons", "reason_id")

    # ══════════════════════════════════════════
    # PHASE 2: HCM transaction tables
    # ══════════════════════════════════════════
    print("\n" + "=" * 60)
    print("PHASE 2: HCM persons & related")
    print("=" * 60)

    # H7: Persons
    n = need("hcm_persons", "person_id")
    if n > 0:
        rows = [(f"EMP{get_max('hcm_persons','person_id')+i+1:05d}", random.choice(FN), random.choice(LN),
                 rd(1965,2002), random.choice(["M","F"]), random.choice(NAT), "EMPLOYEE",
                 random.choices(["ACTIVE","TERMINATED"], weights=[85,15])[0]) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_persons (person_number,first_name,last_name,date_of_birth,gender,nationality,person_type,status) VALUES %s", rows, "hcm_persons")

    all_pids = get_ids("hcm_persons", "person_id")

    # H8: Person names
    n = need("hcm_person_names", "person_name_id")
    if n > 0:
        rows = [(random.choice(all_pids), "LEGAL", random.choice(FN), random.choice(LN), rd(2020,2025)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_person_names (person_id,name_type,first_name,last_name,effective_from) VALUES %s", rows, "hcm_person_names")

    # H9: Person emails
    n = need("hcm_person_emails", "email_id")
    if n > 0:
        rows = [(random.choice(all_pids), "WORK", f"{random.choice(FN).lower()}.{random.choice(LN).lower()}{random.randint(1,9999)}@company.com", True) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_person_emails (person_id,email_type,email_address,is_primary) VALUES %s", rows, "hcm_person_emails")

    # H10: Assignments
    n = need("hcm_assignments", "assignment_id")
    if n > 0:
        base = get_max("hcm_assignments", "assignment_id")
        rows = [(f"ASG-{base+i+1:05d}", random.choice(all_pids), random.choice(position_ids), random.choice(dept_ids),
                 random.choice(org_ids), random.choice(grade_ids), random.choice(job_ids), random.choice(loc_ids),
                 "PRIMARY", "ACTIVE", "ACTIVE", random.choice(JOB_TITLES), random.randint(25,100)*1000,
                 random.choice(all_pids[:500]), rd(2020,2025)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_assignments (assignment_number,person_id,position_id,dept_id,org_id,grade_id,job_id,location_id,assignment_type,assignment_status,employment_status,job_title,salary,manager_person_id,effective_from) VALUES %s", rows, "hcm_assignments")

    all_aids = get_ids("hcm_assignments", "assignment_id")

    # H11: Employment periods
    n = need("hcm_employment_periods", "employment_period_id")
    if n > 0:
        rows = [(random.choice(all_pids), rd(2018,2025)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_employment_periods (person_id,start_date) VALUES %s", rows, "hcm_employment_periods")

    # H13: Workforce actions
    n = need("hcm_workforce_actions", "action_id")
    if n > 0:
        actions = ["HIRE","PROMOTE","TRANSFER","TERMINATE","REHIRE","REASSIGN"]
        rows = [(random.choice(all_pids), random.choice(all_aids), random.choice(actions),
                 f"{random.choice(actions)} action", rd(2020,2025)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_workforce_actions (person_id,assignment_id,action_type,action_reason,effective_date) VALUES %s", rows, "hcm_workforce_actions")

    # H14: Promotions
    n = need("hcm_promotions", "promotion_id")
    if n > 0:
        rows = [(random.choice(all_aids), rd(2022,2025), random.choice(GRADES), random.choice(GRADES),
                 random.randint(30,60)*1000, random.randint(55,95)*1000) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_promotions (assignment_id,effective_date,old_grade,new_grade,old_salary,new_salary) VALUES %s", rows, "hcm_promotions")

    # H15: Transfers
    n = need("hcm_transfers", "transfer_id")
    if n > 0:
        rows = [(random.choice(all_aids), rd(2022,2025), random.choice(dept_ids), random.choice(dept_ids),
                 random.choice(loc_ids), random.choice(loc_ids)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_transfers (assignment_id,effective_date,from_dept_id,to_dept_id,from_location_id,to_location_id) VALUES %s", rows, "hcm_transfers")

    # H16: Salary history
    n = need("hcm_salary_history", "salary_history_id")
    if n > 0:
        rows = [(random.choice(all_aids), random.randint(25,60)*1000, random.randint(55,100)*1000,
                 random.choice(["Annual Review","Promotion","Market Adj"]), rd(2022,2025)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_salary_history (assignment_id,old_salary,new_salary,change_reason,effective_date) VALUES %s", rows, "hcm_salary_history")

    # H17: Compensation elements
    n = need("hcm_compensation_elements", "element_id")
    if n > 0:
        etypes = ["BASE_SALARY","BONUS","ALLOWANCE","OVERTIME","COMMISSION"]
        rows = [(random.choice(all_aids), random.choice(etypes), random.choice(etypes).replace("_"," ").title(),
                 random.randint(1,20)*1000, "MONTHLY", rd(2022,2025)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_compensation_elements (assignment_id,element_type,element_name,amount,frequency,effective_from) VALUES %s", rows, "hcm_compensation_elements")

    # H19: Payroll results
    n = need("hcm_payroll_results", "result_id")
    if n > 0:
        rows = []
        for _ in range(n):
            g = random.randint(2000,9000); t = int(g*.2); ni = int(g*.12); p = int(g*.05)
            rows.append((random.choice(payroll_ids), random.choice(all_aids), g, t, ni, p, g-t-ni-p))
        grand_total += bulk(cur, "INSERT INTO hcm_payroll_results (payroll_run_id,assignment_id,gross_pay,tax_deducted,ni_deducted,pension_deducted,net_pay) VALUES %s", rows, "hcm_payroll_results")

    # H20: Cost allocations
    n = need("hcm_cost_allocations", "allocation_id")
    if n > 0:
        rows = [(random.choice(all_aids), random.choice(cc_ids), 100.00, rd(2022,2025)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_cost_allocations (assignment_id,cost_centre_id,allocation_pct,effective_from) VALUES %s", rows, "hcm_cost_allocations")

    # H21: Performance reviews
    n = need("hcm_performance_reviews", "review_id")
    if n > 0:
        rows = [(random.choice(all_pids), random.choice(all_pids[:200]), random.choice(["FY2023","FY2024","FY2025"]),
                 random.choice(["EXCEEDS","MEETS","BELOW","OUTSTANDING"]), round(random.uniform(1.5,5.0),1),
                 random.randint(30,100), rd(2023,2025)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_performance_reviews (person_id,reviewer_person_id,review_period,overall_rating,rating_score,goals_met_pct,review_date) VALUES %s", rows, "hcm_performance_reviews")

    # H22: Training records
    n = need("hcm_training_records", "training_id")
    if n > 0:
        rows = [(random.choice(all_pids), random.choice(COURSES), random.choice(PROVIDERS),
                 rd(2023,2025), random.randint(50,100), f"CERT-{random.randint(10000,99999)}") for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO hcm_training_records (person_id,course_name,provider,completion_date,score,certificate_id) VALUES %s", rows, "hcm_training_records")

    # ══════════════════════════════════════════
    # PHASE 3: Finance transaction tables
    # ══════════════════════════════════════════
    print("\n" + "=" * 60)
    print("PHASE 3: Finance transactions")
    print("=" * 60)

    # F8: GL journal headers
    n = need("fin_gl_journal_headers", "journal_header_id")
    if n > 0:
        base = get_max("fin_gl_journal_headers", "journal_header_id")
        rows = [(f"JNL-{base+i+1:06d}", random.choice(ledger_ids), random.choice(period_ids), rd(2023,2025),
                 random.choice(["Manual","Subledger","Spreadsheet"]), random.choice(["Adjustment","Accrual","Reclass"]),
                 random.randint(5,500)*1000, random.randint(5,500)*1000, random.choice(all_pids[:100])) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_gl_journal_headers (journal_number,ledger_id,period_id,journal_date,journal_source,journal_category,total_debit,total_credit,created_by) VALUES %s", rows, "fin_gl_journal_headers")

    jh_ids = get_ids("fin_gl_journal_headers", "journal_header_id")

    # F9: GL journal lines
    n = need("fin_gl_journal_lines", "journal_line_id")
    if n > 0:
        rows = [(random.choice(jh_ids), random.randint(1,5), random.choice(ac_ids), random.choice(cc_ids),
                 random.randint(1,200)*1000, random.randint(0,50)*1000, random.choice(GL_DESC)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_gl_journal_lines (journal_header_id,line_number,account_code_id,cost_centre_id,debit_amount,credit_amount,description) VALUES %s", rows, "fin_gl_journal_lines")

    # F10: GL balances
    n = need("fin_gl_balances", "balance_id")
    if n > 0:
        rows = []
        for _ in range(n):
            m = random.choice(MONTHS); yr = random.randint(2023,2026)
            actual = random.randint(10,500)*1000; budget = random.randint(10,500)*1000
            rows.append((random.choice(cc_ids), random.choice(ac_ids), f"{m}-{yr}", yr, (MONTHS.index(m))//3+1,
                         actual, int(actual*0.4), actual, budget, int(actual*0.9)))
        grand_total += bulk(cur, "INSERT INTO fin_gl_balances (cost_centre_id,account_code_id,period_name,fiscal_year,fiscal_quarter,period_debit,period_credit,end_balance,budget_amount,actual_amount) VALUES %s", rows, "fin_gl_balances")

    # F13: Budget lines
    n = need("fin_budget_lines", "budget_line_id")
    if n > 0:
        rows = [(random.choice(bh_ids), random.choice(cc_ids), random.choice(ac_ids),
                 f"{random.choice(MONTHS)}-{random.randint(2023,2026)}", random.randint(10,500)*1000) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_budget_lines (budget_header_id,cost_centre_id,account_code_id,period_name,amount) VALUES %s", rows, "fin_budget_lines")

    # Supplier sites
    n = need("sup_supplier_sites", "site_id")
    if n > 0:
        rows = [(random.choice(supplier_ids), f"SITE-{random.randint(1,99999):05d}", f"Site {random.randint(1,9999)}",
                 f"{random.randint(1,300)} High St", random.choice(CITIES), random.random()>0.7) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO sup_supplier_sites (supplier_id,site_code,site_name,address_line1,city,is_primary) VALUES %s", rows, "sup_supplier_sites")

    # Supplier contacts
    n = need("sup_supplier_contacts", "contact_id")
    if n > 0:
        rows = [(random.choice(supplier_ids), f"{random.choice(FN)} {random.choice(LN)}",
                 f"c{random.randint(1,99999)}@supplier.com", f"+44 7{random.randint(100,999)} {random.randint(100000,999999)}",
                 random.random()>0.8) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO sup_supplier_contacts (supplier_id,contact_name,email,phone,is_primary) VALUES %s", rows, "sup_supplier_contacts")

    # F14-F18: AP invoices, lines, distributions, payments, schedules
    n = need("fin_ap_invoices", "invoice_id")
    if n > 0:
        base = get_max("fin_ap_invoices", "invoice_id")
        rows = []
        for i in range(n):
            amt = random.randint(1,300)*1000; paid = amt if random.random()<0.5 else 0
            idate = rd(2023,2025); ddate = idate + timedelta(days=random.choice([30,60,90]))
            rows.append((f"INV-B{base+i+1:06d}", random.choice(supplier_ids), random.choice(ledger_ids),
                         idate, ddate, amt, paid, amt-paid,
                         "PAID" if paid==amt else random.choice(["PENDING","APPROVED","OVERDUE"]),
                         random.choice(all_pids[:100])))
        grand_total += bulk(cur, "INSERT INTO fin_ap_invoices (invoice_number,supplier_id,ledger_id,invoice_date,due_date,invoice_amount,paid_amount,outstanding_amount,status,created_by) VALUES %s", rows, "fin_ap_invoices")

    inv_ids = get_ids("fin_ap_invoices", "invoice_id")

    n = need("fin_ap_invoice_lines", "invoice_line_id")
    if n > 0:
        rows = [(random.choice(inv_ids), random.randint(1,5), random.choice(ITEMS),
                 random.randint(1,50), round(random.uniform(100,10000),2), random.randint(1,100)*1000) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_ap_invoice_lines (invoice_id,line_number,description,quantity,unit_price,line_amount) VALUES %s", rows, "fin_ap_invoice_lines")

    il_ids = get_ids("fin_ap_invoice_lines", "invoice_line_id")

    n = need("fin_ap_invoice_distributions", "distribution_id")
    if n > 0:
        rows = [(random.choice(il_ids), random.choice(cc_ids), random.choice(ac_ids), random.randint(1,100)*1000) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_ap_invoice_distributions (invoice_line_id,cost_centre_id,account_code_id,amount) VALUES %s", rows, "fin_ap_invoice_distributions")

    n = need("fin_ap_payment_schedules", "schedule_id")
    if n > 0:
        rows = [(random.choice(inv_ids), random.randint(1,3), rd(2024,2026), random.randint(5,200)*1000,
                 random.randint(0,200)*1000, random.choice(["OPEN","PAID"])) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_ap_payment_schedules (invoice_id,installment_num,due_date,amount_due,amount_paid,status) VALUES %s", rows, "fin_ap_payment_schedules")

    n = need("fin_ap_payments", "payment_id")
    if n > 0:
        base = get_max("fin_ap_payments", "payment_id")
        rows = [(f"PAY-B{base+i+1:06d}", random.choice(supplier_ids), rd(2023,2025),
                 random.randint(1,300)*1000, random.choice(PAY_METHODS)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_ap_payments (payment_number,supplier_id,payment_date,payment_amount,payment_method) VALUES %s", rows, "fin_ap_payments")

    # F20-F21: AR invoices + receipts
    n = need("fin_ar_invoices", "ar_invoice_id")
    if n > 0:
        base = get_max("fin_ar_invoices", "ar_invoice_id")
        rows = []
        for i in range(n):
            amt = random.randint(5,500)*1000; paid = amt if random.random()<0.6 else random.randint(0,int(amt*0.8))
            rows.append((f"AR-B{base+i+1:06d}", random.choice(customer_ids), rd(2023,2025), rd(2024,2026),
                         amt, paid, amt-paid, "CLOSED" if paid==amt else "OPEN"))
        grand_total += bulk(cur, "INSERT INTO fin_ar_invoices (invoice_number,customer_id,invoice_date,due_date,invoice_amount,paid_amount,outstanding,status) VALUES %s", rows, "fin_ar_invoices")

    ar_ids = get_ids("fin_ar_invoices", "ar_invoice_id")

    n = need("fin_ar_receipts", "receipt_id")
    if n > 0:
        base = get_max("fin_ar_receipts", "receipt_id")
        rows = [(f"RCT-B{base+i+1:06d}", random.choice(ar_ids), rd(2024,2026),
                 random.randint(5,300)*1000, random.choice(PAY_METHODS)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO fin_ar_receipts (receipt_number,ar_invoice_id,receipt_date,receipt_amount,payment_method) VALUES %s", rows, "fin_ar_receipts")

    # ══════════════════════════════════════════
    # PHASE 4: Procurement transaction tables
    # ══════════════════════════════════════════
    print("\n" + "=" * 60)
    print("PHASE 4: Procurement transactions")
    print("=" * 60)

    # P3: Requisition headers
    n = need("proc_requisition_headers", "requisition_id")
    if n > 0:
        base = get_max("proc_requisition_headers", "requisition_id")
        rows = [(f"REQ-B{base+i+1:06d}", random.choice(all_pids[:500]), random.choice(dept_ids),
                 f"Req for {random.choice(ITEMS)}", random.randint(5,200)*1000,
                 random.choice(["APPROVED","PENDING","REJECTED"]), rd(2023,2025)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_requisition_headers (requisition_number,requester_id,dept_id,description,total_amount,status,submitted_date) VALUES %s", rows, "proc_requisition_headers")

    req_ids = get_ids("proc_requisition_headers", "requisition_id")

    # P4: Requisition lines
    n = need("proc_requisition_lines", "req_line_id")
    if n > 0:
        rows = [(random.choice(req_ids), random.randint(1,5), random.choice(item_ids), random.choice(ITEMS),
                 random.randint(1,50), round(random.uniform(50,5000),2), random.randint(1,100)*1000, rd(2024,2026)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_requisition_lines (requisition_id,line_number,item_id,description,quantity,unit_price,line_amount,need_by_date) VALUES %s", rows, "proc_requisition_lines")

    rl_ids = get_ids("proc_requisition_lines", "req_line_id")

    # P5: Requisition distributions
    n = need("proc_requisition_distributions", "req_dist_id")
    if n > 0:
        rows = [(random.choice(rl_ids), random.choice(cc_ids), random.choice(ac_ids), random.randint(1,100)*1000) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_requisition_distributions (req_line_id,cost_centre_id,account_code_id,amount) VALUES %s", rows, "proc_requisition_distributions")

    # P6: Quotation headers
    n = need("proc_quotation_headers", "quotation_header_id")
    if n > 0:
        base = get_max("proc_quotation_headers", "quotation_header_id")
        rows = []
        for i in range(n):
            orig = random.randint(10,500)*1000; rev = int(orig*random.uniform(0.9,1.2))
            rows.append((f"QH-B{base+i+1:06d}", f"E-{1000+i}", f"Engagement {1000+i}",
                         random.choice(supplier_ids), orig, rev,
                         random.choice(["SUBMITTED","APPROVED","REJECTED"]),
                         random.choice(["IT","CONSULTING","FACILITIES"])))
        grand_total += bulk(cur, "INSERT INTO proc_quotation_headers (quotation_number,engagement_id,engagement_name,supplier_id,original_amount,revised_amount,status,category) VALUES %s", rows, "proc_quotation_headers")

    qh_ids = get_ids("proc_quotation_headers", "quotation_header_id")

    # P7: Quotation lines
    n = need("proc_quotation_lines", "quot_line_id")
    if n > 0:
        rows = [(random.choice(qh_ids), random.randint(1,5), random.choice(item_ids), random.choice(ITEMS),
                 random.randint(1,50), round(random.uniform(100,10000),2), random.randint(1,200)*1000) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_quotation_lines (quotation_header_id,line_number,item_id,description,quantity,unit_price,line_amount) VALUES %s", rows, "proc_quotation_lines")

    # P8: Quote versions
    n = need("proc_quote_versions", "version_id")
    if n > 0:
        rows = [(random.choice(qh_ids), random.randint(1,3), random.randint(10,500)*1000, rd(2023,2025),
                 random.choice(["SUBMITTED","APPROVED","REJECTED"])) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_quote_versions (quotation_header_id,version_number,version_amount,submitted_date,status) VALUES %s", rows, "proc_quote_versions")

    # P9: PO headers
    n = need("proc_po_headers", "po_header_id")
    if n > 0:
        base = get_max("proc_po_headers", "po_header_id")
        rows = []
        for i in range(n):
            tot = random.randint(5,500)*1000; app = tot if random.random()<0.6 else 0
            rows.append((f"PO-B{base+i+1:06d}", random.choice(supplier_ids), random.choice(all_pids[:100]),
                         tot, app, random.choice(["APPROVED","PENDING","REJECTED"]),
                         rd(2023,2025), random.choice(["IT","FACILITIES","CONSULTING","HARDWARE"])))
        grand_total += bulk(cur, "INSERT INTO proc_po_headers (po_number,supplier_id,buyer_id,total_amount,approved_amount,status,created_date,category) VALUES %s", rows, "proc_po_headers")

    po_ids = get_ids("proc_po_headers", "po_header_id")

    # P10: PO lines
    n = need("proc_po_lines", "po_line_id")
    if n > 0:
        rows = [(random.choice(po_ids), random.randint(1,5), random.choice(item_ids), random.choice(ITEMS),
                 random.randint(1,100), round(random.uniform(50,5000),2), random.randint(1,200)*1000) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_po_lines (po_header_id,line_number,item_id,description,quantity,unit_price,line_amount) VALUES %s", rows, "proc_po_lines")

    pol_ids = get_ids("proc_po_lines", "po_line_id")

    # P11: PO distributions
    n = need("proc_po_distributions", "po_dist_id")
    if n > 0:
        rows = [(random.choice(pol_ids), random.choice(cc_ids), random.choice(ac_ids), 100.00, random.randint(1,200)*1000) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_po_distributions (po_line_id,cost_centre_id,account_code_id,distribution_pct,amount) VALUES %s", rows, "proc_po_distributions")

    # P12: PO approvals
    n = need("proc_po_approvals", "approval_id")
    if n > 0:
        rows = [(random.choice(po_ids), random.choice(all_pids[:100]), random.randint(1,3),
                 random.choice(["APPROVED","PENDING","REJECTED"]), rd(2023,2025)) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_po_approvals (po_header_id,approver_id,approval_level,action,action_date) VALUES %s", rows, "proc_po_approvals")

    # P13: Receipt headers
    n = need("proc_receipt_headers", "receipt_header_id")
    if n > 0:
        base = get_max("proc_receipt_headers", "receipt_header_id")
        rows = [(f"RCV-B{base+i+1:06d}", random.choice(po_ids), random.choice(all_pids[:100]), rd(2024,2026)) for i in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_receipt_headers (receipt_number,po_header_id,received_by,receipt_date) VALUES %s", rows, "proc_receipt_headers")

    rh_ids = get_ids("proc_receipt_headers", "receipt_header_id")

    # P14: Receipt lines
    n = need("proc_receipt_lines", "receipt_line_id")
    if n > 0:
        rows = [(random.choice(rh_ids), random.choice(pol_ids), random.randint(1,100),
                 random.randint(1,100), random.randint(0,5), random.choice(["ACCEPTED","REJECTED","PENDING"])) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_receipt_lines (receipt_header_id,po_line_id,quantity_received,quantity_accepted,quantity_rejected,inspection_status) VALUES %s", rows, "proc_receipt_lines")

    # P15: Contract headers
    n = need("proc_contract_headers", "contract_header_id")
    if n > 0:
        base = get_max("proc_contract_headers", "contract_header_id")
        rows = []
        for i in range(n):
            tv = random.randint(50,2000)*1000; rel = int(tv*random.uniform(0.1,0.9)); s = rd(2023,2025)
            rows.append((f"CON-B{base+i+1:06d}", random.choice(supplier_ids), random.choice(["BLANKET","STANDARD"]),
                         s, s+timedelta(days=random.randint(180,730)), tv, rel,
                         random.choice(["ACTIVE","CLOSED","DRAFT"])))
        grand_total += bulk(cur, "INSERT INTO proc_contract_headers (contract_number,supplier_id,contract_type,start_date,end_date,total_value,released_amount,status) VALUES %s", rows, "proc_contract_headers")

    ch_ids = get_ids("proc_contract_headers", "contract_header_id")

    # P16: Contract lines
    n = need("proc_contract_lines", "contract_line_id")
    if n > 0:
        rows = [(random.choice(ch_ids), random.randint(1,5), random.choice(item_ids), random.choice(ITEMS),
                 random.randint(1,200), round(random.uniform(100,5000),2),
                 random.randint(10,500)*1000, random.randint(5,300)*1000) for _ in range(n)]
        grand_total += bulk(cur, "INSERT INTO proc_contract_lines (contract_header_id,line_number,item_id,description,quantity,unit_price,line_amount,released_amount) VALUES %s", rows, "proc_contract_lines")

    # ══════════════════════════════════════════
    # SUMMARY
    # ══════════════════════════════════════════
    print("\n" + "=" * 60)
    print(f"  GRAND TOTAL INSERTED: {grand_total:,} rows")
    print("=" * 60)

    # Show per-table counts
    cur.execute("""
        SELECT relname, n_live_tup::int
        FROM pg_stat_user_tables
        WHERE schemaname='public' AND relname NOT IN ('schema_embeddings','ai_query_log')
        ORDER BY relname
    """)
    print("\nPer-table counts:")
    for name, cnt in cur.fetchall():
        marker = " ✅" if cnt >= TARGET else f" ⚠️ ({cnt})"
        print(f"  {name}: {cnt:,}{marker}")

    cur.close()
    conn.close()
    print(f"\nDone! ✅  ({grand_total:,} rows across all tables)")


if __name__ == "__main__":
    t0 = _time.time()
    run()
    print(f"Total time: {_time.time()-t0:.1f}s")
