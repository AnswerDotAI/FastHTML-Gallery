from uuid import uuid4
from fasthtml.common import *

app, rt = fast_app()

def render_table(rows, next_page=1):
    return Div(
        Table(
            Tr(Th("Name"), Th("Email"), Th("ID")),
            *rows,
            style="margin: 0 auto;"
        ),
        Button("Load More...", 
            hx_get="/more",
            hx_include="[name='page']",
            hx_target="previous tbody",
            hx_swap="beforeend",
            onclick="document.querySelector('[name=page]').value++"),
        Input(type="hidden", name="page", value=next_page)
    )

def get_row(page: int):
    return Tr(Td(f"Agent Smith {page}"), Td(f"smith{page}@matrix.com"), Td(uuid4()))

@rt("/")
def get():
    initial_rows = [get_row(1)]
    return Div(
        H1("Click to Load"),
        P("Dynamically add rows to a table using HTMX."),
        render_table(initial_rows),
        style="text-align: center;",
    )

@rt("/more")
def get(page: int):
    return get_row(page)

serve()
