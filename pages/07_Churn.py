import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.models import prepare_churn_features, train_churn_model
from utils.visualizations import churn_pie, feature_importance_bar
from utils.styles import get_global_css, hero, kpi_card, success_box, warning_box
st.markdown(get_global_css(), unsafe_allow_html=True)


st.markdown(hero("🔄", "Churn Prediction", "Identify customers at risk of churning using ML"), unsafe_allow_html=True)

if "df_clean" not in st.session_state:
    st.warning("Please upload data first."); st.stop()

df = st.session_state["df_clean"]
X, y, feature_cols = prepare_churn_features(df)

if X is None:
    st.error("'churned' column not found. Please use the sample dataset."); st.stop()

tab1, tab2, tab3 = st.tabs(["🏋️ Train Model", "📊 Results & Charts", "🔮 Predict Single Customer"])

with tab1:
    st.markdown("### Churn Model Training")
    st.markdown("#### Feature Overview")
    st.dataframe(X.describe().T.round(2), use_container_width=True)

    c1, c2 = st.columns(2)
    c1.metric("Total Customers", len(y))
    c2.metric("Churn Rate", f"{y.mean()*100:.1f}%")

    churn_dist = y.value_counts().reset_index()
    churn_dist.columns = ["Churned", "Count"]
    churn_dist["Label"] = churn_dist["Churned"].map({0: "Not Churned", 1: "Churned"})
    fig = px.bar(churn_dist, x="Label", y="Count", color="Label",
                 color_discrete_sequence=["#C3F0CA","#FFD6E0"],
                 title="Churn Class Distribution")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(churn_dist[["Label","Count"]], use_container_width=True)

    if st.button("🚀 Train Churn Model", type="primary", use_container_width=True):
        with st.spinner("Training Random Forest Classifier..."):
            model, metrics = train_churn_model(X, y)
        st.session_state["churn_model"] = model
        st.session_state["churn_metrics"] = metrics
        st.success("✅ Model trained!")

with tab2:
    if "churn_metrics" in st.session_state:
        metrics = st.session_state["churn_metrics"]

        c1, c2 = st.columns(2)
        c1.metric("Accuracy", f"{metrics['accuracy']*100:.1f}%")
        c2.metric("AUC-ROC", f"{metrics['auc_roc']:.4f}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Churn Prediction Distribution")
            st.plotly_chart(churn_pie(metrics["y_pred"]), use_container_width=True)

        with col2:
            st.markdown("#### Feature Importance")
            st.plotly_chart(feature_importance_bar(metrics["feature_importance"],
                                                    "Churn Feature Importance"), use_container_width=True)

        st.markdown("#### Classification Report")
        report_df = pd.DataFrame(metrics["report"]).T.round(3)
        st.dataframe(report_df, use_container_width=True)

        # Probability distribution
        st.markdown("#### Churn Probability Distribution")
        proba_df = pd.DataFrame({
            "Churn_Probability": metrics["y_proba"],
            "Actual": metrics["y_test"].values
        })
        fig = px.histogram(proba_df, x="Churn_Probability", color="Actual",
                           nbins=40, barmode="overlay",
                           color_discrete_sequence=["#C3F0CA", "#FFD6E0"],
                           title="Predicted Churn Probability by Actual Class")
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

        # High risk customers
        st.markdown("#### High-Risk Customers (Probability > 0.7)")
        high_risk = proba_df[proba_df["Churn_Probability"] > 0.7].reset_index()
        st.metric("High Risk Count", len(high_risk))
        st.dataframe(high_risk, use_container_width=True)

        # ROC curve
        from sklearn.metrics import roc_curve
        fpr, tpr, _ = roc_curve(metrics["y_test"], metrics["y_proba"])
        roc_fig = go.Figure()
        roc_fig.add_trace(go.Scatter(x=fpr, y=tpr, name="ROC Curve",
                                      line=dict(color="#7C6FF7", width=2)))
        roc_fig.add_trace(go.Scatter(x=[0,1], y=[0,1], name="Random",
                                      line=dict(color="#CCCCCC", dash="dash")))
        roc_fig.update_layout(title=f"ROC Curve (AUC = {metrics['auc_roc']:.3f})",
                               xaxis_title="False Positive Rate",
                               yaxis_title="True Positive Rate",
                               plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(roc_fig, use_container_width=True)

        st.session_state["churn_results_df"] = proba_df
    else:
        st.info("Train the churn model first.")

with tab3:
    if "churn_model" in st.session_state:
        st.markdown("### Predict Churn for a Single Customer")
        model = st.session_state["churn_model"]

        inputs = {}
        cols = st.columns(3)
        for i, feat in enumerate(feature_cols):
            with cols[i % 3]:
                if feat in df.columns:
                    mn = float(df[feat].min())
                    mx = float(df[feat].max())
                    med = float(df[feat].median())
                    inputs[feat] = st.number_input(feat, min_value=mn, max_value=mx, value=med)

        if st.button("🔮 Predict", type="primary"):
            inp = pd.DataFrame([inputs])
            proba = model.predict_proba(inp)[0][1]
            pred = model.predict(inp)[0]
            color = "#FFD6E0" if proba > 0.5 else "#C3F0CA"
            label = "⚠️ LIKELY TO CHURN" if proba > 0.5 else "✅ LIKELY TO STAY"
            st.markdown(f"""
            <div style='background:{color};border-radius:12px;padding:20px;text-align:center;margin-top:12px'>
            <h2>{label}</h2>
            <h3>Churn Probability: {proba*100:.1f}%</h3>
            </div>""", unsafe_allow_html=True)

            gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=proba * 100,
                title={"text": "Churn Risk Score"},
                gauge={"axis": {"range": [0, 100]},
                       "bar": {"color": "#7C6FF7"},
                       "steps": [{"range": [0, 40], "color": "#C3F0CA"},
                                  {"range": [40, 70], "color": "#FFE8A1"},
                                  {"range": [70, 100], "color": "#FFD6E0"}]},
                number={"suffix": "%"}))
            gauge.update_layout(font_color="#2D2D3A", paper_bgcolor="white")
            st.plotly_chart(gauge, use_container_width=True)
    else:
        st.info("Train the churn model first.")