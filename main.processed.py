import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# 📦 팀 스탯 관련 import
from api.fetch_team_stats import fetch_team_stats_for_fixture
from processing.preprocess_team_stats import clean_team_stats
from processing.processed_team_stats import preprocess_team_stats
from pipeline.upload_processed_team_stats import upload_processed_team_stats

# 📦 선수 스탯 관련 import
from api.fetch_player_stats import fetch_player_stats_for_fixture
from processing.preprocess_player_stats import clean_player_stats
from processing.preprocess_processed_player_stats import preprocess_player_stats
from pipeline.upload_processed_player_stats import upload_processed_player_stats

# 공통
from api.fetch_fixtures import fetch_fixtures_raw
from processing.preprocess_fixtures import clean_fixture_data
from pipeline.utils import get_uploaded_fixture_ids
from config.settings import API_KEY, BASE_URL
import requests

# ✅ formation 불러오기 (팀 스탯용)
def fetch_formations(fixture_id):
    url = f"{BASE_URL}/fixtures/lineups"
    headers = {"x-apisports-key": API_KEY}
    params = {"fixture": fixture_id}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code != 200 or "response" not in data:
        print(f"⚠️ Formation fetch failed for fixture {fixture_id}")
        return None, None

    try:
        lineups = data["response"]
        home_formation, away_formation = None, None
        for team in lineups:
            if team.get("team", {}).get("name_type", "home") == "home":
                home_formation = team.get("formation")
            else:
                away_formation = team.get("formation")
        if not home_formation or not away_formation:
            if len(lineups) == 2:
                home_formation = lineups[0].get("formation")
                away_formation = lineups[1].get("formation")
        return home_formation, away_formation
    except (IndexError, KeyError, TypeError) as e:
        print(f"⚠️ Formation data error for fixture {fixture_id}: {e}")
        return None, None

# ✅ 경기 정보 불러오기
raw_fixtures = fetch_fixtures_raw()
fixture_df = clean_fixture_data(raw_fixtures)

# ------------------------------- #
# ✅ 1. 팀 스탯 전처리 및 업로드
# ------------------------------- #
print("\n====================")
print("📊 Processing Team Stats")
print("====================")

all_team_stats = []
for i, row in fixture_df.iterrows():
    fixture_id = row["fixture_id"]
    match_date = row["date"]
    print(f"📦 [{i+1}/{len(fixture_df)}] Team fixture {fixture_id}")
    raw_stats = fetch_team_stats_for_fixture(fixture_id)
    if not raw_stats:
        continue
    team_stats_df = clean_team_stats(raw_stats, fixture_id, match_date)
    home_formation, away_formation = fetch_formations(fixture_id)
    if home_formation:
        team_stats_df["home_formation"] = home_formation
    if away_formation:
        team_stats_df["away_formation"] = away_formation
    all_team_stats.append(team_stats_df)

if all_team_stats:
    final_team_df = pd.concat(all_team_stats).reset_index(drop=True)
    final_team_df = preprocess_team_stats(final_team_df)
    if "passes" in final_team_df.columns:
        final_team_df = final_team_df.drop(columns=["passes"])
    print("✅ Uploading preprocessed team stats...")
    upload_processed_team_stats(final_team_df)
else:
    print("⚠️ No new team stats to upload.")

# ------------------------------- #
# ✅ 2. 선수 스탯 전처리 및 업로드
# ------------------------------- #
print("\n====================")
print("⚽ Processing Player Stats")
print("====================")

uploaded_player_ids = get_uploaded_fixture_ids("preprocessed_player_stat")
player_fixtures = fixture_df[~fixture_df["fixture_id"].isin(uploaded_player_ids)]
player_rows = []

def process_player_fixture(fixture_id):
    raw_players = fetch_player_stats_for_fixture(fixture_id)
    if raw_players:
        return clean_player_stats(raw_players, fixture_id)
    return None

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(process_player_fixture, fid): fid for fid in player_fixtures["fixture_id"]}
    for i, future in enumerate(as_completed(futures), 1):
        fixture_id = futures[future]
        try:
            df = future.result()
            if df is not None:
                player_rows.append(df)
                print(f"✅ [{i}/{len(futures)}] Player fixture {fixture_id}")
            else:
                print(f"⚠️ No player data for fixture {fixture_id}")
        except Exception as e:
            print(f"❌ Error on fixture {fixture_id}: {e}")

if player_rows:
    full_player_df = pd.concat(player_rows).reset_index(drop=True)
    full_player_df["rating"] = pd.to_numeric(full_player_df["rating"], errors="coerce").fillna(-1)
    processed_player_df = preprocess_player_stats(full_player_df)
    print("✅ Uploading preprocessed player stats...")
    upload_processed_player_stats(processed_player_df, table_name="preprocessed_player_stat")
else:
    print("⚠️ No new player stats to upload.")
