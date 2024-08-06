from fasthtml.common import *

hdrs = (MarkdownJS(), HighlightJS(langs=['python', 'javascript', 'html', 'css']), )

app, rt = fast_app(hdrs=hdrs)
    

markdown = """# Some Basic Markdown Components

- List
- Codeblock
- Headers

```python

import requests
response = requests.get('https://fasthtml.gallery')
print(response.text)
```

"""
def homepage():
    return Div(Div(markdown, cls='marked'))

@rt('/')
def get(): 
    return homepage()