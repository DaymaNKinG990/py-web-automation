# Testing Documentation

This document provides comprehensive information about testing in the Web Automation Framework, including test structure, coverage, and guidelines.

## Overview

The Web Automation Framework has comprehensive test coverage with both unit and integration tests. The test suite ensures reliability, correctness, and maintainability of the framework.

## Test Structure

### Unit Tests

Unit tests are located in `tests/unit/` and cover individual components in isolation:

- **Config** - Configuration management and validation
- **HttpClient** - HTTP REST API client
- **GraphQLClient** - GraphQL API client
- **GrpcClient** - gRPC client
- **SoapClient** - SOAP client
- **WebSocketClient** - WebSocket client
- **AsyncUiClient** - Browser automation client (async)
- **Database Clients** - SQLiteClient, PostgreSQLClient, MySQLClient
- **Models** - Data models (HttpResult, GraphQLResult, etc.)
- **RequestBuilder** - Request builder pattern
- **Middleware** - Request/response processing middleware

### Integration Tests

Integration tests are located in `tests/integration/` and verify interactions between components:

- **HttpClient + Database Clients** - Integration between API and database testing
- **AsyncUiClient + Database Clients** - Integration between UI and database testing
- **End-to-End** - Complete workflows from start to finish
- **External Services** - Integration with real external services (optional)

## Test Case Documentation

Detailed test case specifications are documented in:

- `test_cases/unit/` - Unit test case specifications
- `test_cases/integration/` - Integration test case specifications

Each test case document includes:
- Test purpose and scope
- Preconditions
- Test steps
- Expected results
- Code coverage information

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Unit Tests Only

```bash
pytest tests/unit/
```

### Run Integration Tests Only

```bash
pytest tests/integration/
```

### Run with Coverage

```bash
pytest --cov=py_web_automation --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/unit/test_config.py
```

### Run Specific Test

```bash
pytest tests/unit/test_config.py::TestConfig::test_init_with_valid_data
```

## Test Coverage

### Current Coverage Status

- **Unit Tests**: Comprehensive coverage across all components
- **Integration Tests**: Coverage for component interactions
  - HttpClient + Database Clients: Integration tests
  - AsyncUiClient + Database Clients: Integration tests
  - End-to-End: Complete workflow tests
  - External Services: Optional (requires real external services)

### Coverage Goals

- ✅ **Unit Tests**: High coverage across all components
- ⏳ **Integration Tests**: Target comprehensive coverage (excluding external services tests)

## Test Categories

### Unit Test Categories

1. **Initialization Tests** - Verify proper object creation
2. **Validation Tests** - Test input validation and error handling
3. **Method Tests** - Test individual methods and their behavior
4. **Edge Case Tests** - Test boundary conditions and unusual inputs
5. **Error Handling Tests** - Verify proper error handling

### Integration Test Categories

1. **Component Integration** - Test interactions between two components
2. **End-to-End Workflows** - Test complete user journeys
3. **Error Recovery** - Test error handling across components
4. **Performance** - Test system performance under load
5. **External Services** - Test with real external services (optional)

## Test Fixtures

The framework uses pytest fixtures for test setup and teardown:

- `valid_config` - Valid configuration object
- `http_client_with_config` - HttpClient instance
- `ui_client_with_config` - AsyncUiClient instance
- `db_client_with_config` - Database client instance
- `mock_api_url` - Mock API URL
- `mock_response` - Mock HTTP response

## Writing Tests

### Unit Test Example

```python
@pytest.mark.asyncio
async def test_make_request_get_method(
    self, mocker, api_client_with_config, mock_httpx_response_200
):
    """Test make_request with GET method."""
    api_client_with_config.client.request = mocker.AsyncMock(
        return_value=mock_httpx_response_200
    )

    result = await api_client_with_config.make_request("/api/status", method="GET")

    assert result.status_code == 200
    assert result.success is True
```

### Integration Test Example

```python
@pytest.mark.asyncio
async def test_api_and_database_integration(
    self, api_client_with_config, db_client_with_config
):
    """Test API and database integration."""
    # Test API endpoint
    result = await api_client_with_config.make_request("/api/users", method="GET")
    assert result.success is True
    
    # Verify data in database
    users = await db_client_with_config.execute_query("SELECT * FROM users")
    assert len(users) > 0
```

## External Services Testing

Some integration tests require real external services. These tests are documented in `test_cases/integration/external_services.md` and include:

- Real HTTP/HTTPS endpoints
- Real browser automation
- Real database connections
- Network testing scenarios

These tests are optional and can be skipped in CI/CD environments where external services are not available.

## Best Practices

1. **Isolation** - Each test should be independent and not rely on other tests
2. **Mocking** - Use mocks for external dependencies to keep tests fast and reliable
3. **Clear Names** - Use descriptive test names that explain what is being tested
4. **Documentation** - Document complex test scenarios and edge cases
5. **Coverage** - Aim for high coverage but focus on meaningful tests
6. **Performance** - Keep tests fast; use async/await appropriately

## Continuous Integration

Tests are automatically run in CI/CD pipelines:

- All unit tests must pass
- Integration tests (excluding external services) must pass
- Code coverage must meet minimum threshold (configured in `pyproject.toml`)
- Linting and type checking must pass

## Troubleshooting Tests

### Common Issues

1. **Import Errors** - Ensure all dependencies are installed
2. **Async Issues** - Use `@pytest.mark.asyncio` for async tests
3. **Mock Issues** - Ensure mocks are set up before use
4. **Fixture Issues** - Check fixture scope and dependencies
5. **Browser Issues** - Ensure Playwright browsers are installed

### Getting Help

- Check test case documentation in `test_cases/`
- Review existing tests for examples
- Check pytest documentation for advanced features
