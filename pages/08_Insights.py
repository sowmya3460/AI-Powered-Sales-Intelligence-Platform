import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.styles import get_global_css, hero, kpi_card, warning_box
from utils.models import customer_segmentation
from utils.visualizations import segment_scatter


st.markdown(get_global_css(), unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🗂️ Data Options")
    if "df_clean" in st.session_state:
        df0 = st.session_state["df_clean"]
        st.markdown(f"**Active:** `{len(df0):,} rows × {len(df0.columns)} cols`")
        st.markdown("**Select Active Dataset**")
        st.selectbox("", ["Processed Dataset", "Raw Dataset"], label_visibility="collapsed")
    st.markdown("---")

st.markdown(
    hero("💡", "Business Intelligence Insights",
         "KPI dashboard, customer segments, top performers and actionable filters"),
    unsafe_allow_html=True
)

if "df_clean" not in st.session_state:
    st.markdown(warning_box("Please upload data first."), unsafe_allow_html=True)
    st.stop()

df = st.session_state["df_clean"]

# ── Filters ───────────────────────────────────────
with st.expander("🎛️ Filters", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if "region" in df.columns:
            region_f = st.multiselect(
                "Region", options=df["region"].unique().tolist(),
                default=df["region"].unique().tolist(), key="ins_region"
            )
            df = df[df["region"].isin(region_f)]
    with col2:
        if "category" in df.columns:
            cat_f = st.multiselect(
                "Category", options=df["category"].unique().tolist(),
                default=df["category"].unique().tolist(), key="ins_cat"
            )
            df = df[df["category"].isin(cat_f)]
    with col3:
        if "channel" in df.columns:
            ch_f = st.multiselect(
                "Channel", options=df["channel"].unique().tolist(),
                default=df["channel"].unique().tolist(), key="ins_ch"
            )
            df = df[df["channel"].isin(ch_f)]
    with col4:
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            min_d = df["date"].min().date()
            max_d = df["date"].max().date()
            date_range = st.date_input("Date Range", value=(min_d, max_d), key="ins_date")
            if len(date_range) == 2:
                df = df[
                    (df["date"] >= pd.Timestamp(date_range[0])) &
                    (df["date"] <= pd.Timestamp(date_range[1]))
                ]

if df.empty:
    st.markdown(warning_box("No data matches the selected filters. Please adjust your filters."), unsafe_allow_html=True)
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🎯 KPI Dashboard", "👥 Customer Segments", "📋 Top Performers"])

# ─────────────────────────────────────────────────
# TAB 1 — KPI DASHBOARD
# ─────────────────────────────────────────────────
with tab1:
    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(
        kpi_card("Total Sales",
                 f"₹{df['sales_amount'].sum():,.0f}" if "sales_amount" in df.columns else "—", ""),
        unsafe_allow_html=True
    )
    c2.markdown(
        kpi_card("Total Profit",
                 f"₹{df['profit'].sum():,.0f}" if "profit" in df.columns else "—", ""),
        unsafe_allow_html=True
    )
    c3.markdown(
        kpi_card("Avg Order Value",
                 f"₹{df['sales_amount'].mean():,.0f}" if "sales_amount" in df.columns else "—", ""),
        unsafe_allow_html=True
    )
    c4.markdown(kpi_card("Transactions", f"{len(df):,}", "Records"), unsafe_allow_html=True)
    c5.markdown(
        kpi_card("Unique Customers",
                 f"{df['customer_id'].nunique():,}" if "customer_id" in df.columns else "—", ""),
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if "category" in df.columns and "sales_amount" in df.columns:
            fig = px.treemap(
                df, path=["category"], values="sales_amount",
                title="Sales Treemap by Category",
                color="sales_amount",
                color_continuous_scale=["#DBEAFE", "#1565C0"]
            )
            fig.update_layout(font_color="#1A1A2E", paper_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "month" in df.columns and "sales_amount" in df.columns:
            month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                         7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
            monthly = df.groupby("month")["sales_amount"].sum().reset_index()
            monthly["month_name"] = monthly["month"].map(month_map)
            fig2 = px.line_polar(
                monthly, r="sales_amount", theta="month_name",
                line_close=True, title="Sales by Month (Radar)",
                color_discrete_sequence=["#1565C0"]
            )
            fig2.update_traces(fill="toself", fillcolor="rgba(21,101,192,0.12)")
            fig2.update_layout(font_color="#1A1A2E", paper_bgcolor="white")
            st.plotly_chart(fig2, use_container_width=True)

    # Profit margin trend
    if "profit_margin" in df.columns and "date" in df.columns:
        st.markdown("<br>", unsafe_allow_html=True)
        pm_trend = df.groupby("date")["profit_margin"].mean().reset_index()
        fig3 = px.area(
            pm_trend, x="date", y="profit_margin",
            title="Profit Margin Trend (%)",
            color_discrete_sequence=["#1976D2"]
        )
        fig3.update_traces(fill="tozeroy", fillcolor="rgba(25,118,210,0.10)")
        fig3.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_color="#1A1A2E", yaxis_title="Profit Margin (%)"
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.dataframe(
            pm_trend.tail(30).rename(columns={"date": "Date", "profit_margin": "Avg Profit Margin (%)"}),
            use_container_width=True, hide_index=True
        )

    # Category summary table
    if "category" in df.columns and "sales_amount" in df.columns:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Category Summary**")
        cat_summary = df.groupby("category").agg(
            Total_Sales=("sales_amount", "sum"),
            Avg_Sales=("sales_amount", "mean"),
            Transactions=("sales_amount", "count"),
            **({} if "units_sold" not in df.columns else {"Total_Units": ("units_sold", "sum")}),
        ).round(2).reset_index().sort_values("Total_Sales", ascending=False)
        st.dataframe(cat_summary, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────
# TAB 2 — CUSTOMER SEGMENTS
# ─────────────────────────────────────────────────
with tab2:
    st.markdown("### Customer Segmentation (K-Means)")

    n_clusters = st.slider("Number of Segments", 2, 6, 4, key="ins_clusters")

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        seg_btn = st.button("🚀 Run Segmentation", use_container_width=True, key="ins_seg_btn")

    if seg_btn:
        with st.spinner("Clustering customers..."):
            df_seg, km = customer_segmentation(df, n_clusters)
        st.session_state["df_seg"] = df_seg
        st.success("✅ Segmentation complete!")

    if "df_seg" in st.session_state:
        df_seg = st.session_state["df_seg"]

        if "Segment" in df_seg.columns:
            col1, col2 = st.columns(2)

            with col1:
                if "sales_amount" in df_seg.columns and "units_sold" in df_seg.columns:
                    fig = px.scatter(
                        df_seg.sample(min(800, len(df_seg))),
                        x="units_sold", y="sales_amount", color="Segment",
                        title="Customer Segments — Units vs Sales",
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        opacity=0.7
                    )
                    fig.update_layout(
                        plot_bgcolor="white", paper_bgcolor="white", font_color="#1A1A2E"
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                seg_summary = df_seg.groupby("Segment").agg(
                    Count=("sales_amount", "count"),
                    Total_Revenue=("sales_amount", "sum"),
                    Avg_Revenue=("sales_amount", "mean"),
                ).round(2).reset_index()

                fig2 = px.pie(
                    seg_summary, names="Segment", values="Total_Revenue",
                    title="Revenue Share by Segment",
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    hole=0.35
                )
                fig2.update_layout(font_color="#1A1A2E", paper_bgcolor="white")
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("**Segment Summary Table**")
            st.dataframe(seg_summary, use_container_width=True, hide_index=True)

            # Bar chart per segment
            fig3 = px.bar(
                seg_summary, x="Segment", y="Total_Revenue",
                title="Total Revenue by Segment",
                color="Segment",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig3.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_color="#1A1A2E", showlegend=False
            )
            st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────────
# TAB 3 — TOP PERFORMERS
# ─────────────────────────────────────────────────
with tab3:
    st.markdown("### Top Performing Products & Customers")

    col1, col2 = st.columns(2)

    with col1:
        if "product_name" in df.columns and "sales_amount" in df.columns:
            top_prod = (
                df.groupby("product_name")["sales_amount"]
                .sum()
                .reset_index()
                .sort_values("sales_amount", ascending=True)
                .tail(10)
            )
            fig = px.bar(
                top_prod, x="sales_amount", y="product_name",
                orientation="h",
                title="Top 10 Products by Sales",
                color="sales_amount",
                color_continuous_scale=["#DBEAFE", "#1565C0"]
            )
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_color="#1A1A2E", showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(
                top_prod.sort_values("sales_amount", ascending=False)
                        .rename(columns={"product_name": "Product", "sales_amount": "Sales (₹)"}),
                use_container_width=True, hide_index=True
            )

    with col2:
        if "customer_id" in df.columns and "sales_amount" in df.columns:
            top_cust = (
                df.groupby("customer_id")["sales_amount"]
                .sum()
                .reset_index()
                .sort_values("sales_amount", ascending=True)
                .tail(10)
            )
            # Fix: use the actual column name "customer_id" directly
            top_cust["customer_id"] = top_cust["customer_id"].astype(str)

            fig2 = px.bar(
                top_cust, x="sales_amount", y="customer_id",
                orientation="h",
                title="Top 10 Customers by Spend",
                color="sales_amount",
                color_continuous_scale=["#DBEAFE", "#1565C0"]
            )
            fig2.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_color="#1A1A2E", showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.dataframe(
                top_cust.sort_values("sales_amount", ascending=False)
                        .rename(columns={"customer_id": "Customer ID", "sales_amount": "Sales (₹)"}),
                use_container_width=True, hide_index=True
            )

    # Channel performance
    if "channel" in df.columns and "sales_amount" in df.columns:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Channel Performance")
        col3, col4 = st.columns(2)

        with col3:
            ch_data = (
                df.groupby("channel")["sales_amount"]
                .sum()
                .reset_index()
                .sort_values("sales_amount", ascending=True)
            )
            fig3 = px.bar(
                ch_data, x="sales_amount", y="channel",
                orientation="h",
                title="Revenue by Channel",
                color="sales_amount",
                color_continuous_scale=["#DBEAFE", "#1565C0"]
            )
            fig3.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                font_color="#1A1A2E", showlegend=False
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            fig4 = px.pie(
                ch_data, names="channel", values="sales_amount",
                title="Sales Share by Channel",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.35
            )
            fig4.update_layout(font_color="#1A1A2E", paper_bgcolor="white")
            st.plotly_chart(fig4, use_container_width=True)

        st.dataframe(
            ch_data.sort_values("sales_amount", ascending=False)
                   .rename(columns={"channel": "Channel", "sales_amount": "Revenue (₹)"}),
            use_container_width=True, hide_index=True
        )