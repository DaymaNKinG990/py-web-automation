# End-to-End Test Cases

## Overview
Complete user journey tests that verify full workflows from start to finish for web automation testing.

## Test Categories

### 1. Complete Testing Workflows

#### TC-INTEGRATION-E2E-001: Full workflow: Test API → Test UI
- **Purpose**: Verify complete testing workflow combining API and UI components
- **Preconditions**:
  - Web application with both API and UI
  - Valid base URL
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Test API endpoints using `make_request()`
  3. Create `UiClient` with same base URL
  4. Setup browser and test UI elements
  5. Verify both API and UI tests pass
  6. Clean up resources
- **Expected Result**: Complete workflow executes successfully
- **Coverage**: Full integration of API and UI components
- **Dependencies**: Complete web application setup

#### TC-INTEGRATION-E2E-002: Full workflow with authentication
- **Purpose**: Verify complete workflow with authentication
- **Preconditions**: Web application requiring authentication
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Authenticate using `set_auth_token()`
  3. Test authenticated API endpoints
  4. Create `UiClient` and setup browser
  5. Navigate to application
  6. Verify authenticated UI access
  7. Test authenticated UI interactions
- **Expected Result**: Authentication works in full workflow
- **Coverage**: Authentication integration
- **Dependencies**: Web application with auth

#### TC-INTEGRATION-E2E-003: Multiple applications testing workflow
- **Purpose**: Verify testing multiple applications in sequence
- **Preconditions**: Multiple web applications available
- **Test Steps**:
  1. Create `ApiClient` for Application 1
  2. Test Application 1 (API + UI)
  3. Create `ApiClient` for Application 2
  4. Test Application 2 (API + UI)
  5. Verify both tested successfully
- **Expected Result**: Multiple applications tested successfully
- **Coverage**: Multiple applications handling
- **Dependencies**: Multiple web applications

### 2. Authentication Workflows

#### TC-INTEGRATION-E2E-004: Authenticate and test application
- **Purpose**: Verify authentication flow with web application
- **Preconditions**: Web application requiring authentication
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Authenticate using `set_auth_token()`
  3. Use authenticated token for API requests
  4. Create `UiClient` and setup browser
  5. Test UI with authenticated session
  6. Verify authentication persists across requests
- **Expected Result**: Authentication flow works correctly
- **Coverage**: Authentication integration
- **Dependencies**: Web application with auth

#### TC-INTEGRATION-E2E-005: Session management workflow
- **Purpose**: Verify session management across components
- **Preconditions**: Config with authentication settings
- **Test Steps**:
  1. Create Config with timeout and retry settings
  2. Create `ApiClient` with Config
  3. Authenticate and verify session is used
  4. Test API endpoints
  5. Disconnect and reconnect
  6. Verify session persists
- **Expected Result**: Session management works correctly
- **Coverage**: Session management integration
- **Dependencies**: Valid config

### 3. Data Flow Workflows

#### TC-INTEGRATION-E2E-006: API to UI data flow
- **Purpose**: Verify data flow from API to UI
- **Preconditions**: Web application with API and UI
- **Test Steps**:
  1. Create `ApiClient` and fetch data via API
  2. Extract data from API response
  3. Create `UiClient` and setup browser
  4. Navigate to UI
  5. Verify UI displays data from API
  6. Verify data matches API response
- **Expected Result**: Data flows correctly from API to UI
- **Coverage**: Data flow integration
- **Dependencies**: Web application with API and UI

#### TC-INTEGRATION-E2E-007: UI to API data flow
- **Purpose**: Verify data flow from UI to API
- **Preconditions**: Web application with forms that submit to API
- **Test Steps**:
  1. Create `UiClient` and setup browser
  2. Navigate to application
  3. Fill form in UI
  4. Submit form through UI
  5. Verify data submitted via API using `ApiClient`
  6. Verify data was received correctly
- **Expected Result**: Data flows correctly from UI to API
- **Coverage**: Reverse data flow integration
- **Dependencies**: Web application with form submission

