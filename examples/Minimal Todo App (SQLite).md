# Minimal Todo App (SQLite)

> A minimal todo app using SQLite backend.

# Minimal Todo App (SQLite)

This project is a web-based implementation of a minimal todo app built using FastHTML, HTMX, and SQLite.

## Key Technologies and Techniques

1. **FastHTML**: A Python-based framework for building web applications with a focus on web fundamentals.
2. **HTMX**: Used to create dynamic server-side content updates that let you interact with the app without page reloads.
3. **SQLite**: A lightweight, serverless database used to store and manage todo items.
4. **FastSQL**: A library that simplifies database operations and integrates well with FastHTML.

## How It Works

### Server-Side Logic

The app uses FastHTML to define routes and handle todo list operations. Key routes include:

- `GET /`: The main page that renders the initial todo list.
- `POST /`: Handles adding new todo items.
- `DELETE /{id}`: Handles deleting todo items.

### Data Management

Todo items are stored in an SQLite database:

- `todos`: A table storing todo items with `id` and `title` fields.

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

## Implementation

```python
from fasthtml.common import *
from fastsql import *
from sqlite_minutils.db import NotFoundError

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
```
