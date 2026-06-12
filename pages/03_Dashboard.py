import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import get_global_css, hero, kpi_card, warning_box
from utils.models import customer_segmentation
st.markdown(get_global_css(), unsafe_allow_html=True)


from utils.styles import sidebar_brand

with st.sidebar:
    st.markdown(sidebar_brand(), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🗂️ Data Options")
    if "df_clean" in st.session_state:
        df0 = st.session_state["df_clean"]
        st.markdown(f"**Active:** `{len(df0):,} rows × {len(df0.columns)} cols`")
        st.markdown("**Select Active Dataset**")
        st.selectbox("", ["Default Dataset"], label_visibility="collapsed")
    st.markdown("---")

st.markdown(hero("🎯", "Dashboard",
                 "Live KPI overview — sales, churn, inventory and segment performance"),
            unsafe_allow_html=True)

if "df_clean" not in st.session_state:
    st.markdown(warning_box("Please upload data first."), unsafe_allow_html=True)
    st.stop()

df = st.session_state["df_clean"]

# ── Filters ───────────────────────────────────────
with st.expander("🎛️ Filters", expanded=False):
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        if "region" in df.columns:
            regions = st.multiselect("Region", df["region"].unique(), default=list(df["region"].unique()))
            df = df[df["region"].isin(regions)]
    with fc2:
        if "category" in df.columns:
            cats = st.multiselect("Category", df["category"].unique(), default=list(df["category"].unique()))
            df = df[df["category"].isin(cats)]
    with fc3:
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            mn, mx = df["date"].min().date(), df["date"].max().date()
            dr = st.date_input("Date Range", value=(mn, mx))
            if len(dr) == 2:
                df = df[(df["date"] >= pd.Timestamp(dr[0])) & (df["date"] <= pd.Timestamp(dr[1]))]

# ── Top KPIs ──────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown(kpi_card("Total Revenue",    f"₹{df['sales_amount'].sum()/1e6:.2f}M"  if "sales_amount" in df.columns else "—",  ""), unsafe_allow_html=True)
c2.markdown(kpi_card("Gross Profit",     f"₹{df['profit'].sum()/1e6:.2f}M"        if "profit" in df.columns else "—",         ""), unsafe_allow_html=True)
c3.markdown(kpi_card("Orders",           f"{len(df):,}",                                                                       ""), unsafe_allow_html=True)
c4.markdown(kpi_card("Avg Order Value",  f"₹{df['sales_amount'].mean():,.0f}"     if "sales_amount" in df.columns else "—",  ""), unsafe_allow_html=True)
c5.markdown(kpi_card("Churn Rate",       f"{df['churned'].mean()*100:.1f}%"        if "churned" in df.columns else "—",         ""), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts row 1 ─────────────────────────────────
col1, col2 = st.columns([3, 2])
with col1:
    if "date" in df.columns and "sales_amount" in df.columns:
        daily = df.groupby("date")["sales_amount"].sum().reset_index()
        fig = px.area(daily, x="date", y="sales_amount", title="Daily Sales Trend",
                      color_discrete_sequence=["#1976D2"])
        fig.update_traces(fill="tozeroy", fillcolor="rgba(25,118,210,0.10)")
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                           font_color="#1A1A2E", yaxis_title="Revenue (₹)")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if "region" in df.columns and "sales_amount" in df.columns:
        reg = df.groupby("region")["sales_amount"].sum().reset_index()
        fig2 = go.Figure(go.Pie(labels=reg["region"], values=reg["sales_amount"], hole=0.38,
                                 marker_colors=["#BFDBFE","#93C5FD","#60A5FA","#3B82F6","#2563EB"]))
        fig2.update_layout(title="Revenue by Region", font_color="#1A1A2E", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

# ── Charts row 2 ─────────────────────────────────
col3, col4 = st.columns(2)
with col3:
    if "category" in df.columns and "sales_amount" in df.columns:
        cat = df.groupby("category")["sales_amount"].sum().reset_index().sort_values("sales_amount")
        fig3 = px.bar(cat, x="sales_amount", y="category", orientation="h",
                      title="Revenue by Category",
                      color="sales_amount", color_continuous_scale=["#DBEAFE","#1565C0"])
        fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                            font_color="#1A1A2E", showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

with col4:
    if "month" in df.columns and "sales_amount" in df.columns:
        monthly = df.groupby("month")["sales_amount"].sum().reset_index()
        month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                     7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        monthly["Month"] = monthly["month"].map(month_map)
        fig4 = px.bar(monthly, x="Month", y="sales_amount",
                      title="Monthly Revenue",
                      color="sales_amount", color_continuous_scale=["#DBEAFE","#1565C0"])
        fig4.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                            font_color="#1A1A2E", showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

# ── Segmentation ──────────────────────────────────
st.markdown("---")
st.markdown("### 👥 Customer Segments")
col_seg, _ = st.columns([1,3])
with col_seg:
    seg_btn = st.button("🔄 Run Segmentation", use_container_width=True)
if seg_btn:
    df_seg, _ = customer_segmentation(df, n_clusters=4)
    st.session_state["df_seg"] = df_seg

if "df_seg" in st.session_state and "Segment" in st.session_state["df_seg"].columns:
    df_seg = st.session_state["df_seg"]
    col1, col2 = st.columns(2)
    with col1:
        if "sales_amount" in df_seg.columns and "units_sold" in df_seg.columns:
            fig = px.scatter(df_seg.sample(min(800,len(df_seg))),
                             x="units_sold", y="sales_amount", color="Segment",
                             title="Customer Segmentation",
                             color_discrete_sequence=px.colors.qualitative.Pastel, opacity=0.7)
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font_color="#1A1A2E")
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        seg_sum = df_seg.groupby("Segment").agg(
            Count=("sales_amount","count"),
            Total_Revenue=("sales_amount","sum"),
            Avg_Revenue=("sales_amount","mean"),
        ).round(2).reset_index()
        fig2 = px.pie(seg_sum, names="Segment", values="Total_Revenue",
                      title="Revenue Share by Segment",
                      color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.35)
        fig2.update_layout(font_color="#1A1A2E", paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(seg_sum, use_container_width=True, hide_index=True)