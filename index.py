from dash import dcc, html
import dash_bootstrap_components as dbc
#from dash_bootstrap_templates import load_figure_template
import pandas as pd
from dash.dependencies import Input, Output
from datetime import datetime
from datetime import timedelta
import callbacks
import os
from app import app
from datetime import date

# Overall layout
app.layout = html.Div([
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
                dbc.Input(id = 'lat', type = 'number', placeholder='GPS Latitude Goes Here'),
                html.Br(),
                dbc.Input(id = 'long', type = 'number', placeholder='GPS Longitude Goes Here'),
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
            dbc.Row([dbc.Col(sidebar), 
                    dbc.Col(
                        dcc.Graph(id = 'graph_temp'
                            ), width = 9
                        )
                    ])
        ])

tab_2 = html.Div([
            html.Br(),
            html.H3('Changes in Climate Metrics by Season'),
            html.Hr(),
            dbc.Row([dbc.Col(sidebar), 
                    dbc.Col(
                        dcc.Graph(
                            figure=dict(
                                data=[dict(
                                    x=[1, 2, 3],
                                    y=[3, 1, 2],
                                    type='bar'
                                )]
                            )
                        ), width = 9
                    )
            ])
        ])

# Seasonal Climate Changes Tab 

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')

