from fasthtml.common import *
from monsterui.all import *
import ast

app,rt  = fast_app(hdrs=Theme.blue.headers())

status_categories = ['Not Started', 'In Progress', 'Blocked by Client', 'Internal Review', 'Client Review', 'Counterparty Review', 'Out for Signature', "Archive"]

client_names = ['AnswerDotAI', 'Fastai', 'Dunder Mifflin'] 
task_categories = ['Project', 'Hourly', 'Pro Bono', 'Other']

# Setup database
db = Database('kanban.db')
todos = db.t.todos
# if not IS_PROD: todos.drop()
if todos not in db.t:
    todos.create(id=int, client_name=str, task_name=str, task_description=str, status=str, url=str, name=str, task_category=str, 
                 owner=str, collaborators=str, notifiers=str, pk='id')
Todo = todos.dataclass()

# Setup app
app, rt = fast_app(hdrs=Theme.blue.headers())

def tid(id): return f'todo-{id}'

@patch
def __ft__(self:Todo):
    delete = Button('delete', hx_delete=delete_todo.to(id=self.id), hx_target=f'#{tid(self.id)}', 
                    hx_swap='outerHTML', cls=ButtonT.danger, hx_confirm='Are you sure you want to delete this todo?')
    edit =   Button('edit',   hx_get   =edit_todo.  to(id=self.id), hx_target=f'#{tid(self.id)}', 
                    hx_swap='outerHTML', cls=ButtonT.primary)

    status_category = Select(*map(lambda s: Option(s, value=s, selected=s==self.status), status_categories), id='status_category', name='status_category',
                               hx_trigger='change', post=update_status,
                               hx_target='#todo-kanban', hx_vals=f'{{"id": "{self.id}"}}')

    def create_owner_labels(vals):
        parsed_vals = [o.split('@')[0] for o in ast.literal_eval(vals)]
        return map(Label,parsed_vals)

    return Card(DivLAligned(Strong("Owner: "),*create_owner_labels(self.owner)),
        DivFullySpaced(
            H4(A(self.task_name, target_id='current-todo', href=self.url, target="_blank", cls='underline')),
            P(self.client_name, cls=TextFont.muted_sm)),
        A(self.task_description, href=self.url, target="_blank", cls=TextFont.muted_lg),
        DivLAligned(P("Collaborators: ", cls=TextFont.muted_sm),*create_owner_labels(self.collaborators)),
        DivLAligned(P("Notifiers: ", cls=TextFont.muted_sm),*create_owner_labels(self.notifiers)),
        id=tid(self.id),
        footer=DivFullySpaced(edit,delete,status_category,cls='space-x-2'))

# Create/edit todo form
def create_input_field(name: str, todo, input_fn=Input, hidden: bool = False) -> Input:
    return input_fn(id=f'new-{name}',name=name,value=getattr(todo, name, None), 
                 placeholder=' '.join(word.title() for word in name.split('_')), hidden=hidden)

_default_todo = Todo(client_name=None, status="Not Started", task_name=None, task_description=None, url=None, id=None)
def mk_todo_form(todo=_default_todo):
    """Create a form for todo creation/editing with optional pre-filled values"""
    _create_input_field = lambda name: create_input_field(name, todo)

    def _select_option(c, todo_item):
        return Option(c, value=c, selected=c==str(todo_item))

    inputs = [UkSelect(*map(lambda x: _select_option(x,todo.client_name), client_names), 
                    id='new-client_name', name='client_name', placeholder='Select Client')]
    inputs += [UkSelect(*map(lambda x: _select_option(x, todo.task_category), task_categories), 
                    id='new-task_category', name='task_category', placeholder='Select Task Category')]
    inputs += list(map(_create_input_field, ['task_name', 'url']))

    # User tagging
    users = list(r['name'] for r in db['users'].rows)
    def _un_select_option(c, todo_item):
        return Option(c.split('@')[0], value=c, selected=c in str(todo_item))

    user_tagging = [UkSelect(*map(lambda x: _un_select_option(x, todo.owner), users), 
                             id='new-owner', name='owner', placeholder='Select Owner', multiple=True),
                    UkSelect(*map(lambda x: _un_select_option(x, todo.collaborators), users), 
                             id='new-collaborators', name='collaborators', placeholder='Select Collaborators', multiple=True),
                    UkSelect(*map(lambda x: _un_select_option(x, todo.notifiers), users), 
                             id='new-notifiers', name='notifiers', placeholder='Select Notifiers', multiple=True)]

    inputs.append(Select(*map(lambda s: Option(s, value=s, selected=s==todo.status), status_categories), id=f'new-status', name='status'))
    if todo.id: inputs.append(Input(id='new-id', name='id', value=todo.id, hidden=True))
        
    return Form(Grid(*inputs),Grid(*user_tagging),TextArea(todo.task_description, id='new-task_description', name='task_description'),
        Button("Create/Modify Task", cls=ButtonT.primary+'w-full', post=upsert_todo,hx_target='#todo-list'),
        id='todo-input', cls='space-y-3 mb-6', hx_swap_oob='true')

# Index page
@rt
async def index(sess):
    sess['user_name'] = unqid()
    return Container(mk_todo_form(), Divider(),
                     Div(mk_todo_list(sess['user_name']),id='todo-list'),
                     Details(Summary(H1("Archived Todos")),mk_archive_list()))

# Upsert todo
@rt
async def upsert_todo(request, todo:Todo, sess): # owners: List[str]
    form = await request.form()
    todo.owner = form.getlist('owner[]') 
    todo.collaborators = form.getlist('collaborators[]')
    todo.notifiers = form.getlist('notifiers[]')
    print("Owners:", todo.owner)
    print("Collaborators:", todo.collaborators)
    print("Notifiers:", todo.notifiers)
    
    print("I made it into the route.")
    if not todo.status: todo.status = "Not Started"
    todos.insert(todo,replace=True)
    return mk_todo_list(sess['user_name']),mk_todo_form()

def mk_archive_list(): return Grid(*todos(where="status='Archive'"), id='archive-list', cols=1)

def mk_todo_list(user_name):
    un_filtered_todos = f"lower(owner) LIKE '%{user_name.lower()}%' OR lower(collaborators) LIKE '%{user_name.lower()}%' OR lower(notifiers) LIKE '%{user_name.lower()}%'"
    def mk_status_card(status): 
        return Card(*todos(where=f"status='{status}' and ({un_filtered_todos})"), header=H3(status), body_cls='space-y-2')
    return Div(Grid(*[mk_status_card(status) for status in status_categories if status != "Archive"], cols_max=3),id='todo-kanban')

@app.delete
async def delete_todo(id:int):
    try: todos.delete(id)
    except NotFoundError: pass

@rt
async def update_status(id:int, status_category:str, sess):
    todo = todos.get(id)
    todo.status = status_category
    todos.update(todo)
    return Div(mk_todo_list(sess['user_name'])),Div(mk_archive_list()(id='archive-list',hx_swap_oob=f'outerHTML:#archive-list'))

@rt 
async def edit_todo(id:int): return Card(mk_todo_form(todos.get(id)))


serve()
