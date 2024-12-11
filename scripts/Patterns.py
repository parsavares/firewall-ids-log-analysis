import os
import dask.dataframe as dd
import pandas as pd
import ipaddress
from datetime import timedelta

##############################################################
# FINAL EXPANDED PATTERNS ANALYSIS CODE (Dask-based)
##############################################################
# This code builds upon previous steps to analyze firewall and IDS logs for suspicious patterns.
# It uses Dask for memory-efficient parallel computation and handles large datasets gracefully.
#
# GOALS:
#   - Load large refined datasets using Dask.
#   - Identify suspicious teardown/rebuild patterns in firewall logs.
#   - Correlate with IDS alerts, external IP behavior, unusual services, and high-priority assets.
#   - Produce summary CSVs with findings.
#
# CHANGES & IMPROVEMENTS:
#   - Removed deprecated and unnecessary datetime format inference options.
#   - Avoided calling .compute() on already computed pandas DataFrames.
#   - Used .assign() where possible to prevent SettingWithCopy warnings.
#   - Handled scenarios with empty results gracefully.
#
# NOTE: You may still see warnings about inferring datetime formats. To eliminate them,
#       consider specifying the exact datetime format if known, e.g.:
#       dd.read_csv(..., parse_dates=['Date/time'], date_parser=lambda x: pd.to_datetime(x, format='%m/%d/%Y %H:%M:%S'))
#       For now, we rely on dateutil parsing.
#
# After running this script, check the "analysis_summaries" directory for CSV summaries.

##############################################################
# FINAL EXPANDED PATTERNS ANALYSIS CODE (Dask-based)
##############################################################
# This code analyzes firewall and IDS logs for suspicious patterns using Dask.
#
# UPDATES:
#  - Added a date_parser function to specify datetime format (e.g. '%m/%d/%Y %H:%M:%S')
#    to remove warnings about inferring datetime formats.
#  - The rest of the logic remains as previously discussed.
#
# After running this script, check the "analysis_summaries" directory for CSV summaries.

##############################################################
# Configuration
##############################################################
REFINED_DATA_DIR = os.path.join('..', 'data', 'MC2-CSVFirewallandIDSlogs')

# Update file paths as needed
REFINED_FIREWALL_1 = os.path.join(REFINED_DATA_DIR, 'refined_cleaned_Firewall-04062012.csv')
REFINED_FIREWALL_2 = os.path.join(REFINED_DATA_DIR, 'refined_cleaned_Firewall-04072012.csv')
REFINED_IDS_1 = os.path.join(REFINED_DATA_DIR, 'refined_cleaned_IDS-0406.csv')
REFINED_IDS_2 = os.path.join(REFINED_DATA_DIR, 'refined_cleaned_IDS-0407.csv')

# Known datetime format from logs, adjust if necessary
LOG_DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

def date_parser(x):
    # Parse the given datetime string using the known format.
    # If logs contain timezone or different format, adjust accordingly.
    if pd.isna(x) or x.strip() == '':
        return pd.NaT
    return pd.to_datetime(x, format=LOG_DATETIME_FORMAT, errors='coerce')

print("Loading refined firewall and IDS datasets as Dask DataFrames...")

firewall_ddf_1 = dd.read_csv(
    REFINED_FIREWALL_1, 
    parse_dates=['Date/time'], 
    date_parser=date_parser,
    dtype=str
)

firewall_ddf_2 = dd.read_csv(
    REFINED_FIREWALL_2, 
    parse_dates=['Date/time'], 
    date_parser=date_parser,
    dtype=str
)

ids_ddf_1 = dd.read_csv(
    REFINED_IDS_1, 
    parse_dates=['Date/time'], 
    date_parser=date_parser,
    dtype=str
)

ids_ddf_2 = dd.read_csv(
    REFINED_IDS_2, 
    parse_dates=['Date/time'], 
    date_parser=date_parser,
    dtype=str
)

firewall_ddf = dd.concat([firewall_ddf_1, firewall_ddf_2])
ids_ddf = dd.concat([ids_ddf_1, ids_ddf_2])

print("Data loaded. Performing initial computations...")

# Since we used date_parser, 'Date/time' should already be properly parsed
# Sort by time within each partition
firewall_ddf = firewall_ddf.map_partitions(lambda df: df.sort_values('Date/time'))
ids_ddf = ids_ddf.map_partitions(lambda df: df.sort_values('Date/time'))

##############################################################
# Identify Repeated Teardown/Rebuild Patterns with Dask
##############################################################

time_window = pd.Timedelta(minutes=5)

def find_suspicious_pairs(df):
    df = df.sort_values('Date/time')
    built_mask = df['Operation'].str.contains('Built', case=False, na=False)
    teardown_mask = df['Operation'].str.contains('Teardown', case=False, na=False)

    build_times = df.loc[built_mask, 'Date/time'].dropna().values
    teardown_times = df.loc[teardown_mask, 'Date/time'].dropna().values

    suspicious_count = 0
    for bt in build_times:
        soon_teardowns = teardown_times[(teardown_times > bt) & (teardown_times <= bt + time_window)]
        suspicious_count += len(soon_teardowns)

    return pd.DataFrame({'SuspiciousPairCount': [suspicious_count]})

