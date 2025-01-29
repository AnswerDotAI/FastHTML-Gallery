from fasthtml.common import *
import numpy as np
from starlette.responses import JSONResponse

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
    pico=False,
    hdrs=(
        Script(src="https://cdn.jsdelivr.net/npm/d3@7"),
        Script(src="https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6"),
        Script(src="https://unpkg.com/@tailwindcss/browser@4")
    )
)

@rt
def index():
    return Div(
        H1("Observable Plot Demo", cls="text-4xl font-bold"),
        P("This FastHTML example renders an ", A("Observable Plot", href="https://observablehq.com/@observablehq/plot", target="_blank", cls="visited:text-purple-600 underline"), " chart. The data is randomly generated on the server and is fetched on initial page load. You can also click the button to fetch new random data from the server. Try opening the browser tab and viewing the Network tab to see the data reponse for each http request.", cls="my-4"),
        Button("Refresh Data", hx_get="get_data", hx_target="#data-store", cls="cursor-pointer rounded-md bg-slate-600 px-3.5 py-2.5 my-2 text-sm font-semibold text-white shadow-xs hover:bg-slate-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-600"),
        # Store for the JSON chart data
        Div(id="data-store", hx_get="get_data", hx_trigger="load", cls="hidden"),
        # Plot container
        Div(id="plot", cls="mt-12"),
        # Include the JavaScript for the plot
        Script(plot_js),
        cls="m-12"
    )

@rt
def get_data():
    # Generate sample data
    data = [{"value": float(x)} for x in np.random.randn(100)]
    # Return as proper JSON response
    return JSONResponse(data)

serve()
