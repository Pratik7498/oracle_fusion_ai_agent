"""Unit tests for backend/query_intent_parser.py — no DB or LLM required."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from backend.query_intent_parser import parse_intent


# ── Metric detection ─────────────────────────────────────────────────────────

def test_budget_metric():
    intent = parse_intent("what was the last year budget amount")
    assert intent["metric"] == "budget"


def test_actual_metric():
    intent = parse_intent("show actual spend for engineering this quarter")
    assert intent["metric"] == "gl_actual"


def test_salary_metric():
    intent = parse_intent("salary range for software engineer")
    assert intent["metric"] == "salary"


def test_headcount_metric():
    intent = parse_intent("how many employees are active")
    assert intent["metric"] in {"headcount", "employee"}


def test_spend_metric():
    intent = parse_intent("total spend by department")
    assert intent["metric"] == "spend"


def test_supplier_metric():
    intent = parse_intent("which suppliers received highest payments")
    assert intent["metric"] in {"supplier", "payment"}


def test_invoice_metric():
    intent = parse_intent("show overdue AP invoices")
    assert intent["metric"] == "invoice"


# ── Aggregation detection ────────────────────────────────────────────────────

def test_sum_aggregation():
    intent = parse_intent("total budget for engineering")
    assert intent["aggregation"] == "SUM"


def test_count_aggregation():
    intent = parse_intent("how many employees are in the sales team")
    assert intent["aggregation"] == "COUNT"


def test_avg_aggregation():
    intent = parse_intent("average salary by department")
    assert intent["aggregation"] == "AVG"


def test_max_aggregation():
    intent = parse_intent("highest paid employees")
    assert intent["aggregation"] == "MAX"


# ── Dimension detection ──────────────────────────────────────────────────────

def test_department_dimension():
    intent = parse_intent("total spend by department")
    assert intent["dimension"] == "department"


def test_supplier_dimension():
    intent = parse_intent("total invoice amount by supplier")
    assert intent["dimension"] == "supplier"


def test_cost_centre_dimension():
    intent = parse_intent("budget variance by cost centre")
    assert intent["dimension"] == "cost_centre"


def test_month_dimension():
    intent = parse_intent("show AP payments by month")
    assert intent["dimension"] == "month"


# ── Time filter detection ────────────────────────────────────────────────────

def test_last_year_filter():
    intent = parse_intent("what was the last year budget amount")
    assert intent["time_filter"] == "last_year"


def test_current_year_filter():
    intent = parse_intent("show budget this year")
    assert intent["time_filter"] == "current_year"


def test_current_quarter_filter():
    intent = parse_intent("show invoices this quarter")
    assert intent["time_filter"] == "current_quarter"


def test_fiscal_year_filter():
    intent = parse_intent("budget vs actual for FY2024")
    assert intent["time_filter"] == "fiscal_year_2024"


def test_no_time_filter():
    intent = parse_intent("how many employees are active")
    assert intent["time_filter"] is None


# ── Synonym resolution ───────────────────────────────────────────────────────

def test_staff_synonym():
    intent = parse_intent("how many staff are in Engineering")
    # 'staff' should resolve to 'employee' metric or headcount
    assert intent["metric"] in {"employee", "headcount", "salary"}
    assert any("staff" in s for s in intent["synonyms_resolved"])


def test_spend_synonym_is_spend():
    intent = parse_intent("total expenditure by department")
    assert intent["metric"] == "spend"


def test_vendor_synonym():
    intent = parse_intent("which vendors received highest payments")
    # vendor→supplier synonym should be resolved
    assert any("vendor" in s for s in intent["synonyms_resolved"])


def test_cost_center_synonym():
    intent = parse_intent("budget variance by cost center")
    assert intent["dimension"] == "cost_centre"


# ── Cross-domain multi-metric queries ────────────────────────────────────────

def test_variance_metric():
    intent = parse_intent("actual vs budget variance by cost centre")
    assert intent["metric"] in {"gl_variance", "gl_actual", "budget"}


def test_normalised_query_returned():
    intent = parse_intent("headcount by dept")
    assert "normalised_query" in intent
    assert isinstance(intent["normalised_query"], str)
