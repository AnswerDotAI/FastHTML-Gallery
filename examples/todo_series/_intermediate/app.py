from fasthtml.common import *
from datetime import date,datetime
from monsterui.core import *

# fast_app is doing a lot of work here.
# It creates a table in the database if it doesn't exist with columns id and title making id the primary key
# it returns a connector object todos
# it returns a model class Todo
app, rt, todos, Todo= fast_app('intermediate_todo.db',hdrs=Theme.slate.headers(),
                               id=int,title=str,done=bool,due=date,pk='id')

def tid(id): return f'todo-{id}'

def mk_input(**kw):
    return  Form(DivLAligned(
                Input(id='new-title',name='title',placeholder='New Todo',required=True,  **kw),
                Input(id='new-done', name='done',value=False, hidden=True, **kw),
                Input(id='new-due',  name='due', value=date.today(),       **kw),
                Button("Add",cls=ButtonT.primary, post=insert_todo,
                       hx_target='#todo-list',hx_swap='innerHTML')), 
                id='todo-input', cls='mb-6')

def mk_todo_list(): return Grid(*todos(order_by='due'), cols=1)

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
    style = Del if self.done else Strong
    
    _targets = {'hx_target':f'#{tid(self.id)}', 'hx_swap':'outerHTML'}

    done = CheckboxX(checked=self.done,
                    hx_get=toggle_done.to(id=self.id).lstrip('/'),
                    **_targets)
    delete = Button('delete', 
                    hx_delete=delete_todo.to(id=self.id).lstrip('/'),
                    **_targets)
    
    edit = Button('edit',
                    hx_get=edit_todo.to(id=self.id).lstrip('/'),
                    **_targets)
    
    return Card(DivLAligned(done, 
                            style(Strong(self.title, target_id='current-todo')), 
                            P(style(due_date),cls=TextFont.muted_sm),edit,delete),
                id=tid(self.id))

@rt
async def index():
    return Titled('Todo List',mk_input(),Div(mk_todo_list(),id='todo-list'))

@rt 
async def insert_todo(todo:Todo):
    if todo.title.strip(): todos.insert(todo,replace=True)
    return mk_todo_list(),mk_input()(hx_swap_oob='true',hx_target='#todo-input',hx_swap='outerHTML')

@rt 
async def toggle_done(id:int):
    return todos.update(Todo(id=id, done=not todos[id].done))

@rt 
async def edit_todo(id:int):
    todo = todos.get(id)
    return  Card(Form(DivLAligned(
                Input(id='new-title',name='title',value=todo.title,required=True),
                Input(id='new-id',  name='id', value=todo.id,hidden=True),
                Input(id='new-done', name='done',value=todo.done, hidden=True),
                Input(id='new-due',  name='due', value=todo.due),
                Button("Save",cls=ButtonT.primary, post=insert_todo,
                       hx_target='#todo-list',hx_swap='innerHTML')), 
                id='todo-input', cls='mb-6'))
serve()