### 4. Error Recovery Workflows

#### TC-INTEGRATION-E2E-008: Recover from connection error
- **Purpose**: Verify error recovery in full workflow
- **Preconditions**: Network that can be interrupted
- **Test Steps**:
  1. Start workflow: connect, test API
  2. Simulate network interruption
  3. Verify error is detected
  4. Reconnect `ApiClient`
  5. Retry API operations
  6. Verify workflow continues successfully
- **Expected Result**: Error recovery works correctly
- **Coverage**: Error recovery integration
- **Dependencies**: Network interruption simulation

#### TC-INTEGRATION-E2E-009: Sequential calls after failure
- **Purpose**: Verify that sequential make_request calls work correctly after a failure
- **Preconditions**: Web application with API endpoint
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Simulate temporary API failure on first call
  3. Verify first call fails
  4. Make second sequential call (not automatic retry)
  5. Verify second call succeeds
- **Expected Result**: Sequential calls work correctly after failure
- **Coverage**: Sequential request handling after failure
- **Dependencies**: Web application with API endpoint

### 5. Configuration Workflows

#### TC-INTEGRATION-E2E-010: Context manager full workflow
- **Purpose**: Verify complete workflow using context managers
- **Preconditions**: Valid config and base URL
- **Test Steps**:
  1. Use `async with ApiClient(url, config) as api:`
  2. Test API endpoints
  3. Use `async with UiClient(url, config) as ui:`
  4. Setup browser and test UI
  5. Verify all close correctly on exit
- **Expected Result**: Complete workflow works with context managers
- **Coverage**: Context manager integration
- **Dependencies**: Valid setup

#### TC-INTEGRATION-E2E-011: Load config from YAML and test
- **Purpose**: Verify config loading from YAML file
- **Preconditions**: Valid YAML config file
- **Test Steps**:
  1. Create YAML config file
  2. Create Config using `Config.from_yaml()`
  3. Create `ApiClient` with Config
  4. Test API endpoints
  5. Verify all components use config correctly
- **Expected Result**: Config from YAML works
- **Coverage**: YAML config loading integration
- **Dependencies**: Valid YAML file

### 6. Performance Workflows

#### TC-INTEGRATION-E2E-012: Performance test: Full workflow timing
- **Purpose**: Verify full workflow completes in acceptable time
- **Preconditions**: All components available
- **Test Steps**:
  1. Measure start time
  2. Execute full workflow (connect → test API → test UI)
  3. Measure end time
  4. Calculate total time
  5. Verify time is within acceptable limits
- **Expected Result**: Workflow completes in reasonable time
- **Coverage**: Performance integration
- **Dependencies**: Fast components

#### TC-INTEGRATION-E2E-013: Load test: Multiple concurrent workflows
- **Purpose**: Verify system handles concurrent workflows
- **Preconditions**: Multiple test setups
- **Test Steps**:
  1. Start 3 concurrent workflows
  2. Each workflow: connect → test API → test UI
  3. Wait for all to complete
  4. Verify all succeed
  5. Measure total time
- **Expected Result**: Concurrent workflows handled correctly
- **Coverage**: Concurrency integration
- **Dependencies**: Multiple test setups

### 7. Resource Management Workflows

#### TC-INTEGRATION-E2E-014: Resource cleanup after workflow
- **Purpose**: Verify resources are cleaned up properly
- **Preconditions**: Full workflow setup
- **Test Steps**:
  1. Execute full workflow
  2. Verify `ApiClient` client is open
  3. Verify `UiClient` browser is open
  4. Exit context managers
  5. Verify all resources are closed
- **Expected Result**: All resources cleaned up
- **Coverage**: Resource management integration
- **Dependencies**: Full workflow

#### TC-INTEGRATION-E2E-015: Handle resource exhaustion
- **Purpose**: Verify handling when resources are exhausted
- **Preconditions**: Limited resources
- **Test Steps**:
  1. Open multiple browsers/clients
  2. Try to open more than limit
  3. Verify error is handled gracefully
  4. Close some resources
  5. Verify can open new resources
- **Expected Result**: Resource exhaustion handled correctly
- **Coverage**: Resource limit handling
- **Dependencies**: Resource limits

### 8. Real-World Scenarios

#### TC-INTEGRATION-E2E-016: Test real web application
- **Purpose**: Verify framework works with real web application
- **Preconditions**: Real web application available
- **Test Steps**:
  1. Connect with real web application
  2. Test real API endpoints
  3. Test real UI
  4. Verify all work with real service
- **Expected Result**: Works with real web application
- **Coverage**: Real-world integration
- **Dependencies**: Real web application

#### TC-INTEGRATION-E2E-017: Test application with complex UI
- **Purpose**: Verify framework handles complex UI
- **Preconditions**: Web application with complex UI (forms, modals, etc.)
- **Test Steps**:
  1. Setup browser and navigate
  2. Test complex form with multiple fields
  3. Test modal dialogs
  4. Test dynamic content loading
  5. Verify all interactions work
- **Expected Result**: Complex UI tested successfully
- **Coverage**: Complex UI handling
- **Dependencies**: Web application with complex UI

#### TC-INTEGRATION-E2E-018: Test application with real-time updates
- **Purpose**: Verify framework handles real-time updates
- **Preconditions**: Web application with WebSocket or polling
- **Test Steps**:
  1. Setup browser and navigate
  2. Wait for real-time update
  3. Verify UI updates correctly
  4. Interact with updated UI
- **Expected Result**: Real-time updates handled correctly
- **Coverage**: Real-time update handling
- **Dependencies**: Web application with real-time features

### 9. Database Integration Workflows

#### TC-INTEGRATION-E2E-019: Database-backed application testing
- **Purpose**: Verify testing web application with database backend using all components
- **Preconditions**: 
  - Web application with database, API, and UI
  - Database connection available (SQLite, PostgreSQL, or MySQL)
  - Database schema prepared
- **Test Steps**:
  1. Setup database schema via `DBClient` (CREATE TABLE if needed)
  2. Seed test data via `DBClient.execute_command()` (INSERT)
  3. Test API endpoints that query database via `ApiClient.make_request()` (GET)
  4. Test API endpoints that write to database via `ApiClient.make_request()` (POST)
  5. Verify API responses match database data via `DBClient.execute_query()`
  6. Test UI that displays database data via `UiClient` interactions
  7. Verify UI content matches database data
  8. Verify data consistency across all layers (Database ↔ API ↔ UI)
  9. Clean up test data from database
- **Expected Result**: Database-backed application tested successfully with all components
- **Coverage**: `DBClient` + `ApiClient` + `UiClient` integration
- **Dependencies**: Complete web application with database, all components available, database schema

### 10. Multi-Protocol Integration

#### TC-INTEGRATION-E2E-020: REST API + GraphQL integration
- **Purpose**: Verify testing application with both REST and GraphQL APIs
- **Preconditions**: 
  - Web application with REST and GraphQL endpoints
- **Test Steps**:
  1. Create `ApiClient` for REST API
  2. Test REST endpoints using `make_request()`
  3. Create `GraphQLClient` for GraphQL API
  4. Test GraphQL queries and mutations
  5. Verify data consistency between REST and GraphQL
- **Expected Result**: Both REST and GraphQL APIs tested successfully
- **Coverage**: `ApiClient` + `GraphQLClient` integration
- **Dependencies**: Web application with both API types

#### TC-INTEGRATION-E2E-021: REST API + SOAP integration
- **Purpose**: Verify testing application with both REST and SOAP APIs
- **Preconditions**: 
  - Web application with REST and SOAP endpoints
- **Test Steps**:
  1. Create `ApiClient` for REST API
  2. Test REST endpoints
  3. Create `SoapClient` for SOAP API
  4. Test SOAP operations
  5. Verify data consistency between REST and SOAP
- **Expected Result**: Both REST and SOAP APIs tested successfully
- **Coverage**: `ApiClient` + `SoapClient` integration
- **Dependencies**: Web application with both API types

