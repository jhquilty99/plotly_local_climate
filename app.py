from dash import Dash
import dash_bootstrap_components as dbc

#Instantiates the Dash app and identify the server
app = Dash(title='Climate Visualizer', external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP])
