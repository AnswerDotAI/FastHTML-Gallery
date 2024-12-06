from uuid import uuid4
from fasthtml.common import *

app, rt = fast_app()

agent_num = 0
@rt
def get():
    global agent_num
    agent_num += 1
    return Tr(map(Td, (
        f"Agent Smith {agent_num}",
        f"smith{agent_num}@matrix.com",
        uuid4())))

@rt
def index():
    global agent_num
    agent_num = 0
    first_row = get()
    return Div(
        H1("Click to Load"),
        P("Dynamically add rows to a table using HTMX."),
        Table(Tr(map(Th, ("Name", "Email", "ID"))), first_row, id='tbl'),
        Button("Load More...", get=get, hx_target="#tbl", hx_swap="beforeend"),
        style="text-align: center;")

serve()
