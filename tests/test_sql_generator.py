"""Unit tests for backend/agent/sql_generator.py — validate_sql only (no API needed)."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.agent.sql_generator import validate_sql


def test_blocks_insert():
    is_valid, msg = validate_sql("INSERT INTO hcm_employees VALUES (1, 'Test')")
    assert is_valid is False
    assert "INSERT" in msg.upper()


def test_blocks_delete():
    is_valid, msg = validate_sql("DELETE FROM finance_gl_balances")
    assert is_valid is False


def test_blocks_drop():
    is_valid, msg = validate_sql("DROP TABLE hcm_employees")
    assert is_valid is False


def test_allows_select():
    is_valid, sql = validate_sql("SELECT * FROM hcm_employees")
    assert is_valid is True
    assert "LIMIT 1000" in sql


def test_adds_limit():
    _, sql = validate_sql("SELECT department, COUNT(*) FROM hcm_employees GROUP BY department")
    assert "LIMIT 1000" in sql


def test_preserves_existing_limit():
    _, sql = validate_sql("SELECT * FROM hcm_employees LIMIT 50")
    assert "LIMIT 50" in sql
    # Should NOT add a second LIMIT
    assert sql.upper().count("LIMIT") == 1


def test_blocks_truncate():
    is_valid, _ = validate_sql("TRUNCATE TABLE hcm_employees")
    assert is_valid is False


def test_blocks_alter():
    is_valid, _ = validate_sql("ALTER TABLE hcm_employees ADD COLUMN x INT")
    assert is_valid is False


def test_empty_sql():
    is_valid, _ = validate_sql("")
    assert is_valid is False


def test_strips_markdown_fences():
    sql_with_fences = "```sql\nSELECT * FROM hcm_employees\n```"
    is_valid, sql = validate_sql(sql_with_fences)
    assert is_valid is True
    assert sql.strip().startswith("SELECT")
