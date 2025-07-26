# pipeline/upload_preprocessed_matches.py
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

def upload_processed_matches(df, table_name="preprocessed_matches"):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    if df.empty:
        print("⚠️ No data to upload.")
        return

    # ✅ Supabase에 업로드 가능한 형식으로 date 변환
    df["date"] = df["date"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    records = df.to_dict(orient="records")

    for row in records:
        response = supabase.table(table_name).upsert(row).execute()
        if response.data:
            print(f"✅ Uploaded fixture_id={row['fixture_id']}")
        else:
            print(f"❌ Failed fixture_id={row['fixture_id']}")
