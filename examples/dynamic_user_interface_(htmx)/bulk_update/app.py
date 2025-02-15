from fasthtml.common import *
from collections import defaultdict

app, rt = fast_app()

default_data = [
    {'id': 1, 'name': 'Alice', 'age': 25},
    {'id': 2, 'name': 'Bob', 'age': 30},
    {'id': 3, 'name': 'Charlie', 'age': 28},
]

data = defaultdict(lambda: [dict(d) for d in default_data])

@rt 
def index(session):
    # if no id, create one so diff users changes don't conflict
    if not session.get('id'): session['id'] = unqid()
    
    # Create a table based on the current users data
    rows = []
    for item in data[session['id']]:
        rows.append(
            Tr(Td(str(item['id'])),
               Td(Input(value=item['name'],    name=f"name{item['id']}", _id=f"name{item['id']}")),
               Td(Input(value=str(item['age']), name=f"age{item['id']}", _id=f"age{item['id']}"))))
    
    return Div(
        Form(
            Table(
                Thead(Tr(map(Th, ('ID', 'Name', 'Age')))),
                Tbody(*rows)),
            # Bulk update button that submits all inputs from the table because it's inside fot form.
            Button('Bulk Update', hx_post="update", hx_target='#response', hx_indicator="#loading", _type="button", hx_vals={'id': session['id']})),
        
        # Response div that will be updated with the result of the bulk update
        Div(id='response'),
        # Loading indicator that will be shown when the bulk update is happening
        Div(id="loading", style="display:none;", _class="loader"))

@rt
async def update(request, id:str):
    changes = []
    form_data = await request.form()

    # Iterate over the items in the users data
    for item in data[id]:
        # Get the new name and age from the form data
        new_name = form_data.get(f"name{item['id']}")
        new_age  = form_data.get(f"age{item['id']}")

        # Check if the item has changed and if so add it to the changes list
        if new_name != item['name'] or new_age != str(item['age']):
            changes.append(f"Row {item['id']} changed: Name {item['name']} → {new_name}, Age {item['age']} → {new_age}")
            item['name'] = new_name
            item['age'] = int(new_age)
    
    # Return the changes or a message if there are no changes
    return Div(*[Div(change) for change in changes]) if changes else Div("No changes detected")

serve()