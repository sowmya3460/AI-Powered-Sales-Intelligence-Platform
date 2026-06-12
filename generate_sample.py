# generate_sample.py — run once, then delete
import pandas as pd
import numpy as np

np.random.seed(42)
n = 2000
regions = ["North", "South", "East", "West", "Central"]
categories = ["Electronics", "Clothing", "Food", "Furniture", "Sports"]
channels = ["Online", "Retail", "Wholesale"]

df = pd.DataFrame({
    "date": pd.date_range("2021-01-01", periods=n, freq="D").strftime("%Y-%m-%d"),
    "customer_id": np.random.randint(1001, 1500, n),
    "product_id": np.random.randint(2001, 2100, n),
    "product_name": np.random.choice(["Laptop","Phone","Shirt","Bread","Chair","Dumbbell","TV","Shoe","Rice","Desk"], n),
    "category": np.random.choice(categories, n),
    "region": np.random.choice(regions, n),
    "channel": np.random.choice(channels, n),
    "units_sold": np.random.randint(1, 50, n),
    "unit_price": np.round(np.random.uniform(10, 500, n), 2),
    "discount": np.round(np.random.uniform(0, 0.3, n), 2),
    "cost": np.round(np.random.uniform(5, 300, n), 2),
    "customer_age": np.random.randint(18, 70, n),
    "customer_tenure_months": np.random.randint(1, 72, n),
    "num_complaints": np.random.randint(0, 5, n),
    "last_purchase_days_ago": np.random.randint(1, 365, n),
    "churned": np.random.choice([0, 1], n, p=[0.75, 0.25]),
    "stock_on_hand": np.random.randint(0, 500, n),
    "reorder_point": np.random.randint(20, 100, n),
})
df["sales_amount"] = np.round(df["units_sold"] * df["unit_price"] * (1 - df["discount"]), 2)
df["profit"] = np.round(df["sales_amount"] - df["cost"] * df["units_sold"], 2)
df.to_csv("data/sample_data.csv", index=False)
print("✅ Sample data generated!")