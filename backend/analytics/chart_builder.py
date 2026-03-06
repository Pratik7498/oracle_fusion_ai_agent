"""Plotly chart builders — all return fig.to_dict() for JSON serialisation."""

import re
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Keywords that indicate the user wants a chart ──
# Only include EXPLICIT visual requests — not analytical terms like 'breakdown', 'trend', 'distribution'
_CHART_KEYWORDS = {
    "chart", "graph", "plot", "visualize", "visualise", "visual",
    "diagram", "pie chart", "bar chart", "line chart",
    "histogram", "show chart", "display chart", "draw a chart",
    "show me a graph", "show graph", "draw graph",
}


def wants_chart(query: str) -> bool:
    """Return True if the query explicitly asks for a chart/visual."""
    q = query.lower()
    return any(kw in q for kw in _CHART_KEYWORDS)

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


def _extract_parent_dept(name: str) -> str:
    """Extract the parent department prefix from a sub-department name.

    E.g. 'Analytics 1012' -> 'Analytics',  'Legal 2361' -> 'Legal',
         'HR-Benefits 102' -> 'HR-Benefits',  'Finance' -> 'Finance'
    """
    # Strip trailing numeric codes (space + digits at end)
    parent = re.sub(r'\s+\d+$', '', name.strip())
    return parent if parent else name.strip()


def _aggregate_by_parent_dept(
    df: pd.DataFrame, label_col: str, numeric_cols: list[str], top_n: int = 30
) -> pd.DataFrame:
    """Collapse sub-department rows into parent departments by summing numerics.

    Only activates when the label column has > 30 unique values AND at least
    some labels look like '<Word> <number>' sub-department codes.
    Returns a DataFrame sorted by the absolute value of the first numeric col,
    capped at top_n rows.
    """
    unique_labels = df[label_col].astype(str).unique()
    n_unique = len(unique_labels)

    # Detect sub-department pattern: many rows AND trailing digits present
    has_subcode = any(re.search(r'\s+\d+$', lbl) for lbl in unique_labels[:50])

    if n_unique > 30 and has_subcode:
        # Build parent column and aggregate
        df = df.copy()
        df["_parent"] = df[label_col].astype(str).map(_extract_parent_dept)
        agg_dict = {nc: "sum" for nc in numeric_cols if nc in df.columns}
        df = df.groupby("_parent", as_index=False).agg(agg_dict)
        df = df.rename(columns={"_parent": label_col})

    # Sort by absolute value of first numeric metric descending, cap at top_n
    if numeric_cols and numeric_cols[0] in df.columns:
        df = df.reindex(
            df[numeric_cols[0]].abs().sort_values(ascending=False).index
        ).head(top_n)
    else:
        df = df.head(top_n)

    return df.reset_index(drop=True)


