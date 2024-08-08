from fasthtml.common import *
from utils import *
from importlib import import_module
import configparser
from fasthtml.components import Zero_md

application_routes = []
for root, dirs, files in os.walk('applications'):
    if 'app.py' in files:
        application_routes.append(Mount(get_route(root,'app'), import_module(get_module_path(root,'applications')).app))

def image_card_applications(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']

    dpath = dir_path.parts[1]+'/'+dir_path.parts[2]

    return Div(
        Div(
            Div(
                A(Img(
                    src=f"{'/files'/dir_path/'gif.gif'}", alt=meta['ImageAltText'], 
                    cls="card-img-top",
                    data_png=f"{'/files'/dir_path/'img.png'}"), 
                    href=f"/{dpath}/app", target="_blank"),
            ),
            Div(
                H5(meta['ComponentName'], cls="card-title"),
                P(meta['ComponentDescription'], cls="card-text"),
                cls="card-body",
            ),
            Div(
                A(Button("App", cls="btn btn-primary btn-sm"), href=f"/{dpath}/app", target="_blank"),
                A(Button("Code", cls="btn btn-secondary btn-sm"), href=f"/{dpath}/code"),
                A(Button("Info", cls="btn btn-info btn-sm"), href=f"/{dpath}/info"),
                cls="card-footer d-flex justify-content-between"
            ),
            cls="card",
        ),
        cls="col-lg-4 col-md-6 col-sm-12 mb-4"
    )

def render_application_code(dir_path):
    hdrs = (
        Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"),
        Script('hljs.highlightAll();'),
        *get_social_links(dir_path)
    )
    code_text = (dir_path/'app.py').read_text().strip()
    code_text = strip_parent_route(code_text, f"{dir_path.parts[1]}/{dir_path.parts[2]}/app")
    return Html(
        Head(
            *hdrs,
            Title(f"{dir_path.parts[1]}/{dir_path.parts[2]} - Code"),

        ),
        Body(
            Pre(Code(code_text, cls='language-python'))
        )
    )

def render_application_markdown(dir_path):
    code_text = (dir_path/'text.md').read_text()
    return Html(
        Head(
            Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register"),
            Title(f"{dir_path.parts[1]}/{dir_path.parts[2]} - Info"),
            *get_social_links(dir_path)
        ),
        Body(
            Zero_md(Script(code_text, type="text/markdown")),
        )
    )
