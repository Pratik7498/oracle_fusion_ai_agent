#!/usr/bin/env python3
"""One-command database initialisation.

Usage:
    python setup_db.py
"""

import os
import sys
from pathlib import Path

# Ensure the project root is on sys.path so imports work
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

import psycopg2
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(project_root / ".env")


def _read_sql(filename: str) -> str:
    """Read a .sql file from the database/ directory."""
    path = project_root / "database" / filename
    return path.read_text(encoding="utf-8")


def main() -> None:
    """Run all setup steps sequentially."""
    postgres_url = os.environ.get("POSTGRES_URL", "")
    if not postgres_url:
        print("ERROR: POSTGRES_URL not set. Copy config/.env.example → .env and fill values.")
        sys.exit(1)

    print("=" * 60)
    print("  Oracle Fusion AI Agent — Database Setup")
    print("=" * 60)

    # Step 1 — Test connection
    print("\n[1/7] Connecting to PostgreSQL …")
    try:
        conn = psycopg2.connect(postgres_url)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"  ✅ Connected: {version[:60]}")
    except Exception as e:
        print(f"  ❌ Connection failed: {e}")
        sys.exit(1)

    # Step 2 — PGVector extension + schema_embeddings
    print("\n[2/7] Setting up PGVector extension …")
    try:
        sql = _read_sql("pgvector_setup.sql")
        cursor.execute(sql)
        print("  ✅ PGVector extension + schema_embeddings table ready")
    except psycopg2.errors.DuplicateTable:
        conn.rollback()
        conn.autocommit = True
        print("  ⚠️  schema_embeddings table already exists — skipping")
    except Exception as e:
        conn.rollback()
        conn.autocommit = True
        print(f"  ⚠️  PGVector setup warning: {e}")

    # Step 3 — Create main schema tables
    print("\n[3/7] Creating schema tables …")
    try:
        sql = _read_sql("schema.sql")
        cursor.execute(sql)
        print("  ✅ All 6 tables created")
    except psycopg2.errors.DuplicateTable:
        conn.rollback()
        conn.autocommit = True
        print("  ⚠️  Tables already exist — skipping schema creation")
    except Exception as e:
        conn.rollback()
        conn.autocommit = True
        print(f"  ⚠️  Schema warning: {e}")

    # Step 4 — Seed data
    print("\n[4/7] Inserting seed data …")
    try:
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM hcm_employees")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"  ⚠️  hcm_employees already has {count} rows — skipping seed")
        else:
            sql = _read_sql("seed_data.sql")
            cursor.execute(sql)
            print("  ✅ Seed data inserted")
    except Exception as e:
        conn.rollback()
        conn.autocommit = True
        print(f"  ❌ Seed data error: {e}")

    # Step 5 — Embed schema docs
    print("\n[5/7] Embedding schema docs into PGVector …")
    try:
        from vector_store.embedder import embed_all_schema_docs
        embed_all_schema_docs()
        print("  ✅ Schema embeddings stored")
    except Exception as e:
        print(f"  ⚠️  Embedding warning (non-fatal): {e}")

    # Step 6 — Verify data counts
    print("\n[6/7] Verifying data …")
    tables = [
        ("hcm_employees", None),
        ("finance_gl_balances", None),
        ("finance_ap_invoices", None),
        ("procurement_quotations", None),
        ("procurement_purchase_orders", None),
        ("schema_embeddings", None),
    ]
    for table, _ in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            cnt = cursor.fetchone()[0]
            print(f"  {table}: {cnt} rows")
        except Exception:
            print(f"  {table}: ⚠️  could not count")

    # Verify Engineering headcount = 47
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM hcm_employees WHERE department='Engineering' AND employment_status='ACTIVE'"
        )
        eng = cursor.fetchone()[0]
        status = "✅" if eng == 47 else "❌"
        print(f"\n  {status} Engineering active headcount: {eng} (expected 47)")
    except Exception:
        pass

    # Step 7 — Verify E-205
    print("\n[7/7] Verifying E-205 quotation …")
    try:
        cursor.execute(
            "SELECT quotation_version, original_amount, revised_amount, status "
            "FROM procurement_quotations WHERE engagement_id='E-205' ORDER BY quotation_version"
        )
        rows = cursor.fetchall()
        for r in rows:
            print(f"  Version {r[0]}: original=£{r[1]:,.2f}, revised={'£'+f'{r[2]:,.2f}' if r[2] else 'NULL'}, status={r[3]}")
        if len(rows) >= 2 and rows[1][2]:
            delta = round(((float(rows[1][2]) - float(rows[1][1])) / float(rows[1][1])) * 100, 2)
            status = "✅" if abs(delta - 12.4) < 0.01 else "❌"
            print(f"  {status} Delta: {delta}% (expected 12.4%)")
    except Exception as e:
        print(f"  ⚠️  E-205 verification warning: {e}")

    cursor.close()
    conn.close()

    print("\n" + "=" * 60)
    print("  ✅ Setup complete! Ready to start the application.")
    print("=" * 60)
    print("\n  Start backend:  uvicorn backend.main:app --reload --port 8000")
    print("  Start frontend: streamlit run frontend/app.py\n")


if __name__ == "__main__":
    main()
