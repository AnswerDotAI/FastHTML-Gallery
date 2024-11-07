from fasthtml.common import *
app, rt = fast_app()

@rt
def index():
    pdf_path = 'https://arxiv.org/pdf/1706.03762'
    return Embed(src=pdf_path, type='application/pdf',
                 width='100%', height='1000px')

serve()