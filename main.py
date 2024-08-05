from fasthtml.common import *
import os
import asyncio
import uvicorn
from uvicorn.config import Config
from uvicorn.server import Server
import configparser

links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
]

from examples.chat_bubble.app import app as chat_bubble_app
from examples.cascading_dropdowns.app import app as cascading_dropdowns_app


app, rt = fast_app(hdrs=links, 
                   routes=[
                       Mount('/chat_bubble', chat_bubble_app),
                       Mount('/cascading_dropdowns', cascading_dropdowns_app),
                   ])

@rt("/")
def get():
    from pathlib import Path
    dir_paths = Path('examples/').glob('*')
    return Div(
        H1("FastHTML Gallery"),
        Div(*[image_card(i) for i in dir_paths],
            cls="row", 
        ),
        cls="container",
    )

def image_card(dir_path):
    import configparser
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    
    return Div(
        A(
            Card(
                Div(
                    Img(src=dir_path/'img.png', alt=metadata['REQUIRED']['ImageAltText'], cls="card-img-top"),
                    style="height: 200px; overflow: hidden;"
                ),
                Div(
                    H3(metadata['REQUIRED']['ComponentName'][1:-1], cls="card-title"),
                    P(metadata['REQUIRED']['ComponentDescription'][1:-1], cls="card-text"),
                    cls="card-body",
                    style="height: 150px; overflow: auto;"
                ),
                style="height: 350px;"
            ),
            href=f"/{dir_path.name}",
            cls="card-link"
        ),
        cls="col-xs-12 col-sm-6 col-md-4",
        style="margin-bottom: 20px;"
    )

serve()
