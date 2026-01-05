# Pytest Comprehensive Reference Guide

## Pytest Command Line Options

### Basic Options
- `-v`, `--verbose`: Increase verbosity
- `-q`, `--quiet`: Decrease verbosity
- `-x`: Stop after first failure
- `--maxfail=num`: Exit after num failures or errors
- `-l`, `--showlocals`: Show local variables in tracebacks
- `--tb=style`: Traceback print mode (auto/long/short/line/native/no)

### Test Selection
- `-k expression`: Only run tests that match the expression
- `-m marker`: Only run tests marked with the specified marker
- `--lf`, `--last-failed`: Rerun only the tests that failed at the last run
- `--ff`, `--failed-first`: Run all tests, but run the last failures first

### Fixtures
- `--fixtures`: Show available fixtures
- `--fixtures-per-test`: Show fixtures per test
- `--setup-plan`: Show what fixtures and tests would be run
- `--setup-show`: Show setup of fixtures
- `--setup-only`: Show setup of fixtures, don't execute tests

### Reporting
- `--resultlog=path`: Path for machine-readable result log
- `--junitxml=path`: Create junit-xml style report
- `--junit-prefix=prefix`: Prefix for test names in junit-xml
- `--collect-only`: Only collect tests, don't execute them

## Pytest Markers Reference

### Built-in Markers
- `@pytest.mark.skip(reason=None)`: Skip the test
- `@pytest.mark.skipif(condition, reason=None)`: Skip the test if condition is True
- `@pytest.mark.xfail(condition=None, reason=None, run=True, raises=None, strict=False)`: Mark the test as expected to fail
- `@pytest.mark.parametrize(argnames, argvalues)`: Parametrize the test
- `@pytest.mark.usefixtures(*fixturenames)`: Mark tests as needing specified fixtures
- `@pytest.mark.timeout(timeout)`: Mark test to timeout after specified seconds

### Custom Markers
Custom markers can be defined in `pytest.ini` or `pyproject.toml`:
```ini
[tool:pytest]
markers =
    slow: marks tests as slow
    fast: marks tests as fast
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    smoke: marks tests as smoke tests
```

## Pytest Fixtures Reference

### Built-in Fixtures
- `tmp_path`: Provides a temporary directory unique to the test invocation
- `tmp_path_factory`: Factory for temporary directories (session-scoped)
- `capsys`: Capture sys.stdout and sys.stderr
- `capsysbinary`: Capture sys.stdout and sys.stderr in binary mode
- `capfd`: Capture file descriptors stdout and stderr
- `capfdbinary`: Capture file descriptors stdout and stderr in binary mode
- `monkeypatch`: Temporarily modify classes, functions, or other objects
- `pytestconfig`: Access to the pytest config object
- `record_property`: Add extra properties to the test
- `record_testsuite_property`: Add extra properties to the test

### Fixture Scopes
- `function`: Run once per test function (default)
- `class`: Run once per test class
- `module`: Run once per module
- `package`: Run once per package
- `session`: Run once per test session

### Fixture Parameters
```python
@pytest.fixture(scope="function", params=[1, 2, 3])
def param_fixture(request):
    return request.param

def test_with_param(param_fixture):
    assert param_fixture > 0
```

## Pytest Hooks

### Initialization Hooks
- `pytest_addoption(parser)`: Add command-line options
- `pytest_configure(config)`: Modify configuration
- `pytest_cmdline_main(config)`: Main command-line entry point

### Collection Hooks
- `pytest_collect_file(path, parent)`: Process a file for collection
- `pytest_pycollect_makemodule(path, parent)`: Create a Module collector
- `pytest_pycollect_makeitem(collector, name, obj)`: Make a PyCollector for a Python object

### Test Running Hooks
- `pytest_runtest_setup(item)`: Called for performing the setup phase
- `pytest_runtest_call(item)`: Called to run the test item
- `pytest_runtest_teardown(item, nextitem)`: Called after pytest_runtest_call

## Pytest Configuration Files

### pytest.ini
```ini
[tool:pytest]
minversion = 6.0
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    fast: marks tests as fast
    integration: marks tests as integration tests
```

### pyproject.toml
```toml
[tool.pytest.ini_options]
minversion = "6.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = ["-v", "--tb=short"]
markers = [
    "slow: marks tests as slow",
    "fast: marks tests as fast",
    "integration: marks tests as integration tests"
]
```

### setup.cfg
```ini
[tool:pytest]
minversion = 6.0
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    fast: marks tests as fast
    integration: marks tests as integration tests
```

## Common Pytest Patterns

### Arrange-Act-Assert Pattern
```python
def test_user_authentication():
    # Arrange
    user = User("test@example.com", "password")
    auth_service = AuthService()

    # Act
    result = auth_service.authenticate(user)

    # Assert
    assert result is True
```

### Given-When-Then Pattern
```python
def test_calculator_addition():
    # Given a calculator instance
    calc = Calculator()

    # When adding two numbers
    result = calc.add(2, 3)

    # Then the result should be correct
    assert result == 5
```

### Test Data Builders
```python
@pytest.fixture
def user_builder():
    def _create_user(email="test@example.com", active=True):
        return User(email=email, active=active)
    return _create_user

def test_user_creation(user_builder):
    user = user_builder(email="new@example.com")
    assert user.email == "new@example.com"
```

## Pytest Plugins

### Popular Plugins
- `pytest-cov`: Code coverage reporting
- `pytest-mock`: Mock utility
- `pytest-django`: Django testing
- `pytest-flask`: Flask testing
- `pytest-asyncio`: Async testing
- `pytest-bdd`: Behavior-driven development
- `pytest-html`: HTML reports
- `pytest-xdist`: Parallel test execution

### Installing Plugins
```bash
pip install pytest-cov pytest-mock pytest-xdist
```

### Using Plugins
```bash
# With coverage
pytest --cov=myproject --cov-report=html

# With parallel execution
pytest -n auto

# With HTML report
pytest --html=report.html
```

## Best Practices for Large Test Suites

### Test Organization
```
tests/
├── unit/           # Unit tests
│   ├── models/
│   ├── views/
│   └── utils/
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
├── conftest.py    # Shared fixtures
└── fixtures/      # Data fixtures
```

### Performance Optimization
- Use appropriate fixture scopes
- Use `--lf` and `--ff` for faster feedback
- Parallelize tests with `pytest-xdist`
- Use `--maxfail` to stop early on failures
- Use `--cache-clear` to clear cache when needed

### Test Maintenance
- Keep tests independent
- Use descriptive test names
- Follow naming conventions
- Document complex test scenarios
- Regularly review and refactor tests
