# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "python-fasthtml",
#   "plotly",
#   "pandas",
# ]
# ///

import plotly.express as px
from fasthtml.common import *

app, rt = fast_app()


def create_scatter_plot():
    # Create simple scatter plot with 5 points
    fig = px.scatter(
        x=[1, 2, 3, 4, 5], y=[2, 4, 1, 3, 5], labels={"x": "X Value", "y": "Y Value"}
    )
    return fig.to_json()


@rt("/")
def get():
    return Titled(
        "Interactive Plotly Selection",
        Div(
            P("Click any point to see its x-value!"),
            Div(id="plotly-container"),
            Div(id="point-info")(P("No point selected yet")),
            Script(src="https://cdn.plot.ly/plotly-2.24.1.min.js"),
            Script(
                f"""
                // Initialize the plot
                const plotData = {create_scatter_plot()};
                Plotly.newPlot('plotly-container', plotData.data, plotData.layout);

                // Add click event handler
                document.getElementById('plotly-container').on('plotly_click', function(data) {{
                    const point = data.points[0];
                    // Make HTMX request when point is clicked
                    htmx.ajax('GET', `/point/${{point.x}}`, {{target: '#point-info'}});
                }});
                """
            ),
        ),
    )


@rt("/point/{x_val}")
def get(x_val: float):
    return P(f"You clicked the point with x-value: {x_val}")


serve()
