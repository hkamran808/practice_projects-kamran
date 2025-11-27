import numpy as np
import pandas as pd

# datasets
df1 = pd.read_csv("bigger_matches.csv")
df2 = pd.read_csv("team_stats_2021-24.csv")
# merging datasets on team names
df1 = df1.merge(df2, left_on='HOME_TEAM', right_on='TEAM', how='left')
df1 = df1.merge(df2, left_on='AWAY_TEAM', right_on='TEAM', how='left', suffixes=('_HOME', '_AWAY'))

df1.fillna(0, inplace=True)
#print(df1.isna().sum())

# avoiding data leakage by dropping columns that is not considered for true prediction before the match played, and keeping only relevant features
df1.drop(columns=["HOME_GOALS", "AWAY_GOALS"], inplace=True)
X = df1[['AVG_GOALS_HOME', 'AVG_CONCEDED_HOME', 'XG_FOR_HOME', 'XG_AGAINST_HOME',
     'WIN_RATE_HOME', 'UCL_COEFFICIENT_HOME',
     'AVG_GOALS_AWAY', 'AVG_CONCEDED_AWAY', 'XG_FOR_AWAY', 'XG_AGAINST_AWAY',
     'WIN_RATE_AWAY', 'UCL_COEFFICIENT_AWAY']]
Y = df1['RESULT']

print(df1.head())
print(df1.columns)
print(Y.value_counts(normalize=True))  # normalized distribution of target variable

# standardizing features to be more accurate
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_modified = scaler.fit_transform(X)
X_modified = pd.DataFrame(X_modified, columns=X.columns) #conerting back to dataframe for better handling (adding column names back)

print("\n--- Test Set Scores ---")
# splitting data to train and test
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X_modified, Y, test_size=0.2, random_state=42)

# APPLY SMOTE to handle class imbalance
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import SMOTE
sm = SMOTETomek(smote=SMOTE(k_neighbors=3, random_state=42), random_state=42)
X_train_res, Y_train_res = sm.fit_resample(X_train, Y_train)
print("Before SMOTE:", Y_train.value_counts())
print("\nAfter SMOTE:", Y_train_res.value_counts())

# adding class weights to models to handle class imbalance
from sklearn.utils.class_weight import compute_class_weight
weights = compute_class_weight(class_weight='balanced', classes=np.array([-1, 0, 1]), y=Y)
weights_dict = {-1: weights[0], 0: weights[1], 1: weights[2]}


from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
models = {
    "LogReg": LogisticRegression(max_iter=5000),
    "RanFor": RandomForestClassifier(n_estimators=200, class_weight=weights_dict, random_state=42),
    "GradBoost": GradientBoostingClassifier()
}

for name, model in models.items():
    model.fit(X_train_res, Y_train_res)
    print(name, model.score(X_test, Y_test))

print("\n--- Cross Validation Scores ---")
# cross validation to validate the model without trusting only one split
from sklearn.model_selection import cross_val_score
for name, model in models.items():
    score = cross_val_score(model, X_modified, Y, cv=5)
    print(name, score.mean())

# feature importance from random forest
import matplotlib.pyplot as plt
importances = models["RanFor"].feature_importances_
plt.barh(X.columns, importances)
plt.show()

# confusion matrix for random forest (best model)
from sklearn.metrics import confusion_matrix
import seaborn as sns
cm = confusion_matrix(Y_test, models["RanFor"].predict(X_test))
sns.heatmap(cm, annot=True, cmap="Blues")
plt.show()

# after finding best model, we train on full dataset
final_model = RandomForestClassifier(n_estimators=300)
final_model.fit(X, Y)   # here, need raw X for RandomForest to cover all data

# predicting winner of a new match
def predict_match(home, away):
    home_row = df2[df2["TEAM"] == home].iloc[0]  # these return a dataframe, so we use iloc to get the row (0th dimension) as series in home/away_row
    away_row = df2[df2["TEAM"] == away].iloc[0]

    # creating new features for prediction based on the selected teams' stats (home/away_row)
    X_new = pd.DataFrame([{
        "AVG_GOALS_HOME": home_row["AVG_GOALS"],
        "AVG_CONCEDED_HOME": home_row["AVG_CONCEDED"],
        "XG_FOR_HOME": home_row["XG_FOR"],
        "XG_AGAINST_HOME": home_row["XG_AGAINST"],
        "WIN_RATE_HOME": home_row["WIN_RATE"],
        "UCL_COEFFICIENT_HOME": home_row["UCL_COEFFICIENT"],

        "AVG_GOALS_AWAY": away_row["AVG_GOALS"],
        "AVG_CONCEDED_AWAY": away_row["AVG_CONCEDED"],
        "XG_FOR_AWAY": away_row["XG_FOR"],
        "XG_AGAINST_AWAY": away_row["XG_AGAINST"],
        "WIN_RATE_AWAY": away_row["WIN_RATE"],
        "UCL_COEFFICIENT_AWAY": away_row["UCL_COEFFICIENT"]
    }])

    # getting predictions...
    predictions = final_model.predict(X_new)
    # ...and probability
    probabilities = final_model.predict_proba(X_new)

    if predictions == 1:
        print(f"{home} is predicted to WIN against {away}")
    elif predictions == 0:
        print(f"The match between {home} and {away} is predicted to END IN A DRAW")
    else:
        print(f"{away} is predicted to WIN against {home}")

    print(f"Probability for home win: {probabilities[0][2]*100:.1f}%",
          f"Probability for draw: {probabilities[0][1]*100:.1f}%",
          f"Probability for away win: {probabilities[0][0]*100:.1f}%", sep="\n")

H = input("enter home team: ")
A = input("enter away team: ")
predict_match(H, A)

# DETAILED REPORT
from sklearn.metrics import classification_report, accuracy_score
Y_pred = final_model.predict(X_test)
print("Accuracy:", accuracy_score(Y_test, Y_pred))
print("Classification Report:", classification_report(Y_test, Y_pred))


# Some Guides Below:
"""
# encoding teams for model to understand
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df["HOME_TEAM_ENC"] = le.fit_transform(df["HOME_TEAM"])
df["AWAY_TEAM_ENC"] = le.fit_transform(df["AWAY_TEAM"])

#model = LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.5, max_iter=10000)
"""