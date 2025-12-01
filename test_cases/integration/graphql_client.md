# GraphQL Client Integration Test Cases

## Overview
Tests for integration between `GraphQLClient` and other framework components, and real GraphQL API endpoints.

## Test Categories

### 1. GraphQLClient Basic Integration

#### TC-INTEGRATION-GQL-001: GraphQLClient query execution
- **Purpose**: Verify GraphQLClient executes queries successfully
- **Preconditions**: 
  - GraphQL API endpoint available
  - Valid GraphQL schema
- **Test Steps**:
  1. Create `GraphQLClient` with GraphQL endpoint URL
  2. Execute query: `await gql.query("query { user { id name email } }")`
  3. Verify `ApiResult` is returned
  4. Verify response contains expected data
  5. Verify `get_errors()` returns empty list
- **Expected Result**: GraphQL query executes successfully, returns data
- **Coverage**: `GraphQLClient.query()`, `GraphQLClient.get_errors()`
- **Dependencies**: GraphQL API endpoint

#### TC-INTEGRATION-GQL-002: GraphQLClient mutation execution
- **Purpose**: Verify GraphQLClient executes mutations successfully
- **Preconditions**: 
  - GraphQL API endpoint available
  - Valid GraphQL schema with mutations
- **Test Steps**:
  1. Create `GraphQLClient` with GraphQL endpoint URL
  2. Execute mutation: `await gql.mutate("mutation { createUser(name: \"John\") { id } }")`
  3. Verify `ApiResult` is returned
  4. Verify response contains mutation result
  5. Verify `get_errors()` returns empty list
- **Expected Result**: GraphQL mutation executes successfully, returns result
- **Coverage**: `GraphQLClient.mutate()`
- **Dependencies**: GraphQL API endpoint with mutations

#### TC-INTEGRATION-GQL-003: GraphQLClient with variables
- **Purpose**: Verify GraphQLClient handles query variables correctly
- **Preconditions**: 
  - GraphQL API endpoint available
- **Test Steps**:
  1. Create `GraphQLClient` with GraphQL endpoint URL
  2. Execute query with variables: `await gql.query("query GetUser($id: ID!) { user(id: $id) { name } }", variables={"id": "123"})`
  3. Verify variables are included in request payload
  4. Verify response contains correct data for provided variables
- **Expected Result**: GraphQL query with variables executes successfully
- **Coverage**: `GraphQLClient.query()` with variables parameter
- **Dependencies**: GraphQL API endpoint

#### TC-INTEGRATION-GQL-004: GraphQLClient with operation name
- **Purpose**: Verify GraphQLClient handles operation names correctly
- **Preconditions**: 
  - GraphQL API endpoint available
- **Test Steps**:
  1. Create `GraphQLClient` with GraphQL endpoint URL
  2. Execute query with operation name: `await gql.query("query GetUser { user { name } } query GetPosts { posts { title } }", operation_name="GetUser")`
  3. Verify operationName is included in request payload
  4. Verify correct operation is executed
- **Expected Result**: GraphQL query with operation name executes successfully
- **Coverage**: `GraphQLClient.query()` with operation_name parameter
- **Dependencies**: GraphQL API endpoint

### 2. GraphQLClient Authentication Integration

#### TC-INTEGRATION-GQL-005: GraphQLClient with authentication token
- **Purpose**: Verify GraphQLClient includes authentication token in requests
- **Preconditions**: 
  - GraphQL API endpoint requiring authentication
  - Valid authentication token
- **Test Steps**:
  1. Create `GraphQLClient` with GraphQL endpoint URL
  2. Set authentication token using `set_auth_token("token-123")`
  3. Execute query
  4. Verify Authorization header is included in request
  5. Verify query executes successfully
- **Expected Result**: Authentication token is included, query executes successfully
- **Coverage**: `GraphQLClient.set_auth_token()`, authentication header
- **Dependencies**: GraphQL API endpoint with auth

#### TC-INTEGRATION-GQL-006: GraphQLClient with custom token type
- **Purpose**: Verify GraphQLClient uses custom token type
- **Preconditions**: 
  - GraphQL API endpoint requiring custom authentication
- **Test Steps**:
  1. Create `GraphQLClient` with GraphQL endpoint URL
  2. Set authentication token with custom type: `set_auth_token("token-123", "ApiKey")`
  3. Execute query
  4. Verify Authorization header uses custom type: "ApiKey token-123"
- **Expected Result**: Custom token type is used correctly
- **Coverage**: `GraphQLClient.set_auth_token()` with custom type
- **Dependencies**: GraphQL API endpoint with custom auth

