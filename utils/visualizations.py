import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

PASTEL = ["#B5DEFF", "#FFD6E0", "#C3F0CA", "#FFE8A1", "#E2C4F0",
          "#FFDAB9", "#B2EBF2", "#F8BBD0", "#DCEDC8", "#FFF9C4"]
COLOR_SEQ = px.colors.qualitative.Pastel


def sales_trend(df, date_col="date", val_col="sales_amount", group_by=None):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    if group_by and group_by in df.columns:
        grp = df.groupby([date_col, group_by])[val_col].sum().reset_index()
        fig = px.line(grp, x=date_col, y=val_col, color=group_by,
                      title="Sales Trend by " + group_by,
                      color_discrete_sequence=COLOR_SEQ)
    else:
        grp = df.groupby(date_col)[val_col].sum().reset_index()
        fig = px.area(grp, x=date_col, y=val_col, title="Overall Sales Trend",
                      color_discrete_sequence=["#B5DEFF"])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                      font_color="#2D2D3A", legend_title_text="")
    return fig


def category_bar(df, cat_col, val_col="sales_amount", agg="sum"):
    grp = df.groupby(cat_col)[val_col].agg(agg).reset_index().sort_values(val_col, ascending=True)
    fig = px.bar(grp, x=val_col, y=cat_col, orientation="h",
                 title=f"{val_col} by {cat_col}",
                 color=cat_col, color_discrete_sequence=COLOR_SEQ)
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                      showlegend=False, font_color="#2D2D3A")
    return fig


def pie_chart(df, col, val_col="sales_amount"):
    grp = df.groupby(col)[val_col].sum().reset_index()
    fig = px.pie(grp, names=col, values=val_col,
                 title=f"{val_col} Distribution by {col}",
                 color_discrete_sequence=COLOR_SEQ, hole=0.35)
    fig.update_layout(font_color="#2D2D3A")
    return fig


def correlation_heatmap(df):
    num = df.select_dtypes(include=np.number).corr()
    fig = px.imshow(num, color_continuous_scale="RdBu_r",
                    title="Correlation Heatmap", aspect="auto")
    fig.update_layout(font_color="#2D2D3A")
    return fig


def scatter_plot(df, x, y, color=None, size=None):
    fig = px.scatter(df, x=x, y=y, color=color, size=size,
                     title=f"{y} vs {x}",
                     color_discrete_sequence=COLOR_SEQ, opacity=0.65)
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font_color="#2D2D3A")
    return fig


def forecast_chart(dates, actuals, predictions, future_dates=None, future_preds=None, model_name=""):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=actuals, name="Actual",
                             line=dict(color="#7C6FF7", width=2)))
    fig.add_trace(go.Scatter(x=dates, y=predictions, name=f"Predicted ({model_name})",
                             line=dict(color="#FFB347", width=2, dash="dot")))
    if future_dates is not None and future_preds is not None:
        fig.add_trace(go.Scatter(x=future_dates, y=future_preds, name="Forecast",
                                 line=dict(color="#90EE90", width=2, dash="dash"),
                                 fill="tozeroy", fillcolor="rgba(144,238,144,0.1)"))
    fig.update_layout(title=f"Sales Forecast — {model_name}",
                      plot_bgcolor="white", paper_bgcolor="white",
                      font_color="#2D2D3A", xaxis_title="Date", yaxis_title="Sales")
    return fig


def churn_pie(y_pred):
    vals = pd.Series(y_pred).value_counts()
    labels = ["Not Churned", "Churned"]
    fig = go.Figure(go.Pie(labels=labels,
                           values=[vals.get(0, 0), vals.get(1, 0)],
                           marker_colors=["#C3F0CA", "#FFD6E0"], hole=0.4))
    fig.update_layout(title="Churn Distribution", font_color="#2D2D3A")
    return fig


def feature_importance_bar(feat_dict: dict, title="Feature Importance"):
    df = pd.DataFrame(list(feat_dict.items()), columns=["Feature", "Importance"])
    df = df.sort_values("Importance", ascending=True)
    fig = px.bar(df, x="Importance", y="Feature", orientation="h",
                 title=title, color="Importance",
                 color_continuous_scale=["#E2C4F0", "#7C6FF7"])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                      showlegend=False, font_color="#2D2D3A")
    return fig


def segment_scatter(df, x="sales_amount", y="units_sold", color="Segment"):
    if color not in df.columns:
        return None
    fig = px.scatter(df.sample(min(800, len(df))), x=x, y=y, color=color,
                     title="Customer Segments", color_discrete_sequence=COLOR_SEQ,
                     opacity=0.7, size_max=12)
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font_color="#2D2D3A")
    return fig


def anomaly_chart(df, date_col="date", val_col="sales_amount"):
    fig = px.scatter(df, x=date_col, y=val_col, color="anomaly",
                     color_discrete_map={"Normal": "#B5DEFF", "Anomaly": "#FFD6E0"},
                     title="Anomaly Detection in Sales")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font_color="#2D2D3A")
    return fig


def inventory_gauge(stock, reorder):
    ratio = stock / max(reorder, 1)
    color = "#C3F0CA" if ratio > 1.5 else "#FFE8A1" if ratio > 1 else "#FFD6E0"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stock,
        title={"text": "Stock vs Reorder Point"},
        gauge={"axis": {"range": [0, stock * 2]},
               "bar": {"color": color},
               "steps": [{"range": [0, reorder], "color": "#FFD6E0"},
                          {"range": [reorder, stock * 2], "color": "#EEF0FF"}]}))
    fig.update_layout(font_color="#2D2D3A", paper_bgcolor="white")
    return fig