import pandas as pd

filepath = "sales_data.csv"
df = pd.read_csv(filepath)
print(df.head())

mean_val = float(df["Unit_Price"].mean())
print(round(mean_val, 2))

correlation = df["Units_Sold"].corr(df["Unit_Price"])
print(correlation)

df_filtered = df[df["Units_Sold"] > 90]
print(df_filtered)


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.title("Total Sales vs Unit Price")
#plt.scatter(df["Total_Sales"], df["Unit_Price"])
#plt.plot(sorted(df["Total_Sales"]), df["Unit_Price"], label="Total Sales vs Unit Price", color='blue', linestyle='-')
plt.xlabel("Total Sales")
plt.ylabel("Unit Price")
#plt.legend()
#plt.show()

import seaborn as sns

sns.regplot(x="Total_Sales", y="Unit_Price", data=df)
plt.title("Total Sales vs Unit Price with Regression Line")
plt.ylim(0,)
plt.show()