from fasthtml.common import *
from datetime import date,datetime
from fh_frankenui.core import *


# You can use any database you want; it'll be easier if you pick a lib that supports the MiniDataAPI spec.
# Here we are using SQLite, with the FastLite library, which supports the MiniDataAPI spec.
db = database('advanced_todo.db')
# The `t` attribute is the table collection. The `todos` and `users` tables are not created if they don't exist.
# Instead, you can use the `create` method to create them if needed.
todos,users = db.t.todos,db.t.users
if todos not in db.t:
    # You can pass a dict, or kwargs, to most MiniDataAPI methods.
    users.create(dict(name=str, pwd=str), pk='name')
    todos.create(id=int, title=str, done=bool, due=date, name=str, pk='id')
# Although you can just use dicts, it can be helpful to have types for your DB objects.
# The `dataclass` method creates that type, and stores it in the object, so it will use it for any returned items.
Todo,User = todos.dataclass(),users.dataclass()

# Any Starlette response class can be returned by a FastHTML route handler.
# In that case, FastHTML won't change it at all.
# Status code 303 is a redirect that can change POST to GET, so it's appropriate for a login page.
login_redir = RedirectResponse('/login', status_code=303)

# The `before` function is a *Beforeware* function. These are functions that run before a route handler is called.
def before(req, sess):
    # This sets the `auth` attribute in the request scope, and gets it from the session.
    # The session is a Starlette session, which is a dict-like object which is cryptographically signed,
    # so it can't be tampered with.
    # The `auth` key in the scope is automatically provided to any handler which requests it, and can not
    # be injected by the user using query params, cookies, etc, so it should be secure to use.
    auth = req.scope['auth'] = sess.get('auth', None)
    # If the session key is not there, it redirects to the login page.
    if not auth: return login_redir
    # `xtra` is part of the MiniDataAPI spec. It adds a filter to queries and DDL statements,
    # to ensure that the user can only see/edit their own todos.
    todos.xtra(name=auth)

# To create a Beforeware object, we pass the function itself, and optionally a list of regexes to skip.
bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login'])
# The `FastHTML` class is a subclass of `Starlette`, so you can use any parameters that `Starlette` accepts.
# In addition, you can add your Beforeware here, and any headers you want included in HTML responses.
# FastHTML includes the "HTMX" and "Surreal" libraries in headers, unless you pass `default_hdrs=False`.
app, rt = fast_app(hdrs=Theme.slate.headers(),before=bware)

def tid(id): return f'todo-{id}'

def mk_input(**kw):
    return  Form(DivLAligned(
                Input(id='new-title',name='title',placeholder='New Todo',  **kw),
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
    
    return Card(DivLAligned(done, 
                            style(Strong(self.title, target_id='current-todo')), 
                            P(style(due_date),cls=TextFont.muted_sm),delete),
                id=tid(self.id))

@rt
async def index():
    logout = Button("Logout",cls=ButtonT.primary, hx_get="/logout") 
    return Titled('Todo List',logout,mk_input(),Div(mk_todo_list(),id='todo-list'))

@rt 
async def insert_todo(todo:Todo):
    todos.insert(todo)
    return mk_todo_list(),mk_input()(hx_swap_oob='true',hx_target='#todo-input',hx_swap='outerHTML')

@rt 
async def toggle_done(id:int):
    return todos.update(Todo(id=id, done=not todos[id].done))

@rt("/login")
def get():
    # This creates a form with two input fields, and a submit button.
    # All of these components are `FT` objects. All HTML tags are provided in this form by FastHTML.
    # If you want other custom tags (e.g. `MyTag`), they can be auto-generated by e.g
    # `from fasthtml.components import MyTag`.
    # Alternatively, manually call e.g `ft(tag_name, *children, **attrs)`.
    frm = Form(
        # Tags with a `name` attr will have `name` auto-set to the same as `id` if not provided
        Input(id='name', placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('login'),
        action='/login', method='post')
    # If a user visits the URL directly, FastHTML auto-generates a full HTML page.
    # However, if the URL is accessed by HTMX, then one HTML partial is created for each element of the tuple.
    # To avoid this auto-generation of a full page, return a `HTML` object, or a Starlette `Response`.
    # `Titled` returns a tuple of a `Title` with the first arg and a `Container` with the rest.
    # See the comments for `Title` later for details.
    return Titled("Login", frm)

# Handlers are passed whatever information they "request" in the URL, as keyword arguments.
# Dataclasses, dicts, namedtuples, TypedDicts, and custom classes are automatically instantiated
# from form data.
# In this case, the `Login` class is a dataclass, so the handler will be passed `name` and `pwd`.
@dataclass
class Login: name:str; pwd:str

# This handler is called when a POST request is made to the `/login` path.
# The `login` argument is an instance of the `Login` class, which has been auto-instantiated from the form data.
# There are a number of special parameter names, which will be passed useful information about the request:
# `session`: the Starlette session; `request`: the Starlette request; `auth`: the value of `scope['auth']`,
# `htmx`: the HTMX headers, if any; `app`: the FastHTML app object.
# You can also pass any string prefix of `request` or `session`.
@rt("/login")
def post(login:Login, sess):
    if not login.name or not login.pwd: return login_redir
    # Indexing into a MiniDataAPI table queries by primary key, which is `name` here.
    # It returns a dataclass object, if `dataclass()` has been called at some point, or a dict otherwise.
    try: u = users[login.name]
    # If the primary key does not exist, the method raises a `NotFoundError`.
    # Here we use this to just generate a user -- in practice you'd probably to redirect to a signup page.
    except NotFoundError: u = users.insert(login)
    # This compares the passwords using a constant time string comparison
    # https://sqreen.github.io/DevelopersSecurityBestPractices/timing-attack/python
    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")): return login_redir
    # Because the session is signed, we can securely add information to it. It's stored in the browser cookies.
    # If you don't pass a secret signing key to `FastHTML`, it will auto-generate one and store it in a file `./sesskey`.
    sess['auth'] = u.name
    return RedirectResponse('/', status_code=303)

# Instead of using `app.route` (or the `rt` shortcut), you can also use `app.get`, `app.post`, etc.
# In this case, the function name is not used to determine the HTTP verb.
@rt("/logout")
def logout(sess):
    del sess['auth']
    return login_redir
serve()
