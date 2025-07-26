# main.py

from processing.processed_final_data import merge_all_data
from pipeline.upload_final_data import upload_final_dataset

if __name__ == "__main__":
    print("============================")
    print("🚀 Starting Final Data Merge")
    print("============================")

    df = merge_all_data()

    if not df.empty:
        upload_final_dataset(df)
    else:
        print("⚠️ Final DataFrame is empty. Nothing to upload.")
