# api/fetch_team_stats.py
import requests
from config.settings import API_KEY, BASE_URL

def fetch_team_stats_for_fixture(fixture_id):
    url = f"{BASE_URL}/fixtures/statistics"
    headers = {
        "x-apisports-key": API_KEY
    }
    params = {
        "fixture": fixture_id
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code != 200 or "response" not in data:
        print(f"⚠️ Failed to fetch stats for fixture {fixture_id}")
        return None

    return data["response"]  # 팀별 스탯 리스트 (2개)