import os
import dask.dataframe as dd
import pandas as pd
import ipaddress
from datetime import datetime

##############################################################
# PART 1 & 2 (MULTI-DATASET VERSION): REASSESS IMPUTATION STRATEGY & INTEGRATE CONTEXT
##############################################################
# In this script, we process multiple cleaned firewall and IDS datasets to:
#
#  1) Reassess our imputation strategy by removing columns that remain entirely missing 
#     after cleaning. Such columns add no analytical value and only clutter the dataset.
#
#  2) Enrich the cleaned datasets with additional contextual information:
#     - Add time-based features (Hour, Day, DayOfWeek) extracted from 'Date/time'.
#     - Classify IP addresses to determine if they are internal or external, 
#       identify known critical resources (firewalls, financial servers, etc.), 
#       and assign a priority level (High or Normal).
#
# After running this script, we get "refined" datasets, ready for advanced analysis 
# and visualizations. Each refined dataset will have a 'refined_' prefix added to its filename.
#
# Steps to Integrate:
#   1. Run your previous cleaning code so that 'cleaned_*.csv' files exist.
#   2. Update the CLEANED_DATASETS and OUTPUT_DIR paths if necessary.
#   3. Run this script. It processes each cleaned dataset, drops fully missing columns, 
#      enriches with context, and saves the result.
#
# After these steps, you can load the refined datasets into a notebook or dashboard 
# to create insightful visualizations and analyses.

##############################################################
# Configuration
##############################################################

# Directory where the cleaned datasets are located
CLEANED_DATASETS_DIR = os.path.join('..', 'data', 'MC2-CSVFirewallandIDSlogs')

# Dictionary mapping dataset names to their cleaned CSV files
CLEANED_DATASETS = {
    'cleaned_Firewall-04062012.csv': os.path.join(CLEANED_DATASETS_DIR, 'cleaned_Firewall-04062012.csv'),
    'cleaned_Firewall-04072012.csv': os.path.join(CLEANED_DATASETS_DIR, 'cleaned_Firewall-04072012.csv'),
    'cleaned_IDS-0406.csv': os.path.join(CLEANED_DATASETS_DIR, 'cleaned_IDS-0406.csv'),
    'cleaned_IDS-0407.csv': os.path.join(CLEANED_DATASETS_DIR, 'cleaned_IDS-0407.csv')
}


# Directory where refined datasets will be saved
OUTPUT_DIR = CLEANED_DATASETS_DIR

##############################################################
# Helper Functions
##############################################################

def drop_always_missing_columns(df):
    """
    Drops columns that are entirely missing.

    After initial cleaning/imputation, some columns may still be 100% NaN.
    Removing them makes the dataset cleaner and more focused.

    Parameters:
    - df: Dask DataFrame

    Returns:
    - df: Dask DataFrame without fully missing columns
    - dropped_cols: List of dropped column names
    """
    total_rows = df.shape[0].compute()
    missing_counts = df.isnull().sum().compute()
    always_missing = missing_counts[missing_counts == total_rows].index.tolist()
    if always_missing:
        df = df.drop(columns=always_missing)
    return df, always_missing

def classify_ip(ip):
    """
    Classify an IP address based on the Bank of Money network.

    Handles NaN or non-string IPs safely by converting them to strings and checking emptiness.
    
    Categories:
    - IsInternal: True if IP is in 172.x.x.x range
    - NodeType: "Firewall", "DomainController/DNS", "LogServer", "FinancialServer", "Workstation", "Unknown"
    - Priority: "High" for critical nodes, "Normal" for others

    Parameters:
    - ip: IP address value (may not always be a string)

    Returns:
    - dict with keys { "IsInternal": bool, "NodeType": str, "Priority": str }
    """
    classification = {
        "IsInternal": False,
        "NodeType": "Unknown",
        "Priority": "Normal"
    }

    if pd.isna(ip):
        return classification
    
    ip = str(ip).strip()
    if ip == '':
        return classification

    def in_ip_range(ip_str, start, end):
        start_ip = ipaddress.ip_address(start)
        end_ip = ipaddress.ip_address(end)
        current_ip = ipaddress.ip_address(ip_str)
        return start_ip <= current_ip <= end_ip

    # Check if internal
    if ip.startswith("172."):
        classification["IsInternal"] = True

    # Known critical nodes
    firewalls = ["10.32.0.1", "172.23.0.1", "10.32.0.100", "172.25.0.1"]
    if ip in firewalls:
        classification["NodeType"] = "Firewall"
        classification["Priority"] = "High"
        return classification

    if ip == "172.23.0.10":
        classification["NodeType"] = "DomainController/DNS"
        classification["Priority"] = "High"
        return classification

    if ip == "172.23.0.2":
        classification["NodeType"] = "LogServer"
        classification["Priority"] = "High"
        return classification

    # Financial servers: 172.23.214.x through 172.23.229.x
    if ip.startswith("172.23."):
        try:
            if in_ip_range(ip, "172.23.214.0", "172.23.229.255"):
                classification["NodeType"] = "FinancialServer"
                classification["Priority"] = "High"
                return classification
        except:
            pass

    # Internal but not identified as critical => Workstation
    if classification["IsInternal"] and classification["NodeType"] == "Unknown":
        classification["NodeType"] = "Workstation"
        classification["Priority"] = "Normal"

    return classification

