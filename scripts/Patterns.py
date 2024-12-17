import os
import dask.dataframe as dd
import pandas as pd

# Configuration
REFINED_DATA_DIR = os.path.join('..', 'data', 'MC2-CSVFirewallandIDSlogs')

# Corrected file paths
REFINED_FIREWALL = [
    os.path.join(REFINED_DATA_DIR, f'refined_cleaned_Firewall-04062012.csv'),
    os.path.join(REFINED_DATA_DIR, f'refined_cleaned_Firewall-04072012.csv')
]

REFINED_IDS = [
    os.path.join(REFINED_DATA_DIR, f'refined_cleaned_IDS-0406.csv'),
    os.path.join(REFINED_DATA_DIR, f'refined_cleaned_IDS-0407.csv')
]

def load_dask_dataframe(file_paths, file_type="firewall"):
    """Load multiple files into a Dask DataFrame with proper error handling."""
    try:
        ddf = dd.read_csv(
            file_paths, 
            assume_missing=True
        )
        # Strip whitespace from column names
        ddf.columns = [c.strip() for c in ddf.columns]

        # Enforce date format
        if 'Date/time' in ddf.columns:
            print(f"[INFO] Converting 'Date/time' to datetime for {file_type} data...")
            ddf['Date/time'] = dd.to_datetime(ddf['Date/time'], errors='coerce')
        else:
            print(f"[ERROR] 'Date/time' column is missing from {file_type} files.")

        # Force repartition to ensure uniform partitions
        ddf = ddf.repartition(npartitions=4)
        
        print(f"[INFO] Successfully loaded {len(file_paths)} {file_type} files.")
        return ddf
    except Exception as e:
        print(f"[ERROR] Could not load {file_type} data due to: {str(e)}")
        return None


# Load the data
firewall_ddf = load_dask_dataframe(REFINED_FIREWALL, file_type="firewall")
ids_ddf = load_dask_dataframe(REFINED_IDS, file_type="IDS")

# Ensure data loaded correctly
if firewall_ddf is None or ids_ddf is None:
    print("[ERROR] Critical error loading data. Exiting.")
    exit()

# Debug samples
print("\n[DEBUG] Firewall Data Sample:")
print(firewall_ddf.head(5))

print("\n[DEBUG] IDS Data Sample:")
print(ids_ddf.head(5))

# ===============================
# ANALYSIS LOGIC
# ===============================

# 1️⃣ Filter only EXTERNAL traffic
external_firewall_ddf = firewall_ddf[(firewall_ddf['Source_IsInternal'] == False) | (firewall_ddf['Dest_IsInternal'] == False)]
external_ids_ddf = ids_ddf[(ids_ddf['Source_IsInternal'] == False) | (ids_ddf['Dest_IsInternal'] == False)]

print("\n[DEBUG] External Firewall Traffic Sample (5 rows):")
print(external_firewall_ddf.head(5))

print("\n[DEBUG] External IDS Traffic Sample (5 rows):")
print(external_ids_ddf.head(5))

# 2️⃣ Destination Services
try:
    service_counts = (
        external_firewall_ddf['Destination service']
        .value_counts()
        .compute()
        .sort_values(ascending=False)  # Ensure sorting
    )
    print("\n[DEBUG] Top 50 Destination Services in Logs (sorted):")
    print(service_counts.head(50))
except Exception as e:
    print(f"[ERROR] Could not compute 'Destination service' counts due to: {str(e)}")

# 3️⃣ Destination Ports
try:
    port_counts = (
        external_firewall_ddf['Destination port']
        .value_counts()
        .compute()
        .sort_values(ascending=False)  # Ensure sorting
    )
    print("\n[DEBUG] Top 50 Destination Ports in Logs (sorted):")
    print(port_counts.head(50))
except Exception as e:
    print(f"[ERROR] Could not compute 'Destination port' counts due to: {str(e)}")

# 4️⃣ Source Node Types
try:
    firewall_node_types = (
        external_firewall_ddf['Source_NodeType']
        .value_counts()
        .compute()
        .sort_values(ascending=False)  # Ensure sorting
    )
    ids_node_types = (
        external_ids_ddf['Source_NodeType']
        .value_counts()
        .compute()
        .sort_values(ascending=False)  # Ensure sorting
    )

    print("\n[DEBUG] Source Node Types in Firewall Data (sorted):")
    print(firewall_node_types)

    print("\n[DEBUG] Source Node Types in IDS Data (sorted):")
    print(ids_node_types)
except Exception as e:
    print(f"[ERROR] Could not compute 'Source_NodeType' counts due to: {str(e)}")

# 5️⃣ IDS Alerts
try:
    external_ids_alert_counts = (
        external_ids_ddf['Source IP']
        .value_counts()
        .compute()
        .sort_values(ascending=False)  # Ensure sorting
    )
    print("\n[DEBUG] Top 20 External IPs Triggering IDS Alerts (sorted):")
    print(external_ids_alert_counts.head(20))
except Exception as e:
    print(f"[ERROR] Could not compute IDS alert counts due to: {str(e)}")

# 6️⃣ 🔥 **Destination Ports (External Filter)**
try:
    sorted_external_port_counts = (
        external_firewall_ddf['Destination port']
        .value_counts()
        .compute()
        .sort_values(ascending=False)  # Ensure sorting
    )
    print("\n[DEBUG] Top 50 Destination Ports (External Traffic, Sorted):")
    print(sorted_external_port_counts.head(50))
except Exception as e:
    print(f"[ERROR] Could not compute external 'Destination port' counts due to: {str(e)}")

# 7️⃣ 🔥 **Top Destination Services (External Filter)**
try:
    sorted_external_service_counts = (
        external_firewall_ddf['Destination service']
        .value_counts()
        .compute()
        .sort_values(ascending=False)  # Ensure sorting
    )
    print("\n[DEBUG] Top 50 Destination Services (External Traffic, Sorted):")
    print(sorted_external_service_counts.head(50))
except Exception as e:
    print(f"[ERROR] Could not compute external 'Destination service' counts due to: {str(e)}")
