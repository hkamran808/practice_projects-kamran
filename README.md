# practice_projects-kamran
practising data mining and analysis, feature engineering, modeling, pipelines in order to improve at data science and get onto bigger projects like ucl match winner predictor, shown below.
-
# UCL Match Winner Predictor

Predicts UEFA Champions League match outcomes using xG, win rate & UEFA coefficients.

**Live demo:** https://huggingface.co/spaces/hkamran808/ucl-match-winner-predictor

## Features
- 3-way prediction: home win / draw / away win
- Uses xG, average goals, win rate, UEFA coefficient
- SMOTE + class weights to handle draw imbalance
- Random Forest trained on 2021–2024 UCL data

## Tech stack
scikit-learn · pandas · Streamlit · imbalanced-learn
