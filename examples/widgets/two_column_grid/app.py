from fasthtml.common import *
from ui_examples import show_code, FastHTML_Gallery_Standard_HDRS, show_code

app, rt = fast_app(hdrs=FastHTML_Gallery_Standard_HDRS())

@app.get('/')
@show_code
def homepage():
    return Titled('Try editing fields:', Grid(
        Form(post="submit", hx_target="#result", hx_trigger="input delay:200ms")(
            Select(Option("One"), Option("Two"), id="select"),
            Input(value='j', id="name", placeholder="Name"),
            Input(value='h', id="email", placeholder="Email")),
        Div(id="result")
    ))


@app.post('/submit')
def submit(d:dict):
    return Div(*[Div(P(Strong(k),':  ',v)) for k,v in d.items()])
