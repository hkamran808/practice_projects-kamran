"""
The purpose of Project 2 is to improve baseline model from Project 1 by:

~Applying feature engineering to extract more predictive information from your dataset
~Implementing proper validation techniques to ensure your improvements are genuine and not overfitting
~Preparing a robust pipeline that can handle unseen data and can later be extended to more advanced models
"""

#Mean Absolute Error: 105891.87533810796
import pandas as pd
import numpy as np

df = pd.read_csv("house_prices_2.csv")
x = df.drop(columns="SalePrice")
y = df["SalePrice"]

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3, random_state=0)

num_cols = ["OverallQual", "GarageCars", "TotRmsAbvGrd", "LotArea", "YearBuilt", "Fireplaces"]
cat_cols = ["Neighborhood", "HouseStyle", "ExterQual", "KitchenQual"]

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

num_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
cat_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))])

from sklearn.compose import ColumnTransformer
preprocessor_model = ColumnTransformer(transformers=[("numerical", num_pipeline, num_cols), ("categorical", cat_pipeline, cat_cols)])

from sklearn.linear_model import LinearRegression
model = LinearRegression()
modeling = Pipeline(steps=[("preprocessor", preprocessor_model), ("model", model)])

modeling.fit(X_train, Y_train)
predictions = modeling.predict(X_test)

"""
#checking skewness, ...
import matplotlib.pyplot as plt
df.boxplot() # or df.hist()
plt.show()
"""
# checking correlation between every feature and target
for col in num_cols:
    print(f"{col}:", df[col].corr(df["SalePrice"]))

# detecting and understanding what methods to apply those features to improve model...