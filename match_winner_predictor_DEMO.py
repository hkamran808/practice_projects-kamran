import pandas as pd
file = "UEFA Champions League 2016-2022 Data.xlsx"
# names of all sheets
excel = pd.ExcelFile(file)
print(excel.sheet_names)

df = pd.read_excel(file, sheet_name='matches')
#print(df.head())
#print(df.columns)

# dropping unnecessary columns
df.drop(columns=['MATCH_ID', 'SEASON', 'DATE_TIME', 'STADIUM', 'PENALTY_SHOOT_OUT', 'ATTENDANCE'], inplace=True)

# adding target column 'result': 1=homewin, 0=draw, -1=awaywin
def result(row):
    if row["HOME_TEAM_SCORE"] > row["AWAY_TEAM_SCORE"]:
        return 1
    elif row["HOME_TEAM_SCORE"] == row["AWAY_TEAM_SCORE"]:
        return 0
    else:
        return -1
    
df['RESULT'] = df.apply(result, axis=1)

# encoding teams for model to understand
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df["HOME_TEAM_ENC"] = le.fit_transform(df["HOME_TEAM"])
df["AWAY_TEAM_ENC"] = le.fit_transform(df["AWAY_TEAM"])

# setting features and target variable
X = df[['HOME_TEAM_ENC', 'AWAY_TEAM_ENC', 'HOME_TEAM_SCORE', 'AWAY_TEAM_SCORE']]
X = X.drop(columns=['HOME_TEAM_SCORE', 'AWAY_TEAM_SCORE'])  #removing scores to avoid data leakage
Y = df['RESULT']

# splitting data to work on
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

# training model
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.5, max_iter=10000)
model.fit(X_train, Y_train)
print("Accuracy:", model.score(X_test, Y_test))

# adding report
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
Y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(Y_test, Y_pred))
print("Classification Report:", classification_report(Y_test, Y_pred))
print("Confusion Matrix:\n", confusion_matrix(Y_test, Y_pred))
