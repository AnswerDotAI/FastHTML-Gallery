from fasthtml.common import *
links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
]
app, rt = fast_app(hdrs=links)

def homepage():
    return Titled('HTMX Form Demo', Grid(
        Form(hx_post="/two_column_grid/submit", hx_target="#result", hx_trigger="input delay:200ms")(
            Select(Option("One"), Option("Two"), id="select"),
            Input(value='j', type="text", id="name", placeholder="Name"),
            Input(value='h', type="text", id="email", placeholder="Email")),
        Div(id="result")
    ))

@rt('/')
def get():
    return homepage()

@rt('/submit')
def post(d:dict):
    result = []
    for k,v in d.items():
        result.append(Div(P(Strong(k),':   ',v)))
    return Div(*result)