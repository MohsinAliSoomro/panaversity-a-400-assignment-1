#!/usr/bin/env python3
"""
Pytest helper script - Generate basic test structure

This script helps generate basic pytest test structure for a given Python file.
It creates a test file with basic tests based on the functions in the original file.
"""

import ast
import sys
from pathlib import Path


def extract_function_names(file_path):
    """Extract function names from a Python file."""
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    return functions


def generate_test_content(original_file, functions):
    """Generate basic test content for the given functions."""
    module_name = Path(original_file).stem
    test_content = f'''import pytest
from {module_name} import {', '.join(functions) if functions else '*'}


'''

    for func_name in functions:
        test_content += f'''def test_{func_name}():
    """Test for {func_name} function."""
    # TODO: Add proper test cases for {func_name}
    pass


'''

    return test_content


def main():
    if len(sys.argv) < 2:
        print("Usage: example.py <path_to_python_file> [output_file]")
        print("Example: example.py calculator.py test_calculator.py")
        return

    input_file = sys.argv[1]

    if not Path(input_file).exists():
        print(f"Error: File {input_file} does not exist")
        return

    # Extract function names from the input file
    try:
        functions = extract_function_names(input_file)
    except Exception as e:
        print(f"Error parsing {input_file}: {e}")
        return

    # Generate test content
    test_content = generate_test_content(input_file, functions)

    # Determine output file name
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        input_path = Path(input_file)
        output_file = f"test_{input_path.name}"

    # Write test file
    try:
        with open(output_file, 'w') as f:
            f.write(test_content)
        print(f"Generated test file: {output_file}")
        print(f"Functions found: {functions}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")


if __name__ == "__main__":
    main()
