DO $$ DECLARE r RECORD;
BEGIN
  FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname='public') LOOP
    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
  END LOOP;
END $$;

-- Also drop views
DROP VIEW IF EXISTS hcm_employees CASCADE;
DROP VIEW IF EXISTS procurement_quotations CASCADE;
DROP VIEW IF EXISTS procurement_purchase_orders CASCADE;
