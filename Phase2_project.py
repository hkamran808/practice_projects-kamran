import pandas as pd
import numpy as np

df = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 4],
    'age': [25, -5, 40, 300, 40],
    'job': ['Engineer', 'engineer ', 'Doctor', 'doctor', 'Doctor'],
    'income': [50000, np.nan, 120000, 9999999, 120000],
    'loan_amount': [20000, 15000, 30000, 500000, 30000],
    'loan_status': ['Approved', 'Rejected', 'Approved', 'Approved', 'Approved']
})

#1
print(df.info())
print(df.describe())
#2
df = df.drop_duplicates(subset="customer_id")
#3
df["job"] = df["job"].str.strip().str.title()
df["job"] = df["job"].astype("category")
#4
df.loc[(df["age"] < 0 | df["age"] > 120), "age"] = np.nan
#5
df["income"] = df.groupby("job")["income"].transform(lambda x: x.fillna(x.median()))
#6
Q1 = df["income"].quantile(0.25)
Q3 = df["income"].quantile(0.75)
IQR = Q3 - Q1
df["income"] = df["income"].clip(lower= Q1 - 1.5*IQR, upper= Q3 + 1.5*IQR)
#7
target_variable = "loan_status"
Y = df[target_variable]
X = df.drop(columns=target_variable)
#8
from sklearn.preprocessing import StandardScaler
model = StandardScaler()
numerical_cols = ['age', 'income', 'loan_amount']
X[numerical_cols] = model.fit_transform(X[numerical_cols])

# Final Check after All 8 Tasks:
print(X.info())
print(Y.value_counts())