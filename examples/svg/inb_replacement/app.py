from fasthtml.common import *
from fasthtml.svg import *

app, rt = fast_app()

def mk_shape(shape):
    if shape == "circle":
        return Circle(cx=15, cy=15, r=10, fill="red")(hx_get="mk/rect",hx_swap="outerHTML")
    elif shape == "rect":
        return Rect(x=10, y=10, width=10, height=10, fill="blue")(hx_get="mk/circle",hx_swap="outerHTML")

@rt
def index():
    return Div(
        P("Click the object to swap it with another shape"),
        Svg(viewBox="0 0 150 100")(
            mk_shape("rect")))

@rt("/mk/{shape}")
def get(shape: str):
    return SvgInb(mk_shape(shape),)

serve()
