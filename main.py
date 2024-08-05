from fasthtml.common import *
import configparser
from pathlib import Path

from importlib import import_module

links = [
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    *HighlightJS(langs=['python', 'javascript', 'html', 'css']),
    MarkdownJS(),
    Script(defer=True, data_domain="fasthtml.gallery", src="https://plausible-analytics-ce-production-9521.up.railway.app/js/script.js")
]


def create_display_page(dir_path, module_path):
    _app_module = import_module(module_path)
    app = _app_module.app

    homepage = _app_module.homepage
    
    if Path(f'{dir_path}/text.md').exists():
        md = Div(Path(f'{dir_path}/text.md').read_text(),cls='marked')
    else:
        md = ''

    code = Pre(Code(Path(f'{dir_path}/app.py').read_text()))

    column1 = Div(
                    md,
                    H2("Source Code"),
                    code,
                    cls="col-xs-12 col-md-6 px-1"
                )

    column2 = Div(
                    H2("Live Demo"),
                    homepage(),
                    cls="col-xs-12 col-md-6 px-1"
                )


    @app.route('/display')
    def get():
        return Div(*links,
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
                column1,
                column2,
                cls="row mx-n1"
            ),
            cls="container-fluid"
        )
    return app

routes = []
for dir_path in Path('examples/').glob('*'):
    routes.append(Mount(f'/{dir_path.name}', create_display_page(str(dir_path), f'examples.{dir_path.name}.app')))

app, rt = fast_app(hdrs=links, 
                   routes=routes)
@rt("/")
def get():


    dir_paths = Path('examples/').glob('[!_]*')

    toggle_script = Script("""
    function toggleAnimations() {
        const images = document.querySelectorAll('.card-img-top');
        images.forEach(img => {
            if (img.src.endsWith('.png')) {
                img.src = img.getAttribute('data-gif');
            } else {
                img.setAttribute('data-gif', img.src);
                img.src = img.src.replace('gif.gif', 'img.png');
            }
        });
    }
    """)

    return Div(
        H1("FastHTML Gallery"),
        Button("Toggle Animations", onclick="toggleAnimations()", cls="btn btn-secondary mb-3"),
        Div(*[image_card(i) for i in dir_paths],
            cls="row", 
        ),
        toggle_script,
        cls="container",
    )

def image_card(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    
    return Div(
        A(
            Card(
                Div(
                    Img(src=dir_path/'img.png', alt=metadata['REQUIRED']['ImageAltText'], cls="card-img-top", data_gif=dir_path/'gif.gif'),
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
