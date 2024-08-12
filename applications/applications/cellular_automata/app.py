from fasthtml.common import *
from starlette.responses import Response

app, rt = fast_app()

explanation = Div(
    H1("Cellular Automata"),
    H4("Input explanations:"),
    Ul(Li(Strong("Rule Number: "),"Determines the next state of a cell based on the current state of the cell and its neighbors."),
        Li(Strong("Number of Generations: "),"Determines how many generations to run the automaton."),
        Li(Strong("Width: "),"Determines the width of the grid."),))

generator = None
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

def mk_box(color,size=5):
    return Div(cls="box", style=f"background-color:{color_map[color]};height:{size}px;width:{size}px;margin:0;display:inline-block;")

def mk_row(colors,font_size=0,size=5):
    return Div(*[mk_box(color,size) for color in colors], cls="row",style=f"font-size:{font_size}px;")

def mk_button(show):
    return Button("Hide Rule" if show else "Show Rule",
        hx_get="/show_rule?show=" + ("False" if show else "True"),
        hx_target="#rule", id="sh_rule", hx_swap_oob="outerHTML",
        hx_include="[name='rule_number']")

nav = Nav()(
    Div(cls="container")(
        Div(cls="grid")(
            H1("FastHTML Gallery"),
            Div(cls="grid")(
                A("Back to Gallery", cls="outline", href="/", role="button" ),
                A("Info", cls="secondary", href="/applications/cellular_automata/info", role="button"),
                A("Code", href="/applications/cellular_automata/code", role="button")))))
@app.get('/')
def homepage():
    return Title("Cellular Automata"),Main(nav,Div(
        Div(P(explanation,id="explanations")),
        Form(Group(
            Div(hx_target='this', hx_swap='outerHTML')(Label(_for="rule_number", cls="form-label")("Rule Number"),
                Input(type='number', name="rule_number", id='rule_set', value="30", style="width: 340px;",hx_post='/validate/rule_number', hx_indicator='#rule_numberind')),
            Div(hx_target='this', hx_swap='outerHTML')(Label("Number of Generations", cls="form-label"),
                Input(type='number',name="generations", id='generations_set',  value="50",style="width: 340px;",hx_post='/validate/generations', hx_indicator='#generationsind')),
            Div(hx_target='this', hx_swap='outerHTML')(Label("Width", cls="form-label"),
                Input(type='number',name="width", id='width_set',  value="100", style="width: 340px;",hx_post='/validate/width', hx_indicator='#widthind')),    
            Button(cls="btn btn-active btn-primary", type="submit", hx_get="/run", 
                   hx_target="#grid", hx_include="[name='rule_number'],[name='generations'],[name='width']", hx_swap="outerHTML")("Run"))),
        Group(
            Div(
                Div(id="progress_bar"),
                Div(id="grid")), 
                
            Div(style="max-width:200px")(
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

@rt('/run')
def get(rule_number: int, generations: int, width: int):
    start = [0]*(width//2) + [1] + [0]*(width//2)
    global generator 
    generator = run(rule=rule_number,generations=generations,start=start)
    return Div(
        Div(style=f"width: {(width+1)*5}px",id="progress_bar",hx_swap_oob="outerHTML:#progress_bar"),
        Div(id="next",hx_trigger="every .1s", hx_get="/next", hx_target="#grid",hx_swap="beforeend"),id="grid")


@rt('/next')
def get():
    g,val = next(generator,(False,False))
    if val: return Div(
        progress_bar(g),
        mk_row(val))
    else: return Response(status_code=286)

def progress_bar(percent_complete: float):
    return Div(hx_swap_oob="innerHTML:#progress_bar")(
            Progress(value=percent_complete))



@rt('/validate/rule_number')
def post(rule_number: int): return ruleInputTemplate(rule_number, validate_rule_number(rule_number))

@rt('/validate/generations')
def post(generations: int): return generationsInputTemplate(generations, validate_generations(generations))

@rt('/validate/width')
def post(width: int): return widthScaleInputTemplate(width, validate_width(width))


def validate_rule_number(rule_number: int):
    print(rule_number)
    if (rule_number < 0) or (rule_number > 255 ): return "Enter an integer between 0 and 255"

def validate_generations(generations: int):
    if generations < 0: return "Enter a positive integer"

def validate_width(width: int):
    if width < 0: return "Enter a positive integer"

def inputTemplate(label, name, val, errorMsg=None, input_type='text'):
    # Generic template for replacing the input field and showing the validation message
    return Div(hx_target='this', hx_swap='outerHTML', cls=f"{errorMsg if errorMsg else 'Valid'}")(
               Label(label), # Creates label for the input field
               Input(name=name,type=input_type,value=f'{val}',hx_post=f'/dynamic_user_interface/inline_validation/{name.lower()}',hx_indicator=f'#{name.lower()}ind'), # Creates input field
               Div(f'{errorMsg}', style='color: red;') if errorMsg else None) # Creates red error message below if there is an error

def ruleInputTemplate(val, errorMsg=None): return inputTemplate('Rule Number', 'rule_number', val, errorMsg, input_type='number')

def generationsInputTemplate(val, errorMsg=None): return inputTemplate('Generations', 'generations', val, errorMsg, input_type='number')

def widthScaleInputTemplate(val, errorMsg=None): return inputTemplate('Width', 'width', val, errorMsg, input_type='number')