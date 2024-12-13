import os
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ================================
# 🔧 Configuration
# ================================
ANALYSIS_SUMMARIES_DIR = os.path.join('scripts', 'analysis_summaries')

# Load the preprocessed data
try:
    firewall_traffic_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_firewall_traffic.csv')).head(10000)  # Limiting to 10k rows
    ids_traffic_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ids_traffic.csv')).head(10000)  # Limiting to 10k rows
    top_services_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_services.csv'))
    top_ports_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_ports.csv'))
    top_ips_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_20_external_ips.csv'))
    geoip_lookup_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ips_geoip.csv'))
except Exception as e:
    print(f"[ERROR] Could not load one or more analysis files. {e}")
    exit()

# Convert priority columns to numeric
if 'Source_Priority' in firewall_traffic_df.columns:
    firewall_traffic_df['Source_Priority'] = pd.to_numeric(firewall_traffic_df['Source_Priority'], errors='coerce')

if 'priority' in ids_traffic_df.columns:
    ids_traffic_df['priority'] = pd.to_numeric(ids_traffic_df['priority'], errors='coerce')

# Fill NaNs with 0 to avoid Plotly size errors
if 'Source_Priority' in firewall_traffic_df.columns:
    firewall_traffic_df['Source_Priority'] = firewall_traffic_df['Source_Priority'].fillna(0)

if 'priority' in ids_traffic_df.columns:
    ids_traffic_df['priority'] = ids_traffic_df['priority'].fillna(0)

# Fix column names if needed
if 'Destination service' not in top_services_df.columns:
    top_services_df.reset_index(inplace=True)
    top_services_df.rename(columns={'index': 'Destination service'}, inplace=True)

if 'Destination port' not in top_ports_df.columns:
    top_ports_df.reset_index(inplace=True)
    top_ports_df.rename(columns={'index': 'Destination port'}, inplace=True)

if 'Source IP' not in top_ips_df.columns:
    top_ips_df.reset_index(inplace=True)
    top_ips_df.rename(columns={'index': 'Source IP'}, inplace=True)

# ================================
# 🔥 Initialize Dash Application
# ================================
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Firewall & IDS Visualization Dashboard"

# ================================
# 📊 Layout for Dashboard
# ================================
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Firewall Analysis', children=[
            html.H2("Firewall Analysis"),
            dcc.Loading(
                children=[
                    dcc.Graph(
                        id='destination-service-distribution',
                        figure=px.treemap(
                            top_services_df,
                            path=['Destination service'],
                            values='count',
                            title="Top 50 Destination Services"
                        )
                    ),
                    dcc.Graph(
                        id='destination-port-usage',
                        figure=px.bar(
                            top_ports_df,
                            x='Destination port',
                            y='count',
                            title="Top 50 Destination Ports"
                        )
                    ),
                    dcc.Graph(
                        id='source-node-type-distribution',
                        figure=px.pie(
                            firewall_traffic_df,
                            names='Source_NodeType',
                            title="Source Node Type Distribution"
                        )
                    ),
                    dcc.Graph(
                        id='high-priority-traffic-line',
                        figure=px.line(
                            firewall_traffic_df,
                            x='Date/time',
                            y='Source_Priority',
                            title="High-Priority Traffic Analysis"
                        )
                    ),
                    dcc.Graph(
                        id='external-ip-analysis',
                        figure=px.scatter(
                            firewall_traffic_df,
                            x='Source IP',
                            y='Destination IP',
                            size='Source_Priority',  # Now numeric and no NaN
                            color='Operation',
                            title="External IP Analysis"
                        )
                    ),
                ]
            )
        ]),

        dcc.Tab(label='IDS Analysis', children=[
            html.H2("IDS Analysis"),
            dcc.Loading(
                children=[
                    dcc.Graph(
                        id='ids-alert-counts',
                        figure=px.line(
                            ids_traffic_df,
                            x='Date/time',
                            y='priority',
                            title="IDS Alert Counts Over Time"
                        )
                    ),
                    dcc.Graph(
                        id='top-20-external-ips',
                        figure=px.bar(
                            top_ips_df,
                            x='count',
                            y='Source IP',
                            orientation='h',
                            title="Top 20 External IPs Triggering Alerts"
                        )
                    ),
                    dcc.Graph(
                        id='classification-of-alerts',
                        figure=px.pie(
                            ids_traffic_df,
                            names='classification',
                            title="Classification of IDS Alerts"
                        )
                    ),
                    dcc.Graph(
                        id='source-vs-destination-ip',
                        figure=px.scatter(
                            ids_traffic_df,
                            x='Source IP',
                            y='Destination IP',
                            color='priority',
                            size='priority',  # Now priority is numeric and not NaN
                            title="Source IP vs Destination IP"
                        )
                    ),
                    # GEOIP Analysis (Commented Out)
                    # dcc.Graph(
                    #     id='geoip-analysis',
                    #     figure=px.scatter_geo(
                    #         geoip_lookup_df,
                    #         lat='Latitude',
                    #         lon='Longitude',
                    #         text='City',
                    #         title="GeoIP Analysis of External IPs",
                    #         hover_name='City',
                    #         hover_data=['Country', 'IP']
                    #     )
                    # ),
                ]
            )
        ]),

        dcc.Tab(label='Hybrid Analysis', children=[
            html.H2("Hybrid Analysis (IDS + Firewall)"),
            dcc.Loading(
                children=[
                    dcc.Graph(
                        id='combined-alert-traffic-line',
                        figure=px.line(
                            pd.concat([firewall_traffic_df.assign(source='firewall'),
                                       ids_traffic_df.assign(source='ids')]),
                            x='Date/time',
                            y='priority',
                            color='source',
                            title="Combined IDS & Firewall Alert Counts Over Time"
                        )
                    ),
                    dcc.Graph(
                        id='combined-ip-connection',
                        figure=px.scatter(
                            pd.concat([firewall_traffic_df.assign(source='firewall'),
                                       ids_traffic_df.assign(source='ids')]),
                            x='Source IP',
                            y='Destination IP',
                            color='Source_NodeType',
                            title="Combined Source IP vs Destination IP"
                        )
                    ),
                ]
            )
        ]),
    ])
])

# ================================
# 🚀 Run the Dashboard
# ================================
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
