from fasthtml.common import *
from pathlib import Path
import configparser

app, rt = fast_app()

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

def homepage():
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
    return homepage()
    
