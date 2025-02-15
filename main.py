from fasthtml.common import *
import configparser, os
from pathlib import Path
from utils import *
from importlib import import_module
from monsterui.all import *

def get_route(p): return '/'.join(Path(p).parts[1:])
def get_module_path(p,base_dir): return f'{base_dir}.{".".join(Path(p).parts[1:])}.app'

application_routes = [Mount(f"/app/{get_route(root)}", import_module(get_module_path(root,'examples')).app) for root, dirs, files in os.walk('examples') if 'app.py' in files]

site_title = 'FastHTML Gallery'
descr = 'A gallery of FastHTML components showing common patterns in FastHTML apps, including chat bubbles, cascading dropdowns, interactive charts, etc.'
ghub_link = A(UkIcon("github"), title="FastHTML Gallery on Github",
                 href="https://github.com/AnswerDotAI/FastHTML-Gallery"),

hdrs = (
    *Socials(title=site_title, description=descr, site_name='gallery.fastht.ml', twitter_site='@isaac_flath', image=f'/social.png', url=''),
    toggle_script,
    *Theme.blue.headers(highlightjs=True),
    Link(rel='icon', type='image/x-ico', href="/files/gallery.ico"))

app = FastHTML(routes=application_routes+ [Mount('/files', StaticFiles(directory='.')),], hdrs=hdrs, pico=False)

def NavBar(dir_path, info=True, active=''):
    nav_items = [
        Li(A("Back to Gallery", href="/")),
        Li(A("Split", href=f"/split/{dir_path.parts[1]}/{dir_path.parts[2]}"), cls='uk-active' if active == 'split' else ''),
        Li(A("Code", href=f"/code/{dir_path.parts[1]}/{dir_path.parts[2]}"), cls='uk-active' if active == 'code' else ''),
        Li(A("App",  href=f"/app/{dir_path.parts[1]}/{dir_path.parts[2]}"), cls='uk-active' if active == 'app' else '')]
    
    if info:nav_items.insert(1, Li(A("Info", href=f"/info/{dir_path.parts[1]}/{dir_path.parts[2]}"), cls='uk-active' if active == 'info' else ''))
        
    return NavBarContainer(
            NavBarLSide(H1(f"{dir_path.name.replace('_',' ').title()}"), cls="hidden md:block"),
            NavBarRSide(NavBarNav(*nav_items)))

@app.get('/split/{category}/{project}')
def split_view(category: str, project: str):
    try:
        dir_path = Path('examples')/category/project
        code_text = (dir_path/'app.py').read_text().strip()
        info = (dir_path/'info.md').exists()
    except:
        return Response(status_code=404)
    return (
        NavBar(dir_path, info=info, active='split'),
        Title(f"{dir_path.name} - Split View"),
            Grid(Div(Pre(Code(code_text, cls='language-python'))),
                Div(Iframe(src=f"/app/{category}/{project}/",style="width: 100%; height: 100%; border: none;")),
                cols_sm=1, cols_md=1, cols_lg=2))

@app.get('/code/{category}/{project}')
def application_code(category:str, project:str):
    try:
        dir_path = Path('examples')/category/project
        code_text = (dir_path/'app.py').read_text().strip()
        info = (dir_path/'info.md').exists()
    except:
        return Response(status_code=404)
    return  (NavBar(dir_path, info=info, active='code'), Title(f"{dir_path.name} - Code"), Container(Pre(Code(code_text, cls='language-python'))))
    
@app.get('/info/{category}/{project}')
def application_info(category:str, project:str):
    try:
        dir_path = Path('examples')/category/project
        md_text = (dir_path/'info.md').read_text()
    except:
        return Response(status_code=404)
    return (NavBar(dir_path, info=True, active='info'), Title(f"{dir_path.name} - Info"), Container(render_md(md_text)))

def ImageCard(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']
    dpath = dir_path.parts[1]+'/'+dir_path.parts[2]

    text_md_exists = (dir_path/'info.md').exists()
    return Card(
            A(Img(
                src=f"{'/files'/dir_path/'card_thumbnail.gif'}", alt=meta['ImageAltText'],
                style="width: 100%; height: 350px; object-fit: cover;",
                data_png=f"{'/files'/dir_path/'card_thumbnail.png'}",
                loading="lazy",
                cls="card-img-top"), 
                href=f"/split/{dpath}"),
            Div(P(meta['ComponentName'],        cls=(TextT.bold, TextT.lg)),
                render_md(P(meta['ComponentDescription'])),#, cls=(TextT.muted, TextT.lg)),
                style="height: 150px; overflow: auto;"),
            footer=DivFullySpaced(
                A(Button("Split", cls=ButtonT.primary), href=f"/split/{dpath}"),
                A(Button("Code", cls=ButtonT.secondary), href=f"/code/{dpath}"),
                A(Button("App", ), href=f"/app/{dpath}"),
                A(Button("Info"), href=f"/info/{dpath}") if text_md_exists else None))
directories = [Path(f"examples/{x}") for x in [
    'dynamic_user_interface_(htmx)',
    'visualizations',
    'widgets',
    'svg',
    'todo_series',
    'applications']]

def is_example_dir(d): 
    return d.is_dir() and not d.name.startswith('_') and (d/'metadata.ini').exists()

@app.get("/")
def homepage():
    ### HEADERS ###
    all_cards = []
    for section in directories:
        all_cards.append(
            Section(Details(
                Summary(H1(section.name.replace('_',' ').title(), cls='mt-6 mb-4 pb-2 text-center text-3xl font-bold border-b-2 border-gray-300')),
                Grid(*[ImageCard(dir) for dir in sorted(section.iterdir()) if is_example_dir(dir)],
                     cols_min=1, cols_sm=1, cols_md=2, cols_lg=3, cols_xl=3),
                cls='pt-6', open=True)))

    return (Title(site_title),
        NavBarContainer(
        NavBarLSide(H1(site_title)),
        NavBarRSide(
            Button(submit=False)("Toggle Animations", onclick="toggleAnimations()"),
            A(Button("Table View"), href="/table"),
            ghub_link)),
        Container(*all_cards))


def TableRow(dir_path):
    metadata = configparser.ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']
    dpath = dir_path.parts[1]+'/'+dir_path.parts[2]
    
    text_md_exists = (dir_path/'info.md').exists()
    return Tr(
        Td(meta['ComponentName']),
        Td(render_md(meta['ComponentDescription'])),
        Td(DivLAligned(
            A(Button("Split", cls=ButtonT.primary), href=f"/split/{dpath}"),
            A(Button("Code", cls=ButtonT.secondary), href=f"/code/{dpath}"),
            A(Button("App"), href=f"/app/{dpath}"),
            A(Button("Info"), href=f"/info/{dpath}") if text_md_exists else None),
           cls='uk-table-shrink'))

def SectionTable(section):
    section_id = f"section-{section.name}"
    return Section(Details(
            Summary(H1(section.name.replace('_',' ').title(), 
                   cls='mt-6 mb-4 pb-2 text-center text-3xl font-bold border-b-2 border-gray-300 cursor-pointer')),
            Table(
                Thead(Tr(map(Th, ("Component", "Description", "Actions")))),
                Tbody(*[TableRow(dir) for dir in sorted(section.iterdir()) 
                       if is_example_dir(dir)]),
                cls=(TableT.middle, TableT.divider, TableT.hover, TableT.sm)),
            # open=True,
            id=section_id),
        cls='py-2')

@app.get("/table") 
def table_view():
    return (Title(site_title),
        NavBarContainer(
        NavBarLSide(H1("FastHTML Gallery Table View")),
        NavBarRSide(
            Button(submit=False)("Toggle Animations", onclick="toggleAnimations()"),
            A(Button("Card View"), href="/"),
            ghub_link)),
        Container(*[SectionTable(section) for section in directories]))

serve()
