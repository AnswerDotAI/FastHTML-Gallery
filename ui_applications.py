from fasthtml.common import *
from utils import *
from importlib import import_module
import configparser
from fasthtml.components import Zero_md


application_routes = []
for root, dirs, files in os.walk('applications'):
    if 'app.py' in files:
        application_routes.append(Mount(get_route(root,'app'), import_module(get_module_path(root,'applications')).app))
    if 'static' in dirs:
        application_routes.append(Mount(get_route(root,'static'), StaticFiles(directory=f"applications{get_route(root,'static')}")))

def image_card_applications(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']

    dpath = dir_path.parts[1]+'/'+dir_path.parts[2]

    return Div(
        Card(
            Div(
                A(Img(src=dir_path/'gif.gif', alt=meta['ImageAltText'], cls="card-img-top", data_png=dir_path/'img.png'), href=f"/{dpath}/app", target="_blank"),
                style="height: 200px; overflow: hidden; position: relative;"
            ),
            Div(
                H3(meta['ComponentName'], cls="card-title", style="font-size: 1.2rem; margin-bottom: 0.5rem;"),
                P(meta['ComponentDescription'], cls="card-text", style="font-size: 0.9rem; color: #666;"),
                cls="card-body",
                style="height: 120px; overflow: auto;"
            ),
            Div(
                A(Button("App", cls="btn btn-primary btn-sm"), href=f"/{dpath}/app", style="text-decoration: none;",target="_blank"),
                A(Button("Code", cls="btn btn-outline-secondary btn-sm"), href=f"/{dpath}/code", style="text-decoration: none;"),
                A(Button("Info", cls="btn btn-outline-info btn-sm"), href=f"/{dpath}/info", style="text-decoration: none;"),
                cls="card-footer bg-transparent",
                style="display: flex; justify-content: space-between; padding: 0.75rem 1.25rem;"
            ),
            style="height: 400px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;",
            cls="h-100"
        ),
        cls="col-xs-12 col-sm-6 col-md-4",
        style="margin-bottom: 20px; padding: 0 10px;"
    )



def render_application_code(dir_path):
    hdrs = (
        *HighlightJS(langs=['python', 'javascript', 'html', 'css']),
    )
    hdrs = (
        Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"),
        Script('hljs.highlightAll();')
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
        ),
        Body(
            Zero_md(Script(code_text, type="text/markdown")),
        )
    )
