from fasthtml.common import *

app, rt = fast_app()
    
def homepage():
    return Div(H1("Hello, world!"))

@rt('/')
def get():
    return homepage()