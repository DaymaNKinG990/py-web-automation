# Integration Test Cases

## Overview

This directory contains test case documentation for integration tests of the web automation testing framework. Integration tests verify the interaction between multiple components and real services.

## Structure

Integration tests are organized by component interactions:

1. **end_to_end.md** - End-to-end workflows (full user journeys)
2. **external_services.md** - Integration with external services (HTTP endpoints, browser automation)
3. **db_client_integration.md** - Integration for DBClient with all components
4. **graphql_client.md** - Integration for GraphQLClient
5. **soap_client.md** - Integration for SoapClient
6. **websocket_client.md** - Integration for WebSocketClient
7. **grpc_client.md** - Integration for GrpcClient
8. **request_builder.md** - Integration for RequestBuilder
9. **validators.md** - Integration for validators module
10. **SUMMARY.md** - Summary of all integration test cases
11. **MISSING_INTEGRATION_TEST_CASES.md** - Analysis of missing integration test cases (reference)

## Test Categories

### 1. Component Integration Tests
Tests that verify interaction between two or more components:
- ApiClient ↔ DBClient - see [db_client_integration.md](./db_client_integration.md)
- UiClient ↔ DBClient - see [db_client_integration.md](./db_client_integration.md)
- GraphQLClient ↔ Validators - see [graphql_client.md](./graphql_client.md)
- SoapClient ↔ Validators - see [soap_client.md](./soap_client.md)
- WebSocketClient ↔ ApiClient - see [websocket_client.md](./websocket_client.md)
- RequestBuilder ↔ Validators - see [request_builder.md](./request_builder.md)
- Config ↔ All components

### 2. End-to-End Tests
Complete user workflows:
- API + UI testing workflow
- Database-backed application testing
- Multi-protocol integration (REST + GraphQL, REST + SOAP, WebSocket + REST)
- RequestBuilder integration workflow
- Response validation integration workflow

### 3. External Service Integration
Tests with real or mocked external services:
- HTTP endpoints
- Browser automation (Playwright)
- Network conditions
- Security (SSL/TLS)

## Test Case Format

Each test case follows this structure:

```
#### TC-INTEGRATION-XXX: Test Name
- **Purpose**: What this test verifies
- **Preconditions**: Required setup and state
- **Test Steps**:
  1. Step 1
  2. Step 2
  3. Step 3
- **Expected Result**: What should happen
- **Coverage**: Which components/interactions are tested
- **Dependencies**: External services or data required
```

## Markers

Integration tests use the `@pytest.mark.integration` marker and may also use:
- `@pytest.mark.slow` - Tests that take significant time
- `@pytest.mark.external` - Tests requiring external services
- `@pytest.mark.async` - Async integration tests

## Notes

- Integration tests may require real services or test accounts
- Some tests may be skipped in CI/CD if external services are unavailable
- Integration tests should be isolated and not depend on execution order
- Use mock servers or fixtures where possible for CI/CD environments
