# pipeline/upload_processed_player_stats.py
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY
import numpy as np

def upload_processed_player_stats(df, table_name="preprocessed_player_stats"):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    if df.empty:
        print("⚠️ No data to upload.")
        return

    # ✅ 결측치 숫자 변환
    int_cols = [
        "team_name", "is_starting", "minutes_played", "position", "goals", "assists",
        "shots_total", "shots_on_goal", "passes", "tackles", "duels_won",
        "fouls_committed", "yellow_cards", "red_cards"
    ]
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    df = df.replace({np.nan: None})

    # ✅ bulk upsert
    data = df.to_dict(orient="records")
    try:
        response = supabase.table(table_name).upsert(data).execute()
        print(f"✅ Uploaded {len(data)} player records to Supabase.")
    except Exception as e:
        print(f"❌ Upload failed with error: {e}")
