import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import get_global_css, hero, kpi_card, warning_box
from utils.visualizations import (sales_trend, category_bar, pie_chart,
                                   correlation_heatmap, scatter_plot)


st.markdown(get_global_css(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🗂️ Data Options")
    if "df_clean" in st.session_state:
        df0 = st.session_state["df_clean"]
        st.markdown(f"**Active:** `{len(df0):,} rows × {len(df0.columns)} cols`")
        # Filters
        st.markdown("**Select Active Dataset**")
        dataset_option = st.selectbox("", ["Processed Dataset", "Raw Dataset"],
                                       label_visibility="collapsed")
    st.markdown("---")

st.markdown(hero("🔍", "EDA Analysis",
                 "Explore sales trends, product performance, regional breakdowns and statistical patterns"),
            unsafe_allow_html=True)

if "df_clean" not in st.session_state:
    st.markdown(warning_box("Please upload data first."), unsafe_allow_html=True)
    st.stop()

df = st.session_state["df_clean"]

# Summary KPIs
c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi_card("Total Revenue",
    f"₹{df['sales_amount'].sum():,.0f}" if "sales_amount" in df.columns else "—", ""),
    unsafe_allow_html=True)
c2.markdown(kpi_card("Avg Daily Sales",
    f"₹{df.groupby('date')['sales_amount'].sum().mean():,.0f}" if "date" in df.columns and "sales_amount" in df.columns else "—", ""),
    unsafe_allow_html=True)
c3.markdown(kpi_card("Categories",
    str(df['category'].nunique()) if "category" in df.columns else "—", ""),
    unsafe_allow_html=True)
c4.markdown(kpi_card("Regions",
    str(df['region'].nunique()) if "region" in df.columns else "—", ""),
    unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "📦 Products", "🌍 Regions", "🔬 Advanced"])

# ── TRENDS ───────────────────────────────────────
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        if "date" in df.columns and "sales_amount" in df.columns:
            daily = df.groupby("date")["sales_amount"].sum().reset_index()
            fig = px.area(daily, x="date", y="sales_amount",
                          title="Daily Sales Trend",
                          color_discrete_sequence=["#1976D2"])
            fig.update_traces(fill="tozeroy", fillcolor="rgba(25,118,210,0.12)")
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                              font_color="#1A1A2E", yaxis_title="Revenue (₹)",
                              xaxis_title="Date")
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        if "channel" in df.columns and "sales_amount" in df.columns:
            st.plotly_chart(pie_chart(df, "channel"), use_container_width=True)

    if "month" in df.columns and "sales_amount" in df.columns:
        monthly = df.groupby(["year","month"])["sales_amount"].sum().reset_index() if "year" in df.columns else df.groupby("month")["sales_amount"].sum().reset_index()
        month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                     7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        monthly["month_name"] = monthly["month"].map(month_map)
        fig2 = px.bar(monthly, x="month_name", y="sales_amount",
                      title="Monthly Revenue",
                      color="sales_amount", color_continuous_scale=["#DBEAFE","#1565C0"])
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                            font_color="#1A1A2E", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(monthly.rename(columns={"month_name":"Month","sales_amount":"Revenue (₹)"}),
                     use_container_width=True, hide_index=True)

# ── PRODUCTS ─────────────────────────────────────
with tab2:
    if "product_name" in df.columns and "sales_amount" in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            top = (df.groupby("product_name")["sales_amount"]
                     .sum().reset_index()
                     .sort_values("sales_amount", ascending=True).tail(10))
            fig = px.bar(top, x="sales_amount", y="product_name", orientation="h",
                         title="Top 10 Products by Revenue",
                         color="sales_amount", color_continuous_scale=["#DBEAFE","#1565C0"])
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                               font_color="#1A1A2E", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            if "units_sold" in df.columns:
                fig2 = px.box(df, x="product_name", y="units_sold",
                               title="Quantity Distribution by Product",
                               color="product_name",
                               color_discrete_sequence=px.colors.qualitative.Pastel)
                fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                                    font_color="#1A1A2E", showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)

        # Product table
        prod_summary = df.groupby("product_name").agg(
            Revenue=("sales_amount","sum"),
            Units=("units_sold","sum") if "units_sold" in df.columns else ("sales_amount","count"),
            Avg_Price=("unit_price","mean") if "unit_price" in df.columns else ("sales_amount","mean"),
            Transactions=("sales_amount","count"),
        ).round(2).reset_index().sort_values("Revenue", ascending=False)
        st.dataframe(prod_summary, use_container_width=True, hide_index=True)

        # Price vs Quantity bubble
        if "unit_price" in df.columns and "units_sold" in df.columns and "region" in df.columns:
            fig3 = px.scatter(df.sample(min(600,len(df))),
                              x="units_sold", y="unit_price",
                              color="region", size="sales_amount",
                              title="Price vs Quantity (bubble size = revenue)",
                              color_discrete_sequence=px.colors.qualitative.Pastel,
                              opacity=0.7)
            fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white", font_color="#1A1A2E")
            st.plotly_chart(fig3, use_container_width=True)

# ── REGIONS ──────────────────────────────────────
with tab3:
    if "region" in df.columns and "sales_amount" in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(category_bar(df, "region"), use_container_width=True)
        with col2:
            st.plotly_chart(pie_chart(df, "region"), use_container_width=True)

        reg_summary = df.groupby("region").agg(
            Revenue=("sales_amount","sum"),
            Transactions=("sales_amount","count"),
            Avg_Sale=("sales_amount","mean"),
        ).round(2).reset_index().sort_values("Revenue", ascending=False)
        st.dataframe(reg_summary, use_container_width=True, hide_index=True)

        if "category" in df.columns:
            pivot = df.pivot_table(values="sales_amount", index="region",
                                   columns="category", aggfunc="sum").fillna(0)
            fig = px.imshow(pivot, color_continuous_scale=["#DBEAFE","#1565C0"],
                            title="Region × Category Revenue Heatmap", aspect="auto")
            fig.update_layout(font_color="#1A1A2E")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(pivot.round(0), use_container_width=True)

# ── ADVANCED ──────────────────────────────────────
with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Correlation Matrix**")
        st.plotly_chart(correlation_heatmap(df), use_container_width=True)
    with col2:
        st.markdown("**Scatter Analysis**")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        x_c = st.selectbox("X axis", num_cols, index=0, key="sc_x")
        y_c = st.selectbox("Y axis", num_cols, index=min(1,len(num_cols)-1), key="sc_y")
        fig = scatter_plot(df, x_c, y_c)
        st.plotly_chart(fig, use_container_width=True)

    # Full dataset expander
    with st.expander("📋 Full Dataset"):
        st.dataframe(df, use_container_width=True, hide_index=True)