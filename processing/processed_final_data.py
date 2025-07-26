import pandas as pd
from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY

def fetch_all_rows(supabase, table_name):
    """📥 Fetch all rows from a Supabase table in batches of 1000."""
    batch_size = 1000
    offset = 0
    all_rows = []

    while True:
        response = supabase.table(table_name).select("*").range(offset, offset + batch_size - 1).execute()
        rows = response.data
        if not rows:
            break
        all_rows.extend(rows)
        offset += batch_size

    return all_rows

def merge_all_data():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    # 📥 1. Fetch data
    print("📥 Fetching data from Supabase...")
    player_data = fetch_all_rows(supabase, "preprocessed_player_stat")
    team_data = fetch_all_rows(supabase, "preprocessed_team_stats")
    match_data = fetch_all_rows(supabase, "preprocessed_matches")

    df_players = pd.DataFrame(player_data)
    df_teams = pd.DataFrame(team_data)
    df_matches = pd.DataFrame(match_data)

    print(f"✅ Loaded player stats: {df_players.shape}")
    print(f"✅ Loaded team stats: {df_teams.shape}")
    print(f"✅ Loaded match stats: {df_matches.shape}")

    # 📊 2. Rename to avoid column conflicts
    df_players = df_players.rename(columns={
        "shots_total": "player_shots_total",
        "shots_on_goal": "player_shots_on_goal",
        "passes": "player_passes"
    })
    df_teams = df_teams.rename(columns={
        "shots_total": "team_shots_total",
        "shots_on_goal": "team_shots_on_goal"
    })

    # ✅ 3. Add is_home info to players before merge
    home_info = df_teams[["fixture_id", "team_name", "is_home"]]
    df_players = pd.merge(df_players, home_info, on=["fixture_id", "team_name"], how="left")

    # ❌ Remove duplicate column
    df_matches = df_matches.drop(columns=["date"], errors="ignore")

    # 🧩 4. Merge
    merged = pd.merge(
        df_players,
        df_teams,
        on=["fixture_id", "team_name", "is_home"],
        how="left"
    )
    merged = pd.merge(merged, df_matches, on="fixture_id", how="left")

    # 🧼 5. Fill missing
    merged = merged.fillna(-1)

    # ✅ 6. Final column order
    final_columns = [
        "fixture_id", "player_id", "team_name", "is_starting", "minutes_played",
        "position", "rating", "goals", "assists", "player_shots_total", "player_shots_on_goal",
        "player_passes", "tackles", "duels_won", "fouls_committed", "yellow_cards", "red_cards",
        "is_home", "date", "possession", "team_shots_total", "team_shots_on_goal",
        "fouls", "cards_yellow", "cards_red", "offsides", "home_formation", "away_formation",
        "home_team", "away_team", "home_score", "away_score", "winner", "goal_diff", "venue", "referee"
    ]
    merged = merged[final_columns]

    print(f"✅ Final merged shape: {merged.shape}")
    return merged
