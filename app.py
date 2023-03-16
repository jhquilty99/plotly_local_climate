from dash import Dash
import dash_bootstrap_components as dbc
from flask import Flask

#Instantiates the Dash app and identify the server
server = Flask(__name__)
app = Dash(__name__, server = server, title='Climate Visualizer', external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)
