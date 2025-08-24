# processing/preprocess_matches.py

import pandas as pd

# ✅ 인코딩 딕셔너리 (팀, 경기장, 심판)
TEAM_ENCODING = {
    "Arsenal": 0, "Aston Villa": 1, "Bournemouth": 2, "Brentford": 3, "Brighton": 4,
    "Burnley": 5, "Chelsea": 6, "Crystal Palace": 7, "Everton": 8, "Fulham": 9,
    "Liverpool": 10, "Luton": 11, "Manchester City": 12, "Manchester United": 13,
    "Newcastle": 14, "Nottingham Forest": 15, "Sheffield Utd": 16,
    "Tottenham": 17, "West Ham": 18, "Wolves": 19
}

VENUE_ENCODING = {
    "American Express Stadium": 0, "Anfield": 1, "Bramall Lane": 2, "Craven Cottage": 3,
    "Emirates Stadium": 4, "Etihad Stadium": 5, "Goodison Park": 6,
    "Gtech Community Stadium": 7, "Kenilworth Road": 8, "London Stadium": 9,
    "Molineux Stadium": 10, "Old Trafford": 11, "Selhurst Park": 12,
    "Stamford Bridge": 13, "St. James' Park": 14, "The American Express Community Stadium": 15,
    "The City Ground": 16, "Tottenham Hotspur Stadium": 17, "Turf Moor": 18,
    "Villa Park": 19, "Vitality Stadium": 20
}

REFEREE_ENCODING = {
    "A. Madley": 0, "A. Taylor": 1, "C. Kavanagh": 2, "C. Pawson": 3, "D. Bond": 4,
    "D. Coote": 5, "D. England": 6, "G. Scott": 7, "J. Brooks": 8, "J. Gillett": 9,
    "J. Smith": 10, "L. Smith": 11, "M. Donohue": 12, "M. Oliver": 13,
    "M. Salisbury": 14, "P. Bankes": 15, "P. Tierney": 16, "R. Jones": 17,
    "R. Madley": 18, "R. Welch": 19, "S. Allison": 20, "S. Attwell": 21,
    "S. Barrott": 22, "S. Hooper": 23, "S. Singh": 24, "T. Bramall": 25,
    "T. Harrington": 26, "T. Robinson": 27
}

def preprocess_match_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ✅ 문자열 → timestamp
    df["date"] = pd.to_datetime(df["date"])

    # ✅ goal_diff
    df["goal_diff"] = (df["home_score"] - df["away_score"]).abs()

    # ✅ 인코딩 매핑 + 결측값은 -1 처리
    df["home_team"] = df["home_team"].map(TEAM_ENCODING).fillna(-1).astype(int)
    df["away_team"] = df["away_team"].map(TEAM_ENCODING).fillna(-1).astype(int)
    df["venue"] = df["venue"].map(VENUE_ENCODING).fillna(-1).astype(int)
    df["referee"] = df["referee"].map(REFEREE_ENCODING).fillna(-1).astype(int)

    return df[[
        "fixture_id", "date", "home_team", "away_team", "home_score",
        "away_score", "winner", "goal_diff", "venue", "referee"
    ]]