firewall_ddf = firewall_ddf.assign(JoinKey=firewall_ddf['Source IP'] + "_" + firewall_ddf['Destination IP'])
suspicious_pairs_ddf = firewall_ddf.groupby('JoinKey').apply(find_suspicious_pairs, meta={'SuspiciousPairCount': 'int64'})
suspicious_pairs = suspicious_pairs_ddf.compute()

suspicious_pairs = suspicious_pairs.reset_index()
suspicious_pairs['Source IP'] = suspicious_pairs['JoinKey'].apply(lambda x: x.split('_')[0])
suspicious_pairs['Destination IP'] = suspicious_pairs['JoinKey'].apply(lambda x: x.split('_')[1])

print("\nTop 10 IP pairs with frequent short-interval build/teardown patterns (Dask-based):")
print(suspicious_pairs.sort_values('SuspiciousPairCount', ascending=False).head(10))

##############################################################
# Correlate with IDS and External IPs Using Dask
##############################################################
ids_external = ids_ddf[ids_ddf['Source_IsInternal']=='False']
ext_ip_alert_counts_ddf = ids_external.groupby('Source IP').size().to_frame('AlertCount').reset_index()
ext_ip_alert_counts = ext_ip_alert_counts_ddf.compute()

suspicious_pairs_with_ids = pd.merge(suspicious_pairs, ext_ip_alert_counts, on='Source IP', how='inner')
print("\nSuspicious build/teardown IPs that also appear in IDS external alerts (Dask-based):")
print(suspicious_pairs_with_ids.sort_values(['AlertCount','SuspiciousPairCount'], ascending=False).head(10))

##############################################################
# Check for Unusual Services or Ports
##############################################################
suspect_ports = [445, 53]
firewall_ddf = firewall_ddf.assign(DestPortStr=firewall_ddf['Destination port'].astype(str))

ext_suspicious_traffic_ddf = firewall_ddf[(firewall_ddf['Source_IsInternal']=='False') | (firewall_ddf['Dest_IsInternal']=='False')]
ext_suspect_ports_ddf = ext_suspicious_traffic_ddf[ext_suspicious_traffic_ddf['DestPortStr'].isin([str(p) for p in suspect_ports])]

ext_suspect_ports_sample = ext_suspect_ports_ddf.head(10)  # returns a pandas DataFrame
print("\nSample of external traffic on known suspicious ports (Dask-based):")
print(ext_suspect_ports_sample)

allowed_services = ['HTTP','HTTPS','DNS','NTP']
unusual_services_ddf = firewall_ddf[(~firewall_ddf['Destination service'].isin(allowed_services)) & (firewall_ddf['Destination service'].notnull())]

unusual_services_counts = unusual_services_ddf['Destination service'].value_counts().compute()
if unusual_services_counts.empty:
    print("\nNo unusual services detected based on the whitelist.")
else:
    print("\nTop 10 unusual services detected:")
    print(unusual_services_counts.head(10))

##############################################################
# Focus on High-Priority Assets
##############################################################
high_priority_nodes = ['FinancialServer','DomainController/DNS','LogServer','Firewall']

hp_suspicious_traffic_ddf = firewall_ddf[
    (firewall_ddf['Dest_NodeType'].isin(high_priority_nodes) | firewall_ddf['Source_NodeType'].isin(high_priority_nodes)) &
    ((firewall_ddf['Source IP'].isin(suspicious_pairs['Source IP'])) | (firewall_ddf['Destination IP'].isin(suspicious_pairs['Source IP'])))
]

hp_suspicious_traffic_sample = hp_suspicious_traffic_ddf.head(10)  # pandas DataFrame
print("\nSample of high-priority assets involved in suspicious activity (Dask-based):")
print(hp_suspicious_traffic_sample)

##############################################################
# Writing Summary Outputs
##############################################################
summary_dir = os.path.join('.', 'analysis_summaries')
os.makedirs(summary_dir, exist_ok=True)

suspicious_pairs.to_csv(os.path.join(summary_dir, 'suspicious_teardown_rebuild_pairs.csv'), index=False)
ext_ip_alert_counts.to_csv(os.path.join(summary_dir, 'external_ips_ids_alerts.csv'), index=False)

if not unusual_services_counts.empty:
    unusual_services_sample = unusual_services_ddf.head(100)  # pandas DF
    unusual_services_sample.to_csv(os.path.join(summary_dir, 'unusual_services_traffic_sample.csv'), index=False)
else:
    print("No unusual services CSV generated because none were detected.")

print("\nAll summary CSVs saved in 'analysis_summaries' directory.")
print("\nDask-based expanded analysis complete. Review CSV summaries and printed samples.")