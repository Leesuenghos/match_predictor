# api/fetch_player_stats.py
import requests
from config.settings import API_KEY, BASE_URL

def fetch_player_stats_for_fixture(fixture_id):
    url = f"{BASE_URL}/fixtures/players"
    headers = {
        "x-apisports-key": API_KEY
    }
    params = {
        "fixture": fixture_id
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code != 200 or "response" not in data:
        print(f"⚠️ Failed to fetch player stats for fixture {fixture_id}")
        return None

    return data["response"]  # 팀별 선수 리스트 포함
