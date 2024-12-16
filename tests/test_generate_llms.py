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

def test_generate_category_llms_expanded(tmp_path):
    """Test generation of expanded category content"""
    # Create category directory
    category_dir = tmp_path / "test_category"
    category_dir.mkdir()

    # Create example directory
    example_dir = category_dir / "test_example"
    example_dir.mkdir()

    # Create metadata.ini
    with open(example_dir / "metadata.ini", "w") as f:
        f.write("[REQUIRED]\n")
        f.write("ComponentName=Test Example\n")
        f.write("ComponentDescription=A test example\n")

    # Create app.py
    with open(example_dir / "app.py", "w") as f:
        f.write("print('test')\n")

    # Test basic expanded content (llms-ctx)
    content = generate_category_llms(category_dir, "Test Category", expanded=True)
    assert "# Test Example" in content
    assert "> A test example" in content
    assert "```python" in content
    assert "print('test')" in content
    assert "info.md content" not in content

def test_generate_category_llms_full(tmp_path):
    """Test generation of full expanded category content"""
    # Create category directory
    category_dir = tmp_path / "test_category"
    category_dir.mkdir()

    # Create example directory
    example_dir = category_dir / "test_example"
    example_dir.mkdir()

    # Create metadata.ini
    with open(example_dir / "metadata.ini", "w") as f:
        f.write("[REQUIRED]\n")
        f.write("ComponentName=Test Example\n")
        f.write("ComponentDescription=A test example\n")

    # Create app.py
    with open(example_dir / "app.py", "w") as f:
        f.write("print('test')\n")

    # Create info.md
    with open(example_dir / "info.md", "w") as f:
        f.write("# Additional Info\nThis is a test example with documentation.\n")

    # Test full expanded content (llms-ctx-full)
    content = generate_category_llms(category_dir, "Test Category", expanded=True, full=True)
    assert "# Test Example" in content
    assert "> A test example" in content
    assert "```python" in content
    assert "print('test')" in content
    assert "# Additional Info" in content
    assert "This is a test example with documentation" in content

def test_generate_category_llms_multiple_examples(tmp_path):
    """Test generation of category content with multiple examples"""
    # Create category directory
    category_dir = tmp_path / "test_category"
    category_dir.mkdir()

    # Create two example directories
    for i in range(2):
        example_dir = category_dir / f"test_example_{i}"
        example_dir.mkdir()

        # Create metadata.ini
        with open(example_dir / "metadata.ini", "w") as f:
            f.write("[REQUIRED]\n")
            f.write(f"ComponentName=Test Example {i}\n")
            f.write(f"ComponentDescription=A test example {i}\n")

        # Create app.py
        with open(example_dir / "app.py", "w") as f:
            f.write(f"print('test_{i}')\n")

    # Test expanded content with multiple examples
    content = generate_category_llms(category_dir, "Test Category", expanded=True)
    assert "# Test Example 0" in content
    assert "# Test Example 1" in content
    assert "print('test_0')" in content
    assert "print('test_1')" in content
