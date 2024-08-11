from fasthtml.common import *
from fastsql import *
from sqlite_minutils.db import NotFoundError

app,rt,todos,Todo = fast_app(
    'data/todos.db',
    id=int, title=str, pk='id')

def tid(id): return f'todo-{id}'

@patch
def __ft__(self:Todo):
    show = Strong(self.title, target_id='current-todo')
    delete = A('delete',
               hx_delete=f'/start_simple/sqlite_todo/app/{self.id}', 
               hx_target=f'#{tid(self.id)}',
               hx_swap='outerHTML')
    return Li(show, ' | ', delete, id=tid(self.id))

def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)

nav = Nav()(
    Div(cls="container")(
        Div(cls="grid")(
            H1("FastHTML Gallery"),
            Div(cls="grid")(
                A("Back to Gallery", cls="outline", href="/", role="button" ),
                A("Info", cls="secondary", href="/start_simple/sqlite_todo/info", role="button"),
                A("Code", href="/start_simple/sqlite_todo/code", role="button")))))

@app.get("/")
async def homepage():
    add =  Form(Group(mk_input(), Button("Add")), 
                hx_post="/start_simple/sqlite_todo/app/", target_id='todo-list', hx_swap="beforeend")
    card = Card(Ul(*todos(), id='todo-list'), header=add, footer=Div(id='current-todo')),
    title = 'Todo list'
    return Title(title), Main(nav, H1(title), card, cls='container')

@rt("/")
async def post(todo:Todo): return todos.insert(todo), mk_input(hx_swap_oob='true')

@rt("/{id}")
async def delete(id:int): 
    try: todos.delete(id)
    except NotFoundError: pass # If someone else deleted it already we don't have to do anything
