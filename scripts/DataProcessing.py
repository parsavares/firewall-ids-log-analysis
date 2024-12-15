import os
import dask.dataframe as dd
import pandas as pd
import shutil

# ===============================
# 🔧 Configuration
# ===============================
DATA_DIR = os.path.join('..', 'data', 'MC2-CSVFirewallandIDSlogs')
ANALYSIS_SUMMARIES_DIR = os.path.join('scripts', 'analysis_summaries')

os.makedirs(ANALYSIS_SUMMARIES_DIR, exist_ok=True)

FIREWALL_FILES = [
    os.path.join(DATA_DIR, 'Firewall-04062012.csv'),
    os.path.join(DATA_DIR, 'Firewall-04072012.csv')
]
IDS_FILES = [
    os.path.join(DATA_DIR, 'IDS-0406.csv'),
    os.path.join(DATA_DIR, 'IDS-0407.csv')
]

# ===============================
# 📂 Data Loading & Cleaning
# ===============================
def load_and_clean_dask_dataframe(file_paths, file_type="firewall"):
    na_values_list = ["(empty)", "N/A", "NULL", "?", "Unknown"]  # List of representations of missing values
    try:
        ddf = dd.read_csv(file_paths, na_values=na_values_list, assume_missing=True)
        ddf.columns = ddf.columns.str.strip()  # Remove leading and trailing spaces from column names

        # Rename IDS-specific columns to match Firewall column names
        if file_type == "IDS":
            ddf = ddf.rename(columns={'time': 'Date/time', 'sourceIP': 'Source IP', 'sourcePort': 'Source port', 'destIP': 'Destination IP', 'destPort': 'Destination port'})

        # Ensure required columns exist
        required_columns = ['Source IP', 'Destination IP', 'Source port', 'Destination port']
        for col in required_columns:
            if col not in ddf.columns:
                ddf[col] = None  # Set empty values as NaN (not as "Missed_captured")

        # Trim extra whitespace from string columns
        object_columns = ddf.select_dtypes(include=['object']).columns
        for col in object_columns:
            ddf[col] = ddf[col].str.strip()

        # Drop rows where critical columns are missing
        ddf = ddf.dropna(subset=required_columns)

        # Convert 'Date/time' to datetime
        if 'Date/time' in ddf.columns:
            ddf['Date/time'] = dd.to_datetime(ddf['Date/time'], errors='coerce')

        print(f"[INFO] Successfully loaded and cleaned {len(file_paths)} {file_type} files.")
        return ddf
    except Exception as e:
        print(f"[ERROR] Could not load {file_type} data due to: {str(e)}")
        return None

firewall_ddf = load_and_clean_dask_dataframe(FIREWALL_FILES, file_type="firewall")
ids_ddf = load_and_clean_dask_dataframe(IDS_FILES, file_type="IDS")

# ===============================
# 🔥 Internal/External IP Classification
# ===============================
def classify_internal_external(df):
    internal_ip_regex = (
        r'^172\..*|'                 
        r'^10\.32\.0\.(20[1-9]|210)|'
        r'^10\.32\.1\.100|'          
        r'^10\.32\.1\.(20[1-6])|'     
        r'^10\.32\.5\.(\d{1,3})$'     
    )

    df['Source_IsInternal'] = df['Source IP'].str.match(internal_ip_regex, na=False)
    df['Dest_IsInternal'] = df['Destination IP'].str.match(internal_ip_regex, na=False)
    df['IsExternalTraffic'] = ~df['Source_IsInternal'] | ~df['Dest_IsInternal']
    return df

firewall_ddf = classify_internal_external(firewall_ddf)
ids_ddf = classify_internal_external(ids_ddf)

# ===============================
# 🔥 Port to Service Mapping 
# ===============================
PORT_TO_SERVICE = {
    22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS', 80: 'HTTP',
    110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 465: 'SMTPS', 993: 'IMAPS',
    995: 'POP3S', 135: 'Microsoft RPC', 137: 'NetBIOS Name Service',
    138: 'NetBIOS Datagram Service', 139: 'NetBIOS Session Service',
    1433: 'SQL Server', 1521: 'Oracle DB', 3306: 'MySQL', 3389: 'RDP',
    8080: 'HTTP Proxy', 8443: 'HTTPS Proxy', 5900: 'VNC', 5060: 'SIP',
    21: 'FTP', 554: 'RTSP', 1720: 'H.323', 1812: 'RADIUS Authentication',
    1813: 'RADIUS Accounting', 8888: 'Alternate HTTP'
}

def map_ports_to_services(df):
    df['Source Service'] = df['Source port'].replace(PORT_TO_SERVICE)
    df['Destination Service'] = df['Destination port'].replace(PORT_TO_SERVICE)
    return df

firewall_ddf = map_ports_to_services(firewall_ddf)
ids_ddf = map_ports_to_services(ids_ddf)

# ===============================
# 🔥 Data Summarization
# ===============================
def determine_top_n(count_series, coverage_threshold=0.95):
    total = count_series.sum()
    cumulative_sum = count_series.cumsum()
    n = (cumulative_sum / total <= coverage_threshold).sum()
    return max(n, 50)  # Ensure at least 50

def summarize_and_export(df, column, file_name):
    try:
        counts = df[column].value_counts().compute()
        top_n = determine_top_n(counts)
        top_counts = counts.nlargest(top_n)
        top_counts.to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, file_name))
        print(f"[INFO] Exported {file_name} with top {top_n} entries.")
    except Exception as e:
        print(f"[ERROR] Could not export {file_name} due to: {str(e)}")

summarize_and_export(firewall_ddf, 'Destination Service', 'top_50_destination_services.csv')
summarize_and_export(firewall_ddf, 'Destination port', 'top_50_destination_ports.csv')
summarize_and_export(ids_ddf, 'Source IP', 'top_50_external_ips.csv')

# ===============================
# 🧹 Export Cleaned Data
# ===============================
def export_cleaned_data(df, file_name):
    try:
        df.to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, file_name), single_file=True, index=False)
        print(f"[INFO] Exported {file_name}.")
    except Exception as e:
        print(f"[ERROR] Could not export {file_name} due to: {str(e)}")

export_cleaned_data(firewall_ddf, 'external_firewall_traffic.csv')
export_cleaned_data(ids_ddf, 'external_ids_traffic.csv')

print("[INFO] Data processing complete.")
