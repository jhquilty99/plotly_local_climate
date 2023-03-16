import etl 
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# For graph: 'Mean temperature and snowfall chance by month'
def temp_snow(df, monthly_agg_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Violin(x = df['month'], y = df['temperature_2m_mean'], name = 'Historical mean temperatures'),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x = monthly_agg_df.index, y = monthly_agg_df['snow_day'], name = 'Chance of snow fall'),
        secondary_y=True
    )
    fig.add_hrect(y0=-10, y1=32, 
                annotation_text="Freezing Temperatures", annotation_position="top right",  
                annotation_font_size=11,
                annotation_font_color="White",
                fillcolor="blue", opacity=0.25, line_width=0)
    fig.update_xaxes(categoryorder='category ascending', title = 'Month')
    fig.update_yaxes(title = 'Temperature in Fahrenheit', secondary_y=False)
    fig.update_yaxes(title = 'Snow Day Chance', secondary_y=True)
    fig.update_layout(title = 'Mean Temperature and Snowfall Chance by Month', legend_title = 'Metrics', legend_orientation = 'h', plot_bgcolor = '#000', paper_bgcolor = '#000')
    return(fig)

# For graphs: 'Mean temperature heatmap by day and month', and 'Mean temperature heatmap by year and month'
def heatmap_temp(df, by = ['year','month']):
    fig = go.Figure()
    heatmap = df.groupby(by = by).apply(lambda x: x['temperature_2m_mean'].mean())
    heatmap = heatmap.reset_index(name = 'values')
    fig.add_trace(
        go.Heatmap(x = heatmap[by[0]], y = heatmap[by[1]], z = heatmap['values'], name = 'Historical radiation')
    )
    fig.update_xaxes(categoryorder='category ascending', title = by[0].capitalize())
    fig.update_yaxes(categoryorder='category descending', title = by[1].capitalize())
    fig.update_layout(title = f'Mean Temperature by {by[0].capitalize()} and {by[1].capitalize()}', legend_title = 'Temperature in Fahrenheit', legend_orientation = 'h', plot_bgcolor = '#000', paper_bgcolor = '#000')
    return(fig)

# For graph: 'Mean snow and frost days percent by year with trendline' 
def snow_trend(agg_df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = etl.lin_reg_fit(agg_df, 'frost_day')[0], name = 'Frost Days Trendline', line = dict(color = 'Orange'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['frost_day'], name = '% Days of frost', mode = 'markers', marker = dict(color = 'Orange'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = etl.lin_reg_fit(agg_df, 'snow_day')[0], name = 'Snow Days Trendline', line = dict(color = 'Blue'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['snow_day'], name = '% Days of snow', mode = 'markers', marker = dict(color = 'Blue'))
    )
    fig.update_xaxes(title = 'Year')
    fig.update_yaxes(title = 'Average snow and frost day chance')
    fig.update_layout(title ='Average Snow and Frost Day Chance by Year', legend_title = 'Metrics', legend_orientation = 'h', plot_bgcolor = '#000', paper_bgcolor = '#000')
    return(fig)

# For graph: 'Mean temperature by year with trendline'
def temp_trend(agg_df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = etl.lin_reg_fit(agg_df, 'avg_mean_temp')[0], name = 'Trendline', line = dict(color = 'Red'))
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['avg_mean_temp'], name = 'Average Historical Temperature', mode = 'markers', marker = dict(color = 'Red'))
    )
    fig.update_xaxes(title = 'Year')
    fig.update_yaxes(title = 'Average mean temperature in Fahrenheit')
    fig.update_layout(title ='Average Mean Temperature by Year', legend_title = 'Metrics', legend_orientation = 'h', plot_bgcolor = '#000', paper_bgcolor = '#000')
    return(fig)

# For graph: 'Mean snow and frost day chance by month with frost date line'
def frost_line(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Violin(x = df['month'], y = df['frost_day'], name = 'Percent Frost Days'),
        secondary_y=False
    )
    fig.add_trace(
        go.Violin(x = df['month'], y = df['snowfall_sum'], name = 'Snow Fall'),
        secondary_y=True
    )
    fig.update_xaxes(title = 'Month')
    fig.update_yaxes(title = 'Average snow and frost day chance')
    fig.update_layout(title ='Average Snow and Frost Day Chance by Month', legend_title = 'Metrics', legend_orientation = 'h', plot_bgcolor = '#000', paper_bgcolor = '#000')
    return(fig)


