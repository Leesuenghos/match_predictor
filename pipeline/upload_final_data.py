from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY
import pandas as pd

def upload_final_dataset(df, table_name="final_dataset"):
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    if df.empty:
        print("⚠️ No data to upload.")
        return

    # ✅ date → ISO 포맷 문자열 (Supabase가 timestamptz로 자동 인식)
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    # ✅ NaN → None
    df = df.where(pd.notnull(df), None)

    # ✅ Supabase bulk upsert (1000개 단위)
    records = df.to_dict(orient="records")
    batch_size = 1000
    print(f"📤 Uploading to Supabase...\n📦 Uploading {len(records)} records in {(len(records) - 1)//batch_size + 1} batches...")

    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        try:
            supabase.table(table_name).upsert(batch).execute()
            print(f"✅ Uploaded batch {i//batch_size + 1}: {len(batch)} records")
        except Exception as e:
            print(f"❌ Failed batch {i//batch_size + 1}: {e}")
