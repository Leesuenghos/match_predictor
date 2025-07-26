# processing/preprocess_fixtures.py
import pandas as pd

def clean_fixture_data(raw_fixtures):
    rows = []

    for match in raw_fixtures:
        fixture = match["fixture"]
        teams = match["teams"]
        goals = match["goals"]

        row = {
            "fixture_id": fixture["id"],
            "date": fixture["date"],
            "home_team": teams["home"]["name"],
            "away_team": teams["away"]["name"],
            "home_score": goals["home"],
            "away_score": goals["away"],
            "venue": fixture["venue"]["name"],
            "referee": fixture.get("referee")
        }

        # Target: winner
        if goals["home"] > goals["away"]:
            row["winner"] = 1
        elif goals["home"] < goals["away"]:
            row["winner"] = 2
        else:
            row["winner"] = 0

        rows.append(row)

    return pd.DataFrame(rows)
