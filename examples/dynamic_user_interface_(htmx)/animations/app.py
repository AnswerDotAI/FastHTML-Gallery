import random
from fasthtml.common import *

app, rt = fast_app(hdrs=(Style("""
    body { max-width: 800px; padding: 20px; width: 90%; margin: 0 auto; }
    * { text-align: center; }
        
    #fade-me-in.htmx-added {
        opacity: 0;
    }
    #fade-me-in {
        opacity: 1;
        transition: opacity 1s ease-out;
    }
    form.htmx-request {
        opacity: .5;
        transition: opacity 300ms linear;
    }
    .fade-me-out {
        opacity: 1;
        background-color: lightblue;
        padding: 10px;
    }
    .fade-me-out.htmx-swapping {
        opacity: 0;
        transition: opacity 1s ease-out;
    }
"""),))


# 1. Color Throb
@rt("/colors")
def colors():
    return Div(
        "Groovy baby, yeah!",
        id="color-demo",
        style=f"color: {random.choice(['red', 'blue', 'green', 'purple', 'orange'])}; transition: all 1s ease-in;",
        hx_get="/colors",
        hx_swap="outerHTML",
        hx_trigger="every 1s"
    )


# 2. Settling Transitions
@rt("/fade_in_demo", methods=["POST"])
def fade_in_demo():
    return Button(
        "Fade Me In",
        id="fade-me-in",
        class_="btn primary",
        hx_post="/fade_in_demo",
        hx_swap="outerHTML settle:1s"
    )

# 3. Request In Flight Animation
def submit_form():
    return Form(
        Input(name="name", style="width: 300px;", placeholder="Content field"),
        Button("Submit", class_="btn primary"),
        hx_post="/name",
        hx_swap="outerHTML"
    )

@rt("/name", methods=["POST"])
def handle_name():
    return Button(
        "Submitted!",
        class_="btn primary",
        style="background-color: green; color: white;"
    )

@rt
def index():
    return Div(
        H1("Text Animations"),
        Br(),
        H2("1. Color Throb"),
        Div("""Change text color every second in a smooth transition."""),
        Br(),
        colors(),
        Br(),
        H2("2. Settling Transitions"),
        Div("""Make a button disappear on click and gradually fade in."""),
        Br(),
        fade_in_demo(),
        Br(),
        Br(),
        H2("3. Request In Flight Animation"),
        Div("""Let a form change its look on click. In this case it displays a 'Submitted!' response."""),
        Br(),
        submit_form(),
    )

serve()
