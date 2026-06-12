import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import get_global_css, hero, kpi_card, success_box, warning_box
from utils.report_generator import generate_excel_report, generate_pdf_report


st.markdown(get_global_css(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🗂️ Data Options")
    if "df_clean" in st.session_state:
        df0 = st.session_state["df_clean"]
        st.markdown(f"**Active:** `{len(df0):,} rows × {len(df0.columns)} cols`")
        st.markdown("**Select Active Dataset**")
        st.selectbox("", ["Default Dataset"], label_visibility="collapsed")
    st.markdown("---")

st.markdown(hero("📑", "Reports",
                 "Generate and download comprehensive Excel & PDF reports"),
            unsafe_allow_html=True)

if "df_clean" not in st.session_state:
    st.markdown(warning_box("Please upload data first."), unsafe_allow_html=True)
    st.stop()

df = st.session_state["df_clean"]

# Summary charts at top
if "sales_amount" in df.columns:
    col1, col2 = st.columns(2)
    with col1:
        if "product_name" in df.columns:
            prod_rev = df.groupby("product_name")["sales_amount"].sum().reset_index().sort_values("sales_amount", ascending=True).tail(8)
            fig = px.bar(prod_rev, x="sales_amount", y="product_name", orientation="h",
                         title="Revenue by Product",
                         color="sales_amount", color_continuous_scale=["#DBEAFE","#1565C0"])
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                               font_color="#1A1A2E", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        if "region" in df.columns:
            reg_rev = df.groupby("region")["sales_amount"].sum().reset_index()
            fig2 = go.Figure(go.Pie(labels=reg_rev["region"], values=reg_rev["sales_amount"],
                                     hole=0.35,
                                     marker_colors=["#BFDBFE","#93C5FD","#60A5FA","#3B82F6","#2563EB"]))
            fig2.update_layout(title="Revenue by Region", font_color="#1A1A2E", paper_bgcolor="white")
            st.plotly_chart(fig2, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

col_excel, col_pdf = st.columns(2)

# ── EXCEL ─────────────────────────────────────────
with col_excel:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Excel Report")
    if st.button("📊 Generate Excel Report", use_container_width=True, key="gen_excel"):
        sheets = {
            "Sales Data":        df.head(1000),
            "Summary Stats":     df.describe().T.round(2).reset_index(),
        }
        if "category" in df.columns:
            sheets["By Category"] = df.groupby("category").agg(
                Revenue=("sales_amount","sum"), Transactions=("sales_amount","count"),
                Avg_Sale=("sales_amount","mean")).round(2).reset_index()
        if "region" in df.columns:
            sheets["By Region"] = df.groupby("region").agg(
                Revenue=("sales_amount","sum"), Transactions=("sales_amount","count"),
            ).round(2).reset_index()
        if "forecast_df" in st.session_state:
            sheets["Forecast"] = st.session_state["forecast_df"]
        if "churn_results_df" in st.session_state:
            sheets["Churn"] = st.session_state["churn_results_df"]

        excel_bytes = generate_excel_report(sheets)
        st.session_state["excel_bytes"] = excel_bytes
        st.markdown(success_box("Excel report generated successfully!"), unsafe_allow_html=True)

    if "excel_bytes" in st.session_state:
        st.download_button(
            "📥 Download Excel Report",
            data=st.session_state["excel_bytes"],
            file_name="intelligent_sales_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ── PDF ───────────────────────────────────────────
with col_pdf:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📄 PDF Report")
    if st.button("📄 Generate PDF Report", use_container_width=True, key="gen_pdf"):
        total = df["sales_amount"].sum() if "sales_amount" in df.columns else 0
        profit = df["profit"].sum() if "profit" in df.columns else 0
        sections = [
            {"heading": "Executive Summary",
             "data": f"Total Revenue: ₹{total:,.2f} | Total Profit: ₹{profit:,.2f} | "
                     f"Records: {len(df):,} | Date: {df['date'].min().date() if 'date' in df.columns else 'N/A'} to {df['date'].max().date() if 'date' in df.columns else 'N/A'}"},
            {"heading": "Sales Data (Top 20)", "data": df.head(20)},
        ]
        if "category" in df.columns:
            cat_df = df.groupby("category").agg(Revenue=("sales_amount","sum"),
                                                 Transactions=("sales_amount","count")).round(2).reset_index()
            sections.append({"heading": "Category Analysis", "data": cat_df})
        if "region" in df.columns:
            reg_df = df.groupby("region").agg(Revenue=("sales_amount","sum")).round(2).reset_index()
            sections.append({"heading": "Regional Analysis", "data": reg_df})

        pdf_bytes = generate_pdf_report("Intelligent Sales Analytics Report", sections)
        st.session_state["pdf_bytes"] = pdf_bytes
        st.markdown(success_box("PDF report generated successfully!"), unsafe_allow_html=True)

    if "pdf_bytes" in st.session_state:
        st.download_button(
            "📥 Download PDF Report",
            data=st.session_state["pdf_bytes"],
            file_name="intelligent_sales_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)