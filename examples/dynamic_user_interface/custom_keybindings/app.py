from fasthtml.common import fast_app, Div, Button

app, rt = fast_app()


@rt("/")
def homepage():
    return Div(render_button("DO IT (Shift + u)"))


@rt("/doit")
def doit():
    return Div(render_button("😀 DID IT! "))


def render_button(text):
    return Button(
        text,
        hx_trigger="click, keyup[key=='U'] from:body",
        hx_post="/dynamic_user_interface/custom_keybindings/doit/",
    )
