import os
import configparser
import markdown
from pathlib import Path

def read_metadata(path):
    """Read metadata.ini file and return component info"""
    config = configparser.ConfigParser()
    config.read(path / 'metadata.ini')
    return {
        'name': config['REQUIRED']['ComponentName'],
        'description': config['REQUIRED']['ComponentDescription']
    }

def process_example(example_path):
    """Process a single example directory"""
    metadata = read_metadata(example_path)

    # Read app.py content
    with open(example_path / 'app.py', 'r') as f:
        code = f.read()

    # Read info.md if exists
    info_content = ""
    if (example_path / 'info.md').exists():
        with open(example_path / 'info.md', 'r') as f:
            info_content = f.read()

    return {
        'name': metadata['name'],
        'description': metadata['description'],
        'code': code,
        'info': info_content
    }

def generate_category_llms(category_path, category_name):
    """Generate llms.txt content for a category"""
    content = [f"# {category_name}\n"]
    content.append("> A collection of FastHTML examples demonstrating various use cases and patterns.\n")

    examples = []
    for example_dir in category_path.iterdir():
        if example_dir.is_dir():
            example = process_example(example_dir)
            examples.append(example)

    # Add examples section
    content.append("## Examples\n")
    for example in examples:
        content.append(f"- [{example['name']}](examples/{example['name']}.md): {example['description']}\n")

        # Create individual example markdown file
        example_md = Path('examples') / f"{example['name']}.md"
        example_md.parent.mkdir(exist_ok=True)
        with open(example_md, 'w') as f:
            f.write(f"# {example['name']}\n\n")
            f.write(f"> {example['description']}\n\n")
            if example['info']:
                f.write(example['info'] + "\n\n")
            f.write("## Implementation\n\n```python\n")
            f.write(example['code'] + "\n```\n")

    return '\n'.join(content)

def main():
    base_path = Path('examples')
    output_path = Path('llms')
    output_path.mkdir(exist_ok=True)

    # Generate main llms.txt
    main_content = ["# FastHTML Gallery\n"]
    main_content.append("> A collection of FastHTML examples demonstrating various use cases and patterns.\n")
    main_content.append("## Categories\n")

    for category in base_path.iterdir():
        if category.is_dir():
            category_name = category.name.replace('_', ' ').title()
            main_content.append(f"- [{category_name}](categories/{category_name}.md)\n")

            # Generate category llms.txt
            category_content = generate_category_llms(category, category_name)
            category_md = output_path / 'categories' / f"{category_name}.md"
            category_md.parent.mkdir(exist_ok=True)
            with open(category_md, 'w') as f:
                f.write(category_content)

    # Write main llms.txt
    with open(output_path / 'llms.txt', 'w') as f:
        f.write('\n'.join(main_content))

if __name__ == '__main__':
    main()
