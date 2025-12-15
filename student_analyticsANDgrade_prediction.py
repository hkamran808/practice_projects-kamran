import pandas as pd

df = pd.read_csv("student_performance_project.csv")

#basic info/analysis
"""
print(df.head())
print(df.info())
print(df.describe(include='all'))
"""
#searching for outliers
from scipy.stats import zscore
numeric_cols = ["study_hours", "sleep_hours", "math_score", "reading_score", "writing_score"]
z_scores = df[numeric_cols].apply(zscore)
outliers_z = (z_scores.abs() > 3)
print(10*"-", "With Z-Score", 10*"-")
print(outliers_z.sum())

Q1 = df[numeric_cols].quantile(0.25)
Q3 = df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1
outliers_iqr = ((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR)))
print(10*"-", "With IQR", 10*"-")
print(outliers_iqr.sum())

#visualization of columns to see distributions and outliers
import matplotlib.pyplot as plt
df[numeric_cols].boxplot(figsize=(10,5))
plt.title("Boxplot of numeric features")
plt.show()

#df_clean = df.copy()