import index
from dash.dependencies import Input, Output, State
import graph
import etl
from datetime import date
import dash_leaflet as dl
import pandas as pd
from dash import html

@index.app.callback(
    Output('tabs-content', 'children'),
    Output('tabs-value','data'),
    Input('tabs', 'value'),
    #prevent_initial_call=True
)
def render_content(tab):
    if tab == 'tab-1':
        return (index.tab_1, 1)
    elif tab == 'tab-2':
        return (index.tab_2, 2)
    
@index.app.callback(
    Output('statement','children'),
    Output('graph_1', 'figure'),
    Output('graph_2', 'figure'),
    Output('graph_3', 'figure'),
    Input('tabs-value','data'),
    Input('data','data'),
    Input('seasonal-data','data'),
    Input('annual-data','data'),
    State('lat','data'),
    State('long','data'),
    prevent_initial_call=True
) 
def update_graphs(tabs, data, seasonal_data, annual_data, lat, long):
    data = pd.read_json(data)
    seasonal_data = pd.read_json(seasonal_data)
    annual_data = pd.read_json(annual_data)
    if tabs == 1:
        temp_trend = graph.temp_trend(annual_data)
        snow_trend = graph.snow_trend(annual_data)
        return(html.Div([html.P(f'For GPS Coordinates ({str(lat)}, {str(long)}):'),
                        html.P(f' - Yearly mean temperatures have risen from {temp_trend[2]}°F in {snow_trend[7]} to {temp_trend[3]}°F in {snow_trend[8]} or {str(round(temp_trend[1],3))} degrees Fahrenheit per year.'), 
                        html.P(f' - Percent of the year which could be counted as snow days (snow fall > 0) went from {snow_trend[5]}% in {snow_trend[7]} to {snow_trend[6]}% in {snow_trend[8]} or {str(round(100*snow_trend[2],3))}% per year.'), 
                        html.P(f' - Percent of the year that has below freezing average tremperatures went from {snow_trend[3]}% in {snow_trend[7]} to {snow_trend[4]}% in {snow_trend[8]} or {str(round(100*snow_trend[1],3))}% per year.''')]), 
               graph.heatmap_temp(data), 
               temp_trend[0], 
               snow_trend[0])
    else:
        return(html.P(f'Seasonal metrics for GPS Coordinates all years ({str(lat)}, {str(long)}).'),
               graph.heatmap_temp(data, by = ['day','month']), 
               graph.temp_snow(data, seasonal_data), 
               graph.radiation_graph(data))


@index.app.callback(
    Output('data','data'),
    Output('seasonal-data','data'),
    Output('annual-data','data'),
    State('lat','data'),
    State('long','data'),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date'), 
    Input('apply-changes','n_clicks'),
    #prevent_initial_call=True
)
def update_data(lat, long, start_date, end_date, apply_changes):
    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)
    if lat == None:
        data = etl.load_annual_data(38.895, -77.036, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    else: 
        data = etl.load_annual_data(round(lat,3), round(long,3), start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    return(data[0].to_json(), data[1].to_json(), data[2].to_json())

@index.app.callback(
    Output('pin-layer', 'children'), 
    Output('lat','data'),
    Output('long','data'),
    Input('map-figure', "click_lat_lng"),
)
def map_update(click_lat_lng):
    if click_lat_lng == None:
        return([dl.Marker(position=(38.895, -77.036), children=dl.Tooltip("(38.895, -77.036)"))],
                38.895,
                -77.036
                )
    else:    
        return([dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))],
                round(click_lat_lng[0], 3),
                round(click_lat_lng[1], 3)
                )
    
if __name__ == '__main__':
    index.app.run_server(debug=True, host='127.0.0.1')

# To-do list
# - Create a DynamoDB to store API requests (x)
# - Include precipitation graph in seasonal and annual
# - Make blog point to haydenquilty.com
# - Include a slicer for year in seasonal changes 
# - Make summary clearer with absolute changes
# - Make website encode location and date range data in url
# - Add padding around apply changes (x)
    
    