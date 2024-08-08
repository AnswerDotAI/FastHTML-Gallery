from pathlib import Path
from fasthtml.common import *
from configparser import ConfigParser

__all__ = ['get_module_path','get_route','create_image_cards','toggle_script','strip_parent_route','get_social_links']

def get_module_path(p,base_dir):
    return f'{base_dir}.{".".join(Path(p).parts[1:])}.app'

def get_route(p,ext=None):
    route =  f"/{'/'.join(Path(p).parts[1:])}"
    if ext: route += f"/{ext}"
    return route

def create_image_cards(n, ps, image_card_fn):
    return Div(
        H2(n, style="color: #333; font-weight: 600; border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px;"),
        Div(*[image_card_fn(p) for p in ps], cls="row")
)


def get_social_links(dir_path):
    metadata = ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']
    return Socials(title=meta['ComponentName'], description=meta['ComponentDescription'], site_name='fasthtml.gallery', twitter_site='@isaac_flath', image=f"/{dir_path/'img.png'}", url='')




toggle_script = Script("""
    function toggleAnimations() {
        const images = document.querySelectorAll('.card-img-top');
        images.forEach(img => {
            if (img.src.endsWith('.gif')) {
                img.src = img.getAttribute('data-png');
            } else {
                img.setAttribute('data-png', img.src);
                img.src = img.src.replace('img.png', 'gif.gif');
            }
        });
    }""")

def strip_parent_route(text, parent_route):
    htmx_route_methods = ['hx_get', 'hx_post', 'hx_delete', 'hx_put', 'hx_patch']
    for method in htmx_route_methods:
        pattern = f'({method}=(f?[\'"]))/({parent_route})(/[^\'"]*)(\\2|\'|")'
        replacement = r'\1\4\5'
        text = re.sub(pattern, replacement, text)
    return text