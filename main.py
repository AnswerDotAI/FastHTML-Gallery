from fasthtml.common import *
import configparser, re, os
from pathlib import Path

from importlib import import_module

links = (
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    *HighlightJS(langs=['python', 'javascript', 'html', 'css']),
    Script(defer=True, data_domain="fasthtml.gallery", src="https://plausible-analytics-ce-production-9521.up.railway.app/js/script.js"),
)

def create_display_page(dir_path, module_path):
    dir_path = Path(dir_path)
    def strip_parent_route(text, parent_route):
        htmx_route_methods = ['hx_get', 'hx_post', 'hx_delete', 'hx_put', 'hx_patch']
        for method in htmx_route_methods:
            pattern = f'({method}=(f?[\'"]))/({parent_route})(/[^\'"]*)(\\2|\'|")'
            replacement = r'\1\4\5'
            text = re.sub(pattern, replacement, text)
        return text
    _app_module = import_module(module_path)
    app = _app_module.app

    homepage = _app_module.homepage
    md = ''
    if (dir_path/'text.md').exists():
        md = Div((dir_path/'text.md').read_text(),cls='marked')

    code = Pre(Code(strip_parent_route((dir_path/'app.py').read_text().strip(), f"{dir_path.parts[1]}/{dir_path.parts[2]}")))

    dcls="col-xs-12 col-md-6 px-1"
    column1 = Div(
                    md,
                    H2("Source Code"),
                    code,
                    cls=dcls)

    column2 = Div(
                    H2("Live Demo"),
                    homepage(),
                    cls=dcls)


    @app.route('/display')
    def get():
        return (
            Title(f"{dir_path.name.replace('_', ' ').title()}"),
            Div(
                *tuple(links if MarkdownJS() in getattr(_app_module,'hdrs',[]) else links + (MarkdownJS(),)),                Div(
                    A("Back to Gallery",  href="/", style="margin-bottom: 20px;", cls="btn btn-primary"),
                    cls="d-flex align-items-center justify-content-between"
                ),
                Div(column1, column2, cls="row mx-n1"),
                cls="container-fluid"
            )
        )
    return app

def get_module_path(p):
    return f'examples.{".".join(Path(p).parts[1:])}.app'

def get_route(p):
    return f"/{'/'.join(Path(p).parts[1:])}"

routes = tuple(
    Mount(get_route(root), create_display_page(root,get_module_path(root)))
    for root, _, files in os.walk('examples') if 'app.py' in files
)

app, rt = fast_app(hdrs=links, routes=routes)

@rt("/")
def get():
    dir_paths = tuple(Path(root) for root, _, files in os.walk('examples') if 'app.py' in files)
    dir_paths = sorted(dir_paths, key=lambda path: path.parts[0])
    dir_paths = {k: list(vs) for k, vs in groupby(dir_paths, key=lambda path: path.parts[1]).items()}
    keys = ('widgets','dynamic_user_interface','application_layout')

    def create_image_cards(n, ps):
        return Div(
            H2(n, style="color: #333; font-weight: 600; border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px;"),
            Div(*[image_card(p) for p in ps], cls="row")
        )

    toggle_script = Script("""
    function toggleAnimations() {
        const images = document.querySelectorAll('.card-img-top');
        images.forEach(img => {
            if (img.src.endsWith('.gif')) {
                img.src = img.getAttribute('data-png');
            } else {
                img.setAttribute('data-png', img.src);
                img.src = img.src.replace('img.png', 'gif.gif');
            }
        });
    }""")

    return (Title("FastHTML Gallery"),
        Div(
            Div(
                H1("FastHTML Gallery", style="display: inline-block; margin-right: 20px;"),
                Button("Toggle Animations", onclick="toggleAnimations()", cls="btn btn-secondary", style="vertical-align: middle;"),
                style="display: flex; justify-content: space-between; align-items: center;"
            ),
            Hr(),
            Div(*[create_image_cards(k.replace('_', ' ').title(), dir_paths.get(k)) for k in keys]),
            toggle_script,
            cls="container",
        )
    )

def image_card(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']

    return Div(
        A(
            Card(
                Div(
                    Img(src=dir_path/'gif.gif', alt=meta['ImageAltText'], cls="card-img-top", data_png=dir_path/'img.png'),
                    style="height: 200px; overflow: hidden;"
                ),
                Div(
                    H3(meta['ComponentName'][1:-1], cls="card-title"),
                    P(meta['ComponentDescription'][1:-1], cls="card-text"),
                    cls="card-body",
                    style="height: 150px; overflow: auto;"),
                style="height: 350px;"),
            href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/display",
            cls="card-link",
            style="text-decoration: none; color: inherit;"),
        cls="col-xs-12 col-sm-6 col-md-4",
        style="margin-bottom: 20px;")

serve()
