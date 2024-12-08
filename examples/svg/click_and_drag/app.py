from fasthtml.common import *
from fasthtml.svg import *

app, rt = fast_app(hdrs=[Script(src="https://d3js.org/d3.v7.min.js")])

@rt
def index():
    return Div(
        P("Click and drag an SVG rectangle with D3"),
        Svg(viewBox="0 0 200 200",id="svg-box")(
            Rect(x=5,y=5,width=10,height=10,fill="red",id="rect")),
        Script('''
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
                '''))

serve()
