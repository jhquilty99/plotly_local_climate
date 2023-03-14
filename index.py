from dash import dcc, html
import dash_bootstrap_components as dbc
#from dash_bootstrap_templates import load_figure_template
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime
from datetime import timedelta
import os
from datetime import date
from app import app

# Sidebar for tabs
SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "100%",
    "padding": "2rem 1rem",
    "backgroundColor": "#f8f9fa",
}
sidebar = html.Div([
        html.H2("Filters"),
        html.Hr(),
        dbc.Row([
                dbc.Col(dbc.Stack([html.H4('GPS Latitude'),html.H4('GPS Longitude'),html.H4('Start -> End')], gap = 3), width = "auto"), 
                dbc.Col(dbc.Stack([dcc.Input(id = 'lat', type = 'number', min = -90, max = 90, placeholder='GPS Latitude Goes Here', debounce = True, value = 38.80),
                         dcc.Input(id = 'long', type = 'number', min = -180, max = 180, placeholder='GPS Longitude Goes Here', debounce = True, value = -77.05),
                         dcc.DatePickerRange(
                                            id='date-picker-range',
                                            min_date_allowed = date(1960, 1, 1),
                                            max_date_allowed = date.today(),
                                            start_date = date(1970, 3, 1),
                                            end_date = date(2023, 3, 1)
                        )], gap = 3), width = "auto")
        ])
    ], style=SIDEBAR_STYLE)

# Overall layout
app.layout = html.Div([
    dcc.Store(id = 'tabs-value'),
    html.Br(),
    # Header
    html.H1('Climate Visualizer'),
    sidebar,
    # Tabs for each section
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Annual Climate Changes', value='tab-1'),
        dcc.Tab(label='Seasonal Climate Changes', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
], style = {"padding": "1rem"})

# Annual Climate Changes Tab
tab_1 = html.Div([
            html.Br(),
            html.H3('Changes in Climate Metrics by Year'),
            html.Hr(),
            html.P('Visualizes climate metrics by year: temperature, snow day percent, frost day percent.', className="lead"),
            html.P('Mean temperature by year with trendline', className="lead"),
            dcc.Graph(id = 'graph_1'),
            html.P('Mean snow and frost days percent by year with trendline', className="lead"),
            dcc.Graph(id = 'graph_2'),
            html.P('Mean temperature heatmap by year and month', className="lead"),
            dcc.Graph(id = 'graph_3')
        ])

# Seasonal Climate Changes Tab 
tab_2 = html.Div([
            html.Br(),
            html.H3('Changes in Climate Metrics by Season'),
            html.Hr(),
            html.P('Visualizes climate metrics by month: temperature, snowfall chance, frost day percent.', className="lead"),
            html.P('Mean temperature and snowfall chance by month', className="lead"),
            dcc.Graph(id = 'graph_1'),
            html.P('Mean snow and frost day chance by month with frost date line', className="lead"),
            dcc.Graph(id = 'graph_2'),
            html.P('Mean temperature heatmap by day and month', className="lead"),
            dcc.Graph(id = 'graph_3')
        ])





