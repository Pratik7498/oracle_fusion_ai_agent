-- Grant all permissions to poc_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO poc_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO poc_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO poc_user;

-- Verify table count
SELECT 'TABLE_COUNT: ' || COUNT(*) FROM information_schema.tables 
WHERE table_schema='public' AND table_type='BASE TABLE';

-- Verify view count
SELECT 'VIEW_COUNT: ' || COUNT(*) FROM information_schema.views 
WHERE table_schema='public';

-- Verify FK count
SELECT 'FK_COUNT: ' || COUNT(*) FROM information_schema.table_constraints 
WHERE constraint_type='FOREIGN KEY' AND table_schema='public';

-- Verify Engineering active = 47 (via view)
SELECT 'ENG_ACTIVE: ' || COUNT(*) FROM hcm_employees 
WHERE department='Engineering' AND employment_status='ACTIVE';

-- Verify E-205 delta
SELECT 'E205_ORIG: ' || original_amount || ' | E205_REV: ' || revised_amount 
FROM procurement_quotations WHERE engagement_id='E-205' AND quotation_version=2;

-- Row counts per domain
SELECT 'PERSONS: ' || COUNT(*) FROM hcm_persons;
SELECT 'ASSIGNMENTS: ' || COUNT(*) FROM hcm_assignments;
SELECT 'SUPPLIERS: ' || COUNT(*) FROM sup_suppliers;
SELECT 'AP_INVOICES: ' || COUNT(*) FROM fin_ap_invoices;
SELECT 'GL_BALANCES: ' || COUNT(*) FROM fin_gl_balances;
SELECT 'PO_HEADERS: ' || COUNT(*) FROM proc_po_headers;
SELECT 'QUOTATIONS: ' || COUNT(*) FROM proc_quotation_headers;
