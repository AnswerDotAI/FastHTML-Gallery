from fasthtml.common import *
from pathlib import Path
import configparser

links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
]

app, rt = fast_app(hdrs=links)



chapters = ['ch1', 'ch2', 'ch3']
lessons = {
    'ch1': ['lesson1', 'lesson2', 'lesson3'],
    'ch2': ['lesson4', 'lesson5', 'lesson6'],
    'ch3': ['lesson7', 'lesson8', 'lesson9']
}

@rt('/lessons')
def get(chapter: str):
    return Select(
        Option('-- select lesson --', disabled='', selected='', value=''),
        *[Option(lesson) for lesson in lessons[chapter]],
        name='lesson'
    )

def application():
    chapter_dropdown = Select(
        Option('-- select chapter --', disabled='', selected='', value=''),
        *[Option(chapter) for chapter in chapters],
        name='chapter',
        hx_get='/cascading_dropdowns/lessons',
        hx_target='#lessons'
    )

    return Div(
            Div(
                Label("Chapter:", for_="chapter"),
                chapter_dropdown,
            ),
            Div(
                Label("Lesson:", for_="lesson"),
                Div(Div(id='lessons')),
            )
        )


@rt('/')
def get():
    
    return Div(
        Div(
            A(
                "Back to Gallery",
                href="/",
                cls="btn btn-primary",
                style="margin-bottom: 20px;"
            ),
            cls="d-flex align-items-center justify-content-between"
        ),
        Div(
            Div(
                H2("Source Code"),
                Pre(Code(Path('examples/cascading_dropdowns/app.py').read_text())),
                cls="col-xs-12 col-md-6 px-1"
            ),
            Div(
                H2("Live Demo"),
                application(),
                cls="col-xs-12 col-md-6 px-1"
            ),
            cls="row mx-n1"
        ),
        cls="container-fluid"
    )
