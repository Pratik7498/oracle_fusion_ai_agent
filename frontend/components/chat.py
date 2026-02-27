"""Chat display component helpers for the Streamlit UI."""

from typing import Optional
import plotly.graph_objects as go


def render_domain_badge(domain: str) -> str:
    """Return an HTML badge span for a domain."""
    colors = {
        "HCM": "#22C55E",
        "FINANCE": "#A855F7",
        "PROCUREMENT": "#F59E0B",
        "CROSS_DOMAIN": "#3B82F6",
    }
    bg = colors.get(domain, "#64748B")
    return (
        f'<span style="display:inline-block;padding:2px 10px;border-radius:12px;'
        f'font-size:0.75rem;font-weight:600;color:#fff;background:{bg}">{domain}</span>'
    )


def format_metrics_html(metrics: dict) -> str:
    """Return an HTML string for a metrics summary card."""
    if not metrics:
        return ""
    formatted = metrics.get("formatted")
    if formatted:
        return (
            f'<div style="background:#111827;border:1px solid #1E2D45;'
            f'border-radius:10px;padding:12px 16px;color:#E2E8F0;margin:8px 0">'
            f"{formatted}</div>"
        )
    items = ""
    for k, v in metrics.items():
        if isinstance(v, dict):
            continue
        label = k.replace("_", " ").title()
        items += (
            f'<div style="text-align:center;flex:1">'
            f'<div style="font-size:1.4rem;font-weight:700;color:#E2E8F0">{v}</div>'
            f'<div style="font-size:0.75rem;color:#94A3B8">{label}</div></div>'
        )
    if items:
        return (
            f'<div style="display:flex;gap:16px;background:#111827;'
            f'border:1px solid #1E2D45;border-radius:10px;padding:12px 16px;'
            f'margin:8px 0">{items}</div>'
        )
    return ""


def build_chart_figure(chart_data: Optional[dict]) -> Optional[go.Figure]:
    """Convert chart_data dict back into a Plotly Figure."""
    if not chart_data:
        return None
    try:
        fig = go.Figure(chart_data)
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig
    except Exception:
        return None
