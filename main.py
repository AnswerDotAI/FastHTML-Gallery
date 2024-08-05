from fasthtml.common import *
import os
import asyncio
import uvicorn
from uvicorn.config import Config
from uvicorn.server import Server
import configparser
from pathlib import Path

from importlib import import_module

links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    HighlightJS(langs=['python', 'javascript', 'html', 'css']),
]


def create_display_page(dir_path, module_path):
    _app_module = import_module(module_path)
    app = _app_module.app
    homepage = _app_module.homepage

    @app.route('/display')
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
                    Pre(Code(Path(f'{dir_path}/app.py').read_text())),#
                    cls="col-xs-12 col-md-6 px-1"
                ),
                Div(
                    H2("Live Demo"),
                    homepage(),
                    cls="col-xs-12 col-md-6 px-1"
                ),
                cls="row mx-n1"
            ),
            cls="container-fluid"
        )
    return app


app, rt = fast_app(hdrs=links, 
                   routes=[
                       Mount('/matplotlib_charts', create_display_page('examples/matplotlib_charts/', 'examples.matplotlib_charts.app')),
                       Mount('/chat_bubble', create_display_page('examples/chat_bubble/', 'examples.chat_bubble.app')),
                       Mount('/cascading_dropdowns', create_display_page('examples/cascading_dropdowns/', 'examples.cascading_dropdowns.app')),
                       Mount('/_hello_world', create_display_page('examples/_hello_world/', 'examples._hello_world.app')),
                   ])

@rt("/")
def get():
    from pathlib import Path
    dir_paths = Path('examples/').glob('[!_]*')
    return Div(
        H1("FastHTML Gallery"),
        Div(*[image_card(i) for i in dir_paths],
            cls="row", 
        ),
        cls="container",
    )

def image_card(dir_path):
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
            href=f"/{dir_path.name}/display",
            cls="card-link"
        ),
        cls="col-xs-12 col-sm-6 col-md-4",
        style="margin-bottom: 20px;"
    )

serve()
