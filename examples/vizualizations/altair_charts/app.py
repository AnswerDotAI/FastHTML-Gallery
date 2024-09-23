from fh_altair import altair2fasthml, altair_headers
from fasthtml.common import *
import numpy as np
import pandas as pd
import altair as alt
from ui_examples import show_code, hdrs_tailwind_franken_highlightJS_markdownJS

app, rt = fast_app(hdrs=(altair_headers,*hdrs_tailwind_franken_highlightJS_markdownJS))


count = 0
plotdata = []

def generate_chart():
    global plotdata
    if len(plotdata) > 250:
        plotdata = plotdata[-250:]

    pltr = pd.DataFrame({'y': plotdata, 'x': range(len(plotdata))})
    chart = alt.Chart(pltr).mark_line().encode(x='x', y='y').properties(width=400, height=200)
    return altair2fasthml(chart)

@app.get("/")
@show_code
def homepage():
    return Title("Altair Demo"), Main(
        H1("Altair Demo"),
        Div(id="chart"),
        Button("Increment", get=increment, hx_target="#chart", hx_swap="innerHTML", cls='uk-button uk-button-primary'),
        style="margin: 20px"
    )

@app.get("/increment")
def increment():
    global plotdata, count
    count += 1
    plotdata.append(np.random.exponential(1))
    return Div(
        generate_chart(),
        P(f"You have pressed the button {count} times."),
    )
