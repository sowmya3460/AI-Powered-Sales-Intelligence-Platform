import streamlit as st

st.set_page_config(
    page_title="Intelligent Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import get_global_css, hero, kpi_card
st.markdown(get_global_css(), unsafe_allow_html=True)
#st.markdown(get_global_css(), unsafe_allow_html=True)

# ── Sidebar Data Options ──────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🗂️ Data Options")
    if "df_clean" in st.session_state:
        df = st.session_state["df_clean"]
        st.markdown(f"**Active dataset:** `{len(df):,} rows × {len(df.columns)} cols`")
    else:
        st.markdown("*No dataset loaded yet*")
    st.markdown("---")

# ── Hero ─────────────────────────────────────────
st.markdown(hero("📊", "Intelligent Sales Analytics",
                 "AI-powered forecasting, churn prediction, inventory optimization & business intelligence"),
            unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────
if "df_clean" in st.session_state:
    df = st.session_state["df_clean"]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(kpi_card("Total Sales",
                f"₹{df['sales_amount'].sum()/1e6:.2f}M" if "sales_amount" in df.columns else "—",
                "All time"), unsafe_allow_html=True)
    c2.markdown(kpi_card("Total Profit",
                f"₹{df['profit'].sum()/1e6:.2f}M" if "profit" in df.columns else "—",
                "Net"), unsafe_allow_html=True)
    c3.markdown(kpi_card("Transactions", f"{len(df):,}", "Records"), unsafe_allow_html=True)
    c4.markdown(kpi_card("Customers",
                f"{df['customer_id'].nunique():,}" if "customer_id" in df.columns else "—",
                "Unique"), unsafe_allow_html=True)
    c5.markdown(kpi_card("Churn Rate",
                f"{df['churned'].mean()*100:.1f}%" if "churned" in df.columns else "—",
                "Predicted"), unsafe_allow_html=True)
else:
    st.markdown("""
<div class="info-box">
👆 <b>Get started:</b> Navigate to <b>Data Upload</b> in the sidebar to load your dataset.
All pages will populate automatically after upload.
</div>
""", unsafe_allow_html=True)

# ── Feature grid ──────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Platform Modules")
cols = st.columns(4)
modules = [
    ("📤", "Data Upload",        "Upload CSV/Excel and preview your raw dataset"),
    ("🧹", "Data Preprocessing", "Auto-clean, impute missing values, engineer features"),
    ("🔍", "EDA Analysis",       "Trends, distributions, correlations, regional heatmaps"),
    ("🤖", "Model Training",     "Train Random Forest for sales regression"),
    ("📈", "Sales Forecasting",  "Predict future revenue — single or batch"),
    ("📦", "Inventory",          "Reorder points, safety stock, stock alerts"),
    ("📑", "Reports",            "Export Excel & PDF reports instantly"),
    ("🎯", "Dashboard",          "Live KPI dashboard with filters & segments"),
]
for i, (icon, name, desc) in enumerate(modules):
    with cols[i % 4]:
        st.markdown(f"""
<div class="section-card" style="text-align:center;min-height:120px">
  <div style="font-size:2rem">{icon}</div>
  <div style="font-weight:700;color:#0D47A1;margin:6px 0 4px">{name}</div>
  <div style="font-size:0.8rem;color:#6B7280">{desc}</div>
</div>""", unsafe_allow_html=True)
    if i == 3:
        cols = st.columns(4)