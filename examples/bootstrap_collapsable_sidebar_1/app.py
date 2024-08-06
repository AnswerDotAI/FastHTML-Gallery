from fasthtml.common import *
from collections import namedtuple

bootstrap_links = [
    Link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet", integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH", crossorigin="anonymous"),
    Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js", integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz", crossorigin="anonymous"),
    Link(href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css", rel="stylesheet")
]

app, rt = fast_app(hdrs=bootstrap_links)

def create_sidebar_item(icon_class, text, hx_get, hx_target, **kwargs):
    return Div(
        I(cls=f'bi {icon_class}'),
        Span(text),
        cls='list-group-item border-end-0 d-inline-block text-truncate',
        hx_get=hx_get,
        hx_target=hx_target,
        data_bs_parent='#sidebar',
        **kwargs
    )

def create_sidebar(sidebar_items, hx_get, hx_target):
    return Div(
        Div(*(create_sidebar_item(item.icon, item.label, f"{hx_get}?menu={item.label}", hx_target) for item in sidebar_items),
            id='sidebar-nav',
            cls='list-group border-0 rounded-0 text-sm-start min-vh-100'
        ),
        id='sidebar',
        cls='collapse collapse-horizontal show border-end'
    )

SidebarItem = namedtuple('SidebarItem', ['icon', 'label'])
sidebar_items = (
    SidebarItem('bi-film', 'Film'),
    SidebarItem('bi-heart', 'Heart'),
    SidebarItem('bi-bricks', 'Bricks'),
    SidebarItem('bi-clock', 'Clock'),
    SidebarItem('bi-archive', 'Archive'),
    SidebarItem('bi-gear', 'Gear'),
    SidebarItem('bi-calendar', 'Calendar'),
    SidebarItem('bi-envelope', 'Envelope'),
)

@app.get('/')
def homepage():
    return Div(
        Div(
            Div(create_sidebar(sidebar_items, hx_get='/bootstrap_collapsable_sidebar_1/menucontent', hx_target='#current-menu-content'), cls='col-auto px-0'),
            Main(
                A(I(cls='bi bi-list bi-lg py-2 p-1'), 'Menu',
                  href='#', data_bs_target='#sidebar', data_bs_toggle='collapse',
                  cls='border rounded-3 p-1 text-decoration-none'),
                Div(
                  Div(
                    Div(
                    H1("Click a sidebar menu item"),
                    P("They each have their own content"),
                    id="current-menu-content"),
                    cls='col-12'
                ), cls='row'),
                cls='col ps-md-2 pt-2'
            ),
            cls='row flex-nowrap'
        ),
        cls='container-fluid'
    )

@app.get('/menucontent')
def menucontent(menu: str):
    return Div(
        H1(f"{menu} Content"),
        P(f"This is the content for the {menu} menu item."),
        id="current-menu-content"
    )
