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
            Button('Click To Edit'),
            post='form', hx_swap='outerHTML')

contacts = [Contact('Joe', 'Blow', 'joe@blow.com')]

@rt
def index(): return contacts[0]

@rt
def form(c:Contact):
    def item(k,v): return Div(Label(k), Input(name=v, value=getattr(c,v)))
    return Form(
        *(item(v,k) for k,v in flds.items()),
        Button('Submit', name='btn', value='submit'),
        Button('Cancel', name='btn', value='cancel'),
        post="contact", hx_swap='outerHTML'
    )

@rt
def contact(c:Contact, btn:str):
    if btn=='submit': contacts[0] = c
    return contacts[0]

