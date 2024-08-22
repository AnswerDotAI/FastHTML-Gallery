from fasthtml.common import *

app = FastHTML(hdrs=(picolink))

def navitem(txt, cls, href): return A(txt, cls="inline-block px-4 py-2 text-sm font-medium text-white rounded transition-colors duration-300"+cls, href=href),

@app.get('/')
def homepage(session):
    session_form = Form(hx_post='/form_fill_with_session/submit-change-sess', hx_target='#result', hx_trigger="input delay:200ms")(
            Label("First Page Field"),
            Input(label="second page field 1", name="number1", input_type='number'),
        )
    fill_form(
        session_form,
        session.get('result_d', {}))

    return Div(
        Nav(cls="bg-gray-800 shadow-md")(
            Div(cls="container mx-auto px-4 py-3 flex justify-between items-center")(
                H1("FastHTML Gallery", cls="text-white text-xl font-semibold"),
                Div(cls="space-x-2")(
                    navitem("First Page", cls="bg-transparent border border-white hover:bg-white hover:text-gray-800", href="/"),
                    navitem("Second Page", cls="bg-blue-600 hover:bg-blue-700", href="/change-sess"),
                ),
            ),
        ),
        Grid(
        session_form,
        Div(id='result')
    ))

@app.post('/submit')
def submit(session, d: dict):
    session.setdefault('result_d', {})
    session['result_d'].update(d)
    return session['result_d']

@app.get('/change-sess')
def change(session):
    session_form = Form(hx_post='/form_fill_with_session/submit-change-sess', hx_target='#result', hx_trigger="input delay:200ms")(
            Label("Second Page Field 1"),
            Input(label="second page field 1", name="number1", input_type='number'),
            Label("Second Page Field 2"),
            Input(label="second page field 2", name="number2", input_type='number'),
        )
    fill_form(
        session_form,
        session.get('result_d', {}))
    return Div(
        Nav(cls="bg-gray-800 shadow-md")(
            Div(cls="container mx-auto px-4 py-3 flex justify-between items-center")(
                H1("FastHTML Gallery", cls="text-white text-xl font-semibold"),
                Div(cls="space-x-2")(
                    navitem("First Page", cls="bg-transparent border border-white hover:bg-white hover:text-gray-800", href="/"),
                    navitem("Second Page", cls="bg-blue-600 hover:bg-blue-700", href="/change-sess"),
                ),
            ),
        ),
        Grid(
        session_form,
        Div(id='result')
    ))

@app.post('/submit-change-sess')
def submit(session, d: dict):
    session.setdefault('result_d', {})
    session['result_d'].update(d)
    return session['result_d']

serve()