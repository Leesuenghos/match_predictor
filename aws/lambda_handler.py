# aws/lambda_handler.py

from processing.processed_final_data import merge_all_data
from pipeline.upload_final_data import upload_final_dataset

def lambda_handler(event, context):
    print("============================")
    print("🚀 Starting Final Data Merge (Lambda)")
    print("============================")

    df = merge_all_data()

    if df is not None and not df.empty:
        upload_final_dataset(df)
        print(f"✅ Done. Uploaded rows: {len(df)}")
        return {"statusCode": 200, "uploaded": int(len(df))}
    else:
        print("⚠️ Final DataFrame is empty. Nothing to upload.")
        return {"statusCode": 200, "uploaded": 0}
