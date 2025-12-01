# Validators Integration Test Cases

## Overview
Tests for integration between `validators` module and other framework components, and real API responses.

## Test Categories

### 1. Validators + ApiClient Integration

#### TC-INTEGRATION-VAL-001: validate_api_result with ApiClient
- **Purpose**: Verify validate_api_result works with ApiClient responses
- **Preconditions**: 
  - Web application with REST API endpoint
  - msgspec Struct schema defined
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Make API request: `result = await api.make_request("/users/1")`
  3. Define msgspec Struct schema: `class UserResponse(msgspec.Struct): id: int; name: str; email: str`
  4. Validate response: `user = validate_api_result(result, UserResponse)`
  5. Verify validated object is instance of UserResponse
  6. Verify all fields are correctly populated
- **Expected Result**: API response validation works correctly
- **Coverage**: `validators.validate_api_result()` + `ApiClient`
- **Dependencies**: Web application with REST API, schema definition

#### TC-INTEGRATION-VAL-002: validate_api_result with invalid response
- **Purpose**: Verify validate_api_result handles invalid responses correctly
- **Preconditions**: 
  - Web application with REST API endpoint
  - msgspec Struct schema defined
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Make API request that returns invalid data: `result = await api.make_request("/invalid")`
  3. Define msgspec Struct schema
  4. Attempt to validate: `validate_api_result(result, UserResponse)`
  5. Verify `ValidationError` is raised
  6. Verify error message describes validation failure
- **Expected Result**: Invalid responses are handled correctly
- **Coverage**: `validators.validate_api_result()` error handling
- **Dependencies**: Web application with REST API

### 2. Validators + RequestBuilder Integration

#### TC-INTEGRATION-VAL-003: validate_api_result with RequestBuilder
- **Purpose**: Verify validate_api_result works with RequestBuilder responses
- **Preconditions**: 
  - Web application with REST API endpoint
  - msgspec Struct schema defined
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Use `build_request()` to create RequestBuilder
  3. Build and execute request: `result = await builder.get("/users/1").execute()`
  4. Define msgspec Struct schema
  5. Validate response: `user = validate_api_result(result, UserResponse)`
  6. Verify validated object matches schema
- **Expected Result**: RequestBuilder response validation works correctly
- **Coverage**: `validators.validate_api_result()` + `RequestBuilder`
- **Dependencies**: Web application with REST API, schema definition

### 3. Validators + GraphQLClient Integration

#### TC-INTEGRATION-VAL-004: validate_api_result with GraphQLClient
- **Purpose**: Verify validate_api_result works with GraphQLClient responses
- **Preconditions**: 
  - GraphQL API endpoint available
  - msgspec Struct schema defined
- **Test Steps**:
  1. Create `GraphQLClient` with GraphQL endpoint URL
  2. Execute query: `result = await gql.query("query { user { id name email } }")`
  3. Define msgspec Struct schema for GraphQL response
  4. Validate response: `user = validate_api_result(result, UserResponse)`
  5. Verify validated object matches schema
- **Expected Result**: GraphQL response validation works correctly
- **Coverage**: `validators.validate_api_result()` + `GraphQLClient`
- **Dependencies**: GraphQL API endpoint, schema definition

### 4. Validators + DBClient Integration

#### TC-INTEGRATION-VAL-005: validate_api_result with database-backed API
- **Purpose**: Verify validate_api_result works with database-backed API responses
- **Preconditions**: 
  - Web application with database-backed REST API
  - Database connection available
  - msgspec Struct schema defined
- **Test Steps**:
  1. Create `DBClient` and seed test data
  2. Create `ApiClient` with base URL
  3. Make API request: `result = await api.make_request("/users/1")`
  4. Define msgspec Struct schema
  5. Validate response: `user = validate_api_result(result, UserResponse)`
  6. Verify validated data matches database content
- **Expected Result**: Database-backed API response validation works correctly
- **Coverage**: `validators.validate_api_result()` + `DBClient` + `ApiClient`
- **Dependencies**: Web application with database-backed API, schema definition

### 5. Validators Dynamic Schema Integration

#### TC-INTEGRATION-VAL-006: create_schema_from_dict integration
- **Purpose**: Verify create_schema_from_dict works in integration context
- **Preconditions**: 
  - Web application with REST API endpoint
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Make API request: `result = await api.make_request("/users/1")`
  3. Get response data: `data = result.json()`
  4. Create dynamic schema: `UserSchema = create_schema_from_dict("User", {"id": int, "name": str, "email": str})`
  5. Validate response: `user = validate_response(data, UserSchema)`
  6. Verify validated object matches schema
- **Expected Result**: Dynamic schema creation works correctly
- **Coverage**: `validators.create_schema_from_dict()` + `validators.validate_response()`
- **Dependencies**: Web application with REST API

#### TC-INTEGRATION-VAL-007: create_schema_from_dict with optional fields
- **Purpose**: Verify create_schema_from_dict handles optional fields correctly
- **Preconditions**: 
  - Web application with REST API endpoint
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Make API request: `result = await api.make_request("/users/1")`
  3. Get response data: `data = result.json()`
  4. Create dynamic schema with optional fields: `UserSchema = create_schema_from_dict("User", {"id": int, "name": str, "age": (int, 0), "email": (str, "")})`
  5. Validate response: `user = validate_response(data, UserSchema)`
  6. Verify optional fields use defaults when missing
- **Expected Result**: Optional fields are handled correctly
- **Coverage**: `validators.create_schema_from_dict()` with optional fields
- **Dependencies**: Web application with REST API

### 6. Validators Nested Structures Integration

#### TC-INTEGRATION-VAL-008: validate_api_result with nested structures
- **Purpose**: Verify validate_api_result handles nested response structures
- **Preconditions**: 
  - Web application with REST API endpoint returning nested data
  - Nested msgspec Struct schemas defined
- **Test Steps**:
  1. Create `ApiClient` with base URL
  2. Make API request: `result = await api.make_request("/users/1")`
  3. Define nested msgspec Struct schemas (e.g., Address within User)
  4. Validate response: `user = validate_api_result(result, UserResponse)`
  5. Verify nested objects are correctly validated
  6. Verify nested fields are accessible
- **Expected Result**: Nested structures are validated correctly
- **Coverage**: `validators.validate_api_result()` with nested schemas
- **Dependencies**: Web application with REST API, nested schema definition

### 7. Validators Error Handling Integration

#### TC-INTEGRATION-VAL-009: validate_json_response with invalid JSON
- **Purpose**: Verify validate_json_response handles invalid JSON correctly
- **Preconditions**: 
  - Invalid JSON string
- **Test Steps**:
  1. Create invalid JSON string: `invalid_json = '{"id": 1, "name": "John"'`
  2. Define msgspec Struct schema
  3. Attempt to validate: `validate_json_response(invalid_json, UserResponse)`
  4. Verify `ValidationError` is raised
  5. Verify error message indicates JSON parsing failure
- **Expected Result**: Invalid JSON is handled correctly
- **Coverage**: `validators.validate_json_response()` error handling
- **Dependencies**: Invalid JSON data

#### TC-INTEGRATION-VAL-010: validate_response with type mismatches
- **Purpose**: Verify validate_response handles type mismatches correctly
- **Preconditions**: 
  - Data with incorrect types
- **Test Steps**:
  1. Create data with wrong types: `data = {"id": "invalid", "name": 123}`
  2. Define msgspec Struct schema: `class UserResponse(msgspec.Struct): id: int; name: str`
  3. Attempt to validate: `validate_response(data, UserResponse)`
  4. Verify `ValidationError` is raised
  5. Verify error message describes type mismatch
- **Expected Result**: Type mismatches are handled correctly
- **Coverage**: `validators.validate_response()` type validation
- **Dependencies**: Data with incorrect types

## Summary

- **Total test cases**: 10
- **Categories**: 7 (ApiClient, RequestBuilder, GraphQLClient, DBClient, Dynamic schema, Nested structures, Error handling)
- **Coverage**: Complete integration testing of `validators` with framework components

