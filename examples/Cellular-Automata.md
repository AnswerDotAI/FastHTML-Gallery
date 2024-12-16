# Cellular-Automata

> A 1D Cellular Automata using FastHTML

# Cellular Automata
Cellular automata are a class of models used to simulate complex systems. They are used in a wide range of applications, including modeling the spread of diseases, traffic flow, and crowd behavior. This project is a one-dimensional cellular automata.

## Cellular Automata Details

We start with an initial row. In this app, the row is a series of white squares followed by a single black square and more white squares.

A cell is created based on the state of the three cells above it (directly above and to the left and right). That means there are **eight** possible combinations of the three cells. We consider a white square to be a 0 and a black square to be a 1. This gives us a number between 0 and 7 (the cell update number).

The rule is a number between 0 and 255 (inclusive). We take that number and convert it to its binary representation, which will be a sequence of **8**x 0s and 1s. We look at the corresponding digit in the rule by taking the cell update number. If it is a 1, the cell becomes black; if it is a 0, the cell becomes white.

The cellular automata is visualized as a grid of white and black boxes, representing the 0 and 1 states, respectively.

## User Interface

The app provides three main inputs:

- **Rule (0-255):** Determines the cellular automata rule
- **Generations (1-200):** Sets how many rows will be generated
- **Width (1-200):** Defines the width of the grid

## Key Technologies and Techniques

