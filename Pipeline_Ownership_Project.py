# no need for data cleaning since it is well prepared
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

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(Y_test, predictions)
print(f"Mean Absolute Error: {mae}")
print("Modeling complete and evaluated!")  #Mean Absolute Error: 105891.87533810796