import pandas as pd
df = pd.read_csv("student_performance_project.csv")
"""
#basic info/analysis
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

df_clean = df.copy() #copying original data to keep it clean

#t-test
from scipy.stats import ttest_ind
group_completed = df_clean[df_clean['test_preparation'] == 'completed']['avg_score']
group_none = df_clean[df_clean['test_preparation'] == 'none']['avg_score']

t_stat, p_value = ttest_ind(
    group_completed,
    group_none,
    equal_var=False,
    alternative='greater')
print("t-test result: ", t_stat, p_value)

#z-test (when metric is binary)
from statsmodels.stats.proportion import proportions_ztest

successes = [df_clean[df_clean['test_preparation']=='completed']['pass_fail'].sum(),
             df_clean[df_clean['test_preparation']=='none']['pass_fail'].sum()]
nobs = [len(df_clean[df_clean['test_preparation']=='completed']),
        len(df_clean[df_clean['test_preparation']=='none'])]

z_stat, p_val = proportions_ztest(successes, nobs, alternative='larger')
print("z-test result: ", z_stat, p_val)

#contingency & chi-square test
contingency = pd.crosstab(df_clean['test_preparation'], df_clean['pass_fail'])
print("contingency:", contingency)
from scipy.stats import chi2_contingency
chi2, p, dof, expected = chi2_contingency(contingency)
print("chi-square test result: ", chi2, p)

#calculating uplift
mean_control = df_clean[df_clean['test_preparation']=='none']['avg_score'].mean()
mean_treatment = df_clean[df_clean['test_preparation']=='completed']['avg_score'].mean()

uplift = mean_treatment - mean_control
print(f"mean_treatment ({mean_treatment}) - mean_control ({mean_control}) = uplift ({uplift})")
