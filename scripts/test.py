import os
import stat
ANALYSIS_SUMMARIES_DIR = os.path.abspath(os.path.join('scripts', 'analysis_summaries'))

file_path = os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_firewall_traffic.csv')

# Change file permissions to 777 (full read-write-execute)
os.chmod(file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