def enrich_with_context(df):
    """
    Enhances the DataFrame by adding time-based features and IP classification.

    - Converts 'Date/time' to datetime and extracts Hour, Day, DayOfWeek.
    - Adds Source_* and Dest_* columns based on IP classification.

    Parameters:
    - df: Dask DataFrame with at least 'Date/time', 'Source IP', 'Destination IP'

    Returns:
    - df: Enriched DataFrame with additional context columns
    """

    # Convert 'Date/time' to datetime
    df['Date/time'] = dd.to_datetime(df['Date/time'], errors='coerce', infer_datetime_format=True)

    # Extract time-based features
    df['Hour'] = df['Date/time'].dt.hour
    df['Day'] = df['Date/time'].dt.day
    df['DayOfWeek'] = df['Date/time'].dt.dayofweek

    # Prepare meta with new columns to avoid schema mismatch
    # Determine current meta
    meta = df._meta.copy()
    # Add expected new columns with appropriate dtypes
    new_cols = {
        'Source_IsInternal': bool,
        'Source_NodeType': object,
        'Source_Priority': object,
        'Dest_IsInternal': bool,
        'Dest_NodeType': object,
        'Dest_Priority': object
    }
    for col, dtype in new_cols.items():
        meta[col] = pd.Series([], dtype=dtype)

    def classify_ips_partition(pdf):
        source_info = pdf['Source IP'].apply(classify_ip)
        dest_info = pdf['Destination IP'].apply(classify_ip)

        pdf['Source_IsInternal'] = source_info.apply(lambda x: x['IsInternal'])
        pdf['Source_NodeType'] = source_info.apply(lambda x: x['NodeType'])
        pdf['Source_Priority'] = source_info.apply(lambda x: x['Priority'])

        pdf['Dest_IsInternal'] = dest_info.apply(lambda x: x['IsInternal'])
        pdf['Dest_NodeType'] = dest_info.apply(lambda x: x['NodeType'])
        pdf['Dest_Priority'] = dest_info.apply(lambda x: x['Priority'])

        return pdf

    # Use map_partitions with updated meta
    df = df.map_partitions(classify_ips_partition, meta=meta)
    return df

##############################################################
# Main Execution
##############################################################

if __name__ == "__main__":
    # Process each cleaned dataset:
    #  1) Load
    #  2) Drop fully missing columns
    #  3) Enrich with context (time & IP classification)
    #  4) Save as refined dataset

    for dataset_name, dataset_path in CLEANED_DATASETS.items():
        if not os.path.exists(dataset_path):
            print(f"Cleaned dataset not found: {dataset_path}, skipping.")
            continue

        print(f"Loading cleaned dataset: {dataset_path}")
        df = dd.read_csv(dataset_path, dtype=str, on_bad_lines='skip')

        # Drop always-missing columns
        df, dropped_cols = drop_always_missing_columns(df)
        if dropped_cols:
            print(f"Dropped fully-missing columns from {dataset_name}: {dropped_cols}")
        else:
            print(f"No fully-missing columns to drop in {dataset_name}.")

        # Enrich with time-based and IP context
        df = enrich_with_context(df)
        print(f"Enriched {dataset_name} with contextual features.")

        # Construct refined output filename
        refined_filename = "refined_" + dataset_name
        refined_path = os.path.join(OUTPUT_DIR, refined_filename)

        # Save the refined dataset
        df.to_csv(refined_path, single_file=True, index=False)
        print(f"Refined dataset saved to: {refined_path}\n")

    print("All specified datasets have been processed and refined successfully.")
