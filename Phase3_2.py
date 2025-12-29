# Clean a messy real-world dataset and prepare it correctly for machine learning
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105, 106, 107],
    'order_date': [
        '2023-01-10', '10/02/2023', 'March 5 2023',
        'invalid', '2023/04/01', None, '2023-01-10'
    ],
    'customer_age': [25, -1, 35, 120, None, 40, 25],
    'country': ['USA', 'U.S.A', 'us', 'Germany', None, 'Germany', 'USA'],
    'product_category': ['Electronics', 'electronics', 'Clothing',
                          'Clothes', 'Clothing', None, 'Electronics'],
    'price': [299.99, None, 49.99, 5000, 79.99, 89.99, None],
    'quantity': [1, 2, 1, 1, 0, 1, 1],
    'returned': [0, 1, 0, 1, 0, 0, 1]
})

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", dayfirst=True)
df.loc[(df["customer_age"] < 0) | (df["customer_age"] > 120), "customer_age"] = np.nan
df.loc[df["quantity"] < 1, "quantity"] = np.nan
df["country"] = df["country"].str.upper().str.strip()
df["country"] = df["country"].replace({"U.S.A": "USA", "US": "USA"})
df["product_category"] = df["product_category"].str.lower().replace({"clothes": "clothing"})
df = df.drop_duplicates()
df.loc[(df["price"] <= 0) | (df["price"] > 3000), "price"] = np.nan

from sklearn.model_selection import train_test_split
# target is "returned"
x = df.drop(columns=["returned"])
y = df["returned"]
train_X, test_X, train_Y, test_Y = train_test_split(x, y, test_size=0.3, random_state=0)

#imputation
num_cols = ['customer_age', 'price', 'quantity']
cat_cols = ['country', 'product_category']
for col in num_cols:
    median = train_X[col].median()
    train_X[col] = train_X[col].fillna(median)
    test_X[col] = test_X[col].fillna(median)
for col in cat_cols:
    mode = train_X[col].mode()[0]
    train_X[col] = train_X[col].fillna(mode)
    test_X[col] = test_X[col].fillna(mode)

# replacing missing dates with median date to prevent 'NaT's
median_date = train_X["order_date"].median()
train_X["order_date"] = train_X["order_date"].fillna(median_date)
test_X["order_date"] = test_X["order_date"].fillna(median_date)

# feature engineering example:
for df_ in [train_X, test_X]:
    df_["order_month"] = df_["order_date"].dt.month
    df_["order_day"] = df_["order_date"].dt.dayofweek
    df_.drop(columns=["order_date"], inplace=True)

# ML-ready check:
print(df.head())
print(df.info())
print(train_X.isna().sum())
print(test_X.isna().sum())