import plotly.express as px
from fasthtml.common import *

# Add the Plotly library to the headers
app, rt = fast_app(hdrs=(Script(src="https://cdn.plot.ly/plotly-2.24.1.min.js"),))

def create_scatter_plot():
    # Create simple scatter plot with 5 points
    fig = px.scatter(
        x=[1, 2, 3, 4, 5], y=[2, 4, 1, 3, 5], labels={"x": "X Value", "y": "Y Value"}
    )
    return fig.to_json()

@rt
def index():
    return Titled("Interactive Plotly Selection",
        P("Click any point to see its x-value!"),
        # point-info will be updated based on what is clicked
        Div(id="point-info")(P("No point selected yet")),
        # plotly-container will be updated with the plot
        Div(id="plotly-container"),
        # Initialize the plot
        Script(
            f"""
            // All the plot data is given in json form by `create_scatter_plot`
            const plotData = {create_scatter_plot()};
            // Create the plot with that data in location with id `plotly-container`
            Plotly.newPlot('plotly-container', plotData.data, plotData.layout);

            // Add click event handler
            // Get thing with id `plotly-container`, and on plotly_click event,
            // run the function
            document.getElementById('plotly-container').on('plotly_click', function(data) {{
                // Get the first point clicked
                const point = data.points[0];
                // Make HTMX request when point is clicked with the x-value
                htmx.ajax('GET', `point/${{point.x}}`, {{target: '#point-info'}});
            }});
            """
            ))


@rt("/point/{x_val}")
def get(x_val: float):
    # Return the x-value of the point clicked to the UI!
    return P(Strong(f"You clicked the point with x-value: {x_val}"))

serve()
