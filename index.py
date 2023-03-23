from dash import dcc, html
import dash_bootstrap_components as dbc
#from dash_bootstrap_templates import load_figure_template
from datetime import date
from app import app
import dash_leaflet as dl
from dash_iconify import DashIconify

# Sidebar for tabs
SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "100%",
    "padding": "1rem 1rem",
    "backgroundColor": "#000000",
}
SELECT_STYLE = {"backgroundColor": '#3498db','color':'#FFFFFF', 'boxShadow': '0px 7px 15px #000'}
sidebar = html.Div([
        html.H2('Filters'),
        html.Hr(),
        html.H4("Pin a Location Anywhere in the World to See its Historical Climate Data"),
        dbc.Stack([
                dl.Map([dl.TileLayer(), dl.LayerGroup(id = 'pin-layer')], id = 'map-figure', zoom = 7, center = (38.895, -77.036), style={'height': '500px', 'width': '100%', 'margin': "auto", "display": "block"}),
                #dbc.Row([html.H4('GPS Latitude', style=INLINE_STYLE), dcc.Input(id = 'lat', type = 'number', min = -90, max = 90, placeholder='GPS Latitude Goes Here', debounce = True, value = 38.80, style=INLINE_STYLE_PADDING)]), 
                #dbc.Row([html.H4('GPS Longitude', style=INLINE_STYLE), dcc.Input(id = 'long', type = 'number', min = -180, max = 180, placeholder='GPS Longitude Goes Here', debounce = True, value = -77.05, style=INLINE_STYLE_PADDING)]), 
                dbc.Row([dbc.Button('Apply Changes', color = 'info', id = 'apply-changes')], style={'marginBottom':'1rem'}),
                dbc.Row([dcc.Loading(dcc.Store(id = 'data')),dcc.Store(id = 'annual-data'),dcc.Store(id = 'seasonal-data'),dcc.Store(id = 'solar-data')], style={'marginBottom':'1rem'}),
        ], gap = 3)
    ], style=SIDEBAR_STYLE)

# Overall layout
app.layout = html.Div([
    dcc.Store(id = 'tabs-value'),
    dcc.Store(id = 'lat'),
    dcc.Store(id = 'long'),
    html.Br(),
    # Header
    html.H1('CLIMATE VISUALIZER', style = {'display':'inline','width':'49%','fontStyle':'bold'}),
    html.A([
        DashIconify(icon="ion:logo-github", width=50s, color='#ebebeb')
    ], href='https://github.com/jhquilty99/plotly_local_climate', style = {'float':'right'}),
    html.H6('The purpose of this website is to make it easy to identify annual and seasonal changes in climate conditions anywhere in the world. Climate change impacts us all, but it seems like a far away problem sometimes. Find your area of interest on the map, and hit apply changes to get started visualizing climate change in the graphs below.'),
    sidebar,
    # Tabs for each section
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Annual Climate Changes', value='tab-1', selected_style=SELECT_STYLE),
        dcc.Tab(label='Seasonal Climate Changes', value='tab-2', selected_style=SELECT_STYLE),
    ], colors = { 'border': "#000000", 'primary': '#3498db', 'background': "#222"}),
    dcc.Loading(html.Div(id='tabs-content'), type = 'circle'),
    html.H6([dcc.Link('Weather data by Open-Meteo.com.',"https://open-meteo.com/"),
             'ERA5: Generated using Copernicus Climate Change Service information 2023. ', 
             dcc.Link('Data is available under Attribution 4.0 International CC License.','https://creativecommons.org/licenses/by/4.0/')
    ], style={'fontStyle':'italic'}),
    html.H6([dcc.Link('Map data by OpenStreetMap®.','https://wiki.osmfoundation.org/wiki/Main_Page'),
             'Licensed under the ',
             dcc.Link('Open Data Commons Open Database License (ODbL).','https://opendatacommons.org/licenses/odbl/'),
    ], style={'fontStyle':'italic'}),
    html.H6(['Reverse geocoding provided by ', 
             dcc.Link('by Geoapify.','https://www.geoapify.com/term-and-conditions'),
    ], style={'fontStyle':'italic'}),
], style = {"padding": "1rem", "backgroundColor": '#343434', 'color':'#ebebeb'})

# Annual Climate Changes Tab
tab_1 = html.Div([
            html.Br(),
            html.H3('Changes in Climate Metrics by Year'),
            dcc.Loading(html.Div(id = 'statement', style = {"backgroundColor": "#000000","padding": "1rem 1rem"}), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_1'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_2'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_3'), type = 'circle')
        ])

# Seasonal Climate Changes Tab 
tab_2 = html.Div([
            html.Br(),
            html.H4('Changes in Climate Metrics by Season'),
            dcc.Loading(html.Div(id = 'statement', style = {"backgroundColor": "#000000","padding": "1rem 1rem"}), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_1'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_2'), type = 'circle'),
            dcc.Loading(dcc.Graph(id = 'graph_3'), type = 'circle')
        ])





