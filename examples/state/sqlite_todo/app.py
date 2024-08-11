from fasthtml.common import *
from fastsql import *

app,rt,todos,Todo = fast_app(
    '/files/data/todos.db',
    id=int, title=str, pk='id')

def tid(id): return f'todo-{id}'

@patch
def __ft__(self:Todo):
    show = Strong(self.title, target_id='current-todo')
    delete = A('delete',
               hx_delete=f'/state/sqlite_todo/{self.id}', 
               hx_target=f'#{tid(self.id)}',
               hx_swap='outerHTML')
    return Li(show, ' | ', delete, id=tid(self.id))

def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)

@app.get("/")
async def homepage():
    add =  Form(Group(mk_input(), Button("Add")), 
                hx_post="/state/sqlite_todo/", target_id='todo-list', hx_swap="beforeend")
    card = Card(Ul(*todos(), id='todo-list'), header=add, footer=Div(id='current-todo')),
    title = 'Todo list'
    return Title(title), Main(H1(title), card, cls='container')

@rt("/")
async def post(todo:Todo): return todos.insert(todo), mk_input(hx_swap_oob='true')

@rt("/{id}")
async def delete(id:int): todos.delete(id), None
