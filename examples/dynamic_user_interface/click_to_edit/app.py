from fasthtml.common import *
app, rt = fast_app()

def contact_view(firstName: str, lastName: str, email: str, inputs=False):
    if inputs:
        vals = zip(['firstName', 'lastName', 'email'], [firstName, lastName, email])
        firstName, lastName, email = [ Input(type='text', name=o, value=v) for o, v in vals ]
    
    return Div(
        Div(Label(Strong('First Name: '), firstName)),
        Div(Label(Strong('Last Name: '), lastName)),
        Div(Label(Strong('Email: '), email)),
        Button('Click To Edit', 
               hx_get=f'/dynamic_user_interface/click_to_edit/form?firstName={firstName}&lastName={lastName}&email={email}', 
               cls='btn primary'),
        hx_target='this',
        hx_swap='outerHTML'
    )

@app.get('/')
def homepage():
    c = {
        'firstName': 'Joe',
        'lastName': 'Blow',
        'email': 'joe@blow.com'
    }
    return contact_view(**c)


@app.get('/form')
def edit_contact(firstName: str, lastName: str, email: str):
    return Form(
        Div(
            Label('First Name'),
            Input(type='text', name='firstName', value=firstName)
        ),
        Div(
            Label('Last Name'),
            Input(type='text', name='lastName', value=lastName),
        ),
        Div(
            Label('Email Address'),
            Input(type='email', name='email', value=email),
        ),
        Button('Submit', cls='btn'),
        Button('Cancel', hx_get=f'/dynamic_user_interface/click_to_edit/contact?firstName={firstName}&lastName={lastName}&email={email}', cls='btn'),
        hx_put='/dynamic_user_interface/click_to_edit/contact',
        hx_target='this',
        hx_swap='outerHTML'
    )

@app.put('/contact')
def update_contact(firstName: str, lastName: str, email: str):
    return contact_view(firstName, lastName, email)

@app.get('/contact')
def view_contact(firstName: str, lastName: str, email: str):
    return contact_view(firstName, lastName, email)

