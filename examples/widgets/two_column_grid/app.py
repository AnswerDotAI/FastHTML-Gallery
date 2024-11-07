from fasthtml.common import *

app, rt = fast_app()

@rt
def index():
    return Titled('Try editing fields:', 
        Grid(Div(
            Form(post="submit", hx_target="#result", hx_trigger="input delay:200ms")(
                Select(Option("One"), Option("Two"), id="select"),
                Input(value='j', id="name", placeholder="Name"),
                Input(value='h', id="email", placeholder="Email"))),
            Div(id="result")))

@rt
def submit(d:dict):
    return Div(*[Div(P(Strong(k),':  ',v)) for k,v in d.items()])

serve()