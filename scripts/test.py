import os
import pandas as pd

def test_source_ip_summary():
    print("\n[TEST] Testing Top 20 External Source IPs Report...")

    # Correct file path for the top 20 IPs
    file_path = 'scripts/analysis_summaries/top_20_external_ips.csv'
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print("[ERROR] File not found. Did the DataProcessing script run?")
        return

    # Load the CSV
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"[ERROR] Could not read the file: {e}")
        return
    
    # Check if 'Source IP' column exists
    if 'Source IP' not in df.columns:
        print("[ERROR] 'Source IP' column is missing in the CSV.")
        return

    # Check for 'Missed_captured' entries in 'Source IP'
    missed_count = df[df['Source IP'] == 'Missed_captured']['count'].sum()
    total_rows = len(df)
    
    print(f"[INFO] Total rows in 'top_20_external_ips.csv': {total_rows}")
    print(f"[INFO] Total 'Missed_captured' count: {missed_count}")

    if total_rows == 0:
        print("[ERROR] No rows in summary file.")
    elif missed_count > 0:
        print(f"[WARNING] 'Missed_captured' is present in the summary with a count of {missed_count}.")
    else:
        print("[INFO] Test Passed: No 'Missed_captured' in top 20 IPs.")

if __name__ == "__main__":
    test_source_ip_summary()
