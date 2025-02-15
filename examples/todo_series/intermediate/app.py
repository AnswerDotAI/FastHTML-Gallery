from fasthtml.common import *
from datetime import date,datetime
from monsterui.all import *

# fast_app is doing a lot of work here.
# It creates a table in the database if it doesn't exist with columns id and title making id the primary key
# it returns a connector object todos
# it returns a model class Todo
app, rt, todos, Todo= fast_app('intermediate_todo.db',hdrs=Theme.slate.headers(),
                               title=str,done=bool,due=date, id=int,pk='id')

def tid(id): return f'todo-{id}'

# Render all the todos ordered by todo due date
def mk_todo_list():  return Grid(*todos(order_by='due'), cols=1)

@app.delete
async def delete_todo(id:int):
    "Delete if it exists, if not someone else already deleted it so no action needed"
    try: todos.delete(id)
    except NotFoundError: pass
    # Because there is no return, the todo will be swapped with None and removed from UI

# patch is a decorator that patches the __ft__ method of the Todo class
# this is used to customize the html representation of the Todo object
@patch
def __ft__(self:Todo):
    # Set color to red if the due date is passed
    dd = datetime.strptime(self.due, '%Y-%m-%d').date()
    due_date = Strong(dd.strftime('%Y-%m-%d'),style= "" if date.today() <= dd else "background-color: red;") 

    # Action Buttons
    _targets = {'hx_target':f'#{tid(self.id)}', 'hx_swap':'outerHTML'}
    done   = CheckboxX(       hx_get   =toggle_done.to(id=self.id).lstrip('/'), **_targets, checked=self.done), 
    delete = Button('delete', hx_delete=delete_todo.to(id=self.id).lstrip('/'), **_targets)
    edit   = Button('edit',   hx_get   =edit_todo  .to(id=self.id).lstrip('/'), **_targets)
    
    # Strike through todo if it is completed
    style = Del if self.done else noop
    
    return Card(DivLAligned(done, 
                            style(Strong(self.title, target_id='current-todo')), 
                            style(P(due_date,cls=TextPresets.muted_sm)),
                            edit,
                            delete),
                id=tid(self.id))

@rt
async def index():
    "Main page of the app"
    return Titled('Todo List',mk_todo_form(),Div(mk_todo_list(),id='todo-list'))

@rt 
async def upsert_todo(todo:Todo):
    # Create/update a todo if there is content
    if todo.title.strip(): todos.insert(todo,replace=True)
    # Reload main page with updated database content
    return mk_todo_list(),mk_todo_form()(hx_swap_oob='true',hx_target='#todo-input',hx_swap='outerHTML')

@rt 
async def toggle_done(id:int):
    "Reverses done boolean in the database and returns the todo (rendered with __ft__)"
    return todos.update(Todo(id=id, done=not todos[id].done))


def mk_todo_form(todo=Todo(title=None, done=False, due=date.today(), id=None), btn_text="Add"):
    """Create a form for todo creation/editing with optional pre-filled values"""
    inputs = [Input(id='new-title', name='title',value=todo.title, placeholder='New Todo'),
              Input(id='new-done',  name='done', value=todo.done,  hidden=True),
              Input(id='new-due',   name='due',  value=todo.due)]

    # If there is an ID use it for editing existing row in db
    if todo.id: inputs.append(Input(id='new-id', name='id', value=todo.id, hidden=True))
        
    return Form(DivLAligned(
        *inputs,
        Button(btn_text, cls=ButtonT.primary, post=upsert_todo,hx_target='#todo-list', hx_swap='innerHTML')),
        id='todo-input', cls='mb-6')

@rt 
async def edit_todo(id:int): return Card(mk_todo_form(todos.get(id), btn_text="Save"))

serve()
