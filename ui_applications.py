from fasthtml.common import *
from utils import *
from importlib import import_module
import configparser
from fasthtml.components import Zero_md

application_routes = [Mount(get_route(root,'app'), import_module(get_module_path(root,'applications')).app) for root, dirs, files in os.walk('applications') if 'app.py' in files]
    
def image_card_applications(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']

    dpath = dir_path.parts[1]+'/'+dir_path.parts[2]

    return Div(cls="col-lg-4 col-md-6 col-sm-12 mb-4", style="transition: transform 0.3s ease;",
        onmouseover="this.style.transform='scale(1.05)';", onmouseout="this.style.transform='scale(1)';")(
        Div(cls="card h-100 shadow-sm")(
            Div(
                A(Img(
                    src=f"{'/files'/dir_path/'gif.gif'}", alt=meta['ImageAltText'], 
                    cls="card-img-top border",
                    style="width: 100%; height: 100%; object-fit: cover;",
                    data_png=f"{'/files'/dir_path/'img.png'}"), 
                    href=f"/{dpath}/app"),
            ),
            Div(cls="card-body d-flex flex-column",
                style="height: 150px; overflow: auto;",)(
                H5(cls="card-title")(meta['ComponentName']),
                P(cls="card-text")(meta['ComponentDescription']),
                ),
            Div(cls="card-footer d-flex justify-content-between")(
                A(Button("App", cls="btn btn-primary btn-sm"), href=f"/{dpath}/app"),
                A(Button("Code", cls="btn btn-secondary btn-sm"), href=f"/{dpath}/code"),
                A(Button("Info", cls="btn btn-info btn-sm"), href=f"/{dpath}/info"),
            ),
        ),
        )



def render_application_code(dir_path):
    hdrs = (
        Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"),
        Script('hljs.highlightAll();'),
        *get_social_links(dir_path),
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css", integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC", crossorigin="anonymous"),  
        Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js", integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM", crossorigin="anonymous"),
    )
    code_text = (dir_path/'app.py').read_text().strip()
    code_text = strip_parent_route(code_text, f"{dir_path.parts[1]}/{dir_path.parts[2]}/app")
    return Html(
        Head( *hdrs,Title(f"{dir_path.parts[1]}/{dir_path.parts[2]} - Code"),),
        Body(Nav(cls="navbar navbar-expand-lg navbar-light bg-light shadow-sm mb-4")(
                Div(cls="container-fluid")(
                        H1("FastHTML Gallery", cls="navbar-brand mb-0 h1"),
                        cls="navbar-nav me-auto mb-2 mb-lg-0"
                    ),
                    Div(cls="d-flex")(
                        A("Back to Gallery", href="/", cls="btn btn-outline-secondary me-2"),
                        A("Info", href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/info", cls="btn btn-info me-2"),
                        A("App", href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/app", cls="btn btn-primary"),
                    ),
                ),
            Pre(Code(code_text, cls='language-python'))
            ),        
        )
    
def render_application_markdown(dir_path):
    code_text = (dir_path/'text.md').read_text()
    return Html(
        Head(
            Script(type="module", src="https://cdn.jsdelivr.net/npm/zero-md@3?register"),
            Title(f"{dir_path.parts[1]}/{dir_path.parts[2]} - Info"),
            *get_social_links(dir_path),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css", integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC", crossorigin="anonymous"),  
            Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js", integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM", crossorigin="anonymous"),
        ),Body(
            Nav(cls="navbar navbar-expand-lg navbar-light bg-light shadow-sm mb-4")(
                Div(cls="container-fluid")(
                    Div(cls="d-flex")(
                        H1("FastHTML Gallery", cls="navbar-brand mb-0 h1"),
                        cls="navbar-nav me-auto mb-2 mb-lg-0"
                    ),
                    Div(cls="d-flex")(
                        A("Back to Gallery", href="/", cls="btn btn-outline-secondary me-2"),
                        A("Code", href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/code", cls="btn btn-secondary me-2"),
                        A("App", href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/app", cls="btn btn-primary"),
                    ),
                ),
            ),
            Div(cls="container")(
                Zero_md(Script(code_text, type="text/markdown")),
            ),
            
        ))
    
