from fasthtml.common import *
app, rt = fast_app()
flds = dict(firstName='First Name', lastName='Last Name', email='Email')

@dataclass
class Contact:
    firstName:str; lastName:str; email:str; edit:bool=False
    def __ft__(self):
        def item(k, v):
            val = getattr(self,v)
            return Div(Label(Strong(k), val), Hidden(val, id=v))
        return Form(
            *(item(v,k) for k,v in flds.items()),
            Button('Click To Edit', cls='btn btn-primary'),
            hx_post='/dynamic_user_interface/click_to_edit/form', hx_swap='outerHTML')

contacts = [Contact('Joe', 'Blow', 'joe@blow.com')]

@app.get('/')
def homepage(): return contacts[0]

@rt('/form')
def post(c:Contact):
    def item(k,v): return Div(Label(k), Input(name=v, value=getattr(c,v)))
    return Form(
        *(item(v,k) for k,v in flds.items()),
        Button('Submit', cls='btn btn-primary', name='btn', value='submit'),
        Button('Cancel', cls='btn btn-secondary', name='btn', value='cancel'),
        hx_put='/dynamic_user_interface/click_to_edit/contact', hx_swap='outerHTML'
    )

@rt('/contact')
def put(c:Contact, btn:str):
    if btn=='submit': contacts[0] = c
    return contacts[0]