#### TC-INTEGRATION-E2E-022: WebSocket + REST API integration
- **Purpose**: Verify testing application with WebSocket and REST API
- **Preconditions**: 
  - Web application with WebSocket and REST endpoints
- **Test Steps**:
  1. Create `WebSocketClient` and connect
  2. Listen for WebSocket messages
  3. Create `ApiClient` for REST API
  4. Trigger event via REST API
  5. Verify WebSocket receives notification
  6. Verify data consistency
- **Expected Result**: WebSocket and REST API integration works correctly
- **Coverage**: `WebSocketClient` + `ApiClient` integration
- **Dependencies**: Web application with WebSocket and REST

#### TC-INTEGRATION-E2E-023: RequestBuilder integration workflow
- **Purpose**: Verify RequestBuilder works in full workflow
- **Preconditions**: 
  - Web application with API endpoints
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build complex request with chaining: `.get("/users").params(page=1).header("X-Header", "value")`
  4. Execute request using `.execute()`
  5. Verify response is correct
  6. Build and execute POST request with body
  7. Verify all requests work correctly
- **Expected Result**: RequestBuilder works correctly in full workflow
- **Coverage**: `RequestBuilder` integration
- **Dependencies**: Web application with API

#### TC-INTEGRATION-E2E-024: Response validation integration workflow
- **Purpose**: Verify response validation works in full workflow
- **Preconditions**: 
  - Web application with API endpoints
  - msgspec Struct schema defined
- **Test Steps**:
  1. Create `ApiClient` and make API request
  2. Get `ApiResult` from request
  3. Define msgspec Struct schema for response
  4. Use `validate_api_result()` to validate response
  5. Verify validated data matches schema
  6. Test with invalid response data
  7. Verify validation errors are raised correctly
- **Expected Result**: Response validation works correctly in full workflow
- **Coverage**: `validators` integration
- **Dependencies**: Web application with API, schema definition

---

## Parameterized Status Code Tests

### TC-INTEGRATION-E2E-STATUS-001 to TC-INTEGRATION-E2E-STATUS-009: End-to-end workflow handles various HTTP status codes

**Примечание**: Тесты TC-INTEGRATION-E2E-STATUS-001 до TC-INTEGRATION-E2E-STATUS-009 объединены в один параметризованный тест `test_end_to_end_status_codes()` для систематического тестирования различных HTTP статус-кодов в end-to-end сценариях.

#### TC-INTEGRATION-E2E-STATUS-001: End-to-end workflow handles status code 200
- **Purpose**: Verify end-to-end workflow correctly handles HTTP 200 (OK) status code
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Mock HTTP response with status_code=200
  3. Execute API request
  4. Verify result.status_code == 200
  5. Verify result.success == True
- **Expected Result**: End-to-end workflow correctly processes 200 status code
- **Coverage**: `ApiClient.make_request()` with successful response in E2E context
- **Implementation**: Параметризованный тест `test_end_to_end_status_codes()` с параметрами `status_code=200, expected_success=True`

#### TC-INTEGRATION-E2E-STATUS-002: End-to-end workflow handles status code 201
- **Purpose**: Verify end-to-end workflow correctly handles HTTP 201 (Created) status code
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Mock HTTP response with status_code=201
  3. Execute API request
  4. Verify result.status_code == 201
  5. Verify result.success == True
- **Expected Result**: End-to-end workflow correctly processes 201 status code
- **Coverage**: `ApiClient.make_request()` with successful creation response in E2E context
- **Implementation**: Параметризованный тест `test_end_to_end_status_codes()` с параметрами `status_code=201, expected_success=True`

#### TC-INTEGRATION-E2E-STATUS-003: End-to-end workflow handles status code 400
- **Purpose**: Verify end-to-end workflow correctly handles HTTP 400 (Bad Request) status code
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Mock HTTP response with status_code=400
  3. Execute API request
  4. Verify result.status_code == 400
  5. Verify result.success == False
