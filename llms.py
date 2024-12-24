import httpx
from pathlib import Path
    
def llms_txt():
    """Creates llms.txt containing index of example FastHTML apps"""
    # Get all app.py files and their categories 
    examples = Path.cwd()/'examples'

    # Group files by category
    by_cat = {}
    for f in examples.rglob('app.py'):
        cat = f.relative_to(examples).parts[0]
        by_cat.setdefault(cat,[]).append((f.parent.name, f.relative_to(examples)))

    # Create content with categories and examples
    lines = ['# FastHTML Gallery Examples\n',
             '> FastHTML Gallery bring minimal examples of FastHTML apps to allow you to get started with FastHTML more easily\n']
    for cat in sorted(by_cat):
        lines.append(f'\n## {cat.replace("_"," ").title()}')
        for name,path in sorted(by_cat[cat]):
            # Create raw github link
            raw_link = f'https://github.com/AnswerDotAI/fasthtml-gallery/blob/main/examples/{path}'
            lines.append(f'- {name.replace("_"," ").title()}({raw_link})')

    # Write to file
    (examples.parent/'llms.txt').write_text('\n'.join(lines))
    

def llms_ctx_txt():
    """Creates llms_ctx.txt containing XML-formatted index of example FastHTML apps with source code"""
    # Get all app.py files and their categories
    examples = Path.cwd()/'examples'
    
    # Group files by category
    by_cat = {}
    for f in examples.rglob('app.py'):
        cat = f.relative_to(examples).parts[0]
        by_cat.setdefault(cat,[]).append((f.parent.name, f.relative_to(examples)))

    # Create XML-style content
    lines = ['<document>',
            '<title>FastHTML Gallery Examples</title>',
            '<description>FastHTML Gallery bring minimal examples of FastHTML apps to allow you to get started with FastHTML more easily</description>']
    
    for cat in sorted(by_cat):
        lines.append(f'<category name="{cat.replace("_"," ").title()}">')
        for name, path in sorted(by_cat[cat]):
            # Get raw github content
            raw_url = f'https://raw.githubusercontent.com/AnswerDotAI/fasthtml-gallery/main/examples/{path}'
            r = httpx.get(raw_url)
            source_code = r.text
            
            lines.append(f'  <example name="{name.replace("_"," ").title()}">')
            lines.append(source_code)
            lines.append('  </example>')
        lines.append('</category>')
    
    lines.append('</document>')

    # Write to file 
    (examples.parent/'llms_ctx.txt').write_text('\n'.join(lines))
    
    

if __name__ == '__main__':
    llms_txt()
    llms_ctx_txt()
