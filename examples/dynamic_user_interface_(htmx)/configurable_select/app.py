from fasthtml.common import *
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.blue.headers())

@rt 
def index(): return Container(H1('Configurable Select'), mk_form())

@rt
def mk_form(add_option:str=None, options:str='isaac,hamel,curtis'):
    opts = options.split(',')
    if add_option: opts.append(add_option)

    return Form(
        # fh-frankenui helper that adds both a form label and input
        # and does proper linking with for, id, and name automatically
        LabelInput("Add an Option", id="add_option"),
        Button("Add"), 
        # fh-frankenui select allows for search boxes
        Select(map(Option, opts), searchable=True), 
        # When the "Add" button is pressed, make a new form
        get=mk_form,
        # Store options state in DOM
        hx_vals={"options": ','.join(opts)}, 
        # Replace the whole form
        hx_swap="outerHTML")

serve()
