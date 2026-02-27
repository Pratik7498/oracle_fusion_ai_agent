"""Integration / unit tests for the agent layer.

The delta calculation test is a pure unit test (no DB required).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from backend.analytics.calculations import calculate_delta


def test_delta_calc_accuracy():
    """Critical: E-205 delta must be exactly 12.4%."""
    result = calculate_delta(82000, 92180)
    assert result["delta_pct"] == pytest.approx(12.4, abs=0.01)
    assert result["trend"] == "↑"
    assert result["delta_amount"] == pytest.approx(10180.0, abs=0.01)
    assert "12.4" in result["formatted"]


def test_delta_calc_negative():
    """Verify negative deltas produce correct output."""
    result = calculate_delta(100000, 90000)
    assert result["delta_pct"] == -10.0
    assert result["trend"] == "↓"


def test_delta_calc_zero_change():
    """Zero change should have neutral trend."""
    result = calculate_delta(50000, 50000)
    assert result["delta_pct"] == 0.0
    assert result["trend"] == "→"
