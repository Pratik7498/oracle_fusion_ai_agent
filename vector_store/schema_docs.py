"""Schema documentation for vector embedding — used by PGVector RAG retrieval.
Covers the full 63-table Oracle Fusion ERP schema + 3 legacy views.
"""

SCHEMA_DOCS: list[dict] = [
    # ================================================================
    # HCM DOMAIN
    # ================================================================
    {
        "doc_id": "hcm_employees_view",
        "domain": "HCM",
        "title": "HCM Employees View — hcm_employees",
        "content": (
            "View: hcm_employees (legacy-compatible view joining persons + assignments)\n"
            "Exposes employee data including active and terminated staff.\n"
            "Built from: hcm_persons, hcm_person_names, hcm_person_emails, hcm_assignments, "
            "hcm_employment_periods, hcm_departments, hcm_grades, hcm_locations\n\n"
            "Columns:\n"
            "- employee_id: person_id, unique identifier\n"
            "- full_name: first + last name\n"
            "- department: from hcm_departments via assignment\n"
            "- job_title: from assignment\n"
            "- grade_level: grade code, G3(junior) to G8(director)\n"
            "- salary: annual salary GBP from assignment\n"
            "- hire_date: employment period start\n"
            "- termination_date: NULL for active, populated for leavers\n"
            "- employment_status: 'ACTIVE' or 'TERMINATED'\n"
            "- location: London, Manchester, Birmingham, Remote\n"
            "- manager_id: manager person_id\n\n"
            "Key filters:\n"
            "- Active: WHERE employment_status = 'ACTIVE'\n"
            "- Engineering headcount: SELECT COUNT(*) FROM hcm_employees "
            "WHERE department='Engineering' AND employment_status='ACTIVE' -- returns 47\n\n"
            "Example queries:\n"
            "Q: \"How many employees are in Engineering?\"\n"
            "A: SELECT department, COUNT(*) as headcount FROM hcm_employees "
            "WHERE employment_status='ACTIVE' GROUP BY department ORDER BY headcount DESC\n\n"
            "Q: \"List employees in Finance above Grade 5\"\n"
            "A: SELECT full_name, job_title, grade_level, salary FROM hcm_employees "
            "WHERE department='Finance' AND employment_status='ACTIVE' "
            "AND grade_level IN ('G6','G7','G8') ORDER BY grade_level DESC"
        ),
    },
    {
        "doc_id": "hcm_persons_table",
        "domain": "HCM",
        "title": "HCM Persons — Core Identity Table",
        "content": (
            "Table: hcm_persons\n"
            "Core identity record. No org/job/department context — that lives in hcm_assignments.\n"
            "Columns: person_id PK, person_number UNIQUE, first_name, last_name, "
            "date_of_birth, gender, nationality, person_type, status\n"
            "80 persons total (60 active, 20 terminated)\n\n"
            "Related tables:\n"
            "- hcm_person_names: historical name records (name_type, effective_from/to)\n"
            "- hcm_person_emails: email addresses (email_type, is_primary)\n"
            "- hcm_assignments: org context (position, dept, grade, job, salary)\n"
            "- hcm_employment_periods: hire/terminate date spans"
        ),
    },
    {
        "doc_id": "hcm_assignments_table",
        "domain": "HCM",
        "title": "HCM Assignments — Position & Org Context",
        "content": (
            "Table: hcm_assignments\n"
            "Assignment-based modeling: ALL org context lives here, NOT on persons.\n"
            "Columns: assignment_id PK, assignment_number, person_id FK, position_id FK, "
            "dept_id FK, org_id FK, grade_id FK, job_id FK, location_id FK, "
            "assignment_type (PRIMARY), assignment_status (ACTIVE/INACTIVE), "
            "employment_status, job_title, salary, manager_person_id FK, "
            "effective_from, effective_to\n\n"
            "Key: To get current employee info, filter:\n"
            "WHERE assignment_type='PRIMARY' AND assignment_status='ACTIVE'\n\n"
            "Example: SELECT p.first_name, p.last_name, a.job_title, a.salary, "
            "d.dept_name FROM hcm_assignments a JOIN hcm_persons p ON p.person_id=a.person_id "
            "JOIN hcm_departments d ON d.dept_id=a.dept_id "
            "WHERE a.assignment_status='ACTIVE'"
        ),
    },
    {
        "doc_id": "hcm_org_structure",
        "domain": "HCM",
        "title": "HCM Organization Structure — Departments, Positions, Jobs, Grades",
        "content": (
            "Organization hierarchy tables:\n\n"
            "hcm_organizations: Business units (org_id PK, org_code, org_name, org_type, parent_org_id self-ref)\n"
            "hcm_departments: 10 departments (Engineering, Finance, HR, Procurement, Marketing, Sales, Operations, IT, Legal, Executive). "
            "dept_id PK, dept_code D001-D010, dept_name, org_id FK, cost_centre_code\n"
            "hcm_locations: 4 locations (London HQ, Manchester, Birmingham, Remote). location_id PK, location_code LOC001-LOC004\n"
            "hcm_jobs: 20 job definitions (job_id PK, job_code, job_name, job_family, job_level)\n"
            "hcm_positions: Position slots (position_id PK, dept_id FK, job_id FK, location_id FK, grade_id FK)\n"
            "hcm_grades: 6 grades G3-G8 (grade_id PK, grade_code, min/mid/max salary)\n\n"
            "Example: SELECT d.dept_name, COUNT(a.assignment_id) as headcount "
            "FROM hcm_departments d LEFT JOIN hcm_assignments a ON a.dept_id=d.dept_id "
            "AND a.assignment_status='ACTIVE' GROUP BY d.dept_name"
        ),
    },
    {
        "doc_id": "hcm_attrition_calc",
        "domain": "HCM",
        "title": "HCM Attrition Rate Calculation",
        "content": (
            "Attrition rate = (terminated_count / average_headcount) * 100\n"
            "average_headcount = (start_headcount + end_headcount) / 2\n\n"
            "SQL for terminated in date range:\n"
            "SELECT COUNT(*) FROM hcm_employees WHERE employment_status='TERMINATED' "
            "AND termination_date BETWEEN '2025-01-01' AND '2025-12-31'\n\n"
            "IMPORTANT: Percentage calculation done in Python Pandas, not SQL.\n"
            "SQL retrieves raw counts only.\n"
            "For YTD: termination_date >= DATE_TRUNC('year', CURRENT_DATE)"
        ),
    },
    {
        "doc_id": "hcm_compensation_payroll",
        "domain": "HCM",
        "title": "HCM Compensation, Salary History & Payroll",
        "content": (
            "Tables for pay management:\n\n"
            "hcm_salary_history: assignment_id FK, old_salary, new_salary, change_reason, effective_date\n"
            "hcm_compensation_elements: assignment_id FK, element_type (BASE_SALARY/BONUS), amount, frequency\n"
            "hcm_payroll_runs: payroll_run_id PK, period_name (JAN-2025 etc), total_gross/deductions/net\n"
            "hcm_payroll_results: assignment_id FK, payroll_run_id FK, gross_pay, tax/NI/pension deducted, net_pay\n"
            "hcm_cost_allocations: assignment_id FK, cost_centre_id FK→fin_cost_centres (CROSS-DOMAIN)\n\n"
            "Example: SELECT pr.period_name, SUM(pr2.gross_pay) as total_gross "
            "FROM hcm_payroll_runs pr JOIN hcm_payroll_results pr2 ON pr.payroll_run_id=pr2.payroll_run_id "
            "GROUP BY pr.period_name"
        ),
    },
    {
        "doc_id": "hcm_workforce_talent",
        "domain": "HCM",
        "title": "HCM Workforce Actions, Performance & Training",
        "content": (
            "Lifecycle and talent tables:\n\n"
            "hcm_employment_periods: person_id FK, start_date, end_date, status\n"
            "hcm_workforce_actions: person_id FK, assignment_id FK, action_type (HIRE/TERMINATE/PROMOTE/TRANSFER)\n"
            "hcm_termination_reasons: reason_code, reason_name, is_voluntary\n"
            "hcm_promotions: assignment_id FK, old/new grade, old/new salary, effective_date\n"
            "hcm_transfers: assignment_id FK, from/to dept_id, from/to location_id\n"
            "hcm_performance_reviews: person_id FK, review_period, overall_rating, rating_score, goals_met_pct\n"
            "hcm_training_records: person_id FK, course_name, provider, score, certificate_id\n\n"
            "Example: SELECT p.first_name||' '||p.last_name as name, pr.overall_rating, pr.rating_score "
            "FROM hcm_performance_reviews pr JOIN hcm_persons p ON p.person_id=pr.person_id "
            "WHERE pr.review_period='FY2025' ORDER BY pr.rating_score DESC"
        ),
    },

    # ================================================================
    # FINANCE DOMAIN
    # ================================================================
    {
        "doc_id": "fin_gl_balances_table",
        "domain": "FINANCE",
        "title": "Finance GL Balances — fin_gl_balances and finance_gl_balances view",
        "content": (
            "Table: fin_gl_balances (base table)\n"
            "GL summary balances by cost centre, account, and period.\n"
            "Columns: balance_id PK (INTEGER, 1-130), cost_centre_id FK, "
            "account_code_id FK, period_name (JAN-2025 format), "
            "fiscal_year, fiscal_quarter, actual_amount NUMERIC (actual spend GBP), "
            "budget_amount NUMERIC (planned budget GBP), "
            "period_debit, period_credit, period_net, begin_balance, end_balance, currency\n\n"
            "View: finance_gl_balances (PREFERRED for querying — flat, no JOINs needed)\n"
            "Columns: balance_id, cost_centre (CC001-CC010), cost_centre_name, "
            "account_code, account_name, period_name, actual_amount, budget_amount, "
            "fiscal_year, fiscal_quarter, currency\n\n"
            "130 rows: 10 cost centres × 13 periods (JAN-2025 to JAN-2026)\n"
            "balance_id 1-13 = CC001 Engineering, 14-26 = CC002 Finance, "
            "27-39 = CC003 Marketing, 40-52 = CC004 HR, 53-65 = CC005 Procurement, "
            "66-78 = CC006 Sales, 79-91 = CC007 Operations, 92-104 = CC008 IT, "
            "105-117 = CC009 Legal, 118-130 = CC010 Executive\n"
            "CC003 Marketing is OVER BUDGET in Q4 2025\n\n"
            "IMPORTANT: When users say 'invoice id' or 'id' and ask about 'actual vs budget' or "
            "'percentage difference between actual and budget', they mean balance_id in THIS table "
            "(finance_gl_balances), NOT invoice_id in fin_ap_invoices. AP invoices have NO budget column.\n\n"
            "Variance = actual_amount - budget_amount (positive = over budget)\n\n"
            "Example queries:\n"
            "Q: \"What is the percentage difference between actual and budget for balance_id 38-47?\"\n"
            "A: SELECT balance_id, cost_centre_name, period_name, actual_amount, budget_amount, "
            "ROUND(((actual_amount - budget_amount) / NULLIF(budget_amount,0)) * 100, 2) as pct_variance "
            "FROM finance_gl_balances WHERE balance_id BETWEEN 38 AND 47\n\n"
            "Q: \"Which departments are over budget this quarter?\"\n"
            "A: SELECT cost_centre_name, SUM(actual_amount) as actual, SUM(budget_amount) as budget, "
            "SUM(actual_amount - budget_amount) as variance FROM finance_gl_balances "
            "WHERE fiscal_year=2025 AND fiscal_quarter=4 GROUP BY cost_centre, cost_centre_name "
            "HAVING SUM(actual_amount) > SUM(budget_amount) ORDER BY variance DESC\n\n"
            "Q: \"What is the GL balance for CC003?\"\n"
            "A: SELECT period_name, actual_amount, budget_amount, (actual_amount-budget_amount) as variance "
            "FROM finance_gl_balances WHERE cost_centre='CC003' ORDER BY period_name"
        ),
    },
    {
        "doc_id": "fin_gl_journals",
        "domain": "FINANCE",
        "title": "Finance GL Journals — Headers & Lines",
        "content": (
            "GL Journal tables (ledger-driven):\n\n"
            "fin_ledgers: ledger_id PK, ledger_code, ledger_name, currency\n"
            "fin_chart_of_accounts: coa_id PK, coa_code, ledger_id FK\n"
            "fin_coa_segments: segment_id PK, coa_id FK, segment_name (Company/Cost Centre/Account/Project)\n"
            "fin_account_codes: account_code_id PK, account_code (5001-5010=Expense, 4001-4002=Revenue, "
            "1001-1002=Asset, 2001-2002=Liability), coa_id FK\n"
            "fin_cost_centres: cost_centre_id PK, cost_centre_code CC001-CC010, dept_id FK→hcm_departments\n"
            "fin_reporting_periods: period_id PK, period_name, fiscal_year, quarter, start/end_date\n"
            "fin_currency_rates: exchange rates (GBP/USD/EUR)\n\n"
            "fin_gl_journal_headers: journal_header_id PK, journal_number, ledger_id FK, period_id FK, "
            "total_debit, total_credit, status, created_by FK→hcm_persons\n"
            "fin_gl_journal_lines: journal_line_id PK, journal_header_id FK, account_code_id FK, "
            "cost_centre_id FK, debit_amount, credit_amount"
        ),
    },
    {
        "doc_id": "fin_budgets",
        "domain": "FINANCE",
        "title": "Finance Budgets — Version-controlled Budget Management",
        "content": (
            "Budget tables:\n\n"
            "fin_budget_versions: version control (ORIGINAL, REVISED, FORECAST) per fiscal year\n"
            "fin_budget_headers: budget_header_id PK, budget_name, ledger_id FK, budget_version_id FK, fiscal_year\n"
            "fin_budget_lines: budget_line_id PK, budget_header_id FK, cost_centre_id FK, "
            "account_code_id FK, period_name, amount\n\n"
            "Budget is at COST CENTRE + ACCOUNT CODE level per period.\n\n"
            "Example: SELECT cc.cost_centre_name, SUM(bl.amount) as budget_total "
            "FROM fin_budget_lines bl JOIN fin_cost_centres cc ON cc.cost_centre_id=bl.cost_centre_id "
            "JOIN fin_budget_headers bh ON bh.budget_header_id=bl.budget_header_id "
            "WHERE bh.fiscal_year=2025 GROUP BY cc.cost_centre_name"
        ),
    },
    {
        "doc_id": "fin_ap_invoices_table",
        "domain": "FINANCE",
        "title": "Finance AP Invoices — Header/Line/Distribution",
        "content": (
            "AP Invoice tables (Header → Line → Distribution structure):\n\n"
            "fin_ap_invoices: invoice_id PK, invoice_number, supplier_id FK→sup_suppliers, "
            "ledger_id FK, invoice_date, due_date, invoice_amount, paid_amount, outstanding_amount, "
            "status (PAID/APPROVED/PENDING/OVERDUE), created_by/approved_by FK→hcm_persons\n"
            "30 invoices (invoice_id 1-30): 15 PAID, 3 APPROVED, 12 PENDING\n"
            "NOTE: AP invoices do NOT have budget_amount. If user asks about 'actual vs budget' "
            "or 'percentage difference between actual and budget', use finance_gl_balances instead.\n\n"
            "fin_ap_invoice_lines: invoice_line_id PK, invoice_id FK, line_number, description, "
            "quantity, unit_price, line_amount, po_line_id FK→proc_po_lines (3-WAY MATCH)\n\n"
            "fin_ap_invoice_distributions: distribution_id PK, invoice_line_id FK, "
            "cost_centre_id FK→fin_cost_centres, account_code_id FK→fin_account_codes\n\n"
            "=== VERIFIED SQL EXAMPLES ===\n\n"
            "Q: 'Show overdue AP invoices'\n"
            "A: SELECT i.invoice_number, s.supplier_name, i.invoice_amount, i.outstanding_amount, "
            "i.due_date, (CURRENT_DATE - i.due_date) as days_overdue "
            "FROM fin_ap_invoices i JOIN sup_suppliers s ON s.supplier_id=i.supplier_id "
            "WHERE i.status='OVERDUE' ORDER BY i.due_date\n\n"
            "Q: 'Show total invoiced amount by month for the year 2025 as a line chart'\n"
            "A: SELECT EXTRACT(MONTH FROM i.invoice_date)::INT AS invoice_month,\n"
            "     TO_CHAR(i.invoice_date, 'Mon-YYYY') AS month_label,\n"
            "     SUM(i.invoice_amount) AS total_invoice_amount\n"
            "   FROM fin_ap_invoices i\n"
            "   WHERE EXTRACT(YEAR FROM i.invoice_date) = 2025\n"
            "   GROUP BY EXTRACT(MONTH FROM i.invoice_date), TO_CHAR(i.invoice_date, 'Mon-YYYY')\n"
            "   ORDER BY invoice_month\n\n"
            "Q: 'Show monthly invoice trend for 2024'\n"
            "A: SELECT EXTRACT(MONTH FROM i.invoice_date)::INT AS invoice_month,\n"
            "     TO_CHAR(i.invoice_date, 'Mon-YYYY') AS month_label,\n"
            "     SUM(i.invoice_amount) AS total_invoice_amount\n"
            "   FROM fin_ap_invoices i\n"
            "   WHERE EXTRACT(YEAR FROM i.invoice_date) = 2024\n"
            "   GROUP BY EXTRACT(MONTH FROM i.invoice_date), TO_CHAR(i.invoice_date, 'Mon-YYYY')\n"
            "   ORDER BY invoice_month"
        ),
    },
    {
        "doc_id": "fin_ap_payments",
        "domain": "FINANCE",
        "title": "Finance AP Payments & Schedules — Verified Column Structure",
        "content": (
            "VERIFIED COLUMNS (from database inspection):\n\n"
            "fin_ap_payments: payment_id PK, payment_number, supplier_id FK→sup_suppliers, "
            "payment_date, payment_amount, payment_method (BACS/CHAPS), reference, status, created_at\n"
            "CRITICAL: fin_ap_payments has NO invoice_id and NO schedule_id columns.\n"
            "fin_ap_payments joins ONLY to sup_suppliers via supplier_id.\n\n"
            "fin_ap_payment_schedules: schedule_id PK, invoice_id FK→fin_ap_invoices, "
            "installment_num, due_date, amount_due, amount_paid, status (OPEN/PAID)\n"
            "CRITICAL: fin_ap_payment_schedules has NO payment_id column.\n"
            "fin_ap_payment_schedules joins ONLY to fin_ap_invoices via invoice_id.\n\n"
            "IMPORTANT: fin_ap_payments and fin_ap_payment_schedules are NOT directly joined to each other.\n"
            "To get payment + invoice info: join both separately to sup_suppliers or fin_ap_invoices.\n\n"
            "=== VERIFIED SQL EXAMPLES ===\n\n"
            "Q: 'Show total payments by supplier'\n"
            "A: SELECT s.supplier_name, SUM(p.payment_amount) as total_paid, COUNT(p.payment_id) as payment_count\n"
            "   FROM fin_ap_payments p JOIN sup_suppliers s ON s.supplier_id = p.supplier_id\n"
            "   GROUP BY s.supplier_name ORDER BY total_paid DESC\n\n"
            "Q: 'Show full ERP summary for supplier Deloitte UK: POs, invoices, payments, and which departments ordered from them'\n"
            "A: WITH po_data AS (\n"
            "     SELECT s.supplier_name, s.supplier_id,\n"
            "       COUNT(DISTINCT po.po_header_id) AS total_pos,\n"
            "       SUM(pod.amount) AS total_po_value,\n"
            "       STRING_AGG(DISTINCT d.dept_name, ', ') AS departments\n"
            "     FROM sup_suppliers s\n"
            "     LEFT JOIN proc_po_headers po ON po.supplier_id = s.supplier_id\n"
            "     LEFT JOIN proc_po_lines pol ON pol.po_header_id = po.po_header_id\n"
            "     LEFT JOIN proc_po_distributions pod ON pod.po_line_id = pol.po_line_id\n"
            "     LEFT JOIN fin_cost_centres cc ON cc.cost_centre_id = pod.cost_centre_id\n"
            "     LEFT JOIN hcm_departments d ON d.dept_id = cc.dept_id\n"
            "     WHERE s.supplier_name ILIKE '%Deloitte%'\n"
            "     GROUP BY s.supplier_name, s.supplier_id\n"
            "   ),\n"
            "   inv_data AS (\n"
            "     SELECT i.supplier_id,\n"
            "       COUNT(DISTINCT i.invoice_id) AS total_invoices,\n"
            "       SUM(i.invoice_amount) AS total_invoice_value\n"
            "     FROM fin_ap_invoices i\n"
            "     JOIN sup_suppliers s ON s.supplier_id = i.supplier_id\n"
            "     WHERE s.supplier_name ILIKE '%Deloitte%'\n"
            "     GROUP BY i.supplier_id\n"
            "   ),\n"
            "   pay_data AS (\n"
            "     SELECT p.supplier_id,\n"
            "       COUNT(DISTINCT p.payment_id) AS total_payments,\n"
            "       SUM(p.payment_amount) AS total_payment_value\n"
            "     FROM fin_ap_payments p\n"
            "     JOIN sup_suppliers s ON s.supplier_id = p.supplier_id\n"
            "     WHERE s.supplier_name ILIKE '%Deloitte%'\n"
            "     GROUP BY p.supplier_id\n"
            "   )\n"
            "   SELECT pd.supplier_name, pd.total_pos, pd.total_po_value,\n"
            "     COALESCE(id.total_invoices, 0) AS total_invoices,\n"
            "     COALESCE(id.total_invoice_value, 0) AS total_invoice_value,\n"
            "     COALESCE(payd.total_payments, 0) AS total_payments,\n"
            "     COALESCE(payd.total_payment_value, 0) AS total_payment_value,\n"
            "     pd.departments\n"
            "   FROM po_data pd\n"
            "   LEFT JOIN inv_data id ON id.supplier_id = pd.supplier_id\n"
            "   LEFT JOIN pay_data payd ON payd.supplier_id = pd.supplier_id\n\n"
            "CRITICAL: ALWAYS use ILIKE '%<name>%' with wildcards for supplier name search. NEVER use exact match.\n"
            "CRITICAL: To get departments for a supplier's POs, join proc_po_distributions → fin_cost_centres → hcm_departments. proc_po_headers does NOT have cost_centre_id.\n"
            "CRITICAL: fin_ap_payments joins ONLY to sup_suppliers via supplier_id. It has NO invoice_id column.\n"
            "CRITICAL: fin_ap_payment_schedules joins ONLY to fin_ap_invoices via invoice_id. It has NO payment_id.\n\n"
            "Q: 'Show invoice payment schedule status for a supplier'\n"
            "A: SELECT i.invoice_number, i.invoice_amount, ps.due_date, ps.amount_due, ps.amount_paid, ps.status\n"
            "   FROM fin_ap_invoices i\n"
            "   JOIN fin_ap_payment_schedules ps ON ps.invoice_id = i.invoice_id\n"
            "   JOIN sup_suppliers s ON s.supplier_id = i.supplier_id\n"
            "   WHERE s.supplier_name ILIKE '%Deloitte%'\n"
            "   ORDER BY ps.due_date"
        ),
    },
    {
        "doc_id": "fin_ar_tables",
        "domain": "FINANCE",
        "title": "Finance AR — Customers, Invoices & Receipts",
        "content": (
            "Accounts Receivable tables:\n\n"
            "fin_ar_customers: customer_id PK, customer_number, customer_name, customer_type, "
            "payment_terms, credit_limit\n"
            "5 customers: British Airways, Tesco, HSBC, National Grid, GlaxoSmithKline\n\n"
            "fin_ar_invoices: ar_invoice_id PK, invoice_number, customer_id FK, invoice_date, "
            "due_date, invoice_amount, paid_amount, outstanding, status (OPEN/CLOSED)\n\n"
            "fin_ar_receipts: receipt_id PK, receipt_number, ar_invoice_id FK, receipt_date, "
            "receipt_amount, payment_method\n\n"
            "Example: SELECT c.customer_name, SUM(i.outstanding) as total_outstanding "
            "FROM fin_ar_invoices i JOIN fin_ar_customers c ON c.customer_id=i.customer_id "
            "WHERE i.status='OPEN' GROUP BY c.customer_name"
        ),
    },

    # ================================================================
    # SUPPLIER MASTER (UNIFIED)
    # ================================================================
    {
        "doc_id": "sup_suppliers_table",
        "domain": "PROCUREMENT",
        "title": "Unified Supplier Master — sup_suppliers",
        "content": (
            "Tables: sup_suppliers, sup_supplier_sites, sup_supplier_contacts\n"
            "UNIFIED supplier master used by BOTH Finance AP and Procurement.\n\n"
            "sup_suppliers: supplier_id PK, supplier_number SUP001-SUP020, supplier_name, "
            "payment_terms, supplier_type (IT_SERVICES/HARDWARE/CONSULTING/FACILITIES/TELECOM), "
            "risk_rating (LOW/MEDIUM/HIGH), qualification_status, status\n"
            "20 suppliers: Accenture, Deloitte, PwC, KPMG, BT, Computacenter, etc.\n\n"
            "sup_supplier_sites: site_id PK, supplier_id FK, site_code, address, is_primary\n"
            "sup_supplier_contacts: contact_id PK, supplier_id FK, contact_name, email, is_primary\n\n"
            "Cross-domain usage:\n"
            "- fin_ap_invoices.supplier_id → sup_suppliers\n"
            "- proc_po_headers.supplier_id → sup_suppliers\n"
            "- proc_quotation_headers.supplier_id → sup_suppliers\n"
            "- proc_contract_headers.supplier_id → sup_suppliers\n\n"
            "Example: SELECT s.supplier_name, s.supplier_type, s.risk_rating, "
            "COUNT(DISTINCT i.invoice_id) as invoice_count, COUNT(DISTINCT ph.po_header_id) as po_count "
            "FROM sup_suppliers s LEFT JOIN fin_ap_invoices i ON i.supplier_id=s.supplier_id "
            "LEFT JOIN proc_po_headers ph ON ph.supplier_id=s.supplier_id "
            "GROUP BY s.supplier_id, s.supplier_name, s.supplier_type, s.risk_rating"
        ),
    },

    # ================================================================
    # PROCUREMENT DOMAIN
    # ================================================================
    {
        "doc_id": "procurement_quotations_table",
        "domain": "PROCUREMENT",
        "title": "Procurement Quotations — Version-controlled (includes E-205 delta)",
        "content": (
            "Views & Tables:\n"
            "procurement_quotations: LEGACY VIEW joining proc_quotation_headers + proc_quote_versions + sup_suppliers\n"
            "proc_quotation_headers: quotation_header_id PK, quotation_number, engagement_id (E-201 to E-215), "
            "engagement_name, supplier_id FK→sup_suppliers, original_amount, revised_amount, status, category\n"
            "proc_quotation_lines: quot_line_id PK, quotation_header_id FK, item_id FK, line details\n"
            "proc_quote_versions: version_id PK, quotation_header_id FK, version_number, version_amount, status\n\n"
            "CRITICAL DATA — E-205:\n"
            "Version 1: amount=82000, status=SUBMITTED\n"
            "Version 2: amount=92180, status=APPROVED\n"
            "Delta = (92180-82000)/82000*100 = EXACTLY 12.4%\n"
            "NOTE: Delta calculation done in Python Pandas, not SQL.\n\n"
            "SQL for E-205:\n"
            "SELECT engagement_id, engagement_name, original_amount, revised_amount, quotation_version, status "
            "FROM procurement_quotations WHERE engagement_id='E-205' ORDER BY quotation_version\n\n"
            "SQL via base tables:\n"
            "SELECT qh.engagement_id, qh.original_amount, qv.version_number, qv.version_amount, qv.status "
            "FROM proc_quotation_headers qh JOIN proc_quote_versions qv ON qv.quotation_header_id=qh.quotation_header_id "
            "WHERE qh.engagement_id='E-205' ORDER BY qv.version_number"
        ),
    },
    {
        "doc_id": "procurement_po_table",
        "domain": "PROCUREMENT",
        "title": "Procurement Purchase Orders — Header/Line/Distribution with 3-Way Match",
        "content": (
            "PO tables (Header → Line → Distribution):\n\n"
            "procurement_purchase_orders: LEGACY VIEW on proc_po_headers\n"
            "proc_po_headers: po_header_id PK, po_number, supplier_id FK→sup_suppliers, "
            "buyer_id FK→hcm_persons, requisition_id FK, total_amount, approved_amount, "
            "status (PENDING/APPROVED/REJECTED), category\n\n"
            "proc_po_lines: po_line_id PK, po_header_id FK, item_id FK, description, quantity, "
            "unit_price, line_amount, status\n\n"
            "proc_po_distributions: po_dist_id PK, po_line_id FK, cost_centre_id FK→fin_cost_centres, "
            "account_code_id FK→fin_account_codes, distribution_pct, amount\n\n"
            "proc_po_approvals: approval_id PK, po_header_id FK, approver_id FK→hcm_persons, "
            "approval_level, action, action_date\n\n"
            "3-WAY MATCH: proc_po_lines ↔ proc_receipt_lines ↔ fin_ap_invoice_lines\n\n"
            "Example: SELECT po.po_number, s.supplier_name, po.total_amount, po.status "
            "FROM proc_po_headers po JOIN sup_suppliers s ON s.supplier_id=po.supplier_id "
            "WHERE po.status='PENDING' ORDER BY po.created_date"
        ),
    },
    {
        "doc_id": "procurement_requisitions",
        "domain": "PROCUREMENT",
        "title": "Procurement Requisitions — Header/Line/Distribution",
        "content": (
            "Requisition tables:\n\n"
            "proc_requisition_headers: requisition_id PK, requisition_number, "
            "requester_id FK→hcm_persons, dept_id FK→hcm_departments, description, "
            "total_amount, status, submitted_date, approved_by FK\n\n"
            "proc_requisition_lines: req_line_id PK, requisition_id FK, item_id FK→proc_items, "
            "quantity, unit_price, line_amount, need_by_date\n\n"
            "proc_requisition_distributions: req_dist_id PK, req_line_id FK, "
            "cost_centre_id FK→fin_cost_centres, account_code_id FK→fin_account_codes\n\n"
            "Example: SELECT rh.requisition_number, p.first_name||' '||p.last_name as requester, "
            "rh.total_amount, rh.status FROM proc_requisition_headers rh "
            "JOIN hcm_persons p ON p.person_id=rh.requester_id"
        ),
    },
    {
        "doc_id": "procurement_receiving_contracts",
        "domain": "PROCUREMENT",
        "title": "Procurement Receiving & Contracts",
        "content": (
            "Receiving tables (goods receipt):\n\n"
            "proc_receipt_headers: receipt_header_id PK, receipt_number, po_header_id FK, "
            "received_by FK→hcm_persons, receipt_date, status\n"
            "proc_receipt_lines: receipt_line_id PK, receipt_header_id FK, po_line_id FK, "
            "quantity_received, quantity_accepted, quantity_rejected, inspection_status\n\n"
            "Contract tables:\n\n"
            "proc_contract_headers: contract_header_id PK, contract_number, supplier_id FK, "
            "contract_type (BLANKET), start/end_date, total_value, released_amount, status\n"
            "proc_contract_lines: contract_line_id PK, contract_header_id FK, item_id FK, "
            "quantity, unit_price, line_amount, released_amount\n\n"
            "proc_item_categories: category_id PK, category_code, parent_category_id (self-ref hierarchy)\n"
            "proc_items: item_id PK, item_code, item_name, category_id FK, unit_price, item_type\n\n"
            "Example: SELECT ch.contract_number, s.supplier_name, ch.total_value, "
            "ch.released_amount, (ch.total_value-ch.released_amount) as remaining "
            "FROM proc_contract_headers ch JOIN sup_suppliers s ON s.supplier_id=ch.supplier_id"
        ),
    },

    # ================================================================
    # CROSS-DOMAIN DOCUMENTATION
    {
        "doc_id": "cross_domain_links",
        "domain": "ALL",
        "title": "Cross-Domain Foreign Key Links and JOIN Patterns",
        "content": (
            "CROSS-DOMAIN JOIN PATHS — Use these EXACT verified patterns for multi-domain queries.\n\n"
            "=== CRITICAL FACTS (VERIFIED IN DATABASE) ===\n\n"
            "FACT 1: hcm_persons does NOT have cost_centre_id column.\n"
            "FACT 2: proc_po_headers.requisition_id is NULL for all rows — DO NOT join via requisition.\n"
            "FACT 3: hcm_departments has 4000 rows (seeded). To get the 10 real departments,\n"
            "        always join via fin_cost_centres (only 10 real cost centres exist CC001-CC010).\n"
            "FACT 4: PO spend (total_amount) lives in proc_po_headers.\n"
            "        PO cost-centre allocation lives in proc_po_distributions (NOT proc_po_headers).\n"
            "FACT 5: proc_po_headers has NO cost_centre_id column.\n"
            "        To get which cost centre/dept a PO belongs to, always go through proc_po_distributions.\n"
            "FACT 6: hcm_assignments.salary is the salary column. There is NO salary column on hcm_persons.\n"
            "FACT 7: To get departments for a supplier, join:\n"
            "        proc_po_headers → proc_po_distributions → fin_cost_centres → hcm_departments.\n\n"
            "=== VERIFIED JOIN PATHS ===\n\n"
            "1. Headcount by Department (CTE 1):\n"
            "   fin_cost_centres cc → hcm_departments d (ONLY via cc.dept_id = d.dept_id)\n"
            "   d → hcm_assignments a (via a.dept_id = d.dept_id WHERE a.assignment_status='ACTIVE')\n"
            "   COUNT(DISTINCT a.person_id) = headcount\n\n"
            "2. Budget variance by Department (CTE 2):\n"
            "   fin_cost_centres cc → fin_gl_balances gb (via gb.cost_centre_id = cc.cost_centre_id)\n"
            "   SUM(gb.actual_amount - gb.budget_amount) = budget_variance\n\n"
            "3. PO Spend by Department (CTE 3 — NOT via requisition_id):\n"
            "   fin_cost_centres cc → proc_po_distributions pod (via pod.cost_centre_id = cc.cost_centre_id)\n"
            "   pod → proc_po_lines pol (via pol.po_line_id = pod.po_line_id)\n"
            "   pol → proc_po_headers po (via po.po_header_id = pol.po_header_id)\n"
            "   SUM(pod.amount) = PO spend allocated to that cost centre\n\n"
            "4. Supplier across Finance + Procurement:\n"
            "   sup_suppliers → fin_ap_invoices (via supplier_id)\n"
            "   sup_suppliers → proc_po_headers (via supplier_id)\n\n"
            "5. 3-Way Match (PO → Receipt → Invoice):\n"
            "   proc_po_lines → proc_receipt_lines (via po_line_id)\n"
            "   proc_po_lines → fin_ap_invoice_lines (via po_line_id)\n\n"
            "=== VERIFIED WORKING SQL EXAMPLES ===\n\n"
            "Q: 'For each supplier, show total invoice amount, number of POs, and how many employees work in the departments that issued those POs'\n"
            "A: WITH supplier_po AS (\n"
            "     SELECT s.supplier_id, s.supplier_name,\n"
            "       COUNT(DISTINCT po.po_header_id) AS num_pos,\n"
            "       SUM(pod.amount) AS total_po_spend\n"
            "     FROM sup_suppliers s\n"
            "     LEFT JOIN proc_po_headers po ON po.supplier_id = s.supplier_id\n"
            "     LEFT JOIN proc_po_lines pol ON pol.po_header_id = po.po_header_id\n"
            "     LEFT JOIN proc_po_distributions pod ON pod.po_line_id = pol.po_line_id\n"
            "     GROUP BY s.supplier_id, s.supplier_name\n"
            "   ),\n"
            "   supplier_invoices AS (\n"
            "     SELECT i.supplier_id, SUM(i.invoice_amount) AS total_invoice_amount\n"
            "     FROM fin_ap_invoices i\n"
            "     GROUP BY i.supplier_id\n"
            "   ),\n"
            "   dept_employees AS (\n"
            "     SELECT s.supplier_id,\n"
            "       COUNT(DISTINCT a.person_id) AS num_employees\n"
            "     FROM sup_suppliers s\n"
            "     JOIN proc_po_headers po ON po.supplier_id = s.supplier_id\n"
            "     JOIN proc_po_lines pol ON pol.po_header_id = po.po_header_id\n"
            "     JOIN proc_po_distributions pod ON pod.po_line_id = pol.po_line_id\n"
            "     JOIN fin_cost_centres cc ON cc.cost_centre_id = pod.cost_centre_id\n"
            "     JOIN hcm_departments d ON d.dept_id = cc.dept_id\n"
            "     JOIN hcm_assignments a ON a.dept_id = d.dept_id AND a.assignment_status = 'ACTIVE'\n"
            "     GROUP BY s.supplier_id\n"
            "   )\n"
            "   SELECT spo.supplier_name,\n"
            "     COALESCE(si.total_invoice_amount, 0) AS total_invoice_amount,\n"
            "     COALESCE(spo.num_pos, 0) AS num_pos,\n"
            "     COALESCE(de.num_employees, 0) AS num_employees\n"
            "   FROM supplier_po spo\n"
            "   LEFT JOIN supplier_invoices si ON si.supplier_id = spo.supplier_id\n"
            "   LEFT JOIN dept_employees de ON de.supplier_id = spo.supplier_id\n"
            "   ORDER BY total_invoice_amount DESC\n\n"
            "Q: 'Which departments have the highest combined employee salary cost and PO spend?'\n"
            "A: WITH salary_by_dept AS (\n"
            "     SELECT d.dept_name,\n"
            "       COALESCE(SUM(a.salary), 0) AS total_salary_cost\n"
            "     FROM fin_cost_centres cc\n"
            "     JOIN hcm_departments d ON d.dept_id = cc.dept_id\n"
            "     LEFT JOIN hcm_assignments a ON a.dept_id = d.dept_id AND a.assignment_status = 'ACTIVE'\n"
            "     GROUP BY d.dept_name\n"
            "   ),\n"
            "   po_by_dept AS (\n"
            "     SELECT d.dept_name,\n"
            "       COALESCE(SUM(pod.amount), 0) AS total_po_spend\n"
            "     FROM fin_cost_centres cc\n"
            "     JOIN hcm_departments d ON d.dept_id = cc.dept_id\n"
            "     LEFT JOIN proc_po_distributions pod ON pod.cost_centre_id = cc.cost_centre_id\n"
            "     GROUP BY d.dept_name\n"
            "   )\n"
            "   SELECT s.dept_name,\n"
            "     s.total_salary_cost,\n"
            "     p.total_po_spend,\n"
            "     (s.total_salary_cost + p.total_po_spend) AS total_combined_cost\n"
            "   FROM salary_by_dept s\n"
            "   JOIN po_by_dept p ON p.dept_name = s.dept_name\n"
            "   ORDER BY total_combined_cost DESC\n\n"
            "Q: 'Show department-wise breakdown of headcount, budget variance, and total PO spend'\n"
            "A: WITH hr_stats AS (\n"
            "     SELECT d.dept_name, COUNT(DISTINCT a.person_id) AS headcount\n"
            "     FROM fin_cost_centres cc\n"
            "     JOIN hcm_departments d ON d.dept_id = cc.dept_id\n"
            "     LEFT JOIN hcm_assignments a ON a.dept_id = d.dept_id AND a.assignment_status = 'ACTIVE'\n"
            "     GROUP BY d.dept_name\n"
            "   ),\n"
            "   fin_stats AS (\n"
            "     SELECT d.dept_name, SUM(gb.actual_amount - gb.budget_amount) AS budget_variance\n"
            "     FROM fin_cost_centres cc\n"
            "     JOIN hcm_departments d ON d.dept_id = cc.dept_id\n"
            "     LEFT JOIN fin_gl_balances gb ON gb.cost_centre_id = cc.cost_centre_id\n"
            "     GROUP BY d.dept_name\n"
            "   ),\n"
            "   proc_stats AS (\n"
            "     SELECT d.dept_name, SUM(pod.amount) AS total_po_spend\n"
            "     FROM fin_cost_centres cc\n"
            "     JOIN hcm_departments d ON d.dept_id = cc.dept_id\n"
            "     LEFT JOIN proc_po_distributions pod ON pod.cost_centre_id = cc.cost_centre_id\n"
            "     GROUP BY d.dept_name\n"
            "   )\n"
            "   SELECT h.dept_name, h.headcount, f.budget_variance, COALESCE(p.total_po_spend, 0) AS total_po_spend\n"
            "   FROM hr_stats h\n"
            "   LEFT JOIN fin_stats f ON f.dept_name = h.dept_name\n"
            "   LEFT JOIN proc_stats p ON p.dept_name = h.dept_name\n"
            "   ORDER BY h.dept_name\n\n"
            "Q: 'Show headcount per cost centre with budget utilization'\n"
            "A: WITH hr_stats AS (\n"
            "     SELECT cc.cost_centre_name, COUNT(DISTINCT a.person_id) AS headcount\n"
            "     FROM fin_cost_centres cc\n"
            "     JOIN hcm_departments d ON d.dept_id = cc.dept_id\n"
            "     LEFT JOIN hcm_assignments a ON a.dept_id = d.dept_id AND a.assignment_status = 'ACTIVE'\n"
            "     GROUP BY cc.cost_centre_name\n"
            "   ),\n"
            "   fin_stats AS (\n"
            "     SELECT cc.cost_centre_name, SUM(gb.actual_amount) AS actual, SUM(gb.budget_amount) AS budget\n"
            "     FROM fin_cost_centres cc\n"
            "     LEFT JOIN fin_gl_balances gb ON gb.cost_centre_id = cc.cost_centre_id\n"
            "     GROUP BY cc.cost_centre_name\n"
            "   )\n"
            "   SELECT h.cost_centre_name, h.headcount, f.actual, f.budget\n"
            "   FROM hr_stats h\n"
            "   LEFT JOIN fin_stats f ON f.cost_centre_name = h.cost_centre_name\n\n"
            "Q: 'Compare AP invoice amount with PO amount by supplier'\n"
            "A: SELECT s.supplier_name,\n"
            "     COALESCE(SUM(DISTINCT i.invoice_amount), 0) as total_invoiced,\n"
            "     COALESCE(SUM(DISTINCT po.total_amount), 0) as total_po\n"
            "   FROM sup_suppliers s\n"
            "   LEFT JOIN fin_ap_invoices i ON i.supplier_id = s.supplier_id\n"
            "   LEFT JOIN proc_po_headers po ON po.supplier_id = s.supplier_id\n"
            "   GROUP BY s.supplier_name ORDER BY total_invoiced DESC\n\n"
            "Q: 'Which departments have most approved POs?'\n"
            "A: SELECT d.dept_name, COUNT(DISTINCT po.po_header_id) AS approved_pos\n"
            "   FROM fin_cost_centres cc\n"
            "   JOIN hcm_departments d ON d.dept_id = cc.dept_id\n"
            "   JOIN proc_po_distributions pod ON pod.cost_centre_id = cc.cost_centre_id\n"
            "   JOIN proc_po_lines pol ON pol.po_line_id = pod.po_line_id\n"
            "   JOIN proc_po_headers po ON po.po_header_id = pol.po_header_id AND po.status = 'APPROVED'\n"
            "   GROUP BY d.dept_name ORDER BY approved_pos DESC"
        ),
    },
]
