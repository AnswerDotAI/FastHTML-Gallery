from fasthtml.common import *

app, rt = fast_app()

content = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet volutpat tellus, in tincidunt magna. Vivamus congue posuere ligula a cursus. Sed efficitur tortor quis nisi mollis, eu aliquet nunc malesuada. Nulla semper lacus lacus, non sollicitudin velit mollis nec. Phasellus pharetra lobortis nisi ac eleifend. Suspendisse commodo dolor vitae efficitur lobortis. Nulla a venenatis libero, a congue nibh. Fusce ac pretium orci, in vehicula lorem. Aenean lacus ipsum, molestie quis magna id, lacinia finibus neque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas ac ex luctus, dictum erat ut, bibendum enim. Curabitur et est quis sapien consequat fringilla a sit amet purus."""

def mk_button(show):
    return Button("Hide" if show else "Show",
        hx_get="toggle?show=" + ("False" if show else "True"),
        hx_target="#content", id="toggle", hx_swap_oob="outerHTML")

@rt
def index():
    return Div(mk_button(False), Div(id="content"))

@rt
def toggle(show: bool):
    return Div(
        Div(mk_button(show)),
        Div(content if show else ''))
