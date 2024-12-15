import os
import dask.dataframe as dd
import pandas as pd
import geoip2.database  # For GeoIP lookup (requires `geoip2` package)
import shutil

# ===============================
# 🔧 Configuration
# ===============================
REFINED_DATA_DIR = os.path.join('..', 'data', 'MC2-CSVFirewallandIDSlogs')
ANALYSIS_SUMMARIES_DIR = os.path.join('scripts', 'analysis_summaries')

# Ensure ANALYSIS_SUMMARIES_DIR exists
os.makedirs(ANALYSIS_SUMMARIES_DIR, exist_ok=True)

# Corrected file paths
REFINED_FIREWALL = [
    os.path.join(REFINED_DATA_DIR, 'refined_cleaned_Firewall-04062012.csv'),
    os.path.join(REFINED_DATA_DIR, 'refined_cleaned_Firewall-04072012.csv')
]

REFINED_IDS = [
    os.path.join(REFINED_DATA_DIR, 'refined_cleaned_IDS-0406.csv'),
    os.path.join(REFINED_DATA_DIR, 'refined_cleaned_IDS-0407.csv')
]

# Port-to-service mapping
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

# ===============================
# 📂 Data Loading
# ===============================
def load_dask_dataframe(file_paths, file_type="firewall"):
    try:
        ddf = dd.read_csv(file_paths, assume_missing=True)
        ddf.columns = [c.strip() for c in ddf.columns]

        if 'Date/time' in ddf.columns:
            ddf['Date/time'] = dd.to_datetime(ddf['Date/time'], errors='coerce')
        else:
            print(f"[ERROR] 'Date/time' column is missing from {file_type} files.")

        ddf = ddf.repartition(npartitions=4)
        print(f"[INFO] Successfully loaded {len(file_paths)} {file_type} files.")
        return ddf
    except Exception as e:
        print(f"[ERROR] Could not load {file_type} data due to: {str(e)}")
        return None

firewall_ddf = load_dask_dataframe(REFINED_FIREWALL, file_type="firewall")
ids_ddf = load_dask_dataframe(REFINED_IDS, file_type="IDS")

if firewall_ddf is None or ids_ddf is None:
    print("[ERROR] Critical error loading data. Exiting.")
    exit()

# ===============================
# 🔥 Analysis Logic
# ===============================

# 1️⃣ External Traffic Analysis
external_firewall_ddf = firewall_ddf[(firewall_ddf['Source_IsInternal'] == False) | (firewall_ddf['Dest_IsInternal'] == False)]
external_ids_ddf = ids_ddf[(ids_ddf['Source_IsInternal'] == False) | (ids_ddf['Dest_IsInternal'] == False)]

# Function to safely write single-file CSV from Dask without leftover dirs
def dask_to_single_csv(ddf, output_file):
    # If output_file already exists as a directory or file, remove it
    if os.path.exists(output_file):
        if os.path.isdir(output_file):
            shutil.rmtree(output_file)
        else:
            os.remove(output_file)

    ddf.to_csv(output_file, index=False, single_file=True)

dask_to_single_csv(external_firewall_ddf, os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_firewall_traffic.csv'))
print("\n[INFO] Exported external firewall traffic to a single CSV file.")

dask_to_single_csv(external_ids_ddf, os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ids_traffic.csv'))
print("[INFO] Exported external IDS traffic to a single CSV file.")

# 2️⃣ Destination Services & Ports
try:
    # value_counts & nlargest require compute()
    # Instead: Use topk from Dask if we want. But to avoid huge memory usage, do small computations.

    # For large datasets, calling compute() on value_counts is still required.
    # If memory is a problem, consider filtering first or sampling.
    service_counts = external_firewall_ddf['Destination service'].value_counts().nlargest(50).compute()
    service_counts.to_frame('count').to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_services.csv'))
    print("[INFO] Exported top 50 destination services.")

    port_counts = external_firewall_ddf['Destination port'].value_counts().nlargest(50).compute()
    port_counts.to_frame('count').to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_ports.csv'))
    print("[INFO] Exported top 50 destination ports.")
except Exception as e:
    print(f"[ERROR] Could not compute destination services/ports: {str(e)}")

# 3️⃣ IDS Alerting IPs
try:
    alert_counts = external_ids_ddf['Source IP'].value_counts().nlargest(20).compute()
    alert_counts.to_frame('count').to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_20_external_ips.csv'))
    print("[INFO] Exported top 20 external IPs.")
except Exception as e:
    print(f"[ERROR] Could not compute IDS alert counts: {str(e)}")

# 4️⃣ GeoIP Lookup
try:
    geoip_db_path = 'GeoLite2-City.mmdb'
    if not os.path.exists(geoip_db_path):
        print("[WARNING] GeoLite2-City.mmdb not found. GeoIP lookup will have Unknown locations.")
        ip_locations = {}
        # Fill with Unknown
        if 'alert_counts' in locals():
            for ip in alert_counts.index[:20]:
                ip_locations[ip] = {'Country': 'Unknown', 'City': 'Unknown', 'Latitude': None, 'Longitude': None}
        else:
            ip_locations = {}
    else:
        with geoip2.database.Reader(geoip_db_path) as reader:
            ip_locations = {}
            for ip in alert_counts.index[:20]:
                try:
                    response = reader.city(ip)
                    ip_locations[ip] = {
                        'Country': response.country.name,
                        'City': response.city.name,
                        'Latitude': response.location.latitude,
                        'Longitude': response.location.longitude,
                        'IP': ip
                    }
                except:
                    ip_locations[ip] = {'Country': 'Unknown', 'City': 'Unknown', 'Latitude': None, 'Longitude': None, 'IP': ip}

    ip_locations_df = pd.DataFrame.from_dict(ip_locations, orient='index')
    ip_locations_df.to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ips_geoip.csv'))
    print("[INFO] Exported IP GeoIP data.")
except Exception as e:
    print(f"[ERROR] Could not perform GeoIP lookup: {str(e)}")