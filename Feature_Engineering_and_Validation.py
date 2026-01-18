"""
The purpose of Project 2 is to improve baseline model from Project 1 by:

~Applying feature engineering to extract more predictive information from your dataset
~Implementing proper validation techniques to ensure your improvements are genuine and not overfitting
~Preparing a robust pipeline that can handle unseen data and can later be extended to more advanced models
"""

import pandas as pd
import numpy as np

df = pd.read_csv("house_prices_2.csv")
x = df.drop(columns="SalePrice")
y = df["SalePrice"]

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3, random_state=0)

num_cols_improvised = ["OverallQual", "GarageCars", "TotRmsAbvGrd", "Fireplaces"] #"LotArea", "YearBuilt" are no longer needed here
cat_cols = ["Neighborhood", "HouseStyle", "ExterQual", "KitchenQual"]

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

num_pipeline_improvised = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), 
                                          ("scaler", StandardScaler())])

cat_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")), 
                               ("encoder", OneHotEncoder(handle_unknown="ignore"))])

# detecting and understanding what methods to apply those features to improve model
def log_transform(x):
    return np.log1p(x)
def year_to_age(x):
    return 2026 - x

from sklearn.preprocessing import FunctionTransformer
lot_area_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), 
                                    ("lot area", FunctionTransformer(log_transform)), 
                                    ("scaler", StandardScaler())])

age_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), 
                                    ("age",  FunctionTransformer(year_to_age)), 
                                    ("scaler", StandardScaler())])

from sklearn.compose import ColumnTransformer
preprocessor_model = ColumnTransformer(transformers=[("numerical", num_pipeline_improvised, num_cols_improvised), 
                                                     ("categorical", cat_pipeline, cat_cols)])


preprocessor_model_improvised = ColumnTransformer(transformers=[
    ("lotarea", lot_area_pipeline, ["LotArea"]),
    ("age", age_pipeline, ["YearBuilt"]),
    ("other_numeric", num_pipeline_improvised, num_cols_improvised),
    ("categorical", cat_pipeline, cat_cols)])

from sklearn.linear_model import LinearRegression
model = LinearRegression()
modeling_improvised = Pipeline(steps=[("preprocessor", preprocessor_model_improvised), 
                           ("model", model)])

# Target transformation for better modeling (avoiding heteroscedasticity, etc...)
Y_train_log = np.log1p(Y_train)

modeling_improvised.fit(X_train, Y_train_log)
predictions = modeling_improvised.predict(X_test)
original_scale_predictions = np.expm1(predictions)

#Mean Absolute Error: 300695.81500626105 after log transform of target (failure)
"""
#checking skewness, ...
import matplotlib.pyplot as plt
df.boxplot() # or df.hist()
plt.show()
"""
"""
# checking correlation between every feature and target
for col in num_cols_improvised + ["LotArea", "YearBuilt"]:
    print(f"{col}:", df[col].corr(df["SalePrice"]))
"""

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(Y_test, original_scale_predictions)
print(f"Mean Absolute Error: {mae}")
print("Improvised modeling complete and evaluated!")

#Mean Absolute Error before feature engineering: 105891.87533810796
#Mean Absolute Error after feature engineering: 113909.54201972325

# Visualizing predictions vs actuals and residuals to understand model performance better: CHANGED TO original_scale_predictions
import matplotlib.pyplot as plt
scatter_plot = plt.scatter(Y_test, original_scale_predictions, alpha=0.5)
plt.xlabel("Actual SalePrice")
plt.ylabel("Predicted SalePrice")
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'r--')
plt.show()

residual = Y_test - original_scale_predictions
residual_plot = plt.scatter(original_scale_predictions, residual, alpha=0.5)
plt.xlabel("Predicted SalePrice")
plt.ylabel("Residuals")
plt.axhline(y=0, color='r', linestyle='--')
plt.show()
