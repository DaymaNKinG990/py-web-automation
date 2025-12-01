# Request Builder Integration Test Cases

## Overview
Tests for integration between `RequestBuilder` and other framework components, and real API endpoints.

## Test Categories

### 1. RequestBuilder Basic Integration

#### TC-INTEGRATION-RB-001: RequestBuilder GET request execution
- **Purpose**: Verify RequestBuilder executes GET requests successfully
- **Preconditions**: 
  - Web application with REST API endpoint
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build GET request: `builder.get("/users").params(page=1).execute()`
  4. Verify `ApiResult` is returned
  5. Verify response contains expected data
  6. Verify request was made to correct endpoint
- **Expected Result**: GET request executes successfully
- **Coverage**: `RequestBuilder.get()`, `RequestBuilder.params()`, `RequestBuilder.execute()`
- **Dependencies**: Web application with REST API

#### TC-INTEGRATION-RB-002: RequestBuilder POST request execution
- **Purpose**: Verify RequestBuilder executes POST requests successfully
- **Preconditions**: 
  - Web application with REST API endpoint accepting POST
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build POST request: `builder.post("/users").body({"name": "John"}).execute()`
  4. Verify `ApiResult` is returned
  5. Verify response contains created resource
  6. Verify request body was sent correctly
- **Expected Result**: POST request executes successfully
- **Coverage**: `RequestBuilder.post()`, `RequestBuilder.body()`, `RequestBuilder.execute()`
- **Dependencies**: Web application with REST API

#### TC-INTEGRATION-RB-003: RequestBuilder PUT request execution
- **Purpose**: Verify RequestBuilder executes PUT requests successfully
- **Preconditions**: 
  - Web application with REST API endpoint accepting PUT
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build PUT request: `builder.put("/users/1").body({"name": "Jane"}).execute()`
  4. Verify `ApiResult` is returned
  5. Verify response contains updated resource
- **Expected Result**: PUT request executes successfully
- **Coverage**: `RequestBuilder.put()`, `RequestBuilder.execute()`
- **Dependencies**: Web application with REST API

#### TC-INTEGRATION-RB-004: RequestBuilder DELETE request execution
- **Purpose**: Verify RequestBuilder executes DELETE requests successfully
- **Preconditions**: 
  - Web application with REST API endpoint accepting DELETE
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build DELETE request: `builder.delete("/users/1").execute()`
  4. Verify `ApiResult` is returned
  5. Verify resource is deleted
- **Expected Result**: DELETE request executes successfully
- **Coverage**: `RequestBuilder.delete()`, `RequestBuilder.execute()`
- **Dependencies**: Web application with REST API

### 2. RequestBuilder Method Chaining Integration

#### TC-INTEGRATION-RB-005: RequestBuilder complex chaining
- **Purpose**: Verify RequestBuilder supports complex method chaining
- **Preconditions**: 
  - Web application with REST API endpoint
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build complex request: `builder.get("/users").params(page=1, limit=10).header("X-Custom-Header", "value").header("X-Another-Header", "another").execute()`
  4. Verify all parameters are included in request
  5. Verify request executes successfully
- **Expected Result**: Complex method chaining works correctly
- **Coverage**: `RequestBuilder` method chaining
- **Dependencies**: Web application with REST API

#### TC-INTEGRATION-RB-006: RequestBuilder with authentication
- **Purpose**: Verify RequestBuilder works with authentication
- **Preconditions**: 
  - Web application with REST API requiring authentication
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Set authentication token on ApiClient
  3. Use `build_request()` to create RequestBuilder
  4. Build request: `builder.get("/users").execute()`
  5. Verify Authorization header is included
  6. Verify request executes successfully
- **Expected Result**: Authentication works with RequestBuilder
- **Coverage**: `RequestBuilder` + `ApiClient.set_auth_token()`
- **Dependencies**: Web application with auth

#### TC-INTEGRATION-RB-007: RequestBuilder with custom headers
- **Purpose**: Verify RequestBuilder includes custom headers
- **Preconditions**: 
  - Web application with REST API endpoint
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build request with headers: `builder.get("/users").header("X-Custom-Header", "value").headers(X_Another_Header="another").execute()`
  4. Verify custom headers are included in request
  5. Verify request executes successfully
- **Expected Result**: Custom headers are included correctly
- **Coverage**: `RequestBuilder.header()`, `RequestBuilder.headers()`
- **Dependencies**: Web application with REST API

### 3. RequestBuilder + Validators Integration

#### TC-INTEGRATION-RB-008: RequestBuilder response validation
- **Purpose**: Verify RequestBuilder responses can be validated using validators
- **Preconditions**: 
  - Web application with REST API endpoint
  - msgspec Struct schema defined
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build and execute request: `result = await builder.get("/users/1").execute()`
  4. Define msgspec Struct schema for response
  5. Use `validate_api_result()` to validate response
  6. Verify validated data matches schema
- **Expected Result**: RequestBuilder response validation works correctly
- **Coverage**: `RequestBuilder` + `validators.validate_api_result()`
- **Dependencies**: Web application with REST API, schema definition

### 4. RequestBuilder + DBClient Integration

#### TC-INTEGRATION-RB-009: RequestBuilder with database-backed API
- **Purpose**: Verify RequestBuilder works with database-backed API
- **Preconditions**: 
  - Web application with database-backed REST API
  - Database connection available
- **Test Steps**:
  1. Create `DBClient` and seed test data
  2. Create `ApiClient` with base URL
  3. Use `build_request()` to create RequestBuilder
  4. Build and execute request: `result = await builder.get("/users").params(page=1).execute()`
  5. Verify response contains database data
  6. Verify data matches database content
- **Expected Result**: RequestBuilder works correctly with database-backed API
- **Coverage**: `RequestBuilder` + `DBClient` integration
- **Dependencies**: Web application with database-backed API

### 5. RequestBuilder Error Handling Integration

#### TC-INTEGRATION-RB-010: RequestBuilder validation error
- **Purpose**: Verify RequestBuilder validates request configuration
- **Preconditions**: 
  - ApiClient instance
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Attempt to execute without setting endpoint: `await builder.execute()`
  4. Verify `ValidationError` is raised
  5. Verify error message indicates missing endpoint
- **Expected Result**: Request validation works correctly
- **Coverage**: `RequestBuilder.validate()`, `RequestBuilder.execute()` validation
- **Dependencies**: ApiClient instance

#### TC-INTEGRATION-RB-011: RequestBuilder reset and reuse
- **Purpose**: Verify RequestBuilder can be reset and reused
- **Preconditions**: 
  - Web application with REST API endpoint
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build and execute first request: `await builder.get("/users").execute()`
  4. Reset builder: `builder.reset()`
  5. Build and execute second request: `await builder.post("/users").body({"name": "John"}).execute()`
  6. Verify both requests execute successfully
- **Expected Result**: RequestBuilder reset and reuse works correctly
- **Coverage**: `RequestBuilder.reset()`
- **Dependencies**: Web application with REST API

## Summary

- **Total test cases**: 11
- **Categories**: 5 (Basic integration, Method chaining, Validators, DBClient, Error handling)
- **Coverage**: Complete integration testing of `RequestBuilder` with framework components

