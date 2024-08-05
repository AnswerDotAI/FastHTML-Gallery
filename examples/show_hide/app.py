from fasthtml.common import *
app, rt = fast_app()

content = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet volutpat tellus, in tincidunt magna. Vivamus congue posuere ligula a cursus. Sed efficitur tortor quis nisi mollis, eu aliquet nunc malesuada. Nulla semper lacus lacus, non sollicitudin velit mollis nec. Phasellus pharetra lobortis nisi ac eleifend. Suspendisse commodo dolor vitae efficitur lobortis. Nulla a venenatis libero, a congue nibh. Fusce ac pretium orci, in vehicula lorem. Aenean lacus ipsum, molestie quis magna id, lacinia finibus neque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas ac ex luctus, dictum erat ut, bibendum enim. Curabitur et est quis sapien consequat fringilla a sit amet purus."""


def homepage():
    return Div(
        Button("Show",
            hx_trigger="click",
            hx_get="/show_hide/toggle?show=True",
            hx_target="#content",
            id="toggle"),
        Div(id="content"))

@rt('/')
def get():
    return homepage()
    
@rt('/toggle')
def get(show: bool):
    if show==1:
        hx_get = "/show_hide/toggle?show=False"
        content_div = Div(content)
    else:
        hx_get="/show_hide/toggle?show=True"
        content_div = Div()

    return Div(
            Div(Button("Hide",hx_trigger="click",
                hx_get=hx_get,hx_target="#content", id="toggle",
                hx_swap_oob="outerHTML:#toggle")),
            content_div)