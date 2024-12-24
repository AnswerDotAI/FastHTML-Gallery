from fasthtml.common import *

app,rt = fast_app()

def mk_row(name, email):
    return Tr(Td(name), Td(email)),

@rt
def index():
    return Div(H2("Contacts"),
        Table(
            Thead(Tr(map(Th, ("Name",   "Email")))),
            Tbody(
                mk_row("Audrey", "mommy@example.com"),
                mk_row("Uma"   , "kid@example.com"),
                mk_row("Daniel", "daddy@example.com")), 
            id="contacts-table"),
        H2("Add a Contact"),
        Form(
            Label("Name",  Input(name="name",  type="text")),
            Label("Email", Input(name="email", type="email")),
            Button("Save"),
            # When button is clicked run contacts route/function
            post=contacts,
            # Send the results of contacts to #contacts-table
            hx_target="#contacts-table",
            # Add the new row to the end of the target
            hx_swap="beforeend",
            # Reset the form
            hx_on__after_request="this.reset()"))

@rt
def contacts(name:str,email:str):
    print(f"Adding {name} and {email} to table")
    return mk_row(name,email)

serve()
