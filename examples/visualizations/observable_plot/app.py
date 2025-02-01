from fasthtml.common import *
import numpy as np

plot_js = """
function createPlot(data) {
    const plot = Plot.rectY(data, Plot.binX({y: "count"},{x: d => d.value,fill:"steelblue"})).plot();
    const div = document.querySelector("#plot");
    div.replaceChildren(plot);
}

// Set up initial load via HTMX
htmx.on('htmx:afterSettle', evt => {
    if (evt.detail.target.id === 'data-store') {
        // The data is now properly JSON-encoded
        const data = JSON.parse(evt.detail.target.textContent);
        createPlot(data);
    }
});
"""

app, rt = fast_app(
    hdrs=(Script(src="https://cdn.jsdelivr.net/npm/d3@7"),
          Script(src="https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6")))

@rt
def index():
    return Div(
        Section(
            H1(A("Observable", href="https://observablehq.com/@observablehq/plot", target="_blank"), " Plot Demo"),
            P("The data is randomly generated on the server and is fetched on initial page load."),
            P("Try opening the browser developer tools and viewing the Network tab to see the data reponse for each http request."),
            # On bytton click it sends a get request to the `get_data` route and puts the response in the `data-store` div 
            Button("Fetch New Data", get=get_data, hx_target="#data-store")),
        # Store for the JSON chart data
        Div(id="data-store", get=get_data, hx_trigger="load", hidden=True),
        # Plot container
        Div(id="plot"),
        # Include the JavaScript for the plot
        Script(plot_js)
        )

@rt
def get_data():
    # Generate sample data
    data = [{"value": float(x)} for x in np.random.randn(100)]
    # Return as proper JSON response
    return JSONResponse(data)

serve()
