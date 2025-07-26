# pipeline/upload_team_stats.py
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

def upload_team_stats(df, table_name="team_stats"):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    data = df.to_dict(orient="records")

    for row in data:
        response = supabase.table(table_name).upsert(row).execute()
        if response.data:
            print(f"✅ Uploaded (or updated) stats for fixture_id={row['fixture_id']}, team={row['team_name']}")
        elif response.error:
            print(f"⚠️ Failed to upload stats for fixture_id={row['fixture_id']}, team={row['team_name']}: {response.error.message}")