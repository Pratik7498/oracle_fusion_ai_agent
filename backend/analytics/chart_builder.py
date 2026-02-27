"""Plotly chart builders — all return fig.to_dict() for JSON serialisation."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Dark theme constants ──
DARK_BG = "rgba(16, 28, 46, 0.95)"
GRID_COLOR = "#1E2D45"
TEXT_COLOR = "#E2E8F0"

_LAYOUT_DEFAULTS = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=DARK_BG,
    font=dict(color=TEXT_COLOR, family="Inter, sans-serif"),
    margin=dict(l=40, r=20, t=50, b=40),
)


def _apply_defaults(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(title=dict(text=title, x=0.5, font=dict(size=16)), **_LAYOUT_DEFAULTS)
    fig.update_xaxes(gridcolor=GRID_COLOR, showgrid=True)
    fig.update_yaxes(gridcolor=GRID_COLOR, showgrid=True)
    return fig


def build_bar_chart(
    data: dict, title: str, x_label: str, y_label: str
) -> dict:
    """Simple bar chart from {label: value} dict. Dark theme."""
    labels = list(data.keys())
    values = list(data.values())
    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color="#3B82F6",
                text=values,
                textposition="outside",
            )
        ]
    )
    fig = _apply_defaults(fig, title)
    fig.update_xaxes(title_text=x_label)
    fig.update_yaxes(title_text=y_label)
    return fig.to_dict()


def build_variance_chart(df: pd.DataFrame, title: str) -> dict:
    """Grouped bar chart: actual vs budget per cost centre."""
    if "cost_centre_name" not in df.columns:
        labels = df["cost_centre"].astype(str).tolist() if "cost_centre" in df.columns else df.index.astype(str).tolist()
    else:
        labels = df["cost_centre_name"].tolist()

    actual = df["actual_amount"].tolist() if "actual_amount" in df.columns else []
    budget = df["budget_amount"].tolist() if "budget_amount" in df.columns else []

    colors_actual = [
        "#EF4444" if a > b else "#22C55E" for a, b in zip(actual, budget)
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Budget", x=labels, y=budget, marker_color="#3B82F6"))
    fig.add_trace(go.Bar(name="Actual", x=labels, y=actual, marker_color=colors_actual))

    if "variance_pct" in df.columns:
        for i, (lbl, pct) in enumerate(zip(labels, df["variance_pct"])):
            fig.add_annotation(
                x=lbl,
                y=max(actual[i], budget[i]) * 1.05,
                text=f"{pct:+.1f}%",
                showarrow=False,
                font=dict(size=11, color="#EF4444" if pct > 0 else "#22C55E"),
            )

    fig = _apply_defaults(fig, title)
    fig.update_layout(barmode="group")
    return fig.to_dict()


def build_delta_chart(
    original: float, revised: float, label: str
) -> dict:
    """Side-by-side bar chart: Original vs Revised with delta annotation."""
    delta_pct = round(((revised - original) / original) * 100, 2)
    revised_color = "#22C55E" if delta_pct >= 0 else "#EF4444"

    fig = go.Figure(
        data=[
            go.Bar(
                x=["Original", "Revised"],
                y=[original, revised],
                marker_color=["#3B82F6", revised_color],
                text=[f"£{original:,.0f}", f"£{revised:,.0f}"],
                textposition="outside",
            )
        ]
    )
    fig.add_annotation(
        x=0.5,
        y=max(original, revised) * 1.12,
        xref="paper",
        text=f"Δ {delta_pct:+.1f}%",
        showarrow=False,
        font=dict(size=20, color=revised_color),
    )
    fig = _apply_defaults(fig, f"Delta Analysis — {label}")
    return fig.to_dict()


def build_aging_chart(aging_data: dict, title: str) -> dict:
    """Horizontal bar chart showing 4 aging buckets with colour gradient."""
    bucket_labels = ["0–30 days", "31–60 days", "61–90 days", "90+ days"]
    bucket_keys = ["0_30", "31_60", "61_90", "90_plus"]
    colors = ["#22C55E", "#EAB308", "#F97316", "#EF4444"]

    amounts = [aging_data.get(k, {}).get("amount", 0) for k in bucket_keys]
    counts = [aging_data.get(k, {}).get("count", 0) for k in bucket_keys]
    hover_text = [f"Count: {c} | £{a:,.0f}" for c, a in zip(counts, amounts)]

    fig = go.Figure(
        data=[
            go.Bar(
                y=bucket_labels,
                x=amounts,
                orientation="h",
                marker_color=colors,
                text=[f"£{a:,.0f} ({c})" for a, c in zip(amounts, counts)],
                textposition="outside",
                hovertext=hover_text,
            )
        ]
    )
    fig = _apply_defaults(fig, title)
    return fig.to_dict()
