from fasthtml.common import *
from utils import *
from importlib import import_module
import configparser

applications_routes = tuple(
    Mount(get_route(root,'app'), import_module(get_module_path(root,'applications')).app)
    for root, _, files in os.walk('applications') if 'app.py' in files
)

def image_card_applications(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']

    return Div(
        Card(
            Div(
                A(Img(src=dir_path/'gif.gif', alt=meta['ImageAltText'], cls="card-img-top", data_png=dir_path/'img.png'), href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/app"),
                style="height: 200px; overflow: hidden; position: relative;"
            ),
            Div(
                H3(meta['ComponentName'], cls="card-title", style="font-size: 1.2rem; margin-bottom: 0.5rem;"),
                P(meta['ComponentDescription'], cls="card-text", style="font-size: 0.9rem; color: #666;"),
                cls="card-body",
                style="height: 120px; overflow: auto;"
            ),
            Div(
                A(Button("App", cls="btn btn-primary btn-sm"), href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/app", style="text-decoration: none;"),
                A(Button("Code", cls="btn btn-outline-secondary btn-sm"), href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/code", style="text-decoration: none;"),
                A(Button("Info", cls="btn btn-outline-info btn-sm"), href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}", style="text-decoration: none;"),
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
    code_text = (dir_path/'app.py').read_text().strip()
    code_text = strip_parent_route(code_text, f"{dir_path.parts[1]}/{dir_path.parts[2]}/app")
    return Pre(Code(code_text))

def render_application_markdown(dir_path):
    return Div(Div((dir_path/'text.md').read_text(),cls='marked'),MarkdownJS())


