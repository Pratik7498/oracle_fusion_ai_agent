"""Unit tests for backend/analytics/calculations.py"""

import pytest
import pandas as pd
import numpy as np
from datetime import date, timedelta

# Add project root to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.analytics.calculations import (
    calculate_delta,
    calculate_attrition_rate,
    calculate_budget_variance,
    calculate_ap_aging,
    calculate_headcount_summary,
)


# ── Delta tests ──

def test_delta_e205():
    """CRITICAL: E-205 must return exactly 12.4%."""
    result = calculate_delta(82000, 92180)
    assert result["delta_pct"] == pytest.approx(12.4, rel=0.001)
    assert result["delta_amount"] == pytest.approx(10180.0, rel=0.001)
    assert result["trend"] == "↑"


def test_delta_positive():
    result = calculate_delta(100, 115)
    assert result["delta_pct"] == 15.0
    assert result["trend"] == "↑"


def test_delta_negative():
    result = calculate_delta(100, 85)
    assert result["delta_pct"] == -15.0
    assert result["trend"] == "↓"


def test_delta_zero():
    result = calculate_delta(100, 100)
    assert result["delta_pct"] == 0.0
    assert result["trend"] == "→"


# ── Budget variance tests ──

def test_budget_variance_over():
    df = pd.DataFrame({"actual_amount": [162000], "budget_amount": [150000]})
    result = calculate_budget_variance(df)
    assert result["over_budget"].iloc[0] is True or result["over_budget"].iloc[0] == True
    assert result["variance_pct"].iloc[0] == pytest.approx(8.0, rel=0.01)


def test_budget_variance_under():
    df = pd.DataFrame({"actual_amount": [140000], "budget_amount": [150000]})
    result = calculate_budget_variance(df)
    assert result["over_budget"].iloc[0] is False or result["over_budget"].iloc[0] == False


# ── AP aging tests ──

def test_ap_aging_buckets():
    today = date.today()
    df = pd.DataFrame({
        "due_date": [
            today - timedelta(days=15),   # 0-30 bucket
            today - timedelta(days=45),   # 31-60 bucket
            today - timedelta(days=75),   # 61-90 bucket
            today - timedelta(days=120),  # 90+ bucket
        ],
        "outstanding_amount": [1000, 2000, 3000, 4000],
    })
    result = calculate_ap_aging(df)
    assert result["0_30"]["count"] == 1
    assert result["31_60"]["count"] == 1
    assert result["61_90"]["count"] == 1
    assert result["90_plus"]["count"] == 1
    assert result["0_30"]["amount"] == 1000
    assert result["90_plus"]["amount"] == 4000


# ── Headcount summary tests ──

def test_headcount_summary():
    df = pd.DataFrame({
        "department": ["Engineering", "Engineering", "Finance", "HR"],
        "grade_level": ["G5", "G6", "G5", "G4"],
        "location": ["London", "Remote", "London", "Manchester"],
    })
    result = calculate_headcount_summary(df)
    assert result["total"] == 4
    assert result["by_department"]["Engineering"] == 2
    assert result["by_department"]["Finance"] == 1
    assert "London" in result["by_location"]
