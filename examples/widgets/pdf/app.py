from fasthtml.common import *
from ui_examples import show_code, hdrs_tailwind_franken_highlightJS_markdownJS
app, rt = fast_app(hdrs=hdrs_tailwind_franken_highlightJS_markdownJS())
    
@rt('/')
@show_code
def homepage():
    pdf_path = 'https://arxiv.org/pdf/1706.03762'
    return Embed(src=pdf_path, type='application/pdf',
                 width='100%', height='1000px')