### 3. GraphQLClient Error Handling Integration

#### TC-INTEGRATION-GQL-007: GraphQLClient error extraction
- **Purpose**: Verify GraphQLClient extracts errors from response correctly
- **Preconditions**: 
  - GraphQL API endpoint that returns errors
- **Test Steps**:
  1. Create `GraphQLClient` with GraphQL endpoint URL
  2. Execute invalid query: `await gql.query("query { invalidField }")`
  3. Verify `ApiResult` is returned
  4. Call `get_errors()` on result
  5. Verify errors list contains error information
  6. Verify error structure (message, locations, path, etc.)
- **Expected Result**: Errors are extracted correctly from GraphQL response
- **Coverage**: `GraphQLClient.get_errors()`
- **Dependencies**: GraphQL API endpoint that returns errors

#### TC-INTEGRATION-GQL-008: GraphQLClient handles network errors
- **Purpose**: Verify GraphQLClient handles network errors gracefully
- **Preconditions**: 
  - Network that can be interrupted
- **Test Steps**:
  1. Create `GraphQLClient` with invalid endpoint URL
  2. Execute query
  3. Verify error is handled gracefully
  4. Verify `ApiResult` with success=False is returned
- **Expected Result**: Network errors are handled gracefully
- **Coverage**: `GraphQLClient` error handling
- **Dependencies**: Network interruption

### 4. GraphQLClient + Validators Integration

#### TC-INTEGRATION-GQL-009: GraphQLClient response validation
- **Purpose**: Verify GraphQLClient responses can be validated using validators
- **Preconditions**: 
  - GraphQL API endpoint available
  - msgspec Struct schema defined
- **Test Steps**:
  1. Create `GraphQLClient` and execute query
  2. Get `ApiResult` from query
  3. Define msgspec Struct schema for response
  4. Use `validate_api_result()` to validate response
  5. Verify validated data matches schema
- **Expected Result**: GraphQL response validation works correctly
- **Coverage**: `GraphQLClient` + `validators.validate_api_result()`
- **Dependencies**: GraphQL API endpoint, schema definition

#### TC-INTEGRATION-GQL-010: GraphQLClient with nested response validation
- **Purpose**: Verify GraphQLClient handles nested response structures with validation
- **Preconditions**: 
  - GraphQL API endpoint with nested data
  - Nested msgspec Struct schemas defined
- **Test Steps**:
  1. Create `GraphQLClient` and execute query with nested fields
  2. Get `ApiResult` from query
  3. Define nested msgspec Struct schemas
  4. Use `validate_api_result()` to validate nested response
  5. Verify nested objects are correctly validated
- **Expected Result**: Nested GraphQL response validation works correctly
- **Coverage**: `GraphQLClient` + nested `validators.validate_api_result()`
- **Dependencies**: GraphQL API endpoint with nested data

### 5. GraphQLClient + RequestBuilder Integration

#### TC-INTEGRATION-GQL-011: GraphQLClient context manager
- **Purpose**: Verify GraphQLClient works as context manager
- **Preconditions**: 
  - GraphQL API endpoint available
- **Test Steps**:
  1. Use `async with GraphQLClient(url, config) as gql:`
  2. Execute query within context
  3. Verify query executes successfully
  4. Exit context
  5. Verify client is closed properly
- **Expected Result**: Context manager works correctly, resources cleaned up
- **Coverage**: `GraphQLClient` context manager
- **Dependencies**: GraphQL API endpoint

### 6. GraphQLClient + ApiClient Integration

#### TC-INTEGRATION-GQL-012: GraphQLClient and ApiClient side by side
- **Purpose**: Verify GraphQLClient and ApiClient can be used together
- **Preconditions**: 
  - Web application with both GraphQL and REST endpoints
- **Test Steps**:
  1. Create `GraphQLClient` for GraphQL endpoint
  2. Create `ApiClient` for REST endpoint
  3. Execute GraphQL query
  4. Execute REST API request
  5. Verify both work correctly
  6. Verify data consistency between GraphQL and REST
- **Expected Result**: Both clients work correctly together
- **Coverage**: `GraphQLClient` + `ApiClient` integration
- **Dependencies**: Web application with both API types

## Summary

- **Total test cases**: 12
- **Categories**: 6 (Basic integration, Authentication, Error handling, Validators, RequestBuilder, ApiClient integration)
- **Coverage**: Complete integration testing of `GraphQLClient` with framework components

