from fasthtml.common import * 

app, rt = fast_app()

@rt
def index():return Titled(
    "Custom Keybindings with HTMX",
    render_button("DO IT (Press `Shift + u`)"))

@rt
def doit(): return render_button("😀 DID IT! ")

def render_button(text):
    return Button(text, 
                  hx_trigger="click, keyup[key=='U'] from:body", 
                  get=doit)

serve()
