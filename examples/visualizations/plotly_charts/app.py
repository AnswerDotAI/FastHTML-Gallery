from fasthtml.common import *
import pandas as pd
import numpy as np
import plotly.express as px
from fh_plotly import plotly2fasthtml, plotly_headers

app, rt = fast_app(hdrs=(plotly_headers,))

y_data = [1, 2, 3, 2]
x_data = [3, 1, 2, 4]

def generate_line_chart():
    df = pd.DataFrame({'y': y_data, 'x': x_data})
    fig = px.line(df, x='x', y='y')
    return plotly2fasthtml(fig)

def generate_bar_chart():
    df = pd.DataFrame({'y': y_data, 'x': ['A', 'B', 'C','D']})
    fig = px.bar(df, x='x', y='y')
    return plotly2fasthtml(fig)

def generate_scatter_chart():
    df = pd.DataFrame({'y': y_data, 'x': x_data, 'size': [10, 20, 30, 40]})
    fig = px.scatter(df, x='x', y='y', size='size')
    return plotly2fasthtml(fig)

def generate_3d_scatter_chart():
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6],
        'y': [7, 8, 6, 9, 7, 8],
        'z': [3, 5, 4, 6, 5, 7]
    })
    fig = px.scatter_3d(df, x='x', y='y', z='z')
    return plotly2fasthtml(fig)

@rt
def index():
    return Div(
        H1("Plotly Interactive Charts Demo with FastHTML"),
        P("Try interacting with the charts by hovering over data points, zooming in and out, panning, rotating (3D), and more!."),
            Div(Div(Strong("Plot 1: Line Chart"),
                    Div(generate_line_chart()),),
                Div(Strong("Plot 2: Bar Chart"),
                    Div(generate_bar_chart()),),
                Div(Strong("Plot 3: Scatter Chart"),
                    Div(generate_scatter_chart()),),
                Div(Strong("Plot 4: 3D Scatter Chart"),
                    Div(generate_3d_scatter_chart()),),
                style="display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 20px; width: 100%; height: 800px;"
            )
    )

serve()
