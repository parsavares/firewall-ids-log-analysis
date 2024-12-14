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
        'Source Service': 'object',
        'Destination Service': 'object',
        'Source IP': 'object',
        'Destination IP': 'object',
        'Source port': 'object',
        'Destination port': 'object',
        'Source_Priority': 'float64',
        'priority': 'float64',
        'classification': 'object',
        'Operation': 'object',
        'Source_NodeType': 'object',
        'IsExternalTraffic': 'bool'
    }

    # Load large files using Dask
    firewall_traffic_df = dd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_firewall_traffic.csv'),
        dtype=dtypes, 
        assume_missing=True,
        low_memory=False
    ).head(10000)  # Load a small sample

    ids_traffic_df = dd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ids_traffic.csv'),
        dtype=dtypes, 
        assume_missing=True,
        low_memory=False
    ).head(10000)  # Load a small sample

    # Read smaller files directly using Pandas
    top_services_df = pd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_services.csv'),
        dtype={'Destination Service': 'object', 'count': 'int64'}
    )

    top_ports_df = pd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_ports.csv'),
        dtype={'Destination port': 'int64', 'count': 'int64'}
    )

    top_ips_df = pd.read_csv(
        os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_external_ips.csv'),
        dtype={'Source IP': 'object', 'count': 'int64'}
    )

except Exception as e:
    print(f"[ERROR] Could not load one or more analysis files. {e}")
    exit()

# ================================
# 🔥 Data Cleaning and Enhancements
# ================================
try:
    # Normalize column names (strip spaces and lowercase)
    firewall_traffic_df.columns = firewall_traffic_df.columns.str.strip().str.title().str.replace(' ', '_')
    ids_traffic_df.columns = ids_traffic_df.columns.str.strip().str.title().str.replace(' ', '_')
    top_services_df.columns = top_services_df.columns.str.strip().str.title().str.replace(' ', '_')
    top_ports_df.columns = top_ports_df.columns.str.strip().str.title().str.replace(' ', '_')
    top_ips_df.columns = top_ips_df.columns.str.strip().str.title().str.replace(' ', '_')

    # Ensure 'Source_Priority' exists, if not, create it
    if 'Source_Priority' not in firewall_traffic_df.columns:
        firewall_traffic_df['Source_Priority'] = 1

    if 'Priority' not in ids_traffic_df.columns:
        ids_traffic_df['Priority'] = 1

    # Convert 'Source_Priority' to numeric and fill NaNs
    firewall_traffic_df['Source_Priority'] = pd.to_numeric(
        firewall_traffic_df['Source_Priority'], errors='coerce'
    ).fillna(1)

    # Convert 'priority' to numeric and fill NaNs
    ids_traffic_df['Priority'] = pd.to_numeric(
        ids_traffic_df['Priority'], errors='coerce'
    ).fillna(1)

    firewall_traffic_df['Source_Nodetype'] = firewall_traffic_df.get('Source_Nodetype', 'Unknown')
    firewall_traffic_df['Operation'] = firewall_traffic_df.get('Operation', 'Other')

except Exception as e:
    print(f"[ERROR] Data cleaning failed due to: {e}")
    exit()

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
        dcc.Tab(label='Firewall Analysis', children=[
            html.H2("🔥 Firewall Analysis 🔥"),
            dcc.Graph(
                id='internal-vs-external-traffic',
                figure=px.pie(
                    firewall_traffic_df,
                    names='Isexternaltraffic',
                    title="Internal vs External Traffic",
                    hole=0.4
                )
            ),
            dcc.Graph(
                id='destination-service-distribution',
                figure=px.treemap(
                    top_services_df,
                    path=['Destination_Service'],
                    values='Count',
                    title="Top Destination Services"
                )
            ),
            dcc.Graph(
                id='destination-port-bubble',
                figure=px.scatter(
                    top_ports_df,
                    x='Destination_Port',
                    y='Count',
                    size='Count',
                    color='Count',
                    title="Top Destination Ports"
                )
            )
        ]),

        dcc.Tab(label='IDS Analysis', children=[
            html.H2("🚀 IDS Analysis 🚀"),
            dcc.Graph(
                id='ids-alert-counts',
                figure=px.bar(
                    ids_traffic_df,
                    x='Date/Time',
                    y='Priority',
                    title="IDS Alert Counts Over Time"
                )
            ),
            dcc.Graph(
                id='top-external-ips',
                figure=px.funnel(
                    top_ips_df,
                    x='Count',
                    y='Source_Ip',
                    title="Top External IPs"
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
