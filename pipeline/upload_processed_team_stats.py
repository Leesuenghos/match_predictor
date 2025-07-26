# pipeline/upload_processed_team_stats.py
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

def upload_processed_team_stats(df, table_name="preprocessed_team_stats"):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    if df.empty:
        print("⚠️ No data to upload.")
        return

    # ✅ date → ISO8601 문자열로 변환
    df["date"] = df["date"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    data = df.to_dict(orient="records")

    for row in data:
        response = supabase.table(table_name).upsert(row).execute()
        if response.data:
            print(f"✅ Uploaded fixture_id={row['fixture_id']}, team={row['team_name']}")
        else:
            print(f"❌ Failed fixture_id={row['fixture_id']}, team={row['team_name']}")