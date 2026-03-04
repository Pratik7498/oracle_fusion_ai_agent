"""Check table column names for tables used in expand_seed.py."""
import psycopg2

conn = psycopg2.connect(dbname="oracle_fusion_poc", user="postgres", password="12345", host="localhost")
cur = conn.cursor()

tables = [
    "hcm_workforce_actions", "hcm_employment_periods", "hcm_salary_history",
    "hcm_promotions", "hcm_transfers", "hcm_compensation_elements",
    "hcm_performance_reviews", "hcm_training_records", "hcm_cost_allocations",
    "hcm_payroll_results", "fin_ap_invoice_distributions", "fin_ap_payment_schedules",
    "proc_requisition_headers", "proc_requisition_lines", "proc_requisition_distributions",
    "proc_po_headers", "proc_po_lines", "proc_po_distributions",
    "proc_po_approvals", "proc_receipt_headers", "proc_receipt_lines",
    "proc_contract_headers", "proc_contract_lines", "proc_quote_versions",
    "proc_quotation_headers", "proc_quotation_lines", "proc_items",
    "sup_supplier_sites", "sup_supplier_contacts",
    "hcm_persons", "hcm_assignments", "hcm_person_names", "hcm_person_emails",
]

for t in tables:
    cur.execute(
        "SELECT column_name FROM information_schema.columns WHERE table_name=%s ORDER BY ordinal_position",
        (t,)
    )
    cols = [r[0] for r in cur.fetchall()]
    print(f"{t}: {', '.join(cols)}")

cur.close()
conn.close()
