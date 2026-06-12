import streamlit as st
import pandas as pd
from utils.styles import get_global_css, hero, kpi_card, success_box, info_box
from utils.data_loader import load_data, load_sample_data
from utils.preprocessing import clean_data, feature_engineer


st.markdown(get_global_css(), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🗂️ Data Options")
    if "df_clean" in st.session_state:
        df0 = st.session_state["df_clean"]
        st.markdown(f"**Active:** `{len(df0):,} rows × {len(df0.columns)} cols`")
    else:
        st.markdown("*No dataset loaded*")
    st.markdown("---")

st.markdown(hero("📤", "Data Upload",
                 "Upload sales data and persist it across all pages"),
            unsafe_allow_html=True)

col_upload, col_hint = st.columns([1, 1])

with col_upload:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("**Upload CSV file**")
    uploaded = st.file_uploader("", type=["csv", "xlsx", "xls"],
                                 label_visibility="collapsed",
                                 help="200MB per file • CSV, XLSX, XLS")
    st.button("Load Sample Dataset", use_container_width=True, key="load_sample")
    st.markdown('</div>', unsafe_allow_html=True)

with col_hint:
    if "df_clean" not in st.session_state:
        st.markdown(info_box("Upload a CSV or click <b>Load Sample Dataset</b> to begin."),
                    unsafe_allow_html=True)

# Load logic
if st.session_state.get("load_sample"):
    df_raw = load_sample_data()
    st.session_state["df_raw"]   = df_raw
    st.session_state["df_clean"] = clean_data(feature_engineer(df_raw))
    st.markdown(success_box("Sample dataset loaded successfully!"), unsafe_allow_html=True)

if uploaded:
    df_raw = load_data(uploaded)
    if df_raw is not None:
        st.session_state["df_raw"]   = df_raw
        st.session_state["df_clean"] = clean_data(feature_engineer(df_raw))
        st.markdown(success_box(f"**{uploaded.name}** uploaded successfully!"),
                    unsafe_allow_html=True)

# ── Show data if loaded ───────────────────────────
if "df_clean" in st.session_state:
    df = st.session_state["df_clean"]
    st.markdown("<br>", unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(kpi_card("Rows",     f"{len(df):,}",                    "Total records"),    unsafe_allow_html=True)
    c2.markdown(kpi_card("Columns",  str(len(df.columns)),               "Features"),         unsafe_allow_html=True)
    c3.markdown(kpi_card("Missing",  str(df.isnull().sum().sum()),        "Values"),           unsafe_allow_html=True)
    c4.markdown(kpi_card("Duplicates", str(df.duplicated().sum()),        "Rows"),             unsafe_allow_html=True)
    c5.markdown(kpi_card("Memory",   f"{df.memory_usage(deep=True).sum()/1024:.0f} KB", ""),  unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Column Info", "📊 Data Preview"])

    with tab1:
        col_info = pd.DataFrame({
            "Column":    df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Non-Null":  df.notnull().sum().values,
            "Null %":    (df.isnull().mean()*100).round(2).values,
            "Unique":    df.nunique().values,
            "Sample":    [str(df[c].dropna().iloc[0]) if len(df[c].dropna()) > 0 else "" for c in df.columns],
        })
        st.dataframe(col_info, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Numeric Summary**")
        st.dataframe(df.describe().T.round(2), use_container_width=True)

    with tab2:
        n_rows = st.slider("Rows to show", 10, min(500, len(df)), 50)
        st.dataframe(df.head(n_rows), use_container_width=True, hide_index=True)