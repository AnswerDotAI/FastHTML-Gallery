from fasthtml.common import *

app, rt = fast_app()

# This represents the data we are rendering
# The data could original from a database, or any other datastore
@dataclass
class Contact:
    # Data points
    id: int
    name: str
    email: str
    status: str

    def __ft__(self):
        # __ft__ method is used by FastHTML to render an item in the UI
        # By defining this, a `Contact` will show up as a table row automatically
        return Tr(
            *map(Td, (self.name, self.email, self.status)),
            Td(Button('Delete', 
                      hx_delete=delete.to(id=self.id).lstrip('/'),
                      # Give a confirmation prompt before deleting
                      hx_confirm="Are you sure?", 
                      # Target the closest row (The one you clicked on)
                      hx_target="closest tr", 
                      # Removes the row with htmx
                      hx_swap="delete")))

# Sample data
# Often this would come from a database
contacts = [{'id':1, 'name': "Bob Deer",  'email': "bob@deer.org",  'status': "Active"  },
            {'id':2, 'name': "Jon Doe",   'email': "Jon@doe.com",   'status': "Inactive"},
            {'id':3, 'name': "Jane Smith",'email': "jane@smith.com",'status': "Active"  }]

@rt
def index(sess):
    # Save a copy of contacts in your session
    # This is the demo doesn't conflict with other users
    sess['contacts'] = contacts
    # Create initial table
    return Table(
        Thead(Tr(*map(Th, ["Name", "Email", "Status", ""]))),
        # A `Contact` object is rendered as a row automatically using the `__ft__` method 
        Tbody(*(Contact(**x) for x in sess['contacts'])))

@app.delete
def delete(id: int, sess):
    sess['contacts'] = [c for c in sess['contacts'] if c['id'] != id]

serve()
