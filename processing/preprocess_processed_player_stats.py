# processing/preprocess_processed_player_stats.py
import pandas as pd

TEAM_ENCODING = {
    "Arsenal": 0, "Aston Villa": 1, "Bournemouth": 2, "Brentford": 3, "Brighton": 4,
    "Burnley": 5, "Chelsea": 6, "Crystal Palace": 7, "Everton": 8, "Fulham": 9,
    "Liverpool": 10, "Luton": 11, "Manchester City": 12, "Manchester United": 13,
    "Newcastle": 14, "Nottingham Forest": 15, "Sheffield Utd": 16,
    "Tottenham": 17, "West Ham": 18, "Wolves": 19
}

POSITION_ENCODING = {
    "D": 1,
    "F": 2,
    "G": 3,
    "M": 4
}

def preprocess_player_stats(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ✅ Drop player_name
    df = df.drop(columns=["player_name"], errors="ignore")

    # ✅ Encode team_name
    df["team_name"] = df["team_name"].map(TEAM_ENCODING).fillna(-1).astype(int)

    # ✅ Encode position
    df["position"] = df["position"].map(POSITION_ENCODING).fillna(-1).astype(int)

    # ✅ is_starting → int (True/False → 1/0)
    df["is_starting"] = df["is_starting"].astype(int)

    return df[[
        "fixture_id", "player_id", "team_name", "is_starting", "minutes_played",
        "position", "rating", "goals", "assists", "shots_total", "shots_on_goal",
        "passes", "tackles", "duels_won", "fouls_committed", "yellow_cards", "red_cards"
    ]]
