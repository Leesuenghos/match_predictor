# processing/preprocess_team_stats.py
import pandas as pd

def extract_stat(statistics, stat_name):
    for stat in statistics:
        if stat["type"].lower() == stat_name.lower():
            value = stat["value"]
            if isinstance(value, str) and "%" in value:
                return float(value.replace("%", "").strip())
            return value if value is not None else 0
    return 0  # 기본값

def clean_team_stats(raw_stats, fixture_id, date):
    rows = []

    for entry in raw_stats:
        team_name = entry["team"]["name"]
        is_home = entry["team"]["id"] == raw_stats[0]["team"]["id"]  # 첫 번째 팀을 홈팀으로 간주
        statistics = entry["statistics"]

        row = {
            "fixture_id": fixture_id,
            "date": date,
            "team_name": team_name,
            "is_home": is_home,
            "possession": extract_stat(statistics, "Ball Possession"),
            "shots_total": extract_stat(statistics, "Total Shots"),
            "shots_on_goal": extract_stat(statistics, "Shots on Goal"),
            "passes": extract_stat(statistics, "Passes"),
            "fouls": extract_stat(statistics, "Fouls"),
            "cards_yellow": extract_stat(statistics, "Yellow Cards"),
            "cards_red": extract_stat(statistics, "Red Cards"),
            "offsides": extract_stat(statistics, "Offsides"),
        }

        rows.append(row)

    return pd.DataFrame(rows)