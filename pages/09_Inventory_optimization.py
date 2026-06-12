import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import get_global_css, hero, kpi_card, success_box, warning_box, info_box
from utils.models import compute_reorder_signals


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

st.markdown(hero("📦", "Inventory Optimization",
                 "Calculate reorder points, safety stock, and stock alerts"),
            unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🧮 Manual Calculator", "📊 Data-Driven Insights"])

with tab1:
    st.markdown("### Inventory Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        current_stock    = st.number_input("Current Stock",         value=100, step=10)
    with col2:
        avg_daily_sales  = st.number_input("Average Daily Sales",   value=20.0, step=1.0)
    with col3:
        lead_time        = st.number_input("Lead Time (Days)",      value=5, step=1)

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        opt_btn = st.button("⚙️ Optimize Inventory", use_container_width=True)

    if opt_btn:
        safety_stock   = avg_daily_sales * lead_time * 0.5
        reorder_point  = avg_daily_sales * lead_time + safety_stock
        days_of_stock  = current_stock / avg_daily_sales if avg_daily_sales > 0 else 0
        eoq_demand     = avg_daily_sales * 365
        eoq_order_cost = 50
        eoq_hold_cost  = 2
        eoq = np.sqrt((2 * eoq_demand * eoq_order_cost) / eoq_hold_cost) if eoq_hold_cost > 0 else 0

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(kpi_card("Reorder Point",  f"{reorder_point:.0f} units",  "Min stock to order"), unsafe_allow_html=True)
        c2.markdown(kpi_card("Safety Stock",   f"{safety_stock:.0f} units",   "Buffer stock"),       unsafe_allow_html=True)
        c3.markdown(kpi_card("Days of Stock",  f"{days_of_stock:.1f} days",   "At current rate"),    unsafe_allow_html=True)
        c4.markdown(kpi_card("EOQ",            f"{eoq:.0f} units",            "Economic Order Qty"), unsafe_allow_html=True)

        if current_stock < reorder_point:
            st.markdown(warning_box(f"⚠️ Stock below reorder point! Order at least <b>{eoq:.0f} units</b> now."),
                        unsafe_allow_html=True)
        else:
            st.markdown(success_box(f"Stock is adequate. Next reorder when stock hits <b>{reorder_point:.0f} units</b>."),
                        unsafe_allow_html=True)

        # Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_stock,
            title={"text": "Current Stock vs Reorder Point"},
            gauge={"axis": {"range": [0, max(current_stock * 1.5, reorder_point * 2)]},
                   "bar":  {"color": "#1565C0"},
                   "steps":[{"range": [0, reorder_point],              "color": "#FEE2E2"},
                              {"range": [reorder_point, current_stock * 1.5], "color": "#DCFCE7"}],
                   "threshold": {"line":{"color":"#E53935","width":4}, "value": reorder_point}}))
        fig.update_layout(font_color="#1A1A2E", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    if "df_clean" not in st.session_state:
        st.markdown(warning_box("Upload data first."), unsafe_allow_html=True)
        st.stop()

    df = compute_reorder_signals(st.session_state["df_clean"])

    c1, c2, c3 = st.columns(3)
    if "stock_on_hand" in df.columns:
        c1.markdown(kpi_card("Avg Stock",    f"{df['stock_on_hand'].mean():.0f}",    "Units"), unsafe_allow_html=True)
        c2.markdown(kpi_card("Reorder Alerts", str((df.get("reorder_signal", pd.Series([False]*len(df)))).sum()), "Items"), unsafe_allow_html=True)
        c3.markdown(kpi_card("Out of Stock", str((df["stock_on_hand"]==0).sum()),    "Items"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if "product_name" in df.columns:
                top = df.groupby("product_name")["stock_on_hand"].mean().reset_index().sort_values("stock_on_hand", ascending=True).tail(10)
                fig = px.bar(top, x="stock_on_hand", y="product_name", orientation="h",
                             title="Average Stock by Product",
                             color="stock_on_hand", color_continuous_scale=["#FEE2E2","#1565C0"])
                fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                                   font_color="#1A1A2E", showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            if "reorder_signal" in df.columns and "category" in df.columns:
                alerts_df = df[df["reorder_signal"]==True]
                if not alerts_df.empty:
                    fig2 = px.pie(alerts_df, names="category",
                                  title="Reorder Alerts by Category",
                                  color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.35)
                    fig2.update_layout(font_color="#1A1A2E")
                    st.plotly_chart(fig2, use_container_width=True)

        # Alerts table
        if "reorder_signal" in df.columns:
            alerts = df[df["reorder_signal"]==True]
            st.markdown(f"**⚠️ {len(alerts)} Items Requiring Reorder**")
            cols_show = [c for c in ["product_name","category","stock_on_hand","reorder_point","days_of_stock"] if c in df.columns]
            if cols_show:
                st.dataframe(alerts[cols_show].reset_index(drop=True),
                             use_container_width=True, hide_index=True)
    else:
        st.markdown(info_box("This page works best with the sample dataset which includes stock columns."),
                    unsafe_allow_html=True)