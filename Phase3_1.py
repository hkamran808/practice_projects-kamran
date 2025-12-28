# An e-commerce company wants to build a churn model, but the dataset is dirty and inconsistent
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'order_id': [101, 102, 103, 103, 104],
    'customer_id': [1, 2, 3, 3, 4],
    'order_date': ['2023-01-10', '10/02/2023', 'March 5 2023', 'March 5 2023', 'invalid'],
    'price': ['1,200', '800', '-500', '800', 'NaN'],
    'payment_type': ['Card', 'card ', 'CASH', 'cash', None],
    'delivered': ['Yes', 'no', '1', '1', '0']
})

#1
print(df.info())
print(df.describe())
#2
df = df.drop_duplicates(subset=["order_id"])
#3
def parse_date(x):
    try:
        return pd.to_datetime(x, dayfirst=True, errors="coerce")
    except:
        return np.nan
df["order_date"] = df["order_date"].apply(parse_date)
#4
df["price"] = pd.to_numeric(df["price"].str.replace(",", ""), errors="coerce")
df.loc[df["price"] < 0, "price"] = np.nan
#5
df["payment_type"] = df["payment_type"].str.lower().str.strip()
#6
df["delivered"] = df["delivered"].map({"Yes": True, "1": True, "no": False, "0": False})

# Final Check after All 6 Tasks:
print(df.head())

#ready for ML model now!