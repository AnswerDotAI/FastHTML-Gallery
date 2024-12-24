from fasthtml.common import *
from fastsql import *
from apswutils.db import NotFoundError

app,rt,todos,Todo = fast_app(
    'data/todos.db',
    id=int, title=str, pk='id')

def tid(id): return f'todo-{id}'


@app.delete("/delete_todo", name='delete_todo')
async def delete_todo(id:int): 
    try: todos.delete(id)
    except NotFoundError: pass # If someone else deleted it already we don't have to do anything

@patch
def __ft__(self:Todo):
    show = Strong(self.title, target_id='current-todo')
    delete = A('delete',
               hx_delete=delete_todo.to(id=self.id).lstrip('/'), 
               hx_target=f'#{tid(self.id)}',
               hx_swap='outerHTML')
    return Li(show, ' | ', delete, id=tid(self.id))

def mk_input(**kw):
    return Input(
        id="new-title", name="title", placeholder="New Todo",required=True,**kw
    )

@rt
async def index():
    add =  Form(Group(mk_input(), Button("Add")), 
                post="insert_todo", target_id='todo-list', hx_swap="beforeend")
    card = Card(Ul(*todos(), id='todo-list'), header=add, footer=Div(id='current-todo')),
    title = 'Todo list'
    return Title(title), Main(H1(title), card, cls='container')

@rt
async def insert_todo(todo:Todo):
    if not todo.title.strip():
        return  mk_input(hx_swap_oob='true')
    return todos.insert(todo), mk_input( hx_swap_oob='true')

serve()
