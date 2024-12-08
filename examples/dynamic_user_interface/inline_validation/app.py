from fasthtml.common import *
import re
################
### FastHTML ###
################

app, rt = fast_app()

@rt
def index():
    return Form(post='submit', hx_target='#submit-btn-container', hx_swap='outerHTML')(
                # Calls /email route to validate email
                Div(hx_target='this', hx_swap='outerHTML')(
                    Label(_for='email')('Email Address'),
                    Input(type='text', name='email', id='email', post='email')),
                # Calls /cool route to validate cool
                Div(hx_target='this', hx_swap='outerHTML')(
                    Label(_for='cool')('Is this cool?'),
                    Input(type='text', name='cool', id='cool', post='cool')),
                # Calls /coolscale route to validate coolscale
                Div(hx_target='this', hx_swap='outerHTML')(
                    Label(_for='CoolScale')('How cool (scale of 1 - 10)?'),
                    Input(type='number', name='CoolScale', id='CoolScale', post='coolscale')),
                # Submits the form which calls /submit route to validate whole form
                Div(id='submit-btn-container')(
                    Button(type='submit', id='submit-btn',)('Submit')))

### Field Validation Routing ###
# Validates the field and generates FastHTML with appropriate validation and template function

@rt
def email(email: str): return inputTemplate('Email Address', 'email', email, validate_email(email))

@rt
def cool(cool: str): return inputTemplate('Is this cool?', 'cool', cool, validate_cool(cool))
     
@rt
def coolscale(CoolScale: int): return inputTemplate('How cool (scale of 1 - 10)?', 'CoolScale', CoolScale, validate_coolscale(CoolScale), input_type='number')

@rt
def submit(email: str, cool: str, CoolScale: int):
    # Validates all fields in the form
    errors = {'email': validate_email(email),
             'cool': validate_cool(cool),
             'coolscale': validate_coolscale(CoolScale) }
    # Removes the None values from the errors dictionary (No errors)
    errors = {k: v for k, v in errors.items() if v is not None}
    # Return Button with error message if they exist
    return Div(id='submit-btn-container')(
        Button(type='submit', id='submit-btn', post='submit', hx_target='#submit-btn-container', hx_swap='outerHTML')('Submit'),
        *[Div(error, style='color: red;') for error in errors.values()])

########################
### Validation Logic ###
########################

def validate_email(email: str):
    # Check if email address is a valid one
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(email_regex, email): return "Please enter a valid email address"
    # Check if email address is already taken (in this case only test@test.com will pass)
    elif email != "test@test.com":  return "That email is already taken. Please enter another email (only test@test.com will pass)."
    # If no errors, return None (default of python)

def validate_cool(cool: str):
    if cool.lower() not in ["yes", "definitely"]: return "Yes or definitely are the only correct answers"

def validate_coolscale(CoolScale: int):
    if CoolScale < 1 or CoolScale > 10: return "Please enter a number between 1 and 10"

######################
### HTML Templates ###
######################

def inputTemplate(label, name, val, errorMsg=None, input_type='text'):
    # Generic template for replacing the input field and showing the validation message
    return Div(hx_target='this', hx_swap='outerHTML', cls=f"{errorMsg if errorMsg else 'Valid'}")(
               Label(label), # Creates label for the input field
               Input(name=name,type=input_type,value=f'{val}',post=f'{name.lower()}'), # Creates input field
               Div(f'{errorMsg}', style='color: red;') if errorMsg else None) # Creates red error message below if there is an error

