from fasthtml.common import *
import configparser, re
from pathlib import Path

from importlib import import_module

links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    *HighlightJS(langs=['python', 'javascript', 'html', 'css']),
    MarkdownJS(),
    Script(defer=True, data_domain="fasthtml.gallery", src="https://plausible-analytics-ce-production-9521.up.railway.app/js/script.js")
]


def create_display_page(dir_path, module_path):
    
    def strip_parent_route(text, parent_route):
        htmx_route_methods = ['hx_get', 'hx_post', 'hx_delete', 'hx_put', 'hx_patch']
        for method in htmx_route_methods:
            pattern = f'({method}=[\'\"])/{parent_route}(/[^\'\"]*)[\'\"]'
            replacement = f'\\1\\2"'
            text = re.sub(pattern, replacement, text)
        return text

    _app_module = import_module(module_path)
    app = _app_module.app

    homepage = _app_module.homepage
    md = ''
    if Path(f'{dir_path}/text.md').exists():
        md = Div(Path(f'{dir_path}/text.md').read_text(),cls='marked')

    code = Pre(Code(strip_parent_route(Path(f'{dir_path}/app.py').read_text().strip(), Path(dir_path).name)))

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
        return Div(*links,
            Div(
                A(
                    "Back to Gallery",
                    href="/", style="margin-bottom: 20px;",
                    cls="btn btn-primary"),
                cls="d-flex align-items-center justify-content-between"),
            Div(
                column1,
                column2,
                cls="row mx-n1"),
            cls="container-fluid")
    return app

routes = []
for dir_path in Path('examples/').glob('*'):
    routes.append(Mount(f'/{dir_path.name}', create_display_page(str(dir_path), f'examples.{dir_path.name}.app')))

app, rt = fast_app(hdrs=links, routes=routes)

@rt("/")
def get():
    dir_paths = Path('examples/').glob('[!_]*')
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

    return Div(
        H1("FastHTML Gallery"),
        Button("Toggle Animations", onclick="toggleAnimations()", cls="btn btn-secondary mb-3"),
        Div(*[image_card(i) for i in dir_paths], cls="row"),
        toggle_script,
        cls="container",
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
            href=f"/{dir_path.name}/display",
            cls="card-link",
            style="text-decoration: none; color: inherit;"),
        cls="col-xs-12 col-sm-6 col-md-4",
        style="margin-bottom: 20px;")

serve()

