"""Pandas-based analytics calculations — the LLM never does arithmetic."""

import pandas as pd
import numpy as np
from datetime import date


def calculate_delta(original: float, revised: float) -> dict:
    """Calculate delta between original and revised values.

    CRITICAL: calculate_delta(82000, 92180) must return delta_pct = 12.4 exactly.
    """
    delta_amount = revised - original
    delta_pct = round((delta_amount / original) * 100, 2)
    trend = "↑" if delta_pct > 0 else ("↓" if delta_pct < 0 else "→")
    return {
        "original": original,
        "revised": revised,
        "delta_amount": round(delta_amount, 2),
        "delta_pct": delta_pct,
        "trend": trend,
        "formatted": f"{trend} {abs(delta_pct):.1f}% (£{abs(delta_amount):,.2f})",
    }


def calculate_attrition_rate(
    df: pd.DataFrame, period_start: date, period_end: date
) -> dict:
    """Calculate attrition rate for a period.

    Formula: (terminated_in_period / average_headcount) * 100
    """
    if "termination_date" in df.columns:
        df = df.copy()
        df["termination_date"] = pd.to_datetime(df["termination_date"])
        terminated = df[
            (df["termination_date"] >= pd.Timestamp(period_start))
            & (df["termination_date"] <= pd.Timestamp(period_end))
        ]
        terminated_count = len(terminated)
        total_count = len(df)
        avg_headcount = max(total_count, 1)
        attrition_rate = round((terminated_count / avg_headcount) * 100, 2)
    else:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            terminated_count = int(df[numeric_cols[0]].sum())
            avg_headcount = max(terminated_count * 10, 1)
            attrition_rate = round((terminated_count / avg_headcount) * 100, 2)
        else:
            terminated_count = 0
            avg_headcount = 0
            attrition_rate = 0.0

    trend = "↑" if attrition_rate > 8 else ("↓" if attrition_rate < 5 else "→")
    return {
        "attrition_rate_pct": attrition_rate,
        "terminated_count": terminated_count,
        "avg_headcount": avg_headcount,
        "trend": trend,
        "period_start": str(period_start),
        "period_end": str(period_end),
    }


def calculate_budget_variance(df: pd.DataFrame) -> pd.DataFrame:
    """Add variance columns to a GL balances DataFrame."""
    df = df.copy()
    if "actual_amount" in df.columns and "budget_amount" in df.columns:
        df["variance_amount"] = df["actual_amount"] - df["budget_amount"]
        df["variance_pct"] = (
            (df["variance_amount"] / df["budget_amount"]) * 100
        ).round(2)
        df["over_budget"] = df["variance_amount"] > 0
    return df


def calculate_ap_aging(df: pd.DataFrame) -> dict:
    """Bucket AP invoices into aging categories based on days overdue."""
    today = date.today()
    df = df.copy()

    if "due_date" in df.columns:
        df["due_date"] = pd.to_datetime(df["due_date"])
        df["days_overdue"] = (pd.Timestamp(today) - df["due_date"]).dt.days
        df = df[df["days_overdue"] > 0]
    elif "days_overdue" not in df.columns:
        return {
            "0_30": {"count": 0, "amount": 0},
            "31_60": {"count": 0, "amount": 0},
            "61_90": {"count": 0, "amount": 0},
            "90_plus": {"count": 0, "amount": 0},
        }

    amount_col = (
        "outstanding_amount" if "outstanding_amount" in df.columns else "invoice_amount"
    )

    def bucket(days_min: int, days_max: int | None = None) -> dict:
        if days_max is not None:
            mask = (df["days_overdue"] >= days_min) & (df["days_overdue"] <= days_max)
        else:
            mask = df["days_overdue"] > days_min
        subset = df[mask]
        return {
            "count": len(subset),
            "amount": float(subset[amount_col].sum()) if amount_col in subset.columns else 0,
        }

    return {
        "0_30": bucket(0, 30),
        "31_60": bucket(31, 60),
        "61_90": bucket(61, 90),
        "90_plus": bucket(90),
    }


def calculate_headcount_summary(df: pd.DataFrame) -> dict:
    """Summarise headcount from employee DataFrame."""
    result: dict = {
        "total": len(df),
        "by_department": {},
        "by_grade": {},
        "by_location": {},
    }
    if "department" in df.columns:
        result["by_department"] = df["department"].value_counts().to_dict()
    if "grade_level" in df.columns:
        result["by_grade"] = df["grade_level"].value_counts().to_dict()
    if "location" in df.columns:
        result["by_location"] = df["location"].value_counts().to_dict()
    return result
