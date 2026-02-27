"""Schema documentation for vector embedding — used by PGVector RAG retrieval."""

SCHEMA_DOCS: list[dict] = [
    {
        "doc_id": "hcm_employees_table",
        "domain": "HCM",
        "title": "HCM Employees Table — hcm_employees",
        "content": (
            "Table: hcm_employees\n"
            "Stores all employee data including active and terminated staff.\n"
            "Columns:\n"
            "- employee_id: SERIAL PRIMARY KEY, unique identifier\n"
            "- full_name: VARCHAR, employee's full name\n"
            "- department: VARCHAR, one of: Engineering, Finance, HR, Procurement, Marketing, Sales, Operations\n"
            "- job_title: VARCHAR, role title\n"
            "- grade_level: VARCHAR, G3(junior) to G8(director/VP)\n"
            "- salary: NUMERIC, annual salary in GBP\n"
            "- hire_date: DATE, when employee joined\n"
            "- termination_date: DATE, NULL for active employees, populated for leavers\n"
            "- employment_status: VARCHAR, 'ACTIVE' or 'TERMINATED'\n"
            "- location: VARCHAR, one of: London, Manchester, Birmingham, Remote\n"
            "- manager_id: INTEGER FK to employee_id\n\n"
            "Key filters:\n"
            "- Active employees: WHERE employment_status = 'ACTIVE'\n"
            "- Terminated: WHERE employment_status = 'TERMINATED' AND termination_date IS NOT NULL\n"
            "- By department: WHERE department = 'Engineering'\n"
            "- Engineering headcount: SELECT COUNT(*) FROM hcm_employees WHERE department='Engineering' AND employment_status='ACTIVE'  -- returns 47\n\n"
            "Example queries:\n"
            "Q: \"How many employees are in Engineering?\"\n"
            "A: SELECT department, COUNT(*) as headcount FROM hcm_employees WHERE employment_status='ACTIVE' GROUP BY department ORDER BY headcount DESC\n\n"
            "Q: \"List employees in Finance above Grade 5\"\n"
            "A: SELECT full_name, job_title, grade_level, salary FROM hcm_employees WHERE department='Finance' AND employment_status='ACTIVE' AND grade_level IN ('G6','G7','G8') ORDER BY grade_level DESC"
        ),
    },
    {
        "doc_id": "hcm_attrition_calc",
        "domain": "HCM",
        "title": "HCM Attrition Rate — Calculation Method",
        "content": (
            "Attrition rate measures the percentage of employees who left the organisation in a period.\n"
            "Formula: attrition_rate = (count_terminated_in_period / average_headcount) * 100\n"
            "average_headcount = (headcount_at_start_of_period + headcount_at_end_of_period) / 2\n\n"
            "SQL to get terminated employees in a date range:\n"
            "SELECT COUNT(*) FROM hcm_employees\n"
            "WHERE employment_status='TERMINATED'\n"
            "AND termination_date BETWEEN '2025-01-01' AND '2025-12-31'\n\n"
            "SQL for current headcount:\n"
            "SELECT COUNT(*) FROM hcm_employees WHERE employment_status='ACTIVE'\n\n"
            "IMPORTANT: The attrition rate percentage calculation is always done in Python (Pandas), not in SQL.\n"
            "The SQL just retrieves the raw counts. Python then applies the formula.\n\n"
            "For YTD attrition, use: termination_date >= DATE_TRUNC('year', CURRENT_DATE)"
        ),
    },
    {
        "doc_id": "finance_gl_balances_table",
        "domain": "FINANCE",
        "title": "Finance GL Balances — finance_gl_balances",
        "content": (
            "Table: finance_gl_balances\n"
            "Stores General Ledger budget vs actual amounts by cost centre and period.\n"
            "Columns:\n"
            "- balance_id: SERIAL PRIMARY KEY\n"
            "- cost_centre: VARCHAR, CC001 to CC010\n"
            "- cost_centre_name: VARCHAR, e.g. CC001=Engineering, CC002=Finance, CC003=Marketing, CC004=HR, CC005=Procurement\n"
            "- account_code: VARCHAR\n"
            "- account_name: VARCHAR\n"
            "- period_name: VARCHAR, format 'MON-YYYY' e.g. 'JAN-2025', 'OCT-2025', 'DEC-2025'\n"
            "- actual_amount: NUMERIC, actual spend in GBP\n"
            "- budget_amount: NUMERIC, planned spend in GBP\n"
            "- fiscal_year: INTEGER\n"
            "- fiscal_quarter: INTEGER, 1-4\n\n"
            "Budget variance: variance = actual_amount - budget_amount (positive = over budget)\n"
            "CC003 (Marketing) is over budget in Q4 2025 (fiscal_quarter=4)\n\n"
            "Example queries:\n"
            "Q: \"Which departments are over budget this quarter?\"\n"
            "A: SELECT cost_centre_name, SUM(actual_amount) as actual, SUM(budget_amount) as budget, "
            "SUM(actual_amount-budget_amount) as variance FROM finance_gl_balances "
            "WHERE fiscal_year=2025 AND fiscal_quarter=4 GROUP BY cost_centre, cost_centre_name "
            "HAVING SUM(actual_amount) > SUM(budget_amount) ORDER BY variance DESC\n\n"
            "Q: \"What is the GL balance for CC003?\"\n"
            "A: SELECT period_name, actual_amount, budget_amount, (actual_amount-budget_amount) as variance "
            "FROM finance_gl_balances WHERE cost_centre='CC003' ORDER BY period_name"
        ),
    },
    {
        "doc_id": "finance_ap_invoices_table",
        "domain": "FINANCE",
        "title": "Finance AP Invoices — finance_ap_invoices",
        "content": (
            "Table: finance_ap_invoices\n"
            "Accounts Payable invoice register tracking all supplier invoices.\n"
            "Columns:\n"
            "- invoice_id: SERIAL PRIMARY KEY\n"
            "- invoice_number: VARCHAR, unique reference\n"
            "- supplier_name: VARCHAR, supplier company name\n"
            "- invoice_date: DATE, invoice raised date\n"
            "- due_date: DATE, payment due date\n"
            "- invoice_amount: NUMERIC, total invoice value GBP\n"
            "- paid_amount: NUMERIC, amount paid so far\n"
            "- outstanding_amount: NUMERIC, remaining unpaid (invoice_amount - paid_amount)\n"
            "- status: VARCHAR, one of: APPROVED, PENDING, OVERDUE, PAID\n"
            "- cost_centre: VARCHAR\n\n"
            "AP Aging calculation: days_overdue = CURRENT_DATE - due_date (for OVERDUE invoices)\n"
            "Aging buckets (done in Python Pandas):\n"
            "  0-30 days, 31-60 days, 61-90 days, 90+ days\n\n"
            "Example queries:\n"
            "Q: \"Show AP invoices overdue by more than 60 days\"\n"
            "A: SELECT invoice_number, supplier_name, invoice_amount, outstanding_amount, due_date, "
            "(CURRENT_DATE - due_date) as days_overdue FROM finance_ap_invoices "
            "WHERE status='OVERDUE' AND due_date < CURRENT_DATE - INTERVAL '60 days' ORDER BY due_date ASC\n\n"
            "Q: \"What is the total outstanding AP?\"\n"
            "A: SELECT SUM(outstanding_amount) as total_outstanding, COUNT(*) as invoice_count "
            "FROM finance_ap_invoices WHERE status IN ('OVERDUE','PENDING')"
        ),
    },
    {
        "doc_id": "procurement_quotations_table",
        "domain": "PROCUREMENT",
        "title": "Procurement Quotations — procurement_quotations (includes E-205 delta)",
        "content": (
            "Table: procurement_quotations\n"
            "Stores engagement quotations from suppliers, including original and revised versions.\n"
            "Columns:\n"
            "- quotation_id: SERIAL PRIMARY KEY\n"
            "- engagement_id: VARCHAR, format E-201 to E-215\n"
            "- engagement_name: VARCHAR, full project/engagement name\n"
            "- supplier_name: VARCHAR\n"
            "- original_amount: NUMERIC, initial quoted amount in GBP\n"
            "- revised_amount: NUMERIC, revised amount (NULL if no revision exists)\n"
            "- quotation_version: INTEGER, 1=original, 2+=revisions\n"
            "- status: VARCHAR, DRAFT/SUBMITTED/APPROVED/REJECTED\n"
            "- submission_date: DATE\n"
            "- category: VARCHAR, IT Services/Consulting/Hardware/Facilities\n\n"
            "CRITICAL DEMO DATA — Engagement E-205:\n"
            "Version 1: original_amount=82000, revised_amount=NULL, status=SUBMITTED\n"
            "Version 2: original_amount=82000, revised_amount=92180, status=APPROVED\n"
            "Delta = (92180 - 82000) / 82000 * 100 = EXACTLY 12.4%\n"
            "NOTE: Delta calculation is done in Python Pandas, not SQL.\n\n"
            "SQL to fetch E-205 for delta calculation:\n"
            "SELECT engagement_id, engagement_name, original_amount, revised_amount, quotation_version, status "
            "FROM procurement_quotations WHERE engagement_id='E-205' ORDER BY quotation_version\n\n"
            "SQL to find all engagements with revisions:\n"
            "SELECT engagement_id, MAX(original_amount) as original, MAX(revised_amount) as revised "
            "FROM procurement_quotations WHERE revised_amount IS NOT NULL GROUP BY engagement_id"
        ),
    },
    {
        "doc_id": "procurement_po_table",
        "domain": "PROCUREMENT",
        "title": "Procurement Purchase Orders — procurement_purchase_orders",
        "content": (
            "Table: procurement_purchase_orders\n"
            "Tracks purchase orders raised to suppliers.\n"
            "Columns:\n"
            "- po_id: SERIAL PRIMARY KEY\n"
            "- po_number: VARCHAR, format PO-2025-001\n"
            "- supplier_name: VARCHAR\n"
            "- total_amount: NUMERIC, total PO value GBP\n"
            "- approved_amount: NUMERIC, approved portion (may be less than total for partial approval)\n"
            "- status: VARCHAR, PENDING/APPROVED/REJECTED/PARTIALLY_APPROVED\n"
            "- created_date: DATE, when PO was raised\n"
            "- approved_date: DATE, NULL if not yet approved\n"
            "- cost_centre: VARCHAR\n"
            "- category: VARCHAR\n\n"
            "Days pending: CURRENT_DATE - created_date (for PENDING orders)\n\n"
            "Example queries:\n"
            "Q: \"Show all pending purchase orders older than 14 days\"\n"
            "A: SELECT po_number, supplier_name, total_amount, created_date, "
            "(CURRENT_DATE - created_date) as days_pending FROM procurement_purchase_orders "
            "WHERE status='PENDING' AND created_date < CURRENT_DATE - INTERVAL '14 days' ORDER BY created_date ASC\n\n"
            "Q: \"Which supplier has the highest total PO spend?\"\n"
            "A: SELECT supplier_name, SUM(total_amount) as total_spend, COUNT(*) as po_count "
            "FROM procurement_purchase_orders WHERE status IN ('APPROVED','PARTIALLY_APPROVED') "
            "GROUP BY supplier_name ORDER BY total_spend DESC LIMIT 10"
        ),
    },
]
