from fasthtml.common import *
from fasthtml.svg import *
from fasthtml.components import Script

app, rt = fast_app(live=True, hdrs=[Script(src="https://d3js.org/d3.v7.min.js")])

@app.get('/')
def homepage():
    return Div(
        NotStr('''<script>
                    window.onload = function() {
                        var svg = d3.select("svg");
                        var dragHandler = d3.drag()
                            .on("start", function (e) {
                                var current = d3.select(this);
                                deltaX = current.attr("x") - e.x;
                                deltaY = current.attr("y") - e.y;})
                            .on("drag", function (e) {
                                d3.select(this)
                                    .attr("x", e.x+deltaX)
                                    .attr("y", e.y+deltaY);});
                        svg.select("#rect").call(dragHandler);}
               </script>'''),
        P("Simple example to show clicking and dragging an SVG rectangle with D3"),
        Svg(viewBox="0 0 200 200",id="svg-box")(
            Rect(x=5,y=5,width=10,height=10,fill="red",id="rect")
        ),
    )

serve()