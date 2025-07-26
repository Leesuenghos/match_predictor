# pipeline/upload_to_supabase.py
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

def upload_fixtures(df, table_name="matches"):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    data = df.to_dict(orient="records")

    for row in data:
        # ✅ insert → upsert 로 교체
        response = supabase.table(table_name).upsert(row).execute()
        
        if response.data:
            print(f"✅ Uploaded (or updated) fixture_id={row['fixture_id']}")
        elif response.error:
            print(f"⚠️ Upload failed for fixture_id={row['fixture_id']}: {response.error.message}")
