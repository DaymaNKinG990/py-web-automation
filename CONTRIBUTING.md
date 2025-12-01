# Contributing to py-web-automation

Thank you for your interest in contributing to py-web-automation! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)
   - Code examples if applicable

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and examples
   - Potential implementation approach (if you have ideas)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow the code style (see below)
   - Add tests for new functionality
   - Update documentation
   - Ensure all tests pass
4. **Commit your changes**: Use clear, descriptive commit messages
5. **Push to your fork**: `git push origin feature/your-feature-name`
6. **Create a Pull Request**: Provide a clear description of changes

## Development Setup

### Prerequisites

- Python >= 3.12
- `uv` package manager (recommended) or `pip`

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/py-web-automation.git
   cd py-web-automation
   ```

2. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync --all-groups
   
   # Or using pip
   pip install -e ".[test,dev,all]"
   ```

3. **Install Playwright browsers** (for UI tests):
   ```bash
   playwright install
   ```

4. **Run tests**:
   ```bash
   uv run pytest
   ```

## Code Style

### Python Style

- Follow PEP 8 style guide
- Use type hints for all functions
- Maximum line length: 120 characters
- Use `ruff` for linting (configured in `pyproject.toml`)

### Code Formatting

```bash
# Format code
uv run ruff format .

# Check linting
uv run ruff check .
```

### Type Checking

```bash
# Run type checker
uv run pyright py_web_automation
```

### Docstrings

- Use Google-style docstrings
- Include Args, Returns, Raises, Example sections
- Write docstrings in English

Example:
```python
def example_function(param: str) -> int:
    """
    Brief description of function.

    Longer description explaining what the function does,
    its purpose, and any important details.

    Args:
        param: Description of parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When parameter is invalid

    Example:
        >>> result = example_function("test")
        >>> assert result == 42
    """
    pass
```

## Testing Guidelines

### Test Requirements

- All new code must have tests
- Maintain test coverage above 95%
- Use `pytest` for testing
- Use `allure.step()` in integration tests
- Use fixtures from `tests/fixtures/` for mocks

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=py_web_automation --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_api_client.py

# Run with Allure reports
uv run pytest --alluredir=allure-results
```

### Test Structure

- **Unit tests**: Test individual functions/classes in isolation
- **Integration tests**: Test interactions between components
- Use `@pytest.mark.unit` for unit tests
- Use `@pytest.mark.integration` for integration tests

### Test Naming

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Use descriptive names: `test_api_client_makes_get_request`

## Documentation

### Code Documentation

- All public functions/classes must have docstrings
- Include examples in docstrings
- Document parameters and return values

### User Documentation

- Update `docs/` files when adding features
- Add examples to `docs/examples.md`
- Update `docs/api-reference.md` for API changes
- Add troubleshooting tips to `docs/troubleshooting.md`

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add retry mechanism with exponential backoff

- Implement retry decorator with configurable attempts
- Add exponential backoff support
- Integrate with ApiClient

Closes #123
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

## Pull Request Process

1. **Ensure tests pass**: All tests must pass before submitting PR
2. **Update documentation**: Update relevant docs for your changes
3. **Add changelog entry**: Add entry to `CHANGELOG.md` (if applicable)
4. **Request review**: Assign reviewers and wait for feedback
5. **Address feedback**: Make requested changes
6. **Merge**: Once approved, maintainers will merge

## Project Structure

```
py-web-automation/
├── py_web_automation/     # Main package
│   ├── clients/           # Client implementations
│   ├── config.py         # Configuration
│   ├── exceptions.py     # Exception hierarchy
│   ├── validators.py     # Response validation
│   └── ...
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── fixtures/         # Test fixtures
├── docs/                  # Documentation
├── examples/              # Usage examples
└── pyproject.toml        # Project configuration
```

## Architecture Guidelines

### Design Principles

- **SOLID principles**: Follow SOLID design principles
- **Single Responsibility**: Each class should have one responsibility
- **DRY**: Don't Repeat Yourself
- **Type Safety**: Use type hints everywhere
- **Async-First**: Prefer async/await for I/O operations

### Adding New Clients

1. Inherit from `BaseClient`
2. Implement required methods
3. Add type hints and docstrings
4. Write unit and integration tests
5. Update documentation

### Adding New Features

1. Design the feature following existing patterns
2. Implement with tests
3. Add examples to documentation
4. Update API reference

## Questions?

- Open an issue for questions
- Check existing documentation
- Review existing code for patterns

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

