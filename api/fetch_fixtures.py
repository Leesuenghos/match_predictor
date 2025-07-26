# api/fetch_fixtures.py
import requests
from config.settings import API_KEY, BASE_URL

def fetch_fixtures_raw(league_id=39, season=2023):
    url = f"{BASE_URL}/fixtures"
    headers = {
        "x-apisports-key": API_KEY
    }
    params = {
        "league": league_id,
        "season": season
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code != 200 or "response" not in data:
        raise Exception(f"Failed to fetch data: {data}")

    return data["response"]  # 👈 가공하지 않은 JSON
