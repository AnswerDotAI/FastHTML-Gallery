
from fasthtml.common import *

app, rt = fast_app()

@dataclass
class Contact:
    id: int
    name: str
    email: str
    status: str

    def __ft__(self):
        return Tr(
            Td(self.name),
            Td(self.email),
            Td(self.status),
            Td(
                Button(
                    'Delete',
                    cls="btn danger",

                    hx_delete=delete.to(id=self.id).lstrip('/'),
                    # hx_delete=f"{}/delete/{self.id}"
                )
            ),
            id=f"row-{self.id}"
        )

# Sample data
SAMPLE_DATA = [
    Contact(1, "Angie MacDowell", "angie@macdowell.org", "Active"),
    Contact(2, "John Doe", "john@doe.com", "Inactive"),
    Contact(3, "Jane Smith", "jane@smith.com", "Active"),
]
contacts = SAMPLE_DATA

# Main Table
@rt
def index():
    # Repopulating the contacts after refresh
    contacts = SAMPLE_DATA
    return Table(
        Thead(
            Tr(
                Th("Name"), Th("Email"), Th("Status"), Th("")
            )
        ),
        Tbody(
            *(c for c in contacts),
            hx_confirm="Are you sure?",
            hx_target="closest tr",
            hx_swap="outerHTML swap:1s"
        ),
        cls="table delete-row-example"
    )


# Delete Route
@app.delete("/delete", name='delete')
def delete(id: int):
    global contacts
    contacts = [c for c in contacts if c.id != id]
    return ''  # Return empty content to remove the row