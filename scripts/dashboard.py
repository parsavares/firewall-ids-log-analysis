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
    firewall_traffic_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_firewall_traffic.csv')).head(10000)
    ids_traffic_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ids_traffic.csv')).head(10000)
    top_services_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_services.csv'))
    top_ports_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_50_destination_ports.csv'))
    top_ips_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'top_20_external_ips.csv'))
    geoip_lookup_df = pd.read_csv(os.path.join(ANALYSIS_SUMMARIES_DIR, 'external_ips_geoip.csv'))
except Exception as e:
    print(f"[ERROR] Could not load one or more analysis files. {e}")
    exit()

# Data Cleaning
firewall_traffic_df['Source_Priority'] = pd.to_numeric(firewall_traffic_df.get('Source_Priority', 0), errors='coerce').fillna(0)
ids_traffic_df['priority'] = pd.to_numeric(ids_traffic_df.get('priority', 0), errors='coerce').fillna(0)

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
                            title="Top 50 Destination Services",
                            color='count',
                            color_continuous_scale='Blues'
                        )
                    ),
                    dcc.Graph(
                        id='destination-port-usage',
                        figure=px.bar(
                            top_ports_df,
                            x='Destination port',
                            y='count',
                            color='count',
                            title="Top 50 Destination Ports",
                            color_continuous_scale='Viridis'
                        )
                    ),
                    dcc.Graph(
                        id='source-node-type-distribution',
                        figure=px.pie(
                            firewall_traffic_df,
                            names='Source_NodeType',
                            title="Source Node Type Distribution",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                    ),
                    dcc.Graph(
                        id='high-priority-traffic-line',
                        figure=px.line(
                            firewall_traffic_df,
                            x='Date/time',
                            y='Source_Priority',
                            color_discrete_sequence=["#636EFA"],
                            title="High-Priority Traffic Analysis",
                            markers=True
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
                            title="External IP Analysis",
                            color_discrete_sequence=px.colors.qualitative.Dark24
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
                            color_discrete_sequence=["#EF553B"],
                            title="IDS Alert Counts Over Time",
                            markers=True
                        )
                    ),
                    dcc.Graph(
                        id='top-20-external-ips',
                        figure=px.bar(
                            top_ips_df,
                            x='count',
                            y='Source IP',
                            orientation='h',
                            color='count',
                            title="Top 20 External IPs Triggering Alerts",
                            color_continuous_scale='Agsunset'
                        )
                    ),
                    dcc.Graph(
                        id='classification-of-alerts',
                        figure=px.pie(
                            ids_traffic_df,
                            names='classification',
                            title="Classification of IDS Alerts",
                            color_discrete_sequence=px.colors.qualitative.Prism
                        )
                    ),
                    dcc.Graph(
                        id='source-vs-destination-ip',
                        figure=px.scatter(
                            ids_traffic_df,
                            x='Source IP',
                            y='Destination IP',
                            size='priority',
                            color='priority',
                            title="Source IP vs Destination IP",
                            color_continuous_scale='Cividis'
                        )
                    ),
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
