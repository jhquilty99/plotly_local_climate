from index import app
import index
from dash import Dash, dcc, html
from dash.dependencies import Input, Output


@app.callback(
    Output('tabs-content-1', 'children'),
    Input('tabs-1', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return index.tab_1
    elif tab == 'tab-2':
        return index.tab_2