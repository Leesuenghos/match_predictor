# pipeline/utils.py
from supabase import create_client, Client
from config.settings import SUPABASE_URL, SUPABASE_KEY

def get_uploaded_fixture_ids(table_name="player_stats"):
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = supabase.table(table_name).select("fixture_id").execute()
    
    if response.data:
        return set(row["fixture_id"] for row in response.data)
    return set()