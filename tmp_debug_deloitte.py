from backend.db.connection import execute_query

# Check exact columns on proc_po_distributions
print("=== proc_po_distributions columns ===")
df = execute_query("""
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'proc_po_distributions'
ORDER BY ordinal_position
""")
print(df.to_string())

# Check a sample of proc_po_distributions
print("\n=== proc_po_distributions sample ===")
df2 = execute_query("SELECT * FROM proc_po_distributions LIMIT 3")
print(df2.to_string())

# Check proc_po_lines columns
print("\n=== proc_po_lines columns ===")
df3 = execute_query("""
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'proc_po_lines'
ORDER BY ordinal_position
""")
print(df3.to_string())

# Join path: po_headers -> po_lines -> po_distributions
print("\n=== Deloitte PO via lines->distributions ===")
df4 = execute_query("""
SELECT s.supplier_name, po.po_header_id, pol.po_line_id, pod.po_dist_id, pod.cost_centre_id, pod.amount
FROM sup_suppliers s
JOIN proc_po_headers po ON po.supplier_id = s.supplier_id
JOIN proc_po_lines pol ON pol.po_header_id = po.po_header_id
JOIN proc_po_distributions pod ON pod.po_line_id = pol.po_line_id
WHERE s.supplier_name ILIKE '%deloitte%'
LIMIT 5
""")
print(df4.to_string())
