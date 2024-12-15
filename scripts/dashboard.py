import os
import dash
from dash import dcc, html, Input, Output
import dask.dataframe as dd  # For large files
import pandas as pd  # For normal DataFrame usage
import plotly.express as px
import plotly.graph_objects as go

# ================================
# 🔧 Configuration
# ================================
ANALYSIS_SUMMARIES_DIR = os.path.join('scripts', 'analysis_summaries')

# ================================
# 📂 Load Data Using Dask
# ================================
try:
    dtypes = {
        'source_service': 'object',
        'destination_service': 'object',
        'source_ip': 'object',
        'destination_ip': 'object',
        'source_port': 'object',
        'destination_port': 'object',
        'source_priority': 'float64',
        'priority': 'float64',
        'classification': 'object',
        'operation': 'object',
        'source_nodetype': 'object',
        'isexternaltraffic': 'bool'
    }

    firewall_traffic_df = dd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_firewall_traffic.csv'),
        dtype=dtypes, 
        assume_missing=True,
        low_memory=False
    ).head(10000)

    ids_traffic_df = dd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ids_traffic.csv'),
        dtype=dtypes, 
        assume_missing=True,
        low_memory=False
    ).head(10000)

    top_services_df = pd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_services.csv'),
        dtype={'destination_service': 'object', 'count': 'int64'}
    )

    top_ports_df = pd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_ports.csv'),
        dtype={'destination_port': 'int64', 'count': 'int64'}
    )

    top_ips_df = pd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_external_ips.csv'),
        dtype={'source_ip': 'object', 'count': 'int64'}
    )

    # 🔥 Debug: Print the column names and data types for verification
    print("[DEBUG] Firewall Traffic DataFrame Columns and Data Types")
    print(firewall_traffic_df.dtypes)
    print("[DEBUG] IDS Traffic DataFrame Columns and Data Types")
    print(ids_traffic_df.dtypes)
    print("[DEBUG] Firewall Traffic DataFrame Preview")
    print(firewall_traffic_df.head())
    print("[DEBUG] IDS Traffic DataFrame Preview")
    print(ids_traffic_df.head())

except Exception as e:
    print(f"[ERROR] Could not load one or more analysis files. {e}")
    exit()

# ================================
# 🔥 Data Cleaning and Enhancements
# ================================
try:
    # Normalize column names (strip spaces, lowercase, and replace spaces with underscores)
    firewall_traffic_df.columns = firewall_traffic_df.columns.str.strip().str.lower().str.replace(' ', '_')
    ids_traffic_df.columns = ids_traffic_df.columns.str.strip().str.lower().str.replace(' ', '_')
    top_services_df.columns = top_services_df.columns.str.strip().str.lower().str.replace(' ', '_')
    top_ports_df.columns = top_ports_df.columns.str.strip().str.lower().str.replace(' ', '_')
    top_ips_df.columns = top_ips_df.columns.str.strip().str.lower().str.replace(' ', '_')

except Exception as e:
    print(f"[ERROR] Data cleaning failed due to: {e}")
    exit()

# ================================
# 🔥 Initialize Dash Application
# ================================
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "🔥 Firewall & IDS Analysis Dashboard 🔥"

# ================================
# 📊 Layout for Dashboard
# ================================
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Question 1: Critical Security Events', children=[
            html.H2("🔥 Top 5 Most Critical Security Events 🔥"),
            dcc.Graph(
                id='critical-events-sunburst',
                figure=px.sunburst(
                    ids_traffic_df,
                    path=['classification', 'priority'],
                    values='priority',
                    title="Classification of Top 5 Critical Events",
                    color='priority',
                    color_continuous_scale='Viridis'
                )
            ),
            dcc.Graph(
                id='attack-source-distribution',
                figure=px.treemap(
                    top_ips_df,
                    path=['source_ip'],
                    values='count',
                    title="Top Sources of External Attacks",
                    color='count',
                    color_continuous_scale='Blues'
                )
            ),
        ]),

        dcc.Tab(label='Question 2: Security Trends', children=[
            html.H2("📈 Security Trends Over 2-Day Period 📈"),
            dcc.Graph(
                id='firewall-traffic-trend',
                figure=px.line(
                    firewall_traffic_df,
                    x='date/time',
                    y='source_priority',
                    title="Firewall Traffic Over Time",
                    color_discrete_sequence=["#EF553B"]
                )
            ),
            dcc.Graph(
                id='ids-alert-trend',
                figure=px.line(
                    ids_traffic_df,
                    x='date/time',
                    y='priority',
                    title="IDS Alert Counts Over Time",
                    color_discrete_sequence=["#636EFA"]
                )
            ),
        ]),

        dcc.Tab(label='Question 3: Root Cause Analysis', children=[
            html.H2("🕵️ Root Cause Analysis 🕵️"),
            dcc.Graph(
                id='port-usage-analysis',
                figure=px.scatter(
                    top_ports_df,
                    x='destination_port',
                    y='count',
                    size='count',
                    title="Analysis of Frequently Used Ports (Potential Exploits)"
                )
            ),
            dcc.Graph(
                id='source-vs-destination-ip',
                figure=px.scatter(
                    firewall_traffic_df,
                    x='source_ip',
                    y='destination_ip',
                    color='source_nodetype',
                    title="Source IP vs Destination IP (Network Attack Tracing)"
                )
            )
        ]),

        dcc.Tab(label='Hybrid Analysis', children=[
            html.H2("🧬 Hybrid Analysis (IDS + Firewall) 🧬"),
            dcc.Graph(
                id='combined-ip-connection',
                figure=px.scatter(
                    pd.concat([firewall_traffic_df.assign(source='firewall'),
                               ids_traffic_df.assign(source='ids')]),
                    x='source_ip',
                    y='destination_ip',
                    color='source_nodetype',
                    title="Combined Source IP vs Destination IP (Interactive)"
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
