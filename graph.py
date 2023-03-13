import etl 
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def graph_temp(df, monthly_agg_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Violin(x = df['month'], y = df['temperature_2m_mean'], name = 'Historical mean temperatures'),
        secondary_y=False
    )
    fig.add_trace(
        go.Line(x = monthly_agg_df.index, y = monthly_agg_df['snowfall_chance'], name = 'Chance of snow fall'),
        secondary_y=True
    )
    fig.update_layout(template="simple_white",  title="Monthly Temperature Distributions")
    fig.add_hrect(y0=-10, y1=32, 
                annotation_text="Freezing Temperatures", annotation_position="top right",  
                annotation_font_size=11,
                annotation_font_color="White",
                fillcolor="blue", opacity=0.25, line_width=0)
    return(fig)

def heatmap_temp(df):
    fig = go.Figure()
    heatmap = df.groupby(by = ['year','month']).apply(lambda x: x['temperature_2m_mean'].mean())
    heatmap = heatmap.reset_index(name = 'values')
    fig.add_trace(
        go.Heatmap(x = heatmap.year, y = heatmap.month, z = heatmap['values'], name = 'Historical radiation')
    )
    return(fig)




