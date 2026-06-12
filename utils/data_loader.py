import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file) -> pd.DataFrame:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    elif file.name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
    else:
        st.error("Unsupported format. Upload CSV or Excel.")
        return None
    return df

def load_sample_data() -> pd.DataFrame:
    return pd.read_csv("data/sample_data.csv")

def get_data() -> pd.DataFrame:
    """Retrieve data from session state."""
    return st.session_state.get("df", None)

def validate_columns(df: pd.DataFrame) -> dict:
    required = ["date", "sales_amount", "category", "region"]
    missing = [c for c in required if c not in df.columns]
    extra = [c for c in df.columns if c not in required]
    return {"missing": missing, "extra": extra, "valid": len(missing) == 0}