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
from sklearn.preprocessing import OneHotEncoder

num_pipeline_rf = Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))])

cat_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")), 
                               ("encoder", OneHotEncoder(handle_unknown="ignore"))])

# adding feature engineering steps back for LotArea and YearBuilt
from sklearn.preprocessing import FunctionTransformer
def log_transform(x):
    return np.log1p(x)
def year_to_age(x):
    return 2026 - x

lot_area_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), 
                                    ("lot area", FunctionTransformer(log_transform))])

age_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), 
                                    ("age", FunctionTransformer(year_to_age))])

from sklearn.compose import ColumnTransformer
preprocessor_rf = ColumnTransformer(transformers=[("numerical", num_pipeline_rf, num_cols_improvised), 
                                                     ("categorical", cat_pipeline, cat_cols),
                                                     ("lot_area", lot_area_pipeline, ["LotArea"]),
                                                     ("age", age_pipeline, ["YearBuilt"])])

# Trying non-linear models which can further improve performance. PS: max_leaf_nodes=5,max_depth=None is removed to unlock full random forest regressor capacity
from sklearn.ensemble import RandomForestRegressor
rf_model = RandomForestRegressor(n_estimators=300, 
                                 random_state=0, 
                                 n_jobs=-1)
rf_pipeline = Pipeline(steps=[("preprocessor", preprocessor_rf),
                              ("model", rf_model)])
rf_pipeline.fit(X_train, Y_train)
rf_prediction = rf_pipeline.predict(X_test)

# Error diagnostics for non-linear model (RF)
from sklearn.metrics import mean_absolute_error
rf_mae = mean_absolute_error(Y_test, rf_prediction)
print(f"Random Forest MAE: {rf_mae}")

# Visualizing predictions vs actuals and residuals to understand model performance better: CHANGED TO original_scale_predictions
import matplotlib.pyplot as plt
scatter_plot = plt.scatter(Y_test, rf_prediction, alpha=0.5)
plt.xlabel("Actual SalePrice")
plt.ylabel("Predicted SalePrice")
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], 'r--')
plt.show()

residual = Y_test - rf_prediction
residual_plot = plt.scatter(rf_prediction, residual, alpha=0.5)
plt.xlabel("Predicted SalePrice")
plt.ylabel("Residuals")
plt.axhline(y=0, color='r', linestyle='--')
plt.show()

# Feature importance from RF model
preprocessor = rf_pipeline.named_steps["preprocessor"]
model = rf_pipeline.named_steps["model"]

num_features = num_cols_improvised # no need for ["LotArea", "YearBuilt"], because they are not raw features
cat_features = preprocessor.named_transformers_["categorical"].named_steps["encoder"].get_feature_names_out(cat_cols).tolist()
engineered_features = ["LotArea_lot area", "YearBuilt_age"]
all_features = np.concatenate([num_features, cat_features, engineered_features]) # or  all_features = num_features + cat_features + engineered_features
assert len(all_features) == len(model.feature_importances_)

print("Feature importances from Random Forest Model:")
importances = model.feature_importances_
importances_df = pd.DataFrame({
    "Feature": all_features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

# Summing importance of base features (after they be splitted with one-hot encoding)
importances_df["base_feature"] = importances_df["Feature"].str.split("_").str[0]
grouped_importance = importances_df.groupby("base_feature")["Importance"].sum().sort_values(ascending=False)

print(importances_df)
print(grouped_importance)
# Random Forest MAE: 99137.56288888889, least MAE so far. Improved from linear model's MAE: 113909.54201972325