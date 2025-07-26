# processing/preprocess_player_stats.py
import pandas as pd

def clean_player_stats(raw_player_stats, fixture_id):
    rows = []

    for team_entry in raw_player_stats:
        team_name = team_entry["team"]["name"]
        players = team_entry["players"]

        for player_entry in players:
            player = player_entry["player"]
            stats = player_entry["statistics"][0]  # 대부분 1개만 존재

            row = {
                "fixture_id": fixture_id,
                "team_name": team_name,
                "player_id": player["id"],
                "player_name": player["name"],
                "is_starting": stats.get("games", {}).get("substitute") == False,
                "minutes_played": stats.get("games", {}).get("minutes", 0),
                "position": stats.get("games", {}).get("position", ""),
                "rating": float(stats.get("games", {}).get("rating", 0)) if stats.get("games", {}).get("rating") else None,
                "goals": stats.get("goals", {}).get("total", 0),
                "assists": stats.get("goals", {}).get("assists", 0),
                "shots_total": stats.get("shots", {}).get("total", 0),
                "shots_on_goal": stats.get("shots", {}).get("on", 0),
                "passes": stats.get("passes", {}).get("total", 0),
                "tackles": stats.get("tackles", {}).get("total", 0),
                "duels_won": stats.get("duels", {}).get("won", 0),
                "fouls_committed": stats.get("fouls", {}).get("committed", 0),
                "yellow_cards": stats.get("cards", {}).get("yellow", 0),
                "red_cards": stats.get("cards", {}).get("red", 0)
            }

            rows.append(row)

    return pd.DataFrame(rows)
