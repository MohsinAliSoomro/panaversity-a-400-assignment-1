---
name: pytest
description: Comprehensive Python testing with pytest framework, including test creation, fixtures, parameterized tests, and test execution. Use when Claude needs to work with Python testing for creating new tests, modifying existing tests, working with fixtures and test configuration, running tests with specific options, or debugging test failures.
---

# Pytest

## Overview

Pytest is a powerful testing framework for Python that makes it easy to write simple unit tests as well as complex functional testing. This skill provides guidance on pytest best practices, test creation, fixtures, and test execution patterns.

## Quick Start

### Basic Test Structure
```python
# content of test_sample.py
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4  # This should pass
```

### Key Conventions
- Test functions should start with `test_`
- Test files should start with `test_` or end with `_test.py`
- Use plain `assert` statements for testing

## Core Capabilities

### 1. Basic Test Creation
Create simple tests with assert statements:

```python
def test_addition():
    assert 2 + 2 == 4

def test_string_contains():
    text = "Hello, pytest!"
    assert "pytest" in text
```

### 2. Test Fixtures
Fixtures provide a baseline for tests and can set up preconditions and clean up after tests:

```python
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_list_length(sample_data):
    assert len(sample_data) == 5
```

### 3. Parameterized Tests
Run the same test with different inputs:

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 6),
    (4, 8),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### 4. Exception Testing
Test that specific exceptions are raised:

```python
def test_raises():
    with pytest.raises(ValueError):
        int("not_a_number")
```

## Test Execution

### Basic Commands
```bash
pytest                    # Run all tests in current directory
pytest test_file.py       # Run specific test file
pytest test_file.py::test_function  # Run specific test function
pytest -v                 # Verbose output
pytest -x                 # Stop after first failure
pytest --tb=short         # Short traceback format
```

### Running Specific Tests
```bash
pytest -k "test_name"     # Run tests matching pattern
pytest -m "marker_name"   # Run tests with specific marker
pytest --lf               # Run only the tests that failed in the last run
pytest --ff               # Run failed tests first
```

## Advanced Features

### Markers
Use markers to categorize and control test execution:

```python
import pytest

@pytest.mark.skip(reason="Not implemented yet")
def test_incomplete():
    pass

@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_python38_feature():
    pass

@pytest.mark.slow
def test_slow_function():
    pass
```

### Fixtures with Different Scopes
- `function`: Run once per test function (default)
- `class`: Run once per test class
- `module`: Run once per module
- `session`: Run once per test session

```python
@pytest.fixture(scope="session")
def database_connection():
    # Setup database connection once for all tests
    db = connect_to_db()
    yield db
    # Cleanup after all tests are done
    db.close()
```

### Setup and Teardown with Fixtures
```python
@pytest.fixture
def temporary_file(tmp_path):
    file_path = tmp_path / "temp.txt"
    file_path.write_text("test content")
    yield file_path  # This is where the test runs
    # Cleanup happens after the yield
    file_path.unlink()
```

## Best Practices

1. **Use descriptive test names** that explain what is being tested
2. **Follow the Arrange-Act-Assert pattern**: Set up data, perform action, assert result
3. **Keep tests focused** - one assertion per test when possible
4. **Use fixtures** to avoid code duplication across tests
5. **Use parametrized tests** for testing the same logic with different inputs
6. **Use markers** to categorize tests and control execution

## Configuration

Create a `pytest.ini`, `pyproject.toml`, or `setup.cfg` file to configure pytest:

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

Or in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests"
]
```

## Troubleshooting Common Issues

### Test Discovery Issues
- Ensure test files and functions follow naming conventions (`test_` prefix)
- Check that pytest can find your tests with `pytest --collect-only`

### Fixture Issues
- Make sure fixture names match between the fixture definition and test function parameter
- Check fixture scopes to ensure they're appropriate for your use case

### Assertion Failures
- Use `pytest -v` for verbose output to see which tests are running
- Use `pytest --tb=long` for detailed tracebacks
- Pytest provides detailed introspection for assertion failures without special methods
