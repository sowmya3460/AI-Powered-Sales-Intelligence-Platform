import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
                              accuracy_score, classification_report, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import warnings
warnings.filterwarnings("ignore")


# ── Sales Forecasting ──────────────────────────────────────────
def prepare_forecast_features(df: pd.DataFrame, target="sales_amount"):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["day_of_week"] = df["date"].dt.dayofweek
    df["quarter"] = df["date"].dt.quarter
    df["week"] = df["date"].dt.isocalendar().week.astype(int)
    df["lag_1"] = df[target].shift(1).fillna(method="bfill")
    df["lag_7"] = df[target].shift(7).fillna(method="bfill")
    df["rolling_7"] = df[target].rolling(7, min_periods=1).mean()
    df["rolling_30"] = df[target].rolling(30, min_periods=1).mean()
    feature_cols = ["month", "year", "day_of_week", "quarter", "week",
                    "lag_1", "lag_7", "rolling_7", "rolling_30"]
    return df, feature_cols

def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    return model

def train_xgboost(X_train, y_train):
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1,
                              max_depth=5, random_state=42,
                              eval_metric="rmse", verbosity=0)
    model.fit(X_train, y_train)
    return model

def train_linear(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    return {
        "MAE": round(mean_absolute_error(y_test, preds), 2),
        "RMSE": round(np.sqrt(mean_squared_error(y_test, preds)), 2),
        "R2": round(r2_score(y_test, preds), 4),
        "predictions": preds
    }

def forecast_future(model, last_row_features, n_days=30):
    preds = []
    current = last_row_features.copy()
    for _ in range(n_days):
        pred = model.predict([current])[0]
        preds.append(max(0, pred))
        current[0] = (current[0] % 12) + 1  # increment month
    return preds


# ── Churn Prediction ───────────────────────────────────────────
def prepare_churn_features(df: pd.DataFrame):
    churn_features = [c for c in ["customer_tenure_months", "num_complaints",
                                   "last_purchase_days_ago", "customer_age",
                                   "units_sold", "sales_amount"] if c in df.columns]
    target = "churned"
    if target not in df.columns:
        return None, None, None
    valid = df[churn_features + [target]].dropna()
    X = valid[churn_features]
    y = valid[target]
    return X, y, churn_features

def train_churn_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                         random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": round(accuracy_score(y_test, preds), 4),
        "auc_roc": round(roc_auc_score(y_test, proba), 4),
        "report": classification_report(y_test, preds, output_dict=True),
        "feature_importance": dict(zip(X.columns, model.feature_importances_)),
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": preds,
        "y_proba": proba,
    }
    return model, metrics

def predict_churn_proba(model, df_input):
    return model.predict_proba(df_input)[:, 1]


# ── Customer Segmentation ──────────────────────────────────────
def customer_segmentation(df: pd.DataFrame, n_clusters=4):
    seg_features = [c for c in ["sales_amount", "units_sold",
                                  "customer_tenure_months", "num_complaints"] if c in df.columns]
    if len(seg_features) < 2:
        return df, None
    sub = df[seg_features].dropna()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(sub)
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(scaled)
    result = df.copy()
    result.loc[sub.index, "Segment"] = [f"Segment {i+1}" for i in labels]
    return result, km


# ── Anomaly Detection ─────────────────────────────────────────
def detect_anomalies(df: pd.DataFrame, feature_col="sales_amount"):
    sub = df[[feature_col]].dropna()
    iso = IsolationForest(contamination=0.05, random_state=42)
    preds = iso.fit_predict(sub)
    result = df.copy()
    result["anomaly"] = "Normal"
    result.loc[sub.index[preds == -1], "anomaly"] = "Anomaly"
    return result


# ── Inventory Optimization ────────────────────────────────────
def compute_reorder_signals(df: pd.DataFrame):
    if "stock_on_hand" not in df.columns or "reorder_point" not in df.columns:
        return df
    df = df.copy()
    df["reorder_signal"] = df["stock_on_hand"] < df["reorder_point"]
    df["days_of_stock"] = (df["stock_on_hand"] / df["units_sold"].replace(0, 1)).round(1)
    return df