from dash import dcc, html
import dash_bootstrap_components as dbc
#from dash_bootstrap_templates import load_figure_template
import os
from datetime import date
from app import app
from dash_bootstrap_templates import load_figure_template
import dash_leaflet as dl


load_figure_template('DARKLY')

# Sidebar for tabs
SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "100%",
    "padding": "1rem 1rem",
    "backgroundColor": "#000000",
}
INLINE_STYLE = {'display': 'inline-block', 'width':'49%'}
LOADING_STYLE = {'position': 'absolute', 'align-self': 'center'}
sidebar = html.Div([
        html.H2("Filters"),
        html.Hr(),
        dbc.Stack([
                dl.Map([dl.TileLayer(), dl.LayerGroup(id = 'pin-layer')], id = 'map-figure', zoom = 7, center = (38.895, -77.036), style={'height': '500px', 'width': '100%', 'margin': "auto", "display": "block"}),
                #dbc.Row([html.H4('GPS Latitude', style=INLINE_STYLE), dcc.Input(id = 'lat', type = 'number', min = -90, max = 90, placeholder='GPS Latitude Goes Here', debounce = True, value = 38.80, style=INLINE_STYLE_PADDING)]), 
                #dbc.Row([html.H4('GPS Longitude', style=INLINE_STYLE), dcc.Input(id = 'long', type = 'number', min = -180, max = 180, placeholder='GPS Longitude Goes Here', debounce = True, value = -77.05, style=INLINE_STYLE_PADDING)]), 
                dbc.Row([html.H4('Start -> End', style=INLINE_STYLE), dcc.DatePickerRange(
                                                        id='date-picker-range',
                                                        min_date_allowed = date(1960, 1, 1),
                                                        max_date_allowed = date.today(),
                                                        start_date = date(1970, 3, 1),
                                                        end_date = date(2023, 3, 1),
                                                        clearable=True,
                                                        style = INLINE_STYLE 
                                                    )]), 
                dbc.Row([dbc.Button('Apply Changes', color = 'info', id = 'apply-changes')])
        ], gap = 3)
    ], style=SIDEBAR_STYLE)

# Overall layout
app.layout = html.Div([
    dcc.Store(id = 'tabs-value'),
    dcc.Store(id = 'lat'),
    dcc.Store(id = 'long'),
    dcc.Store(id = 'data'),
    dcc.Store(id = 'annual-data'),
    dcc.Store(id = 'seasonal-data'),
    html.Br(),
    # Header
    html.H1('Climate Visualizer'),
    sidebar,
    # Tabs for each section
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Annual Climate Changes', value='tab-1', selected_style={"backgroundColor": '#3498db','color':'#FFFFFF'}),
        dcc.Tab(label='Seasonal Climate Changes', value='tab-2', selected_style={"backgroundColor": '#3498db','color':'#FFFFFF'}),
    ], colors = { 'border': "#000000", 'primary': '#3498db', 'background': "#222"}),
    html.Div(id='tabs-content'),
], style = {"padding": "1rem"})

# Annual Climate Changes Tab
tab_1 = html.Div([
            html.Br(),
            html.H3('Changes in Climate Metrics by Year'),
            html.Hr(),
            html.P('Visualizes climate metrics by year: temperature, snow day percent, frost day percent.', className="lead"),
            dcc.Loading(html.Div(id = 'statement'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_1'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_2'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_3'), type = 'circle')
        ])

# Seasonal Climate Changes Tab 
tab_2 = html.Div([
            html.Br(),
            html.H3('Changes in Climate Metrics by Season'),
            html.Hr(),
            html.P('Visualizes climate metrics by month: temperature, snowfall chance, frost day percent.', className="lead"),
            dcc.Loading(html.Div(id = 'statement'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_1'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_2'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_3'), type = 'circle')
        ])





