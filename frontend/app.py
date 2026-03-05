"""Oracle Fusion AI Agent — Streamlit Chat UI."""

import uuid
import requests
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ── Page config ──
st.set_page_config(page_title="Oracle Fusion AI Agent", page_icon="🔮", layout="wide")

# ── Session state init ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

API_URL = "http://localhost:8000"

# ── Domain badge colours ──
BADGE_COLORS = {
    "HCM": "#22C55E",
    "FINANCE": "#A855F7",
    "PROCUREMENT": "#F59E0B",
    "CROSS_DOMAIN": "#3B82F6",
    "OUT_OF_SCOPE": "#EF4444",
}

# ── Custom CSS ──
st.markdown("""
<style>
    /* Global */
    .stApp { background-color: #0B1320; }
    section[data-testid="stSidebar"] { background-color: #0F1929; }
    .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
    /* Hide default menu/footer */
    #MainMenu, footer, header { visibility: hidden; }
    /* Domain badge */
    .domain-badge {
        display: inline-block; padding: 2px 10px; border-radius: 12px;
        font-size: 0.75rem; font-weight: 600; color: #fff;
    }
    /* Metric card */
    .metric-card {
        background: #111827; border: 1px solid #1E2D45; border-radius: 10px;
        padding: 12px 16px; text-align: center;
    }
    .metric-card .value { font-size: 1.4rem; font-weight: 700; color: #E2E8F0; }
    .metric-card .label { font-size: 0.75rem; color: #94A3B8; }
    /* Sidebar title */
    .sidebar-title { font-size: 1.5rem; font-weight: 700; color: #fff; }
    .sidebar-sub { font-size: 0.85rem; color: #5EEAD4; }
    .section-label { font-family: monospace; font-size: 0.7rem; color: #64748B;
                     text-transform: uppercase; letter-spacing: 2px; margin-top: 16px; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──
with st.sidebar:
    st.markdown('<p class="sidebar-title">🔮 Oracle Fusion AI Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-sub">HCM · Finance · Procurement</p>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<p class="section-label">Quick Queries</p>', unsafe_allow_html=True)

    # Fetch dynamic queries from the API (cached per session)
    if "quick_queries" not in st.session_state:
        try:
            qr = requests.get(f"{API_URL}/sample-queries", timeout=5)
            st.session_state.quick_queries = qr.json().get("queries", {})
        except Exception:
            st.session_state.quick_queries = {
                "HCM": ["Show headcount by department", "What is the attrition rate?",
                         "Show average salary by department", "List top 10 highest paid employees"],
                "FINANCE": ["Which cost centres are over budget?", "Show overdue AP invoices",
                            "Show total AP outstanding", "Show budget vs actual variance"],
                "PROCUREMENT": ["Show purchase orders by status", "Which supplier has highest PO spend?",
                                "Show pending POs", "Show requisitions pending approval"],
            }

    qq = st.session_state.quick_queries

    with st.expander("🟢 HCM / People"):
        for i, q in enumerate(qq.get("HCM", [])):
            if st.button(q, key=f"hcm_q{i}"):
                st.session_state.pending_query = q

    with st.expander("🟣 Finance"):
        for i, q in enumerate(qq.get("FINANCE", [])):
            if st.button(q, key=f"fin_q{i}"):
                st.session_state.pending_query = q

    with st.expander("🟡 Procurement"):
        for i, q in enumerate(qq.get("PROCUREMENT", [])):
            if st.button(q, key=f"proc_q{i}"):
                st.session_state.pending_query = q

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Queries"):
            # Re-fetch dynamic queries
            try:
                qr = requests.get(f"{API_URL}/sample-queries", timeout=5)
                st.session_state.quick_queries = qr.json().get("queries", {})
            except Exception:
                pass
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            if "quick_queries" in st.session_state:
                del st.session_state.quick_queries
            st.rerun()

    st.caption("Powered by Llama 3.3 70B (Groq) + PostgreSQL 15")

# ── Smart table display logic ──
_TABLE_KEYWORDS = {"table", "list", "show all", "details", "show data", "show records",
                   "display data", "view data", "all records", "full data"}
_TABULAR_HINTS = {"for each", "by department", "by supplier", "by cost centre", "per ",
                  "breakdown", "department-wise", "side by side", "compare", "top 10",
                  "top 5", "show me"}
_AGGREGATION_ONLY = {"how many", "what is the total", "count of", "total number",
                     "what is the average", "is there"}


def _should_show_table(query: str, row_count: int, has_chart: bool) -> bool:
    """Decide whether to show the data table based on query intent and data shape."""
    q = query.lower()

    # User explicitly asked for a table → always show
    if any(kw in q for kw in _TABLE_KEYWORDS):
        return True

    # Simple aggregation with small result → answer text is enough
    if any(kw in q for kw in _AGGREGATION_ONLY) and row_count <= 3:
        return False

    # Query implies tabular output → show
    if any(kw in q for kw in _TABULAR_HINTS):
        return True

    # Many rows of data → show (likely a listing query)
    if row_count >= 5:
        return True

    # Chart already shown and small data → chart is the visual, skip table
    if has_chart and row_count <= 10:
        return False

    # Default: show for 3+ rows, hide for 1-2
    return row_count >= 3


# ── Chat history rendering ──
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg.get("answer", ""))

            # Metadata row
            c1, c2, c3, c4 = st.columns(4)
            domain = msg.get("domain", "")
            badge_color = BADGE_COLORS.get(domain, "#64748B")
            c1.markdown(
                f'<span class="domain-badge" style="background:{badge_color}">{domain}</span>',
                unsafe_allow_html=True,
            )
            c2.caption(f"⚡ {msg.get('execution_time_ms', 0)}ms")
            c3.caption(msg.get("query_type", ""))
            row_count = msg.get("row_count", 0)
            if row_count:
                c4.caption(f"{row_count} records")

            # Metrics
            metrics = msg.get("metrics")
            if metrics and isinstance(metrics, dict):
                formatted = metrics.get("formatted")
                if formatted:
                    st.info(formatted)
                else:
                    metric_items = {
                        k: v for k, v in metrics.items()
                        if k not in ("aging_buckets",) and not isinstance(v, dict)
                    }
                    if metric_items:
                        cols = st.columns(min(len(metric_items), 4))
                        for i, (k, v) in enumerate(metric_items.items()):
                            cols[i % len(cols)].metric(k.replace("_", " ").title(), v)

            # Chart
            chart_data = msg.get("chart_data")
            if chart_data:
                try:
                    fig = go.Figure(chart_data)
                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=20, r=20, t=40, b=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    pass

            # Data table — only show when appropriate
            data_rows = msg.get("data")
            if data_rows and isinstance(data_rows, list) and len(data_rows) > 0:
                user_query = ""
                # Find the user message that triggered this response
                msg_idx = st.session_state.messages.index(msg)
                if msg_idx > 0:
                    user_query = st.session_state.messages[msg_idx - 1].get("content", "").lower()

                show_table = _should_show_table(user_query, len(data_rows), bool(msg.get("chart_data")))
                if show_table:
                    try:
                        df_display = pd.DataFrame(data_rows)
                        with st.expander(f"📊 View Data Table ({len(df_display)} rows)", expanded=True):
                            st.dataframe(df_display, use_container_width=True, height=min(400, 35 * len(df_display) + 38))
                    except Exception:
                        pass

            # SQL expander
            sql_used = msg.get("sql_used", "")
            if sql_used:
                with st.expander("🔍 View Generated SQL", expanded=False):
                    st.code(sql_used, language="sql")
                    st.caption("Generated by Llama 3.3 70B · Validated before execution · Read-only SELECT")


# ── Input handling ──
query = st.session_state.pending_query or st.chat_input(
    "Ask anything: headcount, budget, invoice delta..."
)

if query:
    st.session_state.pending_query = None

    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("⚙️ Querying Oracle Fusion data..."):
            try:
                resp = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "query": query,
                        "session_id": st.session_state.session_id,
                    },
                    timeout=120,
                )
                data = resp.json()

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "answer": data.get("answer", "No response."),
                        "domain": data.get("domain", ""),
                        "query_type": data.get("query_type", ""),
                        "sql_used": data.get("sql_used", ""),
                        "chart_data": data.get("chart_data"),
                        "metrics": data.get("metrics"),
                        "data": data.get("data"),
                        "execution_time_ms": data.get("execution_time_ms", 0),
                        "row_count": data.get("row_count", 0),
                    }
                )
                st.rerun()

            except requests.ConnectionError:
                st.error(
                    "❌ Cannot connect to backend. Is FastAPI running on port 8000?\n\n"
                    "Start it with: `uvicorn backend.main:app --reload --port 8000`"
                )
            except Exception as e:
                st.error(f"❌ Error: {e}")
