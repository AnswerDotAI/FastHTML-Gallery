from fasthtml.common import *
from ui_examples import show_code, FastHTML_Gallery_Standard_HDRS


app, rt = fast_app(hdrs=FastHTML_Gallery_Standard_HDRS())
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
            Button('Click To Edit', cls='uk-button uk-button-primary'),
            post='form', hx_swap='outerHTML')

contacts = [Contact('Joe', 'Blow', 'joe@blow.com')]

@app.get('/')
@show_code
def homepage(): return contacts[0]

@app.post('/form', name='form')
def form(c:Contact):
    def item(k,v): return Div(Label(k), Input(name=v, value=getattr(c,v)))
    return Form(
        *(item(v,k) for k,v in flds.items()),
        Button('Submit', cls='uk-button uk-button-primary', name='btn', value='submit'),
        Button('Cancel', cls='uk-button uk-button-default', name='btn', value='cancel'),
        post="contact", hx_swap='outerHTML'
    )

@app.post('/contact', name='contact')
def contact(c:Contact, btn:str):
    if btn=='submit': contacts[0] = c
    return contacts[0]

