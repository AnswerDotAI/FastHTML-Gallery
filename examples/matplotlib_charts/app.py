from fh_matplotlib import matplotlib2fasthtml
from fasthtml.common import * 
import numpy as np
import matplotlib.pylab as plt

links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
]

app, rt = fast_app(hdrs=links)

count = 0
plotdata = []

@matplotlib2fasthtml
def generate_chart():
    global plotdata
    plt.plot(range(len(plotdata)), plotdata)


def homepage():
    return Div(Div(f"You have pressed the button {count} times.", id="chart"),
        Button("Increment", hx_get="/matplotlib_charts/increment", hx_target="#chart", hx_swap="innerHTML"))

@app.get("/")
def home():
    return homepage()

@app.get("/increment/")
def increment():
    global plotdata, count
    count += 1
    plotdata.append(np.random.exponential(1))
    return Div(
        generate_chart(),
        P(f"You have pressed the button {count} times."),
    )

serve()