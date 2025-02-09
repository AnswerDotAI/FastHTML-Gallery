from fasthtml.common import *
from fasthtml.components import Div

htmx = Script(src='https://unpkg.com/htmx.org@1.9.6/dist/htmx.min.js')
app, rt = fast_app(hdrs=[htmx])

data = [
    {'id': 1, 'name': 'Alice', 'age': 25},
    {'id': 2, 'name': 'Bob', 'age': 30},
    {'id': 3, 'name': 'Charlie', 'age': 28},
]

@rt 
def index():
    rows = []
    for item in data:
        rows.append(
            Tr(
                Td(str(item['id'])),
                Td(Input(value=item['name'], name=f"name{item['id']}", _id=f"name{item['id']}")),
                Td(Input(value=str(item['age']), name=f"age{item['id']}", _id=f"age{item['id']}")),
            )
        )
    return Div(
        Form(
            Table(
                Tr(Th('ID'), Th('Name'), Th('Age')),
                *rows
            ),
            Button('Bulk Update', hx_post="update", hx_target='#response', hx_indicator="#loading", _type="button")
        ),
        Div(id='response'),
        Div(id="loading", style="display:none;", _class="loader"),
    )


@rt
async def update(request):
    changes = []
    form_data = await request.form()

    for item in data:
        new_name = form_data.get(f"name{item['id']}")
        new_age = form_data.get(f"age{item['id']}")

        if new_name != item['name'] or new_age != str(item['age']):
            changes.append(f"Row {item['id']} changed: Name {item['name']} → {new_name}, Age {item['age']} → {new_age}")
            item['name'] = new_name
            item['age'] = int(new_age)

    return Div(*[Div(change) for change in changes]) if changes else Div("No changes detected")

serve()