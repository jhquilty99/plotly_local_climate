from index import app
import index
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import graph
import etl
from datetime import date


@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return index.tab_1
    elif tab == 'tab-2':
        return index.tab_2
    

@app.callback(
    Output('graph_temp', 'children'),
    Input('lat','value'),
    Input('long','value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'), 
    #prevent_initial_call=True
    )
def update_temp_graph(lat, long, start_date, end_date):
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    data = etl.load_annual_data(lat, long, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    return(graph.graph_temp(data[0],data[1]))
    