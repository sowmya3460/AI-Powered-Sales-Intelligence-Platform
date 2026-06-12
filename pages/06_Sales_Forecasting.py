import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import timedelta
from utils.styles import get_global_css, hero, kpi_card, warning_box, info_box, success_box


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

st.markdown(hero("📈", "Sales Forecasting",
                 "Predict revenue using the trained ML model"),
            unsafe_allow_html=True)

if "rf_model" not in st.session_state:
    st.markdown(warning_box("Please train a model on the <b>Model Training</b> page first."),
                unsafe_allow_html=True)
    st.stop()

df    = st.session_state["df_clean"]
model = st.session_state["rf_model"]
feats = st.session_state["rf_features"]

tab1, tab2 = st.tabs(["🎯 Single Prediction", "📋 Batch Forecast"])

with tab1:
    st.markdown("### Predict Sales for a Single Order")
    from utils.preprocessing import feature_engineer
    from utils.models import prepare_forecast_features

    df_feat, _ = prepare_forecast_features(df)
    df_feat = df_feat.dropna(subset=feats)
    medians = {f: float(df_feat[f].median()) for f in feats}

    col1, col2, col3, col4 = st.columns(4)
    inputs = {}
    display_feats = feats[:4]
    for i, f in enumerate(display_feats):
        with [col1,col2,col3,col4][i]:
            inputs[f] = st.number_input(f.replace("_"," ").title(),
                                         value=medians[f], key=f"sp_{f}")
    for f in feats[4:]:
        inputs[f] = medians[f]

    col_btn2, _ = st.columns([1,3])
    with col_btn2:
        pred_btn = st.button("🔮 Predict Sales", use_container_width=True)

    if pred_btn:
        inp = pd.DataFrame([inputs])[feats]
        pred = max(0, model.predict(inp)[0])
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(kpi_card("Predicted Sales", f"₹ {pred:,.2f}", "Single order forecast"),
                    unsafe_allow_html=True)
        c2.markdown(kpi_card("Confidence Band Low",  f"₹ {pred*0.9:,.2f}", "-10%"), unsafe_allow_html=True)
        c3.markdown(kpi_card("Confidence Band High", f"₹ {pred*1.1:,.2f}", "+10%"), unsafe_allow_html=True)
        st.markdown(success_box(f"Predicted Sales: <b>₹ {pred:,.2f}</b>"), unsafe_allow_html=True)

with tab2:
    st.markdown("### Batch Forecast — Future Periods")
    n_days = st.slider("Forecast Days", 7, 90, 30)

    col_btn3, _ = st.columns([1,3])
    with col_btn3:
        batch_btn = st.button("📊 Generate Forecast", use_container_width=True)

    if batch_btn or "batch_forecast_df" in st.session_state:
        if batch_btn:
            last = [st.session_state.get("rf_X_last", [5,2024,1,2,10,5000,4800,5100,5050])]
            preds = []
            curr = last[0].copy()
            for i in range(n_days):
                p = max(0, model.predict([curr])[0])
                preds.append(p)
                curr[0] = (curr[0] % 12) + 1
            last_date   = pd.to_datetime(df["date"].max()) if "date" in df.columns else pd.Timestamp.today()
            future_dates = pd.date_range(last_date + timedelta(1), periods=n_days)
            fdf = pd.DataFrame({"Date": future_dates, "Forecasted_Sales": np.round(preds, 2)})
            st.session_state["batch_forecast_df"] = fdf

        fdf = st.session_state["batch_forecast_df"]

        c1, c2, c3 = st.columns(3)
        c1.markdown(kpi_card("Total Forecast",    f"₹ {fdf['Forecasted_Sales'].sum():,.0f}", f"{len(fdf)} days"), unsafe_allow_html=True)
        c2.markdown(kpi_card("Daily Average",      f"₹ {fdf['Forecasted_Sales'].mean():,.0f}", ""), unsafe_allow_html=True)
        c3.markdown(kpi_card("Peak Day",            f"₹ {fdf['Forecasted_Sales'].max():,.0f}", str(fdf.loc[fdf['Forecasted_Sales'].idxmax(),'Date'].date())), unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fdf["Date"], y=fdf["Forecasted_Sales"],
                                  name="Forecast", fill="tozeroy",
                                  line=dict(color="#1565C0", width=2),
                                  fillcolor="rgba(21,101,192,0.10)"))
        fig.update_layout(title=f"Sales Forecast — Next {len(fdf)} Days",
                          plot_bgcolor="white", paper_bgcolor="white",
                          font_color="#1A1A2E", yaxis_title="Revenue (₹)")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(fdf, use_container_width=True, hide_index=True)