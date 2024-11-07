from fasthtml.common import *
import configparser, os
from pathlib import Path
from utils import *
from importlib import import_module
from fh_frankenui.core import *

def get_route(p): return '/'.join(Path(p).parts[1:])
def get_module_path(p,base_dir): return f'{base_dir}.{".".join(Path(p).parts[1:])}.app'

application_routes = [Mount(f"/app/{get_route(root)}", import_module(get_module_path(root,'examples')).app) for root, dirs, files in os.walk('examples') if 'app.py' in files]

descr = 'A gallery of FastHTML components showing common patterns in FastHTML apps, including chat bubbles, cascading dropdowns, interactive charts, etc.'

HLJS_THEMES = {
    'dark': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-dark.css',
    'light': 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-light.css'
}

hjs = (
    # Basic highlight.js setup
    Script(src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/highlight.min.js'),
    Script(src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/python.min.js'),
    
    # Copy button setup
    Script(src='https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.js'),
    Link(rel='stylesheet', href='https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.css'),
    Style('''
        .hljs-copy-button { background-color: #2d2b57; }
        html.dark .hljs-copy-button { background-color: #e0e0e0; color: #2d2b57; }
    '''),
    
    # Theme stylesheets
    Link(rel='stylesheet', href=HLJS_THEMES['dark'], id='hljs-dark-theme', disabled=True),
    Link(rel='stylesheet', href=HLJS_THEMES['light'], id='hljs-light-theme', disabled=True),
    
    # Theme switching logic
    Script('''
        function updateCodeTheme() {
            const isDark = document.documentElement.classList.contains('dark');
            document.getElementById('hljs-dark-theme').disabled = !isDark;
            document.getElementById('hljs-light-theme').disabled = isDark;
        }
        
        // Watch for theme changes
        new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.target.tagName === 'HTML' && mutation.attributeName === 'class') {
                    updateCodeTheme();
                }
            });
        }).observe(document.documentElement, { attributes: true });
        
        // Initial setup
        document.addEventListener('DOMContentLoaded', updateCodeTheme);
    '''),
    # Highlight.js initialization
    Script('''
        hljs.configure({ ignoreUnescapedHTML: true });
        hljs.addPlugin(new CopyButtonPlugin());
        htmx.onLoad(hljs.highlightAll);
    ''', type='module'),
)

hdrs = (
    *hjs,
    Script(defer=True, data_domain="gallery.fastht.ml", src="https://plausible-analytics-ce-production-dba0.up.railway.app/js/script.js"),
    *Socials(title='FastHTML Gallery', description=descr, site_name='gallery.fastht.ml', twitter_site='@isaac_flath', image=f'/social.png', url=''),
    toggle_script,
    *Theme.blue.headers(),
)

app = FastHTML(routes=application_routes+ [Mount('/files', StaticFiles(directory='.')),], hdrs=hdrs, pico=False)

def NavBar(dir_path):
    return NavBarContainer(
            NavBarLSide(
                A(H1("Fh-Gallery", cls="navbar-brand mb-0 h1"), href="/")),
            NavBarCenter(H1(f"{dir_path.name.replace('_',' ').title()}")),
            NavBarRSide(
                NavBarNav(
                    Li(A("Back to Gallery", href="/")),
                    Li(A("Info", href=f"/info/{dir_path.parts[1]}/{dir_path.parts[2]}")),
                    Li(A("Code", href=f"/code/{dir_path.parts[1]}/{dir_path.parts[2]}")),
                    Li(A("App", href=f"/app/{dir_path.parts[1]}/{dir_path.parts[2]}")))))   

@app.get('/split/{category}/{project}')
def split_view(category: str, project: str):
    dir_path = Path('examples')/category/project
    code_text = (dir_path/'app.py').read_text().strip()
    return (
        NavBar(dir_path),
        Title(f"{dir_path.name} - Split View"),
        Container(
            Div(Div(Pre(Code(code_text, cls='language-python')), style="width: 50%; padding: 10px;"),
                Div(Iframe(src=f"/app/{category}/{project}/",style="width: 100%; height: 100%; border: none;"),
                    style="width: 50%; padding: 10px;"),
                style="display: flex; height: calc(100vh - 60px);")))

@app.get('/code/{category}/{project}')
def application_code(category:str, project:str):
    dir_path = Path('examples')/category/project
    code_text = (dir_path/'app.py').read_text().strip()
    return  (NavBar(dir_path), Title(f"{dir_path.name} - Code"), Container(Pre(Code(code_text, cls='language-python'))))
    
@app.get('/info/{category}/{project}')
def application_info(category:str, project:str):
    dir_path = Path('examples')/category/project
    md_text = (dir_path/'text.md').read_text()
    return (NavBar(dir_path), Title(f"{dir_path.name} - Info"), Container(render_md(md_text)))

def ImageCard(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']
    dpath = dir_path.parts[1]+'/'+dir_path.parts[2]

    text_md_exists = (dir_path/'text.md').exists()
    print(dpath)
    return Card(
            A(Img(
                src=f"{'/files'/dir_path/'gif.gif'}", alt=meta['ImageAltText'],
                style="width: 100%; height: 350px; object-fit: cover;",
                data_png=f"{'/files'/dir_path/'img.png'}",
                cls="card-img-top"), 
                href=f"/split/{dpath}"),
            Div(
                P(meta['ComponentName'],        cls=(TextT.bold, TextT.large)),
                P(meta['ComponentDescription'], cls=(TextT.muted, TextT.large)),
                style="height: 150px; overflow: auto;"
                ),
            footer=DivFullySpaced(
                A(Button("Split", cls=ButtonT.primary), href=f"/split/{dpath}"),
                A(Button("Code", cls=ButtonT.secondary), href=f"/code/{dpath}"),
                A(Button("App", ), href=f"/app/{dpath}"),
                A(Button("Info"), href=f"/info/{dpath}") if text_md_exists else None,
            ))

@app.get("/")
def homepage():
    ### HEADERS ###
    directories = [Path(f"examples/{x}") for x in [
        'widgets',
        'visualizations',
        'dynamic_user_interface',
        'svg',
        'start_simple',
        'applications']]

    all_cards = []
    for section in directories:
        all_cards.append(
            Section(
                H1(section.name.replace('_',' ').title(), cls='mt-6 mb-4 pb-2 text-center text-3xl font-bold border-b-2 border-gray-300'),
                Grid(*[ImageCard(dir) for dir in section.iterdir() if dir.is_dir() and not dir.name.startswith('_')],
                     cols_min=1, cols_sm=1, cols_md=2, cols_lg=3,
                     ),
                cls='pt-6'
            )
        )

    return (NavBarContainer(
        NavBarLSide(H1("FastHTML Gallery" )),
        NavBarRSide(
            Button(submit=False)("Toggle Animations", onclick="toggleAnimations()"))),
        Container(*all_cards)
    )
serve()
