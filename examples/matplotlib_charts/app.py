from fh_matplotlib import matplotlib2fasthtml
from fasthtml.common import * 
import numpy as np
import matplotlib.pylab as plt

links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
]

app, rt = fast_app(hdrs=links)

@matplotlib2fasthtml
def generate_chart(num_points):
    plotdata = [np.random.exponential(1) for _ in range(num_points)]
    plt.plot(range(len(plotdata)), plotdata)

def homepage():
    return Div(
        Div(id="chart"),
        Input(
            type="range",
            min="1",
            max="10",
            value="1",
            hx_get="/matplotlib_charts/update_charts",
            hx_target="#chart",
            name='slider',
        )
    )


@app.get("/")
def home():
    return homepage()

@app.get("/update_charts")
def update_chart(slider: int):
    return Div(
        generate_chart(slider),
        P(f"Number of data points: {slider}")
    )

serve()