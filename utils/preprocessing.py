import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Parse dates
    for col in df.columns:
        if "date" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
    # Drop full duplicates
    df.drop_duplicates(inplace=True)
    # Fill numeric NaNs with median
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    # Fill categorical NaNs with mode
    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)
    return df

def feature_engineer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day_of_week"] = df["date"].dt.dayofweek
        df["quarter"] = df["date"].dt.quarter
        df["week"] = df["date"].dt.isocalendar().week.astype(int)
    if "sales_amount" in df.columns and "cost" in df.columns and "units_sold" in df.columns:
        df["profit_margin"] = ((df["sales_amount"] - df["cost"] * df["units_sold"]) / df["sales_amount"].replace(0, np.nan) * 100).round(2)
    return df

def get_preprocessing_summary(raw_df: pd.DataFrame, clean_df: pd.DataFrame) -> dict:
    return {
        "raw_rows": len(raw_df),
        "clean_rows": len(clean_df),
        "duplicates_removed": len(raw_df) - len(raw_df.drop_duplicates()),
        "missing_before": raw_df.isnull().sum().sum(),
        "missing_after": clean_df.isnull().sum().sum(),
        "columns": len(clean_df.columns),
    }

def encode_features(df: pd.DataFrame, cat_cols: list) -> pd.DataFrame:
    df = df.copy()
    le = LabelEncoder()
    for col in cat_cols:
        if col in df.columns:
            df[col + "_enc"] = le.fit_transform(df[col].astype(str))
    return df

def scale_features(X):
    scaler = StandardScaler()
    return scaler.fit_transform(X), scaler