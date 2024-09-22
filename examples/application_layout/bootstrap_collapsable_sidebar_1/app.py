from fasthtml.common import *
from collections import namedtuple

cdn = 'https://cdn.jsdelivr.net/npm/bootstrap'
bootstrap_links = [
    Link(href=cdn+"@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet"),
    Script(src=cdn+"@5.3.3/dist/js/bootstrap.bundle.min.js"),
    Link(href=cdn+"-icons@1.11.3/font/bootstrap-icons.min.css", rel="stylesheet")
]

app, rt = fast_app(hdrs=bootstrap_links)

def SidebarItem(text, hx_get, hx_target, **kwargs):
    return Div(
        I(cls=f'bi bi-{text}'),
        Span(text),
        hx_get=hx_get, hx_target=hx_target,
        data_bs_parent='#sidebar', role='button',
        cls='list-group-item border-end-0 d-inline-block text-truncate',
        **kwargs)

def Sidebar(sidebar_items, hx_get, hx_target):
    return Div(
        Div(*(SidebarItem(o, f"{hx_get}?menu={o}", hx_target) for o in sidebar_items),
            id='sidebar-nav',
            cls='list-group border-0 rounded-0 text-sm-start min-vh-100'
        ),
        id='sidebar',
        cls='collapse collapse-horizontal show border-end')

sidebar_items = ('Film', 'Heart', 'Bricks', 'Clock', 'Archive', 'Gear', 'Calendar', 'Envelope')

@app.get('/')
def homepage():
    return Div(
        Div(
            Div(
                Sidebar(sidebar_items, hx_get='menucontent', hx_target='#current-menu-content'),
                cls='col-auto px-0'),
            Main(
                A(I(cls='bi bi-list bi-lg py-2 p-1'), 'Menu',
                  href='#', data_bs_target='#sidebar', data_bs_toggle='collapse', aria_expanded='false', aria_controls='sidebar',
                  cls='border rounded-3 p-1 text-decoration-none'),
                Div(
                  Div(
                    Div(
                    H1("Click a sidebar menu item"),
                    P("They each have their own content"),
                    id="current-menu-content"),
                    cls='col-12'
                ), cls='row'),
                cls='col ps-md-2 pt-2'),
            cls='row flex-nowrap'),
        cls='container-fluid')

@app.get('/menucontent')
def menucontent(menu: str):
    return Div(
        H1(f"{menu} Content"),
        P(f"This is the content for the {menu} menu item."),
        id="current-menu-content")
