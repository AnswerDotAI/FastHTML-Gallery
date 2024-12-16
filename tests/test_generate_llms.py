import pytest
from pathlib import Path
from generate_llms import process_example, generate_category_llms

def test_process_example(tmp_path):
    # Create mock example directory
    example_dir = tmp_path / "test_example"
    example_dir.mkdir()

    # Create metadata.ini
    with open(example_dir / "metadata.ini", "w") as f:
        f.write("[REQUIRED]\n")
        f.write("ComponentName=Test Example\n")
        f.write("ComponentDescription=A test example\n")

    # Create app.py
    with open(example_dir / "app.py", "w") as f:
        f.write("print('test')\n")

    result = process_example(example_dir)
    assert result['name'] == "Test Example"
    assert result['description'] == "A test example"
    assert result['code'] == "print('test')\n"
