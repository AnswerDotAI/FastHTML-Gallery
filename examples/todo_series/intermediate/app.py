from fasthtml.common import *
from datetime import date,datetime
from fh_frankenui.core import *

# fast_app is doing a lot of work here.
# It creates a table in the database if it doesn't exist with columns id and title making id the primary key
# it returns a connector object todos
# it returns a model class Todo
app, rt, todos, Todo= fast_app(
    '::memory::',id=int,title=str,done=bool,due=date,pk='id',hdrs=Theme.slate.headers())

def tid(id): return f'todo-{id}'

def mk_input(**kw):
    return  Form(DivLAligned(
                Input(id='new-title',name='title',placeholder='New Todo', **kw),
                Input(id='new-done',name='done',hidden=True,value=False, **kw),
                Input(id='new-due',name='due',value=date.today(), **kw),
                Button("Add",post=insert_todo,hx_target='#todo-list',hx_swap='innerHTML')), id='todo-input')

def mk_todo_list():
    return Ul(*todos(order_by='due'))

@app.delete("/delete_todo", name='delete_todo')
async def delete_todo(id:int):
    try: todos.delete(id)
    except NotFoundError: pass

# patch is a decorator that patches the __ft__ method of the Todo class
# this is used to customize the html representation of the Todo object
@patch
def __ft__(self:Todo):

    dd = datetime.strptime(self.due, '%Y-%m-%d').date()
    due_date = Strong(dd.strftime('%Y-%m-%d'),style= "" if date.today() <= dd else "background-color: red;")
        
    show = Strong(self.title, target_id='current-todo')

    style = Del if self.done else Strong
    
    done = CheckboxX(checked=self.done,
                    hx_get=toggle_done.to(id=self.id).lstrip('/'),
                    hx_target=f'#{tid(self.id)}',
                    hx_swap='outerHTML')
    delete = Button('delete',
               hx_delete=delete_todo.to(id=self.id).lstrip('/'),
               hx_target=f'#{tid(self.id)}',
               hx_swap='outerHTML',cls=ButtonT.danger)
    
    return Card(DivLAligned(done, style(show), P(style(due_date),cls=TextFont.muted_sm),delete),id=tid(self.id))

@rt
async def index():
    return Titled('Todo List'),mk_input(),Div(mk_todo_list(),id='todo-list')

@rt 
async def insert_todo(todo:Todo):
    todos.insert(todo)
    return mk_todo_list(),mk_input()(hx_swap_oob='true',hx_target='#todo-input',hx_swap='outerHTML')

@rt 
async def toggle_done(id:int):
    return todos.update(Todo(id=id, done=not todos[id].done))

serve()
