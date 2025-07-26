# test.py
import pandas as pd
from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_all_player_stats():
    page = 0
    limit = 1000
    all_rows = []

    while True:
        start = page * limit
        end = start + limit - 1
        response = supabase.table("player_stats").select("player_id", "player_name").range(start, end).execute()

        if response.data:
            all_rows.extend(response.data)
            if len(response.data) < limit:
                break
            page += 1
        else:
            break

    return all_rows

# 데이터 불러오기
data = fetch_all_player_stats()
df = pd.DataFrame(data)

# 결측치 제거 + 중복 제거
df_cleaned = df.dropna(subset=["player_id", "player_name"]).drop_duplicates(subset=["player_id"])

# 저장
df_cleaned.to_csv("epl_2023_players_final.csv", index=False, encoding="utf-8-sig")

# 요약 출력
print("✅ Saved to epl_2023_players_final.csv")
print("📦 Total unique player_id:", df_cleaned["player_id"].nunique())
print("📦 Total rows saved:", len(df_cleaned))
