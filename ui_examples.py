from pathlib import Path
import re
from importlib import import_module
from fasthtml.common import *
import configparser
from utils import *

links = (
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    *HighlightJS(langs=['python', 'javascript', 'html', 'css']),
    Script(defer=True, data_domain="fasthtml.gallery", src="https://plausible-analytics-ce-production-9521.up.railway.app/js/script.js"),
)

def image_card_examples(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']

    return Div(
        A(
            Card(
                Div(
                    Img(src=f"{'/files'/dir_path/'gif.gif'}", alt=meta['ImageAltText'], cls="card-img-top", data_png=f"{'/files'/dir_path/'img.png'}"),
                    style="height: 200px; overflow: hidden;"
                ),
                Div(
                    H3(meta['ComponentName'], cls="card-title"),
                    P(meta['ComponentDescription'], cls="card-text"),
                    cls="card-body",
                    style="height: 150px; overflow: auto;"),
                style="height: 350px;"),
            href=f"/{dir_path.parts[1]}/{dir_path.parts[2]}/display",
            cls="card-link",
            style="text-decoration: none; color: inherit;"),
        cls="col-xs-12 col-sm-6 col-md-4",
        style="margin-bottom: 20px;")


def create_display_page(dir_path, module_path):
    dir_path = Path(dir_path)

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
        metadata = configparser.ConfigParser()
        metadata.read(dir_path/'metadata.ini')
        meta = metadata['REQUIRED']
        return (
            Title(meta['ComponentName']),
            Div(
                *Socials(title=meta['ComponentName'], description=meta['ComponentDescription'],
                         site_name='fasthtml.gallery', twitter_site='@isaac_flath', image=f"/{dir_path/'img.png'}", url=''),
                *tuple(links if MarkdownJS() in getattr(_app_module,'hdrs',[]) else links + (MarkdownJS(),)),
                Div(
                    A("Back to Gallery",  href="/", style="margin-bottom: 20px;", cls="btn btn-primary"),
                    cls="d-flex align-items-center justify-content-between"
                ),
                Div(column1, column2, cls="row mx-n1"),
                cls="container-fluid"
            )
        )
    return app

examples_routes = [
    Mount(get_route(root), create_display_page(root,get_module_path(root,'examples')))
    for root, _, files in os.walk('examples') if 'app.py' in files
]
