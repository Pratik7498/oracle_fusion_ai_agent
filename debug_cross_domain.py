"""Quick check: does fin_ap_invoice_lines have any non-null po_line_id links to proc_po_lines?"""
import sys, os
sys.path.insert(0, '.')
from dotenv import load_dotenv
import psycopg2
load_dotenv()
url = os.environ.get('POSTGRES_URL', 'postgresql://poc_user:poc_pass_2025@localhost:5432/oracle_fusion_poc')
conn = psycopg2.connect(url)
cur = conn.cursor()

def q(sql):
    cur.execute(sql)
    return cur.fetchall()

print("=== AP Invoice Lines: po_line_id nulls ===")
print(q("SELECT COUNT(*), COUNT(po_line_id), COUNT(*) - COUNT(po_line_id) AS nulls FROM fin_ap_invoice_lines"))

print("\n=== 3-way match: invoices that have matching PO lines ===")
print(q("""SELECT COUNT(*) FROM fin_ap_invoice_lines il 
          JOIN proc_po_lines pol ON pol.po_line_id = il.po_line_id"""))

print("\n=== AP invoices total count and sum ===")
print(q("SELECT COUNT(*), SUM(invoice_amount) FROM fin_ap_invoices"))

print("\n=== POs total count ===")
print(q("SELECT COUNT(*), SUM(total_amount) FROM proc_po_headers"))

print("\n=== Suppliers in AP invoices ===")
print(q("SELECT COUNT(DISTINCT supplier_id) FROM fin_ap_invoices"))

print("\n=== Suppliers in POs ===")
print(q("SELECT COUNT(DISTINCT supplier_id) FROM proc_po_headers"))

print("\n=== Common suppliers: in both invoices AND POs ===")
rows = q("""SELECT COUNT(*) FROM (
    SELECT supplier_id FROM fin_ap_invoices
    INTERSECT
    SELECT supplier_id FROM proc_po_headers
) x""")
print(rows)

print("\n=== Sample supplier invoice amounts ===")
rows = q("""SELECT s.supplier_name, SUM(i.invoice_amount) as total_inv
           FROM fin_ap_invoices i JOIN sup_suppliers s ON s.supplier_id=i.supplier_id
           GROUP BY s.supplier_name ORDER BY total_inv DESC LIMIT 5""")
for r in rows:
    print(r)

print("\n=== Sample PO counts per supplier ===")
rows = q("""SELECT s.supplier_name, COUNT(po.po_header_id) as num_pos
           FROM proc_po_headers po JOIN sup_suppliers s ON s.supplier_id=po.supplier_id
           GROUP BY s.supplier_name ORDER BY num_pos DESC LIMIT 5""")
for r in rows:
    print(r)

conn.close()
print("\nDONE")
