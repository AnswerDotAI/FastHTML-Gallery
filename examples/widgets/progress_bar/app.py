from fasthtml.common import *
import random

app, rt = fast_app()

def get_randomInt():
    return random.randint(0, 100)

@rt('/')
def get():
    return (
        H1("showcasing progressbar"),
        Progress(
            _id="progress_number",
            value="32",
            max="100"
        ),
        Button(
            "click me",
            hx_get='/refresh_progressbar_number',
            hx_target="#progress_number"
        )
    )

@rt('/refresh_progressbar_number', methods=['GET'])
def refresh_progressbar_number():
    new_value = get_randomInt()
    return Progress(
                    id="progress_number",
                    value=new_value,
                    max="100",
                    hx_swap_oob="true"
                   )