from fasthtml.common import fast_app, Div, Button, P

app, rt = fast_app()

button_state = False


@rt("/")
def homepage():
    return Div(render_button())


@rt("/toggle")
def toggle():
    global button_state
    button_state = not button_state
    display_style = "block" if button_state else "none"
    return Div(
        render_button(),
        Div(
            P(
                "FastHTML with HTMX lets you easily add custom keyboard shortcuts to your web app. Using the hx_trigger attribute, you can trigger actions like toggling content visibility with key combos, creating dynamic and responsive interfaces without page reloads."
            ),
            id="content",
            style=f"display: {display_style}; text-align: center; margin-top: 10px;",
        ),
    )


def render_button():
    return Button(
        "Press Shift+u To Toggle!",
        hx_trigger="click, keyup[key=='U'] from:body",
        style="background-color: green; color: white; padding: 10px; margin: 10px; border: none;",
        hx_post="/dynamic_user_interface/custom_keybindings/toggle/",
    )
