import os
import dask.dataframe as dd
import pandas as pd
import geoip2.database  # For GeoIP lookup (requires `geoip2` package)

# ===============================
# 🔧 Configuration
# ===============================
REFINED_DATA_DIR = os.path.join('..', 'data', 'MC2-CSVFirewallandIDSlogs')
ANALYSIS_SUMMARIES_DIR = os.path.join('scripts', 'analysis_summaries')

# Corrected file paths
REFINED_FIREWALL = [
    os.path.join(REFINED_DATA_DIR, f'refined_cleaned_Firewall-04062012.csv'),
    os.path.join(REFINED_DATA_DIR, f'refined_cleaned_Firewall-04072012.csv')
]

REFINED_IDS = [
    os.path.join(REFINED_DATA_DIR, f'refined_cleaned_IDS-0406.csv'),
    os.path.join(REFINED_DATA_DIR, f'refined_cleaned_IDS-0407.csv')
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
        ddf.columns = [c.strip() for c in ddf.columns]  # Strip column names

        if 'Date/time' in ddf.columns:
            ddf['Date/time'] = dd.to_datetime(ddf['Date/time'], errors='coerce')
        else:
            print(f"[ERROR] 'Date/time' column is missing from {file_type} files.")

        ddf = ddf.repartition(npartitions=4)  # Ensure uniform partitioning
        print(f"[INFO] Successfully loaded {len(file_paths)} {file_type} files.")
        return ddf
    except Exception as e:
        print(f"[ERROR] Could not load {file_type} data due to: {str(e)}")
        return None

# Load the data
firewall_ddf = load_dask_dataframe(REFINED_FIREWALL, file_type="firewall")
ids_ddf = load_dask_dataframe(REFINED_IDS, file_type="IDS")

if firewall_ddf is None or ids_ddf is None:
    print("[ERROR] Critical error loading data. Exiting.")
    exit()

# Debug samples
print("\n[DEBUG] Firewall Data Sample:")
print(firewall_ddf.head(5))

print("\n[DEBUG] IDS Data Sample:")
print(ids_ddf.head(5))

# ===============================
# 🔥 Analysis Logic
# ===============================

# 1️⃣ Filter external traffic
external_firewall_ddf = firewall_ddf[(firewall_ddf['Source_IsInternal'] == False) | (firewall_ddf['Dest_IsInternal'] == False)]
external_ids_ddf = ids_ddf[(ids_ddf['Source_IsInternal'] == False) | (ids_ddf['Dest_IsInternal'] == False)]

external_firewall_ddf.to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'high_priority_traffic_sample.csv'), index=False)
print("\n[INFO] Exported high priority traffic sample.")

# 2️⃣ Destination Services
try:
    service_counts = external_firewall_ddf['Destination service'].value_counts().nlargest(50).compute()
    service_counts.to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_services.csv'))
    print("\n[INFO] Exported top 50 destination services.")
except Exception as e:
    print(f"[ERROR] Could not compute 'Destination service' counts due to: {str(e)}")

# 3️⃣ Destination Ports
try:
    port_counts = external_firewall_ddf['Destination port'].value_counts().nlargest(50).compute()
    port_counts.to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_ports.csv'))
    print("\n[INFO] Exported top 50 destination ports.")
except Exception as e:
    print(f"[ERROR] Could not compute 'Destination port' counts due to: {str(e)}")

# 4️⃣ Source Node Types
try:
    firewall_node_types = external_firewall_ddf['Source_NodeType'].value_counts().compute()
    ids_node_types = external_ids_ddf['Source_NodeType'].value_counts().compute()
except Exception as e:
    print(f"[ERROR] Could not compute 'Source_NodeType' counts due to: {str(e)}")

# 5️⃣ IDS Alerts
try:
    external_ids_alert_counts = external_ids_ddf['Source IP'].value_counts().nlargest(20).compute()
    external_ids_alert_counts.to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_20_external_ips.csv'))
    print("\n[INFO] Exported top 20 external IPs.")
except Exception as e:
    print(f"[ERROR] Could not compute IDS alert counts due to: {str(e)}")

# ===============================
# 🌐 GeoIP Lookup for Alerting IPs
# ===============================
try:
    with geoip2.database.Reader('GeoLite2-City.mmdb') as reader:
        ip_locations = {}
        for ip in external_ids_alert_counts.index[:20]:
            try:
                response = reader.city(ip)
                ip_locations[ip] = {
                    'Country': response.country.name,
                    'City': response.city.name,
                    'Latitude': response.location.latitude,
                    'Longitude': response.location.longitude
                }
            except Exception as e:
                ip_locations[ip] = {'Country': 'Unknown', 'City': 'Unknown', 'Latitude': None, 'Longitude': None}

    ip_locations_df = pd.DataFrame.from_dict(ip_locations, orient='index')
    ip_locations_df.to_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ips_ids_alerts.csv'))
    print("\n[INFO] Exported IPs GeoIP lookup data.")
except Exception as e:
    print(f"[ERROR] Could not perform GeoIP lookup due to: {str(e)}")

# ===============================
# 🧹 Data Quality Reports
# ===============================
try:
    total_rows = firewall_ddf.shape[0].compute()
    dropped_rows = firewall_ddf[firewall_ddf['Date/time'].isnull()].shape[0].compute()
    dropped_percentage = (dropped_rows / total_rows) * 100
    print(f"\n[INFO] Total rows in firewall data: {total_rows}")
    print(f"[INFO] Dropped rows (due to 'Date/time' errors): {dropped_rows} ({dropped_percentage:.2f}%)")
except Exception as e:
    print(f"[ERROR] Could not compute data quality reports due to: {str(e)}")
