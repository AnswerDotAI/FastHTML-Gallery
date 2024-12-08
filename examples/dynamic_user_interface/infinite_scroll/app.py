from fasthtml.common import *
import uuid
column_names = ('name', 'email', 'id')

def generate_contact(id: int) -> Dict[str, str]:
    return {'name': 'Agent Smith',
            'email': f'void{str(id)}@matrix.com',
            'id': str(uuid.uuid4())
            }

def generate_table_row(row_num: int) -> Tr:
    contact = generate_contact(row_num)
    return Tr(*[Td(contact[key]) for key in column_names])

def generate_table_part(part_num: int = 1, size: int = 20) -> Tuple[Tr]:
    paginated = [generate_table_row((part_num - 1) * size + i) for i in range(size)]
    paginated[-1].attrs.update({
        'get': f'page?idx={part_num + 1}',
        'hx-trigger': 'revealed',
        'hx-swap': 'afterend'})
    return tuple(paginated)

app, rt = fast_app()

@rt
def index():
    return Titled('Infinite Scroll',
                  Div(Table(
                      Thead(Tr(*[Th(key) for key in column_names])),
                      Tbody(generate_table_part(1)))))

@rt
def page(idx:int|None = 0):
    return generate_table_part(idx)

