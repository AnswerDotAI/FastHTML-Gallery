from fasthtml.common import *
from datetime import date,datetime
from fh_frankenui.core import *


db = database('advanced_todo.db')
todos,users = db.t.todos,db.t.users
if todos not in db.t:
    users.create(dict(name=str), pk='name')
    todos.create(id=int, title=str, description=str, status=str, due=date, name=str, pk='id')
Todo,User = todos.dataclass(),users.dataclass()
login_redir = RedirectResponse('/login', status_code=303)

def before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    todos.xtra(name=auth)

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login'])

app, rt = fast_app(hdrs=(SortableJS('.sortable'),Theme.slate.headers()),before=bware)

def tid(id): return f'todo-{id}'

def mk_todo_form(todo=Todo(title=None, status="Not Started", due=date.today(), description=None, id=None), btn_text="Add"):
    """Create a form for todo creation/editing with optional pre-filled values"""
    inputs = [Input(id='new-title', name='title',value=todo.title, placeholder='New Todo'),
              Input(id='new-status',  name='status', value=todo.status,  hidden=True),
              Input(id='new-due',   name='due',  value=todo.due),
              Input(id='new-description',  name='description', placeholder="Task Description")]

    # If there is an ID use it for editing existing row in db
    if todo.id: inputs.append(Input(id='new-id', name='id', value=todo.id, hidden=True))
        
    return Form(DivLAligned(
        *inputs,
        Button(btn_text, cls=ButtonT.primary, post=upsert_todo,hx_target='#todo-list', hx_swap='innerHTML')),
        id='todo-input', cls='mb-6')



def mk_archive_list(): return Grid(*todos(order_by='due',where="status='Archive'"), cols=1)

def mk_todo_list():
    new_cards = Card(*todos(where=f"status='Not Started'"),header="Not Started",body_cls='space-y-2 sortable', id=f'new')
    inprogress_cards = Card(*todos(where=f"status='In Progress'"),header="In Progress",body_cls='space-y-2 sortable', id=f'inprogress')
    done_cards = Card(*todos(where=f"status='Done'"),header="Done",body_cls='space-y-2 sortable', id=f'done')

    return Div(Grid(min_cols=3)(new_cards,inprogress_cards,done_cards),id='todo-kanban')


@app.delete("/delete_todo", name='delete_todo')
async def delete_todo(id:int):
    try: todos.delete(id)
    except NotFoundError: pass

# patch is a decorator that patches the __ft__ method of the Todo class
# this is used to customize the html representation of the Todo object
@patch
def __ft__(self:Todo):
    def is_old(due):
        dd = datetime.strptime(due, '%Y-%m-%d').date()
        return date.today() <= dd
    
    _targets = {'hx_target':f'#{tid(self.id)}', 'hx_swap':'outerHTML'}

    delete = Button('delete', 
                    hx_delete=delete_todo.to(id=self.id).lstrip('/'),
                    **_targets)
    
    edit = Button('edit',
                    hx_get=edit_todo.to(id=self.id).lstrip('/'),
                    **_targets)
    
    next_status = {"Not Started": "Start", "In Progress": "Complete", "Done": "Archive", "Archive": "Archive"}
    status = Button(next_status[self.status],
                    hx_post=update_status.to(id=self.id).lstrip('/'),hx_swap='delete',hx_target=f'#{tid(self.id)}')
    due_date = Strong(self.due)

    
    return Card(DivLAligned(Strong(self.title, target_id='current-todo'),due_date),
                id=tid(self.id),cls= CardT.default if is_old(self.due) else CardT.danger,footer=DivLAligned(edit,delete,status))

@rt
async def index():
    logout = Button("Logout",cls=ButtonT.primary, hx_get="/logout", hx_target='body') 
    return Titled(
        'Todo List',
        logout,
        mk_todo_form(),
        Div(mk_todo_list(),id='todo-list'),
        Details(Summary(H1("Archived Todos")),mk_archive_list()(id='archive-list')))


@rt 
async def upsert_todo(todo:Todo):
    # Create/update a todo if there is content
    if todo.title.strip(): todos.insert(todo,replace=True)
    # Reload main page with updated database content
    return mk_todo_list(),mk_todo_form()(hx_swap_oob='true',hx_target='#todo-input',hx_swap='outerHTML')

@rt 
async def toggle_done(id:int):
    return todos.update(Todo(id=id, done=not todos[id].done))

@rt 
async def update_status(id:int):
    todo = todos.get(id)
    next_status = {"Not Started": "In Progress", "In Progress": "Done", "Done": "Archive"}
    next_target = {"Not Started": "inprogress", "In Progress": "done", "Done": "archive-list"}
    
    # return Div(todos.update(Todo(id=id, status=next_status[todo.status])))(hx_swap_oob=f'beforeend:#{next_target[todo.status]}')

    todos.update(Todo(id=id, status=next_status[todo.status]))
    return Div(mk_todo_list())(hx_swap_oob=f'outerHTML:#todo-kanban')
@rt 
async def edit_todo(id:int): return Card(mk_todo_form(todos.get(id), btn_text="Save"))

@rt("/login")
def get():
    frm = Form(
        Input(id='name', placeholder='Name'),
        Button('login'),
        action='/login', method='post')
    return Titled("Login", frm)

@dataclass
class Login: name:str

@rt("/login")
def post(login:Login, sess):
    if not login.name: return login_redir
    try: u = users[login.name]
    except NotFoundError: u = users.insert(login)
    sess['auth'] = u.name
    return RedirectResponse('/', status_code=303)

@rt("/logout")
def logout(sess):
    del sess['auth']
    return login_redir
serve()
