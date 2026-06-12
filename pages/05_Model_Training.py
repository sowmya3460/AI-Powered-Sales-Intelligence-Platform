import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import get_global_css, hero, kpi_card, success_box, warning_box, info_box
from utils.models import (prepare_forecast_features, train_random_forest,
                           train_xgboost, train_linear, evaluate_model)


st.markdown(get_global_css(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🗂️ Data Options")
    if "df_clean" in st.session_state:
        df0 = st.session_state["df_clean"]
        st.markdown(f"**Active:** `{len(df0):,} rows × {len(df0.columns)} cols`")
        st.markdown("**Select Active Dataset**")
        st.selectbox("", ["Processed Dataset"], label_visibility="collapsed")
    st.markdown("---")

st.markdown(hero("🤖", "Model Training",
                 "Train a Random Forest regressor for sales forecasting"),
            unsafe_allow_html=True)

if "df_clean" not in st.session_state:
    st.markdown(warning_box("Please upload data first."), unsafe_allow_html=True)
    st.stop()

df = st.session_state["df_clean"]

# Prepare features
df_feat, feature_cols = prepare_forecast_features(df)
df_feat = df_feat.dropna(subset=feature_cols + ["sales_amount"])
X = df_feat[feature_cols].values
y = df_feat["sales_amount"].values

# Info banner
feat_str = ", ".join(feature_cols[:5])
target_str = "sales_amount"
st.markdown(info_box(f"Dataset ready with <b>{len(df_feat):,}</b> records. "
                     f"Features used: <code>{feat_str}...</code> → target: <code>{target_str}</code>"),
            unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_btn, _ = st.columns([1, 3])
with col_btn:
    train_btn = st.button("🚀 Train Model", use_container_width=True)

if train_btn:
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    dates_test = df_feat["date"].values[split:]

    with st.spinner("Training Random Forest... please wait"):
        model = train_random_forest(X_train, y_train)
        results = evaluate_model(model, X_test, y_test)

    st.session_state["rf_model"]      = model
    st.session_state["rf_results"]    = results
    st.session_state["rf_y_test"]     = y_test
    st.session_state["rf_dates_test"] = dates_test
    st.session_state["rf_features"]   = feature_cols
    st.session_state["rf_X_last"]     = X_test[-1].tolist()

    st.markdown(success_box("Model trained and saved successfully!"), unsafe_allow_html=True)

if "rf_results" in st.session_state:
    res   = st.session_state["rf_results"]
    y_test     = st.session_state["rf_y_test"]
    dates_test = st.session_state["rf_dates_test"]

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown(kpi_card("R² Score", str(res["R2"]),   "Accuracy"), unsafe_allow_html=True)
    c2.markdown(kpi_card("MAE",      f"₹ {res['MAE']:,.2f}", "Mean Abs Error"), unsafe_allow_html=True)
    c3.markdown(kpi_card("RMSE",     f"₹ {res['RMSE']:,.2f}", "Root Mean Sq Error"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        # Actual vs Predicted
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(y_test))), y=y_test,
                                  name="Actual Sales", line=dict(color="#1565C0", width=2)))
        fig.add_trace(go.Scatter(x=list(range(len(y_test))), y=res["predictions"],
                                  name="Predicted Sales", line=dict(color="#E53935", width=2, dash="dot")))
        fig.update_layout(title="Model: Actual vs Predicted Sales",
                          plot_bgcolor="white", paper_bgcolor="white",
                          font_color="#1A1A2E", legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Feature importance
        model = st.session_state["rf_model"]
        fi = dict(zip(st.session_state["rf_features"], model.feature_importances_))
        fi_df = pd.DataFrame(list(fi.items()), columns=["Feature","Importance"]).sort_values("Importance")
        fig2 = px.bar(fi_df, x="Importance", y="Feature", orientation="h",
                      title="Feature Importance",
                      color="Importance", color_continuous_scale=["#DBEAFE","#1565C0"])
        fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                            font_color="#1A1A2E", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Residuals table
    res_df = pd.DataFrame({
        "Actual":    np.round(y_test[:30], 2),
        "Predicted": np.round(res["predictions"][:30], 2),
        "Residual":  np.round(y_test[:30] - res["predictions"][:30], 2),
    })
    st.dataframe(res_df, use_container_width=True, hide_index=True)