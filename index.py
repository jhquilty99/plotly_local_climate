from dash import dcc, html
import dash_bootstrap_components as dbc
#from dash_bootstrap_templates import load_figure_template
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime
from datetime import timedelta
import os
from app import app
from datetime import date

# Overall layout
app.layout = html.Div([
    dcc.Store(id = 'tabs-value'),
    html.Br(),
    # Header
    html.H1('Climate Visualizer'),
    # Tabs for each section
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Annual Climate Changes', value='tab-1'),
        dcc.Tab(label='Seasonal Climate Changes', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

# Sidebar for tabs
SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
sidebar = html.Div(
    [
        html.H2("Filters"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with filters", className="lead"
        ),
        dbc.Nav(
            [
                dcc.Input(id = 'lat', type = 'number', min = -90, max = 90, placeholder='GPS Latitude Goes Here', debounce = True, value = 38.80),
                html.Br(),
                dcc.Input(id = 'long', type = 'number', min = -180, max = 180, placeholder='GPS Longitude Goes Here', debounce = True, value = -77.05),
                html.Br(),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed = date(1960, 1, 1),
                    max_date_allowed = date.today(),
                    start_date = date(1970, 3, 1),
                    end_date = date(2023, 3, 1)
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Annual Climate Changes Tab
tab_1 = html.Div([
            html.Br(),
            html.H3('Changes in Climate Metrics by Year'),
            html.Hr(),
            html.P('Visualizes climate metrics by year: temperature, snow day percent, frost day percent.', className="lead"),
            dbc.Row([dbc.Col(sidebar), 
                    dbc.Col([
                        html.P('Mean temperature by year with trendline', className="lead"),
                        dcc.Graph(id = 'graph_1'),
                        html.P('Mean snow and frost days percent by year with trendline', className="lead"),
                        dcc.Graph(id = 'graph_2'),
                        html.P('Mean temperature heatmap by year and month', className="lead"),
                        dcc.Graph(id = 'graph_3'),
                    ], width = 9)
                ])
        ])

tab_2 = html.Div([
            html.Br(),
            html.H3('Changes in Climate Metrics by Season'),
            html.Hr(),
            html.P('Visualizes climate metrics by month: temperature, snowfall chance, frost day percent.', className="lead"),
            dbc.Row([dbc.Col(sidebar), 
                    dbc.Col([
                        html.P('Mean temperature and snowfall chance by month', className="lead"),
                        dcc.Graph(id = 'graph_1'),
                        html.P('Mean snow and frost day chance by month with frost date line', className="lead"),
                        dcc.Graph(id = 'graph_2'),
                        html.P('Mean temperature heatmap by day and month', className="lead"),
                        dcc.Graph(id = 'graph_3'),
                    ], width = 9)
                ])
        ])

# Seasonal Climate Changes Tab 

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')

