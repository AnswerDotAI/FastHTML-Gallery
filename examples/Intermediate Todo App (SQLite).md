# Intermediate Todo App (SQLite)

> An intermediate todo app using SQLite backend.

# Intermediate Todo App (SQLite)

This project is a web-based implementation of an intermediate todo app built using FastHTML, HTMX, and SQLite. This builds on the minimal todo app by adding a due date and a done field to todos. Functionality related to these new fields has been added to the app. 

## Key Technologies and Techniques

1. **FastHTML**: A Python-based framework for building web applications with a focus on web fundamentals.
2. **HTMX**: Used to create dynamic server-side content updates that let you interact with the app without page reloads.
3. **SQLite**: A lightweight, serverless database used to store and manage todo items.
4. **FastSQL**: A library that simplifies database operations and integrates well with FastHTML.
5. **MonsterUI**: A library that creates modern UI components for FastHTML

## How It Works

### Server-Side Logic

The app uses FastHTML to define routes and handle todo list operations. Key routes include:

- `GET /`: The main page that renders the initial todo list.
- `POST /`: Handles adding new todo items.
- `DELETE /{id}`: Handles deleting todo items.

### Data Management

Todo items are stored in an SQLite database:

- `todos`: A table storing todo items with `id`, `title`, `done`, and `due`fields.

### Dynamic Content

HTMX is used to create a dynamic user interface:

- `hx-post` attribute on the form triggers a POST request to add new todos.
- `hx-delete` attribute on delete links triggers DELETE requests to remove todos.
- `hx-target` specifies where the response from the server should be inserted.
- `hx-swap` determines how the new content should be added or replaced.
    + `beforeend`: Adds the new content at the end of the target element.  This is used to add the new list item to end of the todo list.
    + `outerHTML`: Replaces the entire target element with the new content.  This is used to replaces the todo list item completely with `None` to remove it from the list.

### Key Features

1. **Add Todo**: Users can add new todos using a form at the top of the list.
2. **Delete Todo**: Each todo item has a delete link to remove it from the list.
3. **Real-time Updates**: The list updates dynamically without full page reloads.
4. **Persistent Storage**: Todos are stored in an SQLite database for data persistence.
5. **Due Date**: Each todo item has a due date field and the list is sorted by due date. If the item is past due the date is displayed in red.
6. **Done**: Each todo item has a done field. Items can be marked as done and the list shows completed items crossed out.
7. **MonsterUI**: Simple styling is done using the MonsterUI library.
8. **Edit Todo**: Each todo item has an edit link to edit the item. The edit form is displayed in a card and the todo list is updated with the new values.


## Implementation

```python
from fasthtml.common import *
from datetime import date,datetime
from monsterui.core import *

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
                            style(P(due_date,cls=TextFont.muted_sm)),
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

```
