from fasthtml.common import *

links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
]

app, rt = fast_app(hdrs=links)
    
def homepage():
    return Div(H1("Hello, world!"))

@rt('/')
def get():
    return homepage()