from fasthtml.common import *
from datetime import date,datetime
from fh_frankenui.core import *


db = database('advanced_todo.db')
todos,users = db.t.todos,db.t.users
if todos not in db.t:
    users.create(dict(name=str), pk='name')
    todos.create(id=int, title=str, status=str, due=date, name=str, pk='id')
Todo,User = todos.dataclass(),users.dataclass()
login_redir = RedirectResponse('/login', status_code=303)

def before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    todos.xtra(name=auth)

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login'])

app, rt = fast_app(hdrs=Theme.slate.headers(),before=bware)

def tid(id): return f'todo-{id}'

def mk_input(**kw):
    return  Form(Grid(min_cols=3)(
                Input(id='new-title',name='title',placeholder='New Todo',  **kw),
                Input(id='new-status', name='status',value="Not Started", hidden=True, **kw),
                Input(id='new-due',  name='due', value=date.today(),       **kw),
                Button("Add",cls=ButtonT.primary, post=insert_todo,
                       hx_target='#todo-list',hx_swap='innerHTML')), 
                id='todo-input', cls='mb-6')

# def mk_todo_list(): return Grid(*todos(order_by='due'), cols=1)

def mk_todo_list():
    def is_old(due):
        dd = datetime.strptime(due, '%Y-%m-%d').date()
        return date.today() <= dd
    date_cards = []
    for td in todos(select="distinct due",order_by='due',where="status != 'Archive'"):
        new_card = [Card(*todos(where=f"due='{td.due}' and status='Not Started'"),header="Not Started",body_cls='space-y-2',cls=CardT.default if is_old(td.due) else CardT.danger, id=f'new-{td.due}')]
        inprogress_card = [Card(*todos(where=f"due='{td.due}' and status='In Progress'"),header="In Progress",body_cls='space-y-2',cls=CardT.default if is_old(td.due) else CardT.danger, id=f'inprogress-{td.due}')]
        done_cards = [Card(*todos(where=f"due='{td.due}' and status='Done'"),header="Done",body_cls='space-y-2',cls=CardT.default if is_old(td.due) else CardT.danger, id=f'done-{td.due}')]
    
        date_cards.append(Card(Grid(min_cols=3)(*new_card,*inprogress_card,*done_cards),header=td.due))

    # date_cards = [Card(*todos(where=f"due='{td.due}'"),header=td.due,body_cls='space-y-2',cls=CardT.default if is_old(td.due) else CardT.danger) for td in todos(select="distinct due",order_by='due')]
    return Div(*date_cards,id='todo-dates')

@app.delete("/delete_todo", name='delete_todo')
async def delete_todo(id:int):
    try: todos.delete(id)
    except NotFoundError: pass

# patch is a decorator that patches the __ft__ method of the Todo class
# this is used to customize the html representation of the Todo object
@patch
def __ft__(self:Todo):
    
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
    
    return Card(DivLAligned(Strong(self.title, target_id='current-todo'), 
                            edit,delete,status),
                id=tid(self.id))

@rt
async def index():
    logout = Button("Logout",cls=ButtonT.primary, hx_get="/logout", hx_target='body') 
    return Titled('Todo List',logout,mk_input(),Div(mk_todo_list(),id='todo-list'))

@rt 
async def insert_todo(todo:Todo):
    todos.insert(todo,replace=True)
    return mk_todo_list(),mk_input()(hx_swap_oob='true',hx_target='#todo-input',hx_swap='outerHTML')

@rt 
async def toggle_done(id:int):
    return todos.update(Todo(id=id, done=not todos[id].done))

@rt 
async def update_status(id:int):
    todo = todos.get(id)
    next_status = {"Not Started": "In Progress", "In Progress": "Done", "Done": "Archive"}
    next_target = {"Not Started": "inprogress", "In Progress": "done", "Done": "archive"}
    print(f'beforeend:#{next_target[todo.status]}-{todo.due}')
    return Div(todos.update(Todo(id=id, status=next_status[todo.status])))(hx_swap_oob=f'beforeend:#{next_target[todo.status]}-{todo.due}')

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
