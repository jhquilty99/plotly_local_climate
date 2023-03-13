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
    fig.update_layout(template="simple_white")
    fig.add_hrect(y0=-10, y1=32, 
                annotation_text="Freezing Temperatures", annotation_position="top right",  
                annotation_font_size=11,
                annotation_font_color="White",
                fillcolor="blue", opacity=0.25, line_width=0)
    fig.update_xaxes(categoryorder='category ascending')
    return(fig)

# For graphs: 'Mean temperature heatmap by day and month', and 'Mean temperature heatmap by year and month'
def heatmap_temp(df, by = ['year','month']):
    fig = go.Figure()
    heatmap = df.groupby(by = by).apply(lambda x: x['temperature_2m_mean'].mean())
    heatmap = heatmap.reset_index(name = 'values')
    fig.add_trace(
        go.Heatmap(x = heatmap[by[0]], y = heatmap[by[1]], z = heatmap['values'], name = 'Historical radiation')
    )
    fig.update_xaxes(categoryorder='category ascending')
    return(fig)

# For graph: 'Mean snow and frost days percent by year with trendline' 
def snow_trend(agg_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['frost_day'], name = '% Days of frost'),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x = agg_df.index, y = agg_df['snow_day'], name = '% Days of snow'),
        secondary_y=True
    )
    fig.update_layout(template="simple_white")
    return(fig)

# For graph: 'Mean temperature by year with trendline'
def temp_trend(agg_df):
    fig = px.scatter(agg_df, y = 'avg_min_temp', trendline="ols", trendline_color_override="red")
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
    return(fig)


