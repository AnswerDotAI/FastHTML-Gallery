from fasthtml.common import *
import configparser, re, os
from pathlib import Path

from utils import *
from ui_applications import applications_routes, image_card_applications, render_application_code, render_application_markdown
from ui_examples import examples_routes, image_card_examples

descr = 'A gallery of FastHTML components showing common patterns in FastHTML apps, including chat bubbles, cascading dropdowns, interactive charts, etc.'

links = (
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    *HighlightJS(langs=['python', 'javascript', 'html', 'css']),
    Script(defer=True, data_domain="fasthtml.gallery", src="https://plausible-analytics-ce-production-9521.up.railway.app/js/script.js"),
)
app, rt = fast_app(hdrs=links+(*Socials(title='FastHTML Gallery', description=descr, site_name='fasthtml.gallery', twitter_site='@isaac_flath', image=f'/social.png', url=''),), 
                   routes=examples_routes+applications_routes)

@rt("/")
def get():
    ### EXAMPLES ###
    example_directories = tuple(Path(root) for root, _, files in os.walk('examples') if 'app.py' in files)
    example_directories = sorted(example_directories, key=lambda path: path.parts[0])
    example_directories = {k: list(vs) for k, vs in groupby(example_directories, key=lambda path: path.parts[1]).items()}
    example_section_names = ('widgets','dynamic_user_interface','application_layout')
    examples_sections = Div(*[create_image_cards(k.replace('_', ' ').title(), example_directories.get(k), image_card_examples) for k in example_section_names])

    ### APPLICATIONS ###
    application_directories = tuple(Path(root) for root, _, files in os.walk('applications') if 'app.py' in files)
    application_directories = sorted(application_directories, key=lambda path: path.parts[0])
    application_directories = {k: list(vs) for k, vs in groupby(application_directories, key=lambda path: path.parts[1]).items()}
    application_section_names = ('applications',)
    applications_sections = Div(*[create_image_cards(k.replace('_', ' ').title(), application_directories.get(k), image_card_applications) for k in application_section_names])

    ### COMBINE ###
    return (Title("FastHTML Gallery"),
        Div(
            Div(
                H1("FastHTML Gallery", style="display: inline-block; margin-right: 20px;"),
                Button("Toggle Animations", onclick="toggleAnimations()", cls="btn btn-secondary", style="vertical-align: middle;"),
                style="display: flex; justify-content: space-between; align-items: center;"
            ),
            Hr(),
            examples_sections,
            applications_sections,
            toggle_script,
            cls="container",
        )
    )

application_directories = tuple(Path(root) for root, _, files in os.walk('applications') if 'app.py' in files)
for dir_path in application_directories:
    app.add_route(get_route(dir_path,'code'), render_application_code(dir_path))
    app.add_route(get_route(dir_path,'info'), render_application_markdown(dir_path))




serve()
