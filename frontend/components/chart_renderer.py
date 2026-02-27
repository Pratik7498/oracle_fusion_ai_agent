"""Chart renderer helpers for the Streamlit frontend."""

from typing import Optional
import plotly.graph_objects as go


def render_chart(chart_data: Optional[dict]) -> Optional[go.Figure]:
    """Reconstruct a Plotly Figure from a serialised chart_data dict.

    Returns None if chart_data is empty or invalid.
    """
    if not chart_data:
        return None
    try:
        fig = go.Figure(chart_data)
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig
    except Exception:
        return None


def apply_dark_theme(fig: go.Figure) -> go.Figure:
    """Apply consistent dark theme to any Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(16, 28, 46, 0.95)",
        font=dict(color="#E2E8F0", family="Inter, sans-serif"),
        margin=dict(l=40, r=20, t=50, b=40),
    )
    fig.update_xaxes(gridcolor="#1E2D45", showgrid=True)
    fig.update_yaxes(gridcolor="#1E2D45", showgrid=True)
    return fig
