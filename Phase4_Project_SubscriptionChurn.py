"""
Context: You are predicting whether a customer churned (churn = 1) or not
Objectives:
~Parse dates
~Handle missing & invalid values & etc...
~Engineer features
~Use Pipeline + ColumnTransformer
~Prevent data leakage
"""

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "customer_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011],
    
    "signup_date": [
        "2022-01-10", "10/02/2022", "March 5 2022",
        "invalid", None, "2022/04/01",
        "2022-01-10", "2022-07-15", "15-08-2022",
        "2022-09-01", "2022-09-01"
    ],
    
    "last_active_date": [
        "2023-01-01", None, "2022-12-30",
        "invalid", "2023-02-01", "2023-01-15",
        "2023-01-01", "2022-07-20", None,
        "2022-09-15", "invalid"
    ],
    
    "age": [25, -5, 35, 200, None, 40, 25, 30, 29, None, 45],
    
    "country": [
        "USA", "U.S.A", "us", "Germany", None,
        "DE", "USA", "France", "france", "USA", None
    ],
    
    "subscription_type": [
        "Basic", "basic", "Premium", "PREMIUM",
        None, "Basic", "Premium", "Basic",
        "premium", "Basic", None
    ],
    
    "monthly_fee": [9.99, None, 19.99, 999, 14.99, 9.99, None, 9.99, 19.99, None, 9.99],
    
    "support_tickets": [0, 1, 2, -1, None, 0, 3, 0, 1, None, 5],
    
    "churn": [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1]
})

# parsing dates
def parse(s):
    if pd.isna(s):
        return pd.NaT

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%B %d %Y"):
        try:
            return pd.to_datetime(s, format=fmt)
        except ValueError:
            continue

    return pd.NaT

df["signup_date"] = df["signup_date"].apply(parse)
df["last_active_date"] = df["last_active_date"].apply(parse)

# engineering feature "age of account", and dropping raw date columns
df["account_age_in_days"] = (df["last_active_date"] - df["signup_date"]).dt.days
df = df.drop(columns=["last_active_date", "signup_date"])

# fixing categorical inconsistencies
df["country"] = df["country"].str.upper().replace({"U.S.A":"USA", "US": "USA", "DE":"GERMANY"})
df["subscription_type"] = df["subscription_type"].str.strip().str.lower()

# converting impossible age & tickets to none
df.loc[(df["support_tickets"] < 0), "support_tickets"] = np.nan
df.loc[(df["age"] < 0) | (df["age"] > 120), "age"] = np.nan

# training-test split
from sklearn.model_selection import train_test_split
x = df.drop(columns=["churn", "customer_id"])
y = df["churn"]
train_X, test_X, train_Y, test_Y = train_test_split(x, y, test_size=0.3, random_state=0)

# filtering outliers for fee
Q1 = train_X["monthly_fee"].quantile(0.25)
Q3 = train_X["monthly_fee"].quantile(0.75)
IQR = Q3 - Q1
train_X.loc[(train_X["monthly_fee"] < Q1-IQR*1.5) | (train_X["monthly_fee"] > Q3+IQR*1.5), "monthly_fee"] = np.nan
test_X.loc[(test_X["monthly_fee"] < Q1-IQR*1.5) | (test_X["monthly_fee"] > Q3+IQR*1.5), "monthly_fee"] = np.nan

# building pipeline
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

num_cols = ["age", "monthly_fee", "support_tickets", "account_age_in_days"]
cat_cols = ["country", "subscription_type"]
num_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
cat_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))])

transformer = ColumnTransformer(transformers=[("num", num_pipeline, num_cols), ("cat", cat_pipeline, cat_cols)])

# modeling
from sklearn.linear_model import LogisticRegression
model = Pipeline(steps=[("preprocessor", transformer), ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))])
model.fit(train_X, train_Y)

# evaluation
from sklearn.metrics import classification_report, confusion_matrix

prediction = model.predict(test_X)

print(confusion_matrix(test_Y, prediction))
print(classification_report(test_Y, prediction))

# cross-validation
from sklearn.model_selection import cross_val_score
cv_scores = cross_val_score(model, train_X, train_Y, cv=3, scoring="f1")
print("CV F1 Scores:", cv_scores)
print("Mean CV F1 Score:", cv_scores.mean())  #RUN ELE, TERMINAL KOHNEDI, CONFUSION MATRIXI YAXSI TEKRARLA!!!

print(df.head(11))
print(train_X.head())
print(test_X.head())