def auto_chart(df: pd.DataFrame, query: str) -> dict | None:
    """Smart auto-chart: pick the best chart type based on DataFrame shape and query.

    Returns a Plotly figure dict or None if the data isn't suited for a chart.
    """
    if df is None or df.empty or len(df) < 2:
        return None

    # Convert Decimal/object columns to numeric where possible
    # (PostgreSQL returns Decimal which pandas stores as dtype 'object')
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass  # genuinely text — leave as-is

    query_lower = query.lower()
    cols = list(df.columns)
    n_cols = len(cols)
    n_rows = len(df)

    # Identify column types
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    text_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if not numeric_cols:
        return None  # nothing to chart

    # ── Handle all-numeric DataFrames (e.g. EXTRACT(MONTH) + SUM(amount)) ──
    # Treat first numeric column as label/axis if no text columns exist
    if not text_cols and len(numeric_cols) >= 2:
        # Promote first numeric column to label column
        label_col = numeric_cols[0]
        text_cols = [label_col]
        numeric_cols = numeric_cols[1:]
        # Convert the label column to string for display
        df[label_col] = df[label_col].astype(int).astype(str)

    # ── Force line chart when user explicitly requests one ──
    if "line chart" in query_lower and len(text_cols) >= 1 and len(numeric_cols) >= 1:
        # Prefer a display-label text column (e.g. 'month_label', 'period_name')
        # over a raw ordinal col name when multiple text cols exist.
        _label_priority = ["label", "name", "period", "month", "date", "quarter", "year"]
        label_col = next(
            (c for c in text_cols if any(p in c.lower() for p in _label_priority)),
            text_cols[0],
        )

        # Skip ordinal/sort-key numerics (invoice_month, quarter_num etc. max ≤ 366).
        # Pick the first column whose max value looks like a real metric (> 366).
        value_col = next(
            (nc for nc in numeric_cols if df[nc].max() > 366),
            numeric_cols[-1],  # fallback: last numeric col
        )

        labels = df[label_col].astype(str).tolist()
        values = df[value_col].tolist()
        title = f"{value_col.replace('_', ' ').title()} by {label_col.replace('_', ' ').title()}"
        fig = go.Figure(
            data=[go.Scatter(
                x=labels, y=values,
                mode="lines+markers",
                line=dict(color="#3B82F6", width=2),
                marker=dict(size=8, color="#22C55E"),
                fill="tozeroy",
                fillcolor="rgba(59, 130, 246, 0.1)",
            )]
        )
        fig = _apply_defaults(fig, title)
        fig.update_xaxes(title_text=label_col.replace("_", " ").title())
        fig.update_yaxes(title_text=value_col.replace("_", " ").title())
        return fig.to_dict()

    # ── Heuristic 1: Category + single numeric = bar chart ──
    if len(text_cols) >= 1 and len(numeric_cols) >= 1:
        label_col = text_cols[0]
        value_col = numeric_cols[0]

        # ── Aggregate sub-departments into parent departments when needed ──
        # This handles queries like "department-wise breakdown" where the SQL
        # returns one row per sub-department (e.g. 'Analytics 1012') but the
        # user wants aggregated totals per top-level department.
        plot_df = _aggregate_by_parent_dept(df, label_col, numeric_cols, top_n=30)

        labels = plot_df[label_col].astype(str).tolist()
        values = plot_df[value_col].tolist()

        # Pick chart title from column names
        title = f"{value_col.replace('_', ' ').title()} by {label_col.replace('_', ' ').title()}"

        # Check if pie chart makes sense (proportion/distribution, small categories)
        use_pie = (
            len(labels) <= 10
            and all(v >= 0 for v in values if v is not None)
            and any(w in query_lower for w in ["distribution", "breakdown", "proportion", "split", "share", "pie"])
        )

        if use_pie:
            fig = go.Figure(
                data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    marker=dict(colors=px.colors.qualitative.Set2),
                    textinfo="label+percent",
                    textposition="outside",
                )]
            )
            fig = _apply_defaults(fig, title)
            return fig.to_dict()

        # Check if we have 2+ numeric cols (grouped bar)
        if len(numeric_cols) >= 2 and len(text_cols) >= 1:
            fig = go.Figure()
            bar_colors = ["#3B82F6", "#22C55E", "#F59E0B", "#EF4444", "#8B5CF6"]
            for i, nc in enumerate(numeric_cols[:4]):
                col_values = plot_df[nc].tolist() if nc in plot_df.columns else []
                fig.add_trace(go.Bar(
                    name=nc.replace("_", " ").title(),
                    x=labels,
                    y=col_values,
                    marker_color=bar_colors[i % len(bar_colors)],
                ))
            fig = _apply_defaults(fig, title)
            fig.update_layout(barmode="group")
            return fig.to_dict()

        # Check if time-series (period_name, date, month, quarter in label col)
        is_time = any(t in label_col.lower() for t in ["period", "date", "month", "quarter", "year"])
        if is_time and n_rows >= 3:
            fig = go.Figure(
                data=[go.Scatter(
                    x=labels,
                    y=values,
                    mode="lines+markers",
                    line=dict(color="#3B82F6", width=2),
                    marker=dict(size=6, color="#22C55E"),
                    fill="tozeroy",
                    fillcolor="rgba(59, 130, 246, 0.1)",
                )]
            )
            fig = _apply_defaults(fig, title)
            fig.update_xaxes(title_text=label_col.replace("_", " ").title())
            fig.update_yaxes(title_text=value_col.replace("_", " ").title())
            return fig.to_dict()

        # Default: bar chart
        # Color bars based on sign (positive=green, negative=red) if variance-like
        is_variance = any(w in value_col.lower() for w in ["variance", "diff", "delta", "pct"])
        if is_variance:
            colors = ["#EF4444" if v > 0 else "#22C55E" for v in values]
        else:
            colors = "#3B82F6"

        fig = go.Figure(
            data=[go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=[f"{v:,.1f}" if isinstance(v, float) else str(v) for v in values],
                textposition="outside",
            )]
        )
        fig = _apply_defaults(fig, title)
        fig.update_xaxes(title_text=label_col.replace("_", " ").title())
        fig.update_yaxes(title_text=value_col.replace("_", " ").title())
        return fig.to_dict()

    # ── Heuristic 2: All numeric, small rows = horizontal bar ──
    if len(numeric_cols) >= 1 and not text_cols and n_rows <= 10:
        fig = go.Figure(
            data=[go.Bar(
                y=[str(i) for i in df.index],
                x=df[numeric_cols[0]].tolist(),
                orientation="h",
                marker_color="#3B82F6",
            )]
        )
        fig = _apply_defaults(fig, numeric_cols[0].replace("_", " ").title())
        return fig.to_dict()

    return None
