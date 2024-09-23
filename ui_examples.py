from pathlib import Path
from importlib import import_module
from fasthtml.common import *
import configparser
from utils import *
import inspect
from functools import wraps

def hdrs_tailwind_franken_highlightJS_markdownJS():
    return (
        Script(src='https://cdn.tailwindcss.com'),
        Script(src='https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit.min.js'),
        Script(src='https://cdn.jsdelivr.net/npm/uikit@3.21.6/dist/js/uikit-icons.min.js'),
        Script(type='module', src='https://unpkg.com/franken-wc@0.0.6/dist/js/wc.iife.js'),
        Link(rel='stylesheet', href='https://unpkg.com/franken-wc@0.0.6/dist/css/blue.min.css'),
        Script(defer=True, data_domain="gallery.fastht.ml", src="https://plausible-analytics-ce-production-dba0.up.railway.app/js/script.js"),
        HighlightJS(langs=['python', 'javascript', 'html', 'css']),
        MarkdownJS(),)


def navbar():
    return Nav(cls="uk-navbar-container", uk_navbar=True)(
        Div(cls="uk-navbar-left")(
            Ul(cls="uk-navbar-nav")(Li(A("FastHTML Gallery", href="/", cls='uk-h3 custom-nav-left', style="padding: 0 10px;")))),
        Div(cls='uk-navbar-right')(
            Ul(cls='uk-navbar-nav')(Li(A('Back to Gallery',href='/', style="padding: 0 10px;")))))

# def remove_show_code_lines(file_path):
#     with open(file_path, 'r') as f:
#         lines = f.readlines()
#
#     filtered_lines = [line for line in lines if '@show_code' not in line]
#
#     return ''.join(filtered_lines)

def remove_show_code_lines(file_path):
    with open(file_path, 'r') as f: lines = f.readlines()
    filtered_lines = [line for line in lines if '@show_code' not in line]
    hdrs_def = inspect.getsource(hdrs_tailwind_franken_highlightJS_markdownJS).splitlines()
    from_uiexamples_idx = next((i for i, line in enumerate(filtered_lines) if 'from ui_examples' in line), -1)
    filtered_lines = filtered_lines[:from_uiexamples_idx] + hdrs_def + filtered_lines[from_uiexamples_idx+1:]
    return ''.join(filtered_lines)

def show_code(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        file = Path(inspect.getfile(func))
        metadata = configparser.ConfigParser()
        metadata.read(file.parent/'metadata.ini')
        meta = metadata['REQUIRED']
        socials = Socials(title=meta['ComponentName'], description=meta['ComponentDescription'], site_name='gallery.fastht.ml',
                          twitter_site='@isaac_flath', image=str(file.parent/'img.png'), url=''),
        md=''
        if (file.parent/'text.md').exists():
            md = Div((file.parent/'text.md').read_text(),cls='marked')
        code = remove_show_code_lines(file)
        return socials,navbar(),H1(meta['ComponentName'],cls='uk-h1'),Br(),Div(cls="uk-grid")(
                                    Div(cls="uk-width-1-2@m uk-overflow-auto")(
                                        md,Pre(Code(cls="language-python")(code))),
                                    Div(cls="uk-width-1-2@m uk-overflow-auto")(func(*args, **kwargs)))
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

examples_routes = [Mount(get_route(root,'display'), import_module(get_module_path(root,'examples')).app) for root, dirs, files in os.walk('examples') if 'app.py' in files]
