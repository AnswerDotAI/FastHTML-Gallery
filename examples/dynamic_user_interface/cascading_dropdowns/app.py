from fasthtml.common import *
from ui_examples import show_code, hdrs_tailwind_franken_highlightJS_markdownJS

app, rt = fast_app(hdrs=hdrs_tailwind_franken_highlightJS_markdownJS())

chapters = ['ch1', 'ch2', 'ch3']
lessons = {
    'ch1': ['lesson1', 'lesson2', 'lesson3'],
    'ch2': ['lesson4', 'lesson5', 'lesson6'],
    'ch3': ['lesson7', 'lesson8', 'lesson9']}

def mk_opts(nm, cs):
    return (
        Option(f'-- select {nm} --', disabled='', selected='', value=''),
        *map(Option, cs))

@app.get('/get_lessons')
def get_lessons(chapter: str):
    return Select(*mk_opts('lesson', lessons[chapter]), name='lesson')

@app.get('/')
@show_code
def homepage():
    chapter_dropdown = Select(
        *mk_opts('chapter', chapters),
        name='chapter',
        get='get_lessons', hx_target='#lessons')

    return Div(
        Div(Label("Chapter:", for_="chapter"),
            chapter_dropdown),
        Div(Label("Lesson:", for_="lesson"),
            Div(Div(id='lessons')),))

