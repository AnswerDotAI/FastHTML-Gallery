from fasthtml.common import *
from dataclasses import dataclass

app, rt = fast_app()

@dataclass
class Contact:
    name: str
    email: str
    status: str = 'Active'

# Initial data store
contacts = {
    "joe@smith.org": Contact("Joe Smith", "joe@smith.org"),
    "angie@macdowell.org": Contact("Angie MacDowell", "angie@macdowell.org"),
    "fuqua@tarkenton.org": Contact("Fuqua Tarkenton", "fuqua@tarkenton.org"),
    "kim@yee.org": Contact("Kim Yee", "kim@yee.org", "Inactive"),
}

def make_toast(activated: int, deactivated: int):
    return Div(
        Span(
            f"Activated {activated} and deactivated {deactivated} users",
            id="toast",
            aria_live="polite",
            style="background: #E1F0DA; padding: 5px 10px; border-radius: 4px; "
                  "display: inline-block; margin: 10px 0; opacity: 1; "
                  "transition: opacity 1s ease-out;"
        ),
        _script="""
        setTimeout(function() {
            document.getElementById('toast').style.opacity = '0';
        }, 2000);
        """
    )

@rt
def index():
    def make_row(contact):
        return Tr(
            Td(contact.name),
            Td(contact.email),
            Td(Input(type="checkbox", name=f"active:{contact.email}",
                    checked=True if contact.status == "Active" else False))
        )

    return Div(
        H3("Select Rows And Activate Or Deactivate Below"),
        Form(
            Table(
                Thead(Tr(map(Th, ("Name", "Email", "Active")))),
                Tbody(*(make_row(c) for c in contacts.values()))
            ),
            Input(type="submit", value="Bulk Update", cls="btn primary",
                  style="background: #0d6efd; color: white; border: none; "
                        "padding: 8px 16px; border-radius: 4px; cursor: pointer; "
                        "margin: 10px 0;"),
            Div(id="toast-container", style="min-height: 40px;"),
            id="checked-contacts",
            hx_post="/users",
            hx_target="#toast-container",
            hx_swap="innerHTML",
            style="text-align: center;"
        )
    )

@rt("/users")
def post(form_data):
    active_emails = {k[7:] for k in form_data.keys() if k.startswith('active:')}
    activated = deactivated = 0

    for email, contact in contacts.items():
        if email in active_emails and contact.status != "Active":
            contact.status = "Active"
            activated += 1
        elif email not in active_emails and contact.status != "Inactive":
            contact.status = "Inactive"
            deactivated += 1

    return make_toast(activated, deactivated)

serve()
