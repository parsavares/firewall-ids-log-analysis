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

# Data Cleaning and Enhancements
firewall_traffic_df['Source_Priority'] = pd.to_numeric(firewall_traffic_df.get('Source_Priority', 1), errors='coerce').fillna(1)
ids_traffic_df['priority'] = pd.to_numeric(ids_traffic_df.get('priority', 1), errors='coerce').fillna(1)

# Replace zero weights to avoid ZeroDivisionError
firewall_traffic_df.loc[firewall_traffic_df['Source_Priority'] == 0, 'Source_Priority'] = 1
ids_traffic_df.loc[ids_traffic_df['priority'] == 0, 'priority'] = 1

# Replace NaN or None in critical columns for sunburst
firewall_traffic_df['Source_NodeType'] = firewall_traffic_df['Source_NodeType'].fillna('Unknown')
firewall_traffic_df['Operation'] = firewall_traffic_df['Operation'].fillna('Other')

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
            dcc.Loading(
                children=[
                    dcc.Graph(
                        id='destination-service-distribution',
                        figure=px.treemap(
                            top_services_df,
                            path=['Destination service'],
                            values='count',
                            title="Top Destination Services",
                            color='count',
                            color_continuous_scale='Blues'
                        )
                    ),
                    dcc.Graph(
                        id='destination-port-bubble',
                        figure=px.scatter(
                            top_ports_df,
                            x='Destination port',
                            y='count',
                            size='count',
                            color='count',
                            title="Top Destination Ports (Bubble Chart)",
                            color_continuous_scale='Viridis'
                        )
                    ),
                    dcc.Graph(
                        id='source-node-type-distribution',
                        figure=px.sunburst(
                            firewall_traffic_df,
                            path=['Source_NodeType', 'Operation'],
                            values='Source_Priority',
                            title="Source Node Type & Operations",
                            color='Source_Priority',
                            color_continuous_scale='Cividis'
                        )
                    ),
                    dcc.Graph(
                        id='high-priority-traffic',
                        figure=px.area(
                            firewall_traffic_df,
                            x='Date/time',
                            y='Source_Priority',
                            title="High-Priority Traffic Analysis (Area Chart)",
                            color_discrete_sequence=["#EF553B"]
                        )
                    )
                ]
            )
        ]),

        dcc.Tab(label='IDS Analysis', children=[
            html.H2("🚀 IDS Analysis 🚀"),
            dcc.Loading(
                children=[
                    dcc.Graph(
                        id='ids-alert-counts',
                        figure=px.bar(
                            ids_traffic_df,
                            x='Date/time',
                            y='priority',
                            title="IDS Alert Counts Over Time",
                            color='priority',
                            color_continuous_scale='Reds'
                        )
                    ),
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
                        id='classification-of-alerts',
                        figure=px.sunburst(
                            ids_traffic_df,
                            path=['classification', 'priority'],
                            values='priority',
                            title="Classification of IDS Alerts",
                            color='priority',
                            color_continuous_scale='Cividis'
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
                            title="Source IP vs Destination IP (Color by Priority)",
                            color_continuous_scale='Magma'
                        )
                    )
                ]
            )
        ]),

        dcc.Tab(label='Hybrid Analysis', children=[
            html.H2("🧬 Hybrid Analysis (IDS + Firewall) 🧬"),
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
                            title="Combined IDS & Firewall Alert Counts Over Time",
                            color_discrete_sequence=px.colors.qualitative.Pastel
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
                            title="Combined Source IP vs Destination IP (Interactive)",
                            color_discrete_sequence=px.colors.qualitative.T10
                        )
                    )
                ]
            )
        ])
    ])
])

# ================================
# 🚀 Run the Dashboard
# ================================
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