- **Expected Result**: End-to-end workflow correctly processes 400 status code
- **Coverage**: `ApiClient.make_request()` with client error response in E2E context
- **Implementation**: Параметризованный тест `test_end_to_end_status_codes()` с параметрами `status_code=400, expected_success=False`

#### TC-INTEGRATION-E2E-STATUS-004: End-to-end workflow handles status code 401
- **Purpose**: Verify end-to-end workflow correctly handles HTTP 401 (Unauthorized) status code
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Mock HTTP response with status_code=401
  3. Execute API request
  4. Verify result.status_code == 401
  5. Verify result.success == False
- **Expected Result**: End-to-end workflow correctly processes 401 status code
- **Coverage**: `ApiClient.make_request()` with authentication error response in E2E context
- **Implementation**: Параметризованный тест `test_end_to_end_status_codes()` с параметрами `status_code=401, expected_success=False`

#### TC-INTEGRATION-E2E-STATUS-005: End-to-end workflow handles status code 403
- **Purpose**: Verify end-to-end workflow correctly handles HTTP 403 (Forbidden) status code
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Mock HTTP response with status_code=403
  3. Execute API request
  4. Verify result.status_code == 403
  5. Verify result.success == False
- **Expected Result**: End-to-end workflow correctly processes 403 status code
- **Coverage**: `ApiClient.make_request()` with authorization error response in E2E context
- **Implementation**: Параметризованный тест `test_end_to_end_status_codes()` с параметрами `status_code=403, expected_success=False`

#### TC-INTEGRATION-E2E-STATUS-006: End-to-end workflow handles status code 404
- **Purpose**: Verify end-to-end workflow correctly handles HTTP 404 (Not Found) status code
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Mock HTTP response with status_code=404
  3. Execute API request
  4. Verify result.status_code == 404
  5. Verify result.success == False
- **Expected Result**: End-to-end workflow correctly processes 404 status code
- **Coverage**: `ApiClient.make_request()` with not found error response in E2E context
- **Implementation**: Параметризованный тест `test_end_to_end_status_codes()` с параметрами `status_code=404, expected_success=False`

#### TC-INTEGRATION-E2E-STATUS-007: End-to-end workflow handles status code 500
- **Purpose**: Verify end-to-end workflow correctly handles HTTP 500 (Internal Server Error) status code
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Mock HTTP response with status_code=500
  3. Execute API request
  4. Verify result.status_code == 500
  5. Verify result.success == False
- **Expected Result**: End-to-end workflow correctly processes 500 status code
- **Coverage**: `ApiClient.make_request()` with server error response in E2E context
- **Implementation**: Параметризованный тест `test_end_to_end_status_codes()` с параметрами `status_code=500, expected_success=False`

#### TC-INTEGRATION-E2E-STATUS-008: End-to-end workflow handles status code 502
- **Purpose**: Verify end-to-end workflow correctly handles HTTP 502 (Bad Gateway) status code
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Mock HTTP response with status_code=502
  3. Execute API request
  4. Verify result.status_code == 502
  5. Verify result.success == False
- **Expected Result**: End-to-end workflow correctly processes 502 status code
- **Coverage**: `ApiClient.make_request()` with gateway error response in E2E context
- **Implementation**: Параметризованный тест `test_end_to_end_status_codes()` с параметрами `status_code=502, expected_success=False`

#### TC-INTEGRATION-E2E-STATUS-009: End-to-end workflow handles status code 503
- **Purpose**: Verify end-to-end workflow correctly handles HTTP 503 (Service Unavailable) status code
- **Preconditions**: ApiClient instance
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Mock HTTP response with status_code=503
  3. Execute API request
  4. Verify result.status_code == 503
  5. Verify result.success == False
- **Expected Result**: End-to-end workflow correctly processes 503 status code
- **Coverage**: `ApiClient.make_request()` with service unavailable error response in E2E context
- **Implementation**: Параметризованный тест `test_end_to_end_status_codes()` с параметрами `status_code=503, expected_success=False`
