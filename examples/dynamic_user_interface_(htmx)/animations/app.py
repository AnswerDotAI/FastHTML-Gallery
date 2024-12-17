import random
from fasthtml.common import *

app, rt = fast_app(hdrs=(Style("""
    /* CSS to center content of the app */
    body { max-width: 800px; padding: 20px; width: 90%; margin: 0 auto; }
    * { text-align: center; }
        
    /* CSS to fade in to full opacity in 1 second */
    #fade-me-in.htmx-added {
        opacity: 0;
    }
    #fade-me-in {
        opacity: 1;
        transition: opacity 1s ease-out;
    }

    /* CSS to fade out to 0 opacity in 1 second */
    .fade-me-out {
        opacity: 1;
    }
    .fade-me-out.htmx-swapping {
        opacity: 0;
        transition: opacity 1s ease-out;
    }
"""),))


@rt
def color_throb_demo():
    # Each time this route is called it chooses a random color
    random_color = random.choice(['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink'])

    return P("Groovy baby, yeah!", id="color-demo",
        # Make text random color and do a smooth transition
        style=f"color: {random_color}; transition: all 1s ease-in;",
        # Call this route and replace the text every 1 second
        get=color_throb_demo, hx_swap="outerHTML", hx_trigger="every 1s")

# 2. Settling Transitions
@rt
def fade_in_demo():
    return Button( "Fade Me In", id="fade-me-in", class_="btn primary",
                  # hx_trigger defaults to click so we do not have to specify it
                  # When the button is clicked, create a new button with a 1 second settling transition
                  post=fade_in_demo, hx_swap="outerHTML settle:1s")

def in_flight_animation_demo():
    " Create a form that changes its look on click. In this case it displays a 'Submitted!' response. "
    return Form(
        Input(name="name", style="width: 300px;", placeholder="Content field"),
        Button("Submit", class_="btn primary"),
        # When the button is clicked, swap it with the button specified in form_completion_message
        post=form_completion_message, hx_swap="outerHTML")

@rt
def form_completion_message():
    # A button with green background and white text
    return Button("Submitted!", class_="btn primary", 
                  style="background-color: green; color: white;")


# Helper function to create a section for an example
def section(title, desc, content): return Card(H2(title), P(desc), Br(), content, Br())

@rt
def index():
    return Div(
        H1("Text Animations"), Br(),
        section("Color Throb", 
                "Change text color every second in a smooth transition.",
                color_throb_demo()),
        section("Settling Transitions",
                "Make a button disappear on click and gradually fade in.",
                fade_in_demo()),
        section("Request In Flight Animation",
                "Let a form change its look on click. In this case it displays a 'Submitted!' response.",
                in_flight_animation_demo()))

serve()
