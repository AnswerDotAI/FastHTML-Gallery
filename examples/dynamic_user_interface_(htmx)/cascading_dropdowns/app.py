from fasthtml.common import *

app, rt = fast_app()

chapters = ['ch1', 'ch2', 'ch3']
lessons = {
    'ch1': ['lesson1', 'lesson2', 'lesson3'],
    'ch2': ['lesson4', 'lesson5', 'lesson6'],
    'ch3': ['lesson7', 'lesson8', 'lesson9']}

def mk_opts(nm, cs):
    return (
        Option(f'-- select {nm} --', disabled='', selected='', value=''),
        *map(Option, cs))

@rt
def get_lessons(chapter: str):
    return Select(*mk_opts('lesson', lessons[chapter]), name='lesson')

@rt
def index():
    chapter_dropdown = Select(
        *mk_opts('chapter', chapters),
        name='chapter',
        get='get_lessons', hx_target='#lessons')

    return Div(
        Div(Label("Chapter:", for_="chapter"),
            chapter_dropdown),
        Div(Label("Lesson:", for_="lesson"),
            Div(Div(id='lessons')),))

