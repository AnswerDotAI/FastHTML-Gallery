from pathlib import Path
from importlib import import_module
from fasthtml.common import *
import configparser
from utils import *
import inspect
from functools import wraps

hdrs_tailwind_franken_highlightJS_markdownJS = (
        Script(src='https://cdn.tailwindcss.com'),
        Script(src='https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit.min.js'),
        Script(src='https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit-icons.min.js'),
        Script(type='module', src='https://unpkg.com/franken-wc@0.0.6/dist/js/wc.iife.js'),
        Link(rel='stylesheet', href='https://unpkg.com/franken-wc@0.0.6/dist/css/blue.min.css'),
        Script(defer=True, data_domain="gallery.fastht.ml", src="https://plausible-analytics-ce-production-dba0.up.railway.app/js/script.js"),
        HighlightJS(langs=['python', 'javascript', 'html', 'css']),
        MarkdownJS(),)

def show_code(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO:  Add socials
        # TODO: Add MD FILE
        # TODO: Add TITLE
        # TODO: Add Navbar
        with open(inspect.getfile(func), 'r') as f: code = f.read()
        return Div(cls="flex")(
            Div(cls="w-1/2 p-4 overflow-auto")(
                Pre(Code(cls="language-python")(code))),
            Div(cls="w-1/2 p-4 overflow-auto")(func(*args, **kwargs)))
    return wrapper

def image_card_examples(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']

    return Div(Div(Div(Img(
                    src=f"{'/files'/dir_path/'gif.gif'}", alt=meta['ImageAltText'],
                    cls="card-img-top border",
                    style="width: 100%; height: 100%; object-fit: cover;",
                    data_png=f"{'/files'/dir_path/'img.png'}"),
                    style="height: 200px; overflow: hidden;"),
                Div(H5(meta['ComponentName'], cls="card-title fw-bold"),
                    P(meta['ComponentDescription'], cls="card-text text-muted"),
                    cls="card-body d-flex flex-column",
                    style="height: 150px; overflow: auto;",),
            cls="card h-100 shadow-sm",),
        A(href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/display", cls='stretched-link'),
        cls="col-lg-4 col-md-6 col-sm-12 mb-4",
        style="transform: rotate(0); transition: transform 0.3s ease;",
        onmouseover="this.style.transform='scale(1.05)';",
        onmouseout="this.style.transform='scale(1)';")

def create_display_page(dir_path, module_path):
    dir_path = Path(dir_path)

    _app_module = import_module(module_path)
    app = _app_module.app
    homepage = _app_module.homepage
    if hasattr(homepage, '__wrapped__'):
        homepage = homepage.__wrapped__
    md = ''
    if (dir_path/'text.md').exists():
        md = Div((dir_path/'text.md').read_text(),cls='marked')

    code = Pre(Code(strip_parent_route((dir_path/'app.py').read_text().strip(), f"{dir_path.parts[1]}/{dir_path.parts[2]}")))

    dcls="col-xs-12 col-md-6 px-1"
    column1 = Div(cls=dcls)(md,
                            H2("Source Code"),
                            code,)
    column2 = Div(H2("Live Demo"),
                    homepage(),
                    cls=dcls)
    @app.route('/display')
    def get():
        metadata = configparser.ConfigParser()
        metadata.read(dir_path/'metadata.ini')
        meta = metadata['REQUIRED']
        return (
            Title(meta['ComponentName']),
            Head(*links),
            Nav(cls="navbar navbar-expand-lg navbar-light bg-light shadow-sm mb-4")(
                Div(cls="container-fluid")(
                    Div(H1("FastHTML Gallery", cls="navbar-brand mb-0 h1"), A(href='/',cls="stretched-link"), cls="navbar-nav me-auto mb-2 mb-lg-0 position-relative"),
                    Div(A("Back to Gallery", href="/", cls="btn btn-outline-secondary me-2"),cls="d-flex"),),),
            Div(cls="container-fluid")(
                *Socials(title=meta['ComponentName'], description=meta['ComponentDescription'], site_name='gallery.fastht.ml', twitter_site='@isaac_flath', image=f"/{dir_path/'img.png'}", url=''),
                Div(column1, column2, cls="row mx-n1"),))
    return app

examples_routes = [Mount(get_route(root,'display'), import_module(get_module_path(root,'examples')).app) for root, dirs, files in os.walk('examples') if 'app.py' in files]
