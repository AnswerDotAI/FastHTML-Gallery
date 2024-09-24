from fasthtml.common import *
import configparser, re, os
from pathlib import Path

from utils import *
from ui_applications import application_routes, image_card_applications, render_application_code, render_application_markdown
from ui_examples import examples_routes, image_card_examples
from functools import partial

descr = 'A gallery of FastHTML components showing common patterns in FastHTML apps, including chat bubbles, cascading dropdowns, interactive charts, etc.'

app = FastHTML(routes=examples_routes+application_routes+ [Mount('/files', StaticFiles(directory='.')),])

## Add application code/info routes
application_directories = tuple(Path(root) for root, _, files in os.walk('applications') if 'app.py' in files)
for dir_path in application_directories:
    app.add_route(get_route(dir_path,'code'), partial(render_application_code,dir_path))
    app.add_route(get_route(dir_path,'info'), partial(render_application_markdown,dir_path))

@app.get("/")
def homepage():
    ### HEADERS ###
    hdrs = (
        Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
        Style('body {padding:1rem}'),
        *HighlightJS(langs=['python', 'javascript', 'html', 'css']),
        Script(defer=True, data_domain="gallery.fastht.ml", src="https://plausible-analytics-ce-production-dba0.up.railway.app/js/script.js"),
        *Socials(title='FastHTML Gallery', description=descr, site_name='gallery.fastht.ml', twitter_site='@isaac_flath', image=f'/social.png', url=''),
        toggle_script,
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css", integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC", crossorigin="anonymous"),
        Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js", integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM", crossorigin="anonymous"),
    )

    def get_sections(path, section_names, card_fn):
        directories = tuple(Path(root) for root, _, files in os.walk(path) if 'app.py' in files and not Path(root).name.startswith('_'))
        directories = sorted(directories, key=lambda path: path.parts[0])
        directories = {k: list(vs) for k, vs in groupby(directories, key=lambda path: path.parts[1]).items()}
        return Div(*[create_image_cards(k.replace('_', ' ').title(), directories.get(k), card_fn) for k in section_names])

    ### COMBINE###
    # Return HTML as standard so I can have better control of headers to minimze conflict between submounted app headers and gallery headers
    return Html(
        Head(Title("FastHTML Gallery"),
            *hdrs,),
        Body(Nav(Div(cls="container-fluid d-flex justify-content-between align-items-center")(
                    H1(cls="navbar-brand mb-0 h1")("FastHTML Gallery" ),
                    Button(cls="btn btn-outline-primary", type="button")("Toggle Animations", onclick="toggleAnimations()"),),
                cls="navbar navbar-expand-lg navbar-light bg-light mb-4"),
            get_sections('examples', ('widgets','dynamic_user_interface','vizualizations', 'svg'), image_card_examples),
            get_sections('applications', ('start_simple','applications',), image_card_applications),))

serve()
