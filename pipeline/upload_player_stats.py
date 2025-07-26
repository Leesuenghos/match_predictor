# pipeline/upload_player_stats.py
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY
import numpy as np

def upload_player_stats(df, table_name="player_stats"):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    if df.empty:
        print("⚠️ No player stats to upload.")
        return

    # ✅ 정수형 컬럼 변환
    int_cols = [
        "minutes_played", "goals", "assists", "shots_total",
        "shots_on_goal", "passes", "tackles", "duels_won",
        "fouls_committed", "yellow_cards", "red_cards"
    ]
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    # ✅ NaN → None
    df = df.replace({np.nan: None})

    # ✅ ✅ bulk upsert (리스트 전체 업로드)
    data = df.to_dict(orient="records")
    try:
        response = supabase.table(table_name).upsert(data).execute()
        print(f"✅ Uploaded {len(data)} player records to Supabase.")
    except Exception as e:
        print(f"❌ Upload failed with error: {e}")
