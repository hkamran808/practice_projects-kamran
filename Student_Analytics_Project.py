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
print(10*"=", "T-Test Result", 10*"=")
print(t_stat, p_value)

#z-test (when metric is binary)
from statsmodels.stats.proportion import proportions_ztest

successes = [df_clean[df_clean['test_preparation']=='completed']['pass_fail'].sum(),
             df_clean[df_clean['test_preparation']=='none']['pass_fail'].sum()]
nobs = [len(df_clean[df_clean['test_preparation']=='completed']),
        len(df_clean[df_clean['test_preparation']=='none'])]

z_stat, p_val = proportions_ztest(successes, nobs, alternative='larger')
print(10*"=", "Z-Test Result", 10*"=")
print(z_stat, p_val)

#contingency & chi-square test
contingency = pd.crosstab(df_clean['test_preparation'], df_clean['pass_fail'])
print(10*"=", "Contingency", 10*"=")
print(contingency)
from scipy.stats import chi2_contingency
chi2, p, dof, expected = chi2_contingency(contingency)
print(10*"=", "Chi-Square Test Result", 10*"=")
print(chi2, p)

#calculating uplift
mean_control = df_clean[df_clean['test_preparation']=='none']['avg_score'].mean()
mean_treatment = df_clean[df_clean['test_preparation']=='completed']['avg_score'].mean()

uplift = mean_treatment - mean_control
print(10*"=", "Calculating Uplift", 10*"=")
print(f"mean_treatment ({mean_treatment}) - mean_control ({mean_control}) = uplift ({uplift})")

#1. Preparing Data
from sklearn.model_selection import train_test_split
features = [
    "study_hours",
    "sleep_hours",
    "math_score",
    "reading_score",
    "writing_score"
]
x = df[features]
y = df["pass_fail"]

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=1)

#2. scaling to avoid imbalance
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#3. Logistic Regressor Model
from sklearn.linear_model import LogisticRegression
LR_model = LogisticRegression()
LR_model.fit(X_train_scaled, Y_train)
prediction_LR = LR_model.predict(X_test_scaled) #0-fail, 1-pass

#Accuracy and Report
from sklearn.metrics import accuracy_score, classification_report
print(10*"=", "Accuracy", 10*"=")
print(accuracy_score(Y_test, prediction_LR))

print(10*"=", "Classification Report", 10*"=")
print(classification_report(Y_test, prediction_LR))

#4. Interpreting LR Model (weights of features=> '+' is increase | '-' is decrease of probability of class 1 (pass))
print(10*"=", "Interpretation of LR Model: + means increase | - means decrease of probability of pass", 10*"=")
for feature, coef in zip(features, LR_model.coef_[0]):
    print(feature, coef)
"""
ps: we use [0] to get into array, because coef_ is 2D
coef_[0] represents how features affect the probability of the positive class (label 1)
"""

#5. K-Nearest-Neighbors (w/ accuracy & report)
print(10*"=", "K-Nearest-Neighbors Results", 10*"=")
from sklearn.neighbors import KNeighborsClassifier
for i in [1, 3, 5, 10, 20]:
    knn_model = KNeighborsClassifier(n_neighbors=i)
    knn_model.fit(X_train_scaled, Y_train)
    prediction_KNN = knn_model.predict(X_test_scaled)
    prediction_probabilities_KNN = knn_model.predict_proba(X_test_scaled)

    print(f"Accuracy with {i} nearest neighbors: ", {accuracy_score(Y_test, prediction_KNN)})
    print(f"Classification Report for {i} nearest neighbors: ", {classification_report(Y_test, prediction_KNN)})

#6. Naive Bayes
print(10*"=", "Naive Bayes Results", 10*"=")
from sklearn.naive_bayes import GaussianNB
NB_model = GaussianNB()
NB_model.fit(X_train_scaled, Y_train)
prediction_NB = NB_model.predict(X_test_scaled)
prediction_probabilities_NB = NB_model.predict_proba(X_test_scaled)

from sklearn.metrics import accuracy_score, classification_report
print("Accuracy (Naive Bayes):", accuracy_score(Y_test, prediction_NB))
print("Classification Report (Naive Bayes):", classification_report(Y_test, prediction_NB))

#Interpretation of NB model
print("Mean per class: ", NB_model.theta_) # mean per feature per class
print("Variance per class: ", NB_model.var_) # variance per feature per class

#7. K-Means
print(10*"=", "K-Means Results", 10*"=")
from sklearn.cluster import KMeans

KM_model = KMeans(n_clusters=2, random_state=1) # number of classes (pass/fail)
KM_model.fit(X_train_scaled)

cluster_labels = KM_model.labels_  # Get cluster labels assigned by K-Means
import numpy as np
from scipy.stats import mode
mapped_labels = np.zeros_like(cluster_labels) # Map clusters to actual classes (pass/fail)

for cluster in range(2):  # 2 clusters, and for each cluster, assign the most frequent label inside it
    true_false = (cluster_labels == cluster)
    mapped_labels[true_false] = mode(Y_train[true_false])[0]

# Predict on test data
cluster_labels_test = KM_model.predict(X_test_scaled)
mapped_labels_test = np.zeros_like(cluster_labels_test)  #mapping labels again on test set
for cluster in range(2):
    true_false = (cluster_labels_test == cluster)
    mapped_labels_test[true_false] = mode(Y_test[true_false])[0]

# Accuracy and Report
print("Accuracy of K-Means: ", accuracy_score(Y_test, mapped_labels_test))
print("Classification Report of K-Means: ", classification_report(Y_test, mapped_labels_test))

#8. SUMMARY
print(10*"=", "Final Results", 10*"=")
model_names = ["Logistic Regression", "Naive Bayes", "K-Means"]
accuracies = [
    accuracy_score(Y_test, prediction_LR),
    accuracy_score(Y_test, prediction_KNN),
    accuracy_score(Y_test, prediction_NB),
    accuracy_score(Y_test, mapped_labels_test)
]
for name, acc in zip(model_names, accuracies):
    print(f"{name}'s accuracy: {acc}")