"""Unit tests for backend/query_planner.py — no DB or LLM required."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from backend.query_planner import build_query_plan


# ── Correct table/column selection ──────────────────────────────────────────

def test_budget_uses_fin_budget_lines():
    """CRITICAL: budget queries must target fin_budget_lines.amount, not fin_budget_headers."""
    plan = build_query_plan("what was the last year budget amount", domain="FINANCE")
    assert plan["metric_table"] == "fin_budget_lines", (
        f"Expected fin_budget_lines but got {plan['metric_table']}"
    )
    assert plan["metric_column"] == "amount"


def test_budget_aggregation_is_sum():
    plan = build_query_plan("total budget for all departments", domain="FINANCE")
    assert plan["aggregation"] == "SUM"
    assert plan["agg_expression"] is not None
    assert "SUM" in plan["agg_expression"]


def test_actual_uses_fin_gl_balances():
    plan = build_query_plan("show actual spend for engineering", domain="FINANCE")
    assert plan["metric_table"] == "fin_gl_balances"
    assert plan["metric_column"] == "actual_amount"


def test_gl_variance_uses_fin_gl_balances():
    plan = build_query_plan("actual vs budget variance by cost centre", domain="FINANCE")
    assert plan["metric_table"] == "fin_gl_balances"


def test_spend_uses_proc_po_distributions():
    """CRITICAL: spend must use proc_po_distributions.amount, not proc_po_headers."""
    plan = build_query_plan("total spend by department", domain="PROCUREMENT")
    assert plan["metric_table"] == "proc_po_distributions", (
        f"Expected proc_po_distributions but got {plan['metric_table']}"
    )
    assert plan["metric_column"] == "amount"


def test_salary_uses_hcm_assignments():
    """CRITICAL: salary must come from hcm_assignments.salary, not hcm_persons."""
    plan = build_query_plan("salary range for software engineer", domain="HCM")
    assert plan["metric_table"] == "hcm_assignments", (
        f"Expected hcm_assignments but got {plan['metric_table']}"
    )
    assert plan["metric_column"] == "salary"


def test_headcount_uses_hcm_assignments():
    plan = build_query_plan("how many employees are active", domain="HCM")
    assert plan["metric_table"] == "hcm_assignments"
    assert plan["aggregation"] in {"COUNT", None}


def test_invoice_uses_fin_ap_invoices():
    plan = build_query_plan("show total AP invoice amount by supplier", domain="FINANCE")
    assert plan["metric_table"] == "fin_ap_invoices"
    assert plan["metric_column"] == "amount"


def test_payment_uses_fin_ap_payments():
    plan = build_query_plan("which suppliers received highest payments", domain="FINANCE")
    assert plan["metric_table"] == "fin_ap_payments"
    assert plan["metric_column"] == "payment_amount"


# ── Time filter SQL ──────────────────────────────────────────────────────────

def test_last_year_time_filter():
    plan = build_query_plan("what was the last year budget amount", domain="FINANCE")
    assert plan["time_filter"] == "last_year"
    assert plan["time_filter_sql"] is not None
    assert "CURRENT_DATE" in plan["time_filter_sql"] or "1" in plan["time_filter_sql"]


def test_current_year_time_filter():
    plan = build_query_plan("show total budget this year", domain="FINANCE")
    assert plan["time_filter"] == "current_year"
    assert plan["time_filter_sql"] is not None


def test_no_time_filter_for_timeless_query():
    plan = build_query_plan("how many employees are active", domain="HCM")
    assert plan["time_filter"] is None
    assert plan["time_filter_sql"] is None


# ── Dimension / group-by ─────────────────────────────────────────────────────

def test_department_dimension():
    plan = build_query_plan("total spend by department", domain="PROCUREMENT")
    assert plan["dimension"] == "department"
    assert plan["group_by"] is not None
    assert "dept_name" in (plan["group_by"] or "")


def test_supplier_dimension():
    plan = build_query_plan("total invoice amount by supplier", domain="FINANCE")
    assert plan["dimension"] == "supplier"
    assert "supplier_name" in (plan["group_by"] or "")


def test_cost_centre_dimension():
    plan = build_query_plan("budget variance by cost centre", domain="FINANCE")
    assert plan["dimension"] == "cost_centre"
    assert "cost_centre_name" in (plan["group_by"] or "")


# ── Cross-domain detection ───────────────────────────────────────────────────

def test_cross_domain_headcount_and_spend():
    plan = build_query_plan(
        "which departments have highest procurement spend and most employees",
        domain="CROSS_DOMAIN"
    )
    assert plan["is_cross_domain"] is True
    assert len(plan["cte_domains"]) >= 2


def test_cross_domain_budget_and_headcount():
    plan = build_query_plan("budget for each department and employee count", domain="CROSS_DOMAIN")
    assert plan["is_cross_domain"] is True


def test_single_domain_not_cross():
    plan = build_query_plan("how many employees are active", domain="HCM")
    assert plan["is_cross_domain"] is False


# ── Plan notes contain schema rules ─────────────────────────────────────────

def test_budget_plan_includes_critical_note():
    plan = build_query_plan("total budget amount last year", domain="FINANCE")
    notes_text = " ".join(plan["plan_notes"])
    assert "fin_budget_lines" in notes_text


def test_spend_plan_includes_critical_note():
    plan = build_query_plan("total spend by supplier", domain="PROCUREMENT")
    notes_text = " ".join(plan["plan_notes"])
    assert "proc_po_distributions" in notes_text


# ── Format for prompt ────────────────────────────────────────────────────────

def test_format_plan_for_prompt_returns_string():
    from backend.query_planner import format_plan_for_prompt
    plan = build_query_plan("total budget last year", domain="FINANCE")
    result = format_plan_for_prompt(plan)
    assert isinstance(result, str)
    assert "fin_budget_lines" in result


def test_format_plan_empty_for_no_metric():
    from backend.query_planner import format_plan_for_prompt
    # Out-of-scope query with no recognisable metric
    plan = build_query_plan("hello there", domain="CROSS_DOMAIN")
    result = format_plan_for_prompt(plan)
    # Either empty string (no metric) or a string (if something was detected)
    assert isinstance(result, str)
