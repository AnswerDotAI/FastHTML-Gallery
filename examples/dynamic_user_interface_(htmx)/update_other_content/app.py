from fasthtml.common import *

app,rt = fast_app()

def mk_row(name, email):
    return Tr(Td(name), Td(email)),

@rt
def index():
    return Div(
            H2("Contacts"),
            Table(
                Thead(Tr(Th("Name"), Th("Email"))),
                Tbody(
                    Tr(Td("Audrey"), Td("mommy@example.com")),
                    Tr(Td("Uma"), Td("kid@example.com")),
                    Tr(Td("Daniel"), Td("daddy@example.com"))), 
                id="contacts-table",
                cls="table"),
            H2("Add a Contact"),
            Form(
                Label("Name", Input(name="name", type="text")),
                Label("Email", Input(name="email", type="email")),
                Button("Save"),
                hx_post="/contacts",
                hx_target="#contacts-table",
                hx_swap="beforeend",
                hx_on__after_request="this.reset()"
            ),
            id="table-and-form"
        )

@rt
def contacts(name:str,email:str):
    print(f"Adding {name} and {email} to table")
    return mk_row(name,email)

serve()