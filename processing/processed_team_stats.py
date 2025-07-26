# processing/processed_team_stats.py
import pandas as pd

FORMATION_ENCODING = {
    "4-4-2": 0, "4-3-3": 1, "3-5-2": 2, "4-2-3-1": 3, "3-4-3": 4,
    "5-3-2": 5, "5-4-1": 6, "3-4-2-1": 7, "4-5-1": 8, "3-1-4-2": 9,
    "4-1-4-1": 10, "4-3-1-2": 11, "3-3-1-3": 12, "4-1-3-2": 13, "4-2-2-2": 14,
    "3-5-1-1": 15, "5-4-1-1": 16, "3-4-1-2": 17, "4-4-1-1": 18, "5-4-1-1": 19,
    "4-4-1": 21, "3-5-1": 22, "3-4-1": 23, "3-2-4-1": 24, "4-2-4": 25, "4-3-2-1": 26
}

TEAM_ENCODING = {
    "Arsenal": 0, "Aston Villa": 1, "Bournemouth": 2, "Brentford": 3, "Brighton": 4,
    "Burnley": 5, "Chelsea": 6, "Crystal Palace": 7, "Everton": 8, "Fulham": 9,
    "Liverpool": 10, "Luton": 11, "Manchester City": 12, "Manchester United": 13,
    "Newcastle": 14, "Nottingham Forest": 15, "Sheffield Utd": 16,
    "Tottenham": 17, "West Ham": 18, "Wolves": 19
}

def preprocess_team_stats(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ✅ 문자열 → datetime
    df["date"] = pd.to_datetime(df["date"])

    # ✅ team_name 인코딩
    df["team_name"] = df["team_name"].map(TEAM_ENCODING).fillna(-1).astype(int)

    # ✅ formation 인코딩 (결측치는 -1 처리)
    df["home_formation"] = df["home_formation"].map(FORMATION_ENCODING).fillna(-1).astype(int)
    df["away_formation"] = df["away_formation"].map(FORMATION_ENCODING).fillna(-1).astype(int)

    return df[[
        "fixture_id", "team_name", "date", "is_home", "possession",
        "shots_total", "shots_on_goal", "passes", "fouls",
        "cards_yellow", "cards_red", "offsides",
        "home_formation", "away_formation"
    ]]
