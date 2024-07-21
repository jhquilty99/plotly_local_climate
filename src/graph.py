import etl 
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# For graph: 'Mean temperature and snowfall chance by month'
def temp_snow(df, monthly_agg_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Violin(x = df['month'], y = df['temperature_2m_mean'], name = 'Historical mean temperatures', fillcolor = 'Salmon', line = dict(color = 'Red')),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x = monthly_agg_df.index, y = monthly_agg_df['snow_day'], name = 'Chance of snow fall', line = dict(color = 'aqua')),
        secondary_y=True
    )
    fig.add_hrect(y0=-10, y1=32, 
                annotation_text="Freezing Temperatures", annotation_position="top",  
                annotation_font_size=11,
                annotation_font_color="White",
                fillcolor="blue", opacity=0.25, line_width=0)
    fig.update_xaxes(categoryorder='category ascending', 
                     title = 'Month', 
                     showgrid=False, 
                     showline=True, 
                     linewidth=2, 
                     linecolor='white')
    fig.update_yaxes(title = 'Temperature in Fahrenheit', 
                     secondary_y=False, 
                     showgrid=False,
                     range = [0, 100],
                     showline=True, 
                     linewidth=2, 
                     linecolor='white')
    fig.update_yaxes(title = 'Snow Day Chance',
                     secondary_y=True,
                     showgrid=False, 
                     range = [0, 1],
                     showline=True, 
                     linewidth=2, 
                     linecolor='white')
    fig.update_layout(title = 'Mean Temperature and Snowfall Chance by Month', 
                      template = "plotly_dark", 
                      legend_title = 'Metrics', 
                      legend_orientation = 'h', 
                      legend_y = -0.2,
                      plot_bgcolor = '#000', 
                      paper_bgcolor = '#000')
    return(fig)

# For graphs: 'Mean temperature heatmap by day and month', and 'Mean temperature heatmap by year and month'
def heatmap_temp(df, by = ['year','month']):
    fig = go.Figure()
    heatmap = df.groupby(by = by).apply(lambda x: x['temperature_2m_mean'].mean())
    heatmap = heatmap.reset_index(name = 'values')
    fig.add_trace(
        go.Heatmap(x = heatmap[by[0]], y = heatmap[by[1]], z = heatmap['values'], name = 'Historical radiation', colorbar_orientation='h', zmin = 0, zmax = 100, colorbar_y = -0.75, colorbar_title = 'Temperature in Fahrenheit', colorbar_title_side = 'bottom')
    )
    fig.update_xaxes(categoryorder='category ascending', 
                     title = by[0].capitalize(),
                     showgrid=False)
    fig.update_yaxes(categoryorder='category descending', 
                     title = by[1].capitalize(),
                     showgrid=False)
    fig.update_layout(title = f'Mean Temperature by {by[0].capitalize()} and {by[1].capitalize()}', 
                      template = "plotly_dark", 
                      legend_title = 'Temperature in Fahrenheit', 
                      plot_bgcolor = '#000', 
                      paper_bgcolor = '#000')
    return(fig)

# For graph: 'Mean snow and frost days percent by year with trendline' 
def snow_trend(agg_df):
    fig = go.Figure()
    frost_fit = etl.lin_reg_fit(agg_df, 'frost_day')
    snow_fit = etl.lin_reg_fit(agg_df, 'snow_day')
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = frost_fit[0], name = 'Frost Days Trendline', line = dict(color = 'mediumseagreen'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['frost_day'], name = '% Days of frost', mode = 'markers', marker = dict(color = 'mediumseagreen'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = snow_fit[0], name = 'Snow Days Trendline', line = dict(color = 'aqua'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['snow_day'], name = '% Days of snow', mode = 'markers', marker = dict(color = 'aqua'))
    )
    fig.update_xaxes(title = 'Year', 
                     showgrid=False,
                     showline=True, 
                     linewidth=2, 
                     linecolor='white')
    fig.update_yaxes(title = 'Average snow and frost day chance', 
                     showgrid=False, 
                     rangemode="tozero",
                     showline=True, 
                     linewidth=2, 
                     linecolor='white')
    fig.update_layout(title ='Average Snow and Frost Day Chance by Year', 
                      template = "plotly_dark", 
                      legend_title = 'Metrics', 
                      legend_orientation = 'h', 
                      legend_y = -0.2,
                      plot_bgcolor = '#000', 
                      paper_bgcolor = '#000')
    return(fig, frost_fit[1], snow_fit[1], round(frost_fit[0][0],3), round(frost_fit[0][-1],3), round(snow_fit[0][0],3), round(snow_fit[0][-1],3), str(agg_df.index[0]), str(agg_df.index[-1]))

# For graph: 'Mean temperature by year with trendline'
def temp_trend(agg_df):
    fig = go.Figure()
    lin_fit = etl.lin_reg_fit(agg_df, 'avg_mean_temp')
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = lin_fit[0], name = 'Trendline', line = dict(color = 'mediumvioletred'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['avg_max_temp'], name = 'Max Historical Temperature', mode = 'markers', marker = dict(color = 'Red'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['avg_mean_temp'], name = 'Average Historical Temperature', mode = 'markers', marker = dict(color = 'mediumvioletred'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['avg_min_temp'], name = 'Min Historical Temperature', mode = 'markers', marker = dict(color = 'Blue'))
    )
    fig.update_xaxes(title = 'Year', 
                     showgrid=False,
                     showline=True, 
                     linewidth=2, 
                     linecolor='white')
    fig.update_yaxes(title = 'Average mean temperature in Fahrenheit', 
                     showgrid=False,
                     showline=True, 
                     linewidth=2, 
                     linecolor='white')
    fig.update_layout(title ='Average Mean Temperature by Year', 
                      template = "plotly_dark", 
                      legend_title = 'Metrics', 
                      legend_orientation = 'h', 
                      legend_y = -0.2,
                      plot_bgcolor = '#000', 
                      paper_bgcolor = '#000')
    return(fig, lin_fit[1], round(lin_fit[0][0],1), round(lin_fit[0][-1],1))

# For graph: 'Radiation by month'
def radiation_graph(df):
    fig = px.line(df, x = 'time', y = 'sunlight_minutes')
    fig.update_traces(line_color='goldenrod', 
                      line_width=5)
    fig.update_xaxes(title = 'Day of Year', 
                     showgrid=False, 
                     type = 'date', 
                     showline=True, 
                     linewidth=2, 
                     linecolor='white')
    fig.update_yaxes(title = 'Minutes of Sunlight', 
                     showgrid=False, 
                     rangemode="tozero",
                     showline=True, 
                     linewidth=2, 
                     linecolor='white')
    fig.update_layout(title ='Sunlight by Day of Year', 
                      template = "plotly_dark", 
                      legend_title = 'Metrics', 
                      legend_orientation = 'h', 
                      plot_bgcolor = '#000', 
                      paper_bgcolor = '#000')
    return(fig)