* **HTMX Polling**: We use polling to update the grid every 100ms. This is done by setting the `hx-trigger` attribute `every .1s`. This triggers a GET request until we run out of generations, and then the `Response(status_code=286)` stops the polling.  See the [HTMX documentation for polling](https://htmx.org/docs/#polling)
* **Progress Bar**:  A progress bar that shows the progress of the cellular automata.  Check out the [FastHTML Gallery page for progress bars!](https://gallery.fastht.ml/split/widgets/progress_bar)
* **Show Hide Button**: A button that shows and hides the rule number.  Check out the [FastHTML Gallery page for show hide buttons!](https://gallery.fastht.ml/split/widgets/show_hide)
* **Inline Input Validation**:  Real-time validation for rule number, generations, and width inputs.  Check out the [FastHTML Gallery page for inline validation!](https://gallery.fastht.ml/split/dynamic_user_interface/inline_validation)
+ **Dynamic Grid Generation**: The automata grid is generated row by row, creating an animated effect.
+ **Server-Side Session State**: The state of each in-progress generation is stored on the server by a session ID.

### Server-Side Logic
The app uses FastHTML to define routes and handle the cellular automata logic on the server. Key routes include:

- `/`: The main page that renders the initial form and explanation.
- `/run`: Initializes and runs the cellular automata based on user input.
- `/next`: Generates the next row of the automata.
- `/validate/*`: Handles input validation for rule number, generations, and width.
- `/show_rule`: Toggles the display of the rule visualization.

### State Management
The automata state is managed server-side using a generator function:

- `generator`: A global variable that stores the cellular automata generator for each session.
- `run()`: A yields each automata generation.

### Dynamic Content
HTMX is used extensively to create a dynamic user interface:

- `hx-get` attributes trigger GET requests for various actions, such as running the automata or showing/hiding the rule.
- `hx-post` is used for inline validation of user inputs.
- `hx-target` specifies where the response from the server should be inserted.
- `hx-swap` determines how the new content should replace the old content. Various swap methods are used, including `outerHTML` and `beforeend.`
- `hx-trigger="every .1s"` creates an animation effect by periodically requesting new rows.






## Implementation

```python
from fasthtml.common import *
from starlette.responses import Response
from uuid import uuid4


generator = {}
bindict = {
    (1,1,1):0,
    (1,1,0):1,
    (1,0,1):2,
    (1,0,0):3,
    (0,1,1):4,
    (0,1,0):5,
    (0,0,1):6,
    (0,0,0):7}
initial_row = [0]*50 + [1] + [0]*50
color_map = {0:"white", 1:"black"}

####################
### HTML Widgets ###
####################

explanation = Div(
    H1("Cellular Automata"),
    H4("Input explanations:"),
    Ul(Li(Strong("Rule: "),"Determines the next state of a cell based on the current state of the cell and its neighbors."),
        Li(Strong("Generations: "),"Determines how many generations to run the automaton."),
        Li(Strong("Width: "),"Determines the width of the grid."),))

def progress_bar(percent_complete: float):
    return Div(hx_swap_oob="innerHTML:#progress_bar")(
            Progress(value=percent_complete))

def mk_box(color,size=5):
    return Div(cls="box", style=f"background-color:{color_map[color]};height:{size}px;width:{size}px;margin:0;display:inline-block;")

def mk_row(colors,font_size=0,size=5):
    return Div(*[mk_box(color,size) for color in colors], cls="row",style=f"font-size:{font_size}px;")

def mk_button(show):
    return Button("Hide Rule" if show else "Show Rule",
        hx_get="show_rule?show=" + ("False" if show else "True"),
        hx_target="#rule", id="sh_rule", hx_swap_oob="outerHTML",
        hx_include="[name='rule_number']")

########################
### FastHTML Section ###
########################

app, rt = fast_app()


@rt
def index(sess):
    if 'id' not in sess: sess['id'] = str(uuid4())
    return Title("Cellular Automata"),Main(Div(
        Div(P(explanation,id="explanations")),
        Form(Group(
            Div(hx_target='this', hx_swap='outerHTML')(Label(_for="rule_number", cls="form-label")("Rule"),
                Input(type='number', name="rule_number", id='rule_set', value="30",hx_post='validate/rule_number')),
            Div(hx_target='this', hx_swap='outerHTML')(Label("Generations", cls="form-label"),
                Input(type='number',name="generations", id='generations_set',  value="50",hx_post='validate/generations', hx_indicator='#generationsind')),
            Div(hx_target='this', hx_swap='outerHTML')(Label("Width", cls="form-label"),
                Input(type='number',name="width", id='width_set',  value="100", hx_post='validate/width', hx_indicator='#widthind')), 
            Button(cls="btn btn-active btn-primary", type="submit", hx_get="run", 
                   hx_target="#grid", hx_include="[name='rule_number'],[name='generations'],[name='width']", hx_swap="outerHTML")("Run"))),
        Group(
            Div(style="margin-left:50px")(
                Div(id="progress_bar"),
                Div(id="grid")),
            Div(style="margin-right:50px; max-width:200px")(
                    mk_button(False),
                    Div(id="rule"),
                    ))))

@rt('/show_rule')
def get(rule_number: int, show: bool):
    rule = [int(x) for x in f'{rule_number:08b}']
    return Div(
        Div(mk_button(show)),
        Div(*[Group(
            Div(mk_row(list(k),font_size=10,size=20),style="max-width:100px"), 
            Div(P(" -> "),style="max-width:100px"), 
            Div(mk_box(rule[v],size=20),style="max-width:100px")) for k,v in bindict.items()] if show else '')
    )

@rt('/run')
def get(rule_number: int, generations: int, width: int, sess):

    errors = {'rule_number': validate_rule_number(rule_number),
              'generations': validate_generations(generations),
              'width': validate_width(width)}
    # Removes the None values from the errors dictionary (No errors)
    errors = {k: v for k, v in errors.items() if v is not None}
    # Return Button with error message if they exist
    
    if errors:
        return Div(Div(id="grid"),
                   Div(id="progress_bar",hx_swap_oob="outerHTML:#progress_bar"),
                Div(id='submit-btn-container',hx_swap_oob="outerHTML:#submit-btn-container")(
                    Button(cls="btn btn-active btn-primary", type="submit", 
                           hx_get="run", hx_target="#grid", 
                           hx_include="[name='rule_number'],[name='generations'],[name='width']", hx_swap="outerHTML")("Run"),
                    *[Div(error, style='color: red;') for error in errors.values()]))

    start = [0]*(width//2) + [1] + [0]*(width//2)
    global generator 
    generator[sess['id']] = run(rule=rule_number,generations=generations,start=start)
    return Div(
        Div(style=f"width: {(width+1)*5}px",id="progress_bar",hx_swap_oob="outerHTML:#progress_bar"),
        Div(id="next",hx_trigger="every .1s", hx_get="next", hx_target="#grid",hx_swap="beforeend"),id="grid")

@rt('/next')
def get(sess):
    global generator
    g,val = next(generator[sess['id']],(False,False))
    if val: return Div(
        progress_bar(g),
        mk_row(val))
    else: 
        del generator[sess['id']]
        return Response(status_code=286)

@rt('/validate/rule_number')
def post(rule_number: int): return inputTemplate('Rule Number', 'rule_number',rule_number, validate_rule_number(rule_number))

@rt('/validate/generations')
def post(generations: int): return inputTemplate('Generations', 'generations', generations, validate_generations(generations))

@rt('/validate/width')
def post(width: int): return inputTemplate('Width', 'width', width, validate_width(width))

#########################
### Application Logic ###
#########################

def run(rule=30, start = initial_row, generations = 100):
    rule = [int(x) for x in f'{rule:08b}']
    yield 0, start
    old_row = [0] + start + [0]
    new_row = []
    for g in range(1,generations):
        for i in range(1,len(old_row)-1):
            key=tuple(old_row[i-1:i+2])
            new_row.append(rule[bindict[key]])
        yield (g+1)/generations,new_row
        old_row = [0] + new_row + [0]
        new_row = []

########################
### Validation Logic ###
########################

def validate_rule_number(rule_number: int):
    if (rule_number < 0) or (rule_number > 255 ): return "Enter an integer between 0 and 255 (inclusive)"

def validate_generations(generations: int):
    if generations < 0: return "Enter a positive integer"
    if generations > 200: return "Enter a number less than 200"

def validate_width(width: int):
    if width < 0: return "Enter a positive integer"
    if width > 200: return "Enter a number less than 200"

def inputTemplate(label, name, val, errorMsg=None, input_type='number'):
    # Generic template for replacing the input field and showing the validation message
    return Div(hx_target='this', hx_swap='outerHTML', cls=f"{errorMsg if errorMsg else 'Valid'}")(
               Label(label), # Creates label for the input field
               Input(name=name,type=input_type,value=f'{val}',style="width: 340px;",hx_post=f'validate/{name.lower()}'), # Creates input field
               Div(f'{errorMsg}', style='color: red;') if errorMsg else None) # Creates red error message below if there is an error

```
