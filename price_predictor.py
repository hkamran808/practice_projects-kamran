import pandas as pd
import sklearn

file = "house_prices.csv"
df = pd.read_csv(file)
print(df.describe())  #for example, mean => print(round(float(df["Price"].mean()), 2))
print(df.head())

# building our model
# simple linear regression
from sklearn.linear_model import LinearRegression
ln = LinearRegression()
X = df[["Size_sqft", "Bedrooms", "Bathrooms", "Age"]]
Y = df["Price"]
ln.fit(X, Y)
print(ln.score(X, Y))  #getting first useful data (r^2 / determination of correlation)

# working with train test split to improve model
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
ln.fit(X_train, Y_train)
print(ln.score(X_test, Y_test))  #getting second useful data (r^2 / determination of correlation)

# features of our model formula: intercept and all coefficients
print(ln.intercept_)
#print(ln.coef_)
for attribute, coef in zip(X.columns, ln.coef_):
    print(f"{attribute}: {coef:.2f}")

Y_pred = ln.predict(X_test) #getting predictions
"""# visualizing the accuracy of our model
import matplotlib.pyplot as plt
plt.scatter(Y_test, Y_pred, color='green')
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.title("Accuracy of the model")
plt.show()
"""
#adding MAE and RMSE
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
mae = mean_absolute_error(Y_test, Y_pred)
rmse = np.sqrt(mean_squared_error(Y_test, Y_pred))
print(f"Mean absolute Error: {mae:.2f}")
print(f"Root Mean Squared Error: {rmse:.2f}")

"""#checking if non-linear patterns exist in the data with the help of polynomial features
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
ln_poly = LinearRegression()
ln_poly.fit(X_poly, Y)
print("Polynomial Regression Rate~: ", ln_poly.score(X_poly, Y))
"""
import joblib
joblib.dump(ln, "house_price_predictor_model.pkl")
print("model saved successfully")

# predicting price of a new house of a user
size = float(input("Enter size in sqft: "))
bedrooms = int(input("Enter number of bedrooms: "))
bathrooms = int(input("Enter number of bathrooms: "))
age = int(input("Enter house age: "))

new_house = [[size, bedrooms, bathrooms, age]]
predicted_price = ln.predict(new_house)
print(f"Predicted price for the new house: ${predicted_price[0]:.2f}")

# ALPHA PARAMETER & CROSS-VALIDATION TO BE ADDED!!!