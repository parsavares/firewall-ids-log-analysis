import os
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ================================
# 🔧 Configuration
# ================================
ANALYSIS_SUMMARIES_DIR = os.path.join('scripts', 'analysis_summaries')

# ================================
# 📂 Load Data Using Sampling
# ================================
try:
    firewall_traffic_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_firewall_traffic.csv')).iloc[::100]  # Sample 1 out of every 50 rows
    ids_traffic_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ids_traffic.csv')).iloc[::10]  # Sample 1 out of every 10 rows
    top_services_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_services.csv'))
    top_ports_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_ports.csv'))
    top_ips_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_external_ips.csv'))
except Exception as e:
    print(f"[ERROR] Could not load one or more analysis files. {e}")
    exit()

# ================================
# 🔥 Data Cleaning and Enhancements
# ================================
# Normalize column names (remove leading and trailing whitespace)
firewall_traffic_df.columns = firewall_traffic_df.columns.str.strip()
ids_traffic_df.columns = ids_traffic_df.columns.str.strip()

# Replace NaN or None in critical columns
firewall_traffic_df['Source_Priority'] = pd.to_numeric(firewall_traffic_df.get('Source_Priority', 1), errors='coerce').fillna(1)
ids_traffic_df['priority'] = pd.to_numeric(ids_traffic_df.get('priority', 1), errors='coerce').fillna(1)

# Replace zero weights to avoid ZeroDivisionError
firewall_traffic_df.loc[firewall_traffic_df['Source_Priority'] == 0, 'Source_Priority'] = 1
ids_traffic_df.loc[ids_traffic_df['priority'] == 0, 'priority'] = 1

# Replace NaN or None in critical columns for sunburst
firewall_traffic_df['Source_NodeType'] = firewall_traffic_df['Source_NodeType'].fillna('Unknown')
firewall_traffic_df['Operation'] = firewall_traffic_df['Operation'].fillna('Other')

# Apply logarithmic transformation for better scaling
top_ports_df['log_count'] = top_ports_df['count'].apply(lambda x: max(1, x))  # Avoid log(0) errors
top_ports_df['log_count'] = top_ports_df['log_count'].apply(lambda x: np.log10(x))  # Log10 for better distribution

# ================================
# 🔥 Initialize Dash Application
# ================================
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "🔥 Firewall & IDS Visualization Dashboard 🔥"

# ================================
# 📊 Layout for Dashboard
# ================================
app.layout = html.Div([
    dcc.Tabs([
        # 🔥 Answer 1: Critical Security Events
        dcc.Tab(label='Question 1: Critical Security Events', children=[
            html.H2("🔥 Top 5 Most Critical Security Events 🔥"),
            dcc.Graph(
                id='top-external-ips',
                        figure=px.funnel(
                            top_ips_df,
                            x='count',
                            y='Source IP',
                            title="Top External IPs Triggering Alerts",
                            color='count'
                        )
            ),
            dcc.Graph(
                id='attack-source-distribution',
                figure=px.treemap(
                    top_ips_df,
                    path=['Source IP'],
                    values='count',
                    title="Top Sources of External Attacks",
                    color='count',
                    color_continuous_scale='Blues'
                )
            )
        ]),

        # 📈 Answer 2: Security Trends
        dcc.Tab(label='Question 2: Security Trends', children=[
            html.H2("📈 Security Trends Over 2-Day Period 📈"),
            dcc.Graph(
                id='firewall-traffic-trend',
                figure=px.line(
                    firewall_traffic_df,
                    x='Date/time',
                    y='Connections built',  # Corrected to 'Connections built'
                    title="Firewall Connections Built Over Time",
                    color_discrete_sequence=["#EF553B"]
                )
            ),
            '''
            dcc.Graph(
                id='ids-alert-trend',
                figure=px.line(
                    ids_traffic_df,
                    x='Date/time',
                    y='priority',
                    title="IDS Alert Counts Over Time",
                    color_discrete_sequence=["#636EFA"]
                )
            )'''
        ]),

        # 🕵️ Answer 3: Root Cause Analysis
        dcc.Tab(label='Question 3: Root Cause Analysis', children=[
            html.H2("🕵️ Root Cause Analysis 🕵️"),
            dcc.Graph(
                id='port-usage-analysis',
                        figure=px.scatter(
                            top_ports_df,
                            x='Destination port',
                            y='count',
                            size='log_count',  # Use the log-transformed count for bubble sizes
                            color='count',  # Color by the count itself
                            title="Frequently Used Ports (Potential Exploits)",
                            size_max=40,  # Make sure even small counts are visible
                            color_continuous_scale='Viridis',  # Optional but visually appealing
                            #hover_data={'count': True, 'log_count': True}  # Show both original count and log count
                        )
            ),
            dcc.Graph(
                id='external-ip-analysis',
                        figure=px.scatter(
                            firewall_traffic_df,
                            x='Source IP',
                            y='Destination IP',
                            size='Source_Priority',
                            color='Operation',
                            #opacity=0.7,  # Makes overlapping points visible
                            title="External IP Analysis",
                            color_discrete_sequence=px.colors.qualitative.Dark24
                        ).update_traces(marker=dict(size=5))  # Uniform size for all dots
            )
        ]),

        # 🔥 Hybrid Analysis
        dcc.Tab(label='Hybrid Analysis', children=[
            html.H2("🧬 Hybrid Analysis (IDS + Firewall) 🧬"),
            dcc.Graph(
                id='combined-ip-connection',
                figure=px.scatter(
                    pd.concat([firewall_traffic_df.assign(source='firewall'),
                               ids_traffic_df.assign(source='ids')]),
                    x='Source IP',
                    y='Destination IP',
                    color='Source_NodeType',
                    title="Combined Source IP vs Destination IP (Interactive)",
                    color_discrete_sequence=px.colors.qualitative.T10
                )
            )
        ])
    ])
])

# ================================
# 🚀 Run the Dashboard
# ================================
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
