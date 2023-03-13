from index import app
import index
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import graph
import etl
from datetime import date


@app.callback(
    Output('tabs-content', 'children'),
    Output('tabs-value','data'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return (index.tab_1, 1)
    elif tab == 'tab-2':
        return (index.tab_2, 2)
    

@app.callback(
    Output('graph_1', 'figure'),
    Output('graph_2', 'figure'),
    Output('graph_3', 'figure'),
    Input('lat','value'),
    Input('long','value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'), 
    Input('tabs-value','data'),
    #prevent_initial_call=True
    )
def update_temp_graph(lat, long, start_date, end_date, tabs):
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    data = etl.load_annual_data(lat, long, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    if tabs == 1:
        return(graph.temp_trend(data[2]), graph.snow_trend(data[2]), graph.heatmap_temp(data[0]))
    else:
        return(graph.temp_snow(data[0],data[1]), graph.frost_line(data[0]), graph.heatmap_temp(data[0], by = ['day','month']))
    
    