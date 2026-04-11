import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="UCL Match Predictor", page_icon="⚽", layout="centered")

@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_teams():
    df = pd.read_csv("team_stats_clean.csv")
    return df

bundle = load_model()
model = bundle["model"]
scaler = bundle["scaler"]
df2 = load_teams()
teams = sorted(df2["TEAM"].tolist())

st.title("UCL Match Predictor")
st.caption("Predicts UEFA Champions League match outcomes using xG, win rate & UEFA coefficients")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Home team**")
    home = st.selectbox("Home", teams, label_visibility="collapsed")
with col2:
    st.markdown("**Away team**")
    away = st.selectbox("Away", teams, index=1, label_visibility="collapsed")

if home == away:
    st.warning("Please select two different teams.")
else:
    if st.button("Predict match", use_container_width=True):
        home_row = df2[df2["TEAM"] == home].iloc[0]
        away_row = df2[df2["TEAM"] == away].iloc[0]

        X_new = pd.DataFrame([{
            "AVG_GOALS_HOME":      home_row["AVG_GOALS"],
            "AVG_CONCEDED_HOME":   home_row["AVG_CONCEDED"],
            "XG_FOR_HOME":         home_row["XG_FOR"],
            "XG_AGAINST_HOME":     home_row["XG_AGAINST"],
            "WIN_RATE_HOME":       home_row["WIN_RATE"],
            "UCL_COEFFICIENT_HOME":home_row["UCL_COEFFICIENT"],
            "AVG_GOALS_AWAY":      away_row["AVG_GOALS"],
            "AVG_CONCEDED_AWAY":   away_row["AVG_CONCEDED"],
            "XG_FOR_AWAY":         away_row["XG_FOR"],
            "XG_AGAINST_AWAY":     away_row["XG_AGAINST"],
            "WIN_RATE_AWAY":       away_row["WIN_RATE"],
            "UCL_COEFFICIENT_AWAY":away_row["UCL_COEFFICIENT"],
        }])

        X_scaled = scaler.transform(X_new)
        pred = model.predict(X_scaled)[0]
        proba = model.predict_proba(X_scaled)[0]

        # Map class order: your classes are [-1, 0, 1]
        # predict_proba returns columns in sorted class order
        prob_away = proba[0] * 100
        prob_draw = proba[1] * 100
        prob_home = proba[2] * 100

        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric(f"{home} win", f"{prob_home:.1f}%")
        c2.metric("Draw", f"{prob_draw:.1f}%")
        c3.metric(f"{away} win", f"{prob_away:.1f}%")

        if pred == 1:
            st.success(f"Predicted result: {home} wins")
        elif pred == 0:
            st.info("Predicted result: Draw")
        else:
            st.success(f"Predicted result: {away} wins")

        st.divider()
        st.markdown("**Team stats comparison**")
        stats_df = pd.DataFrame({
            "Stat": ["Avg goals", "Avg conceded", "xG for", "xG against", "Win rate", "UCL coefficient"],
            home: [home_row["AVG_GOALS"], home_row["AVG_CONCEDED"], home_row["XG_FOR"],
                   home_row["XG_AGAINST"], f'{home_row["WIN_RATE"]:.0%}', home_row["UCL_COEFFICIENT"]],
            away: [away_row["AVG_GOALS"], away_row["AVG_CONCEDED"], away_row["XG_FOR"],
                   away_row["XG_AGAINST"], f'{away_row["WIN_RATE"]:.0%}', away_row["UCL_COEFFICIENT"]],
        })
        st.dataframe(stats_df, hide_index=True, use_container_width=True)