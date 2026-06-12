import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.styles import get_global_css, hero, kpi_card, success_box, warning_box
from utils.preprocessing import get_preprocessing_summary


st.markdown(get_global_css(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🗂️ Data Options")
    if "df_clean" in st.session_state:
        df0 = st.session_state["df_clean"]
        st.markdown(f"**Active:** `{len(df0):,} rows × {len(df0.columns)} cols`")
    st.markdown("---")

st.markdown(hero("🧹", "Data Preprocessing",
                 "Automated cleaning pipeline — missing values, duplicates, feature engineering"),
            unsafe_allow_html=True)

if "df_raw" not in st.session_state:
    st.markdown(warning_box("Please upload data on the Data Upload page first."), unsafe_allow_html=True)
    st.stop()

raw   = st.session_state["df_raw"]
clean = st.session_state["df_clean"]
s     = get_preprocessing_summary(raw, clean)

# KPI row
c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi_card("Rows Before",         f"{s['raw_rows']:,}",                           "Original"),  unsafe_allow_html=True)
c2.markdown(kpi_card("Rows After",          f"{s['clean_rows']:,}",                          "Cleaned"),   unsafe_allow_html=True)
c3.markdown(kpi_card("Duplicates Removed",  str(s['duplicates_removed']),                    "Dropped"),   unsafe_allow_html=True)
c4.markdown(kpi_card("Missing Fixed",       str(s['missing_before'] - s['missing_after']),   "Imputed"),   unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Pipeline steps
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("**Preprocessing Pipeline — Steps Applied**")
steps = [
    ("✅", "Date columns detected and parsed to datetime"),
    ("✅", "Exact duplicate rows removed"),
    ("✅", "Numeric missing values filled with column median"),
    ("✅", "Categorical missing values filled with column mode"),
    ("✅", "Feature engineered: year, month, quarter, week, day_of_week"),
    ("✅", "Feature engineered: profit_margin (sales − cost) / sales × 100"),
]
for icon, text in steps:
    st.markdown(f"{icon} {text}")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Show raw data and button to re-run
st.markdown("**Raw Data Preview** *(before preprocessing)*")
st.dataframe(raw.head(20), use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("▶️ Run Preprocessing Pipeline", use_container_width=False):
    from utils.preprocessing import clean_data, feature_engineer
    cleaned = clean_data(feature_engineer(raw))
    st.session_state["df_clean"] = cleaned
    st.markdown(success_box("Preprocessing pipeline executed successfully! Dataset updated."),
                unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("**Cleaned Data Preview** *(after preprocessing)*")
st.dataframe(clean.head(30), use_container_width=True, hide_index=True)

# Missing value heatmap
if raw.isnull().sum().sum() > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Missing Value Analysis**")
    miss = raw.isnull().mean().reset_index()
    miss.columns = ["Column","Missing %"]
    miss["Missing %"] = (miss["Missing %"]*100).round(2)
    miss = miss[miss["Missing %"] > 0].sort_values("Missing %", ascending=False)
    if not miss.empty:
        fig = px.bar(miss, x="Column", y="Missing %", title="Missing Values by Column (%)",
                     color="Missing %", color_continuous_scale=["#DBEAFE","#1565C0"])
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                          font_color="#1A1A2E", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(miss, use_container_width=True, hide_index=True)