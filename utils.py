from pathlib import Path
from fasthtml.common import *
from configparser import ConfigParser

__all__ = ['toggle_script','get_social_links']

def get_social_links(dir_path):
    metadata = ConfigParser()
    metadata.read(dir_path/'metadata.ini')
    meta = metadata['REQUIRED']
    return Socials(title=meta['ComponentName'], description=meta['ComponentDescription'], site_name='gallery.fastht.ml', twitter_site='@isaac_flath', image=f"/files/{dir_path/'card_thumbnail.png'}", url='')

toggle_script = Script("""
    function toggleAnimations() {
        const images = document.querySelectorAll('.card-img-top');
        images.forEach(img => {
            if (img.src.endsWith('.gif')) {
                img.src = img.getAttribute('data-png');
            } else {
                img.setAttribute('data-png', img.src);
                img.src = img.src.replace('card_thumbnail.png', 'card_thumbnail.gif');
            }
        });
    }""")