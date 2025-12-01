# SOAP Client Integration Test Cases

## Overview
Tests for integration between `SoapClient` and other framework components, and real SOAP API endpoints.

## Test Categories

### 1. SoapClient Basic Integration

#### TC-INTEGRATION-SOAP-001: SoapClient SOAP 1.1 operation call
- **Purpose**: Verify SoapClient executes SOAP 1.1 operations successfully
- **Preconditions**: 
  - SOAP API endpoint available (SOAP 1.1)
  - Valid WSDL or known operation
- **Test Steps**:
  1. Create `SoapClient` with SOAP endpoint URL (default SOAP 1.1)
  2. Execute operation: `await soap.call("GetUser", {"userId": "123"})`
  3. Verify `ApiResult` is returned
  4. Verify response contains SOAP envelope
  5. Verify response body contains operation result
- **Expected Result**: SOAP 1.1 operation executes successfully
- **Coverage**: `SoapClient.call()` with SOAP 1.1
- **Dependencies**: SOAP API endpoint (SOAP 1.1)

#### TC-INTEGRATION-SOAP-002: SoapClient SOAP 1.2 operation call
- **Purpose**: Verify SoapClient executes SOAP 1.2 operations successfully
- **Preconditions**: 
  - SOAP API endpoint available (SOAP 1.2)
  - Valid WSDL or known operation
- **Test Steps**:
  1. Create `SoapClient` with SOAP endpoint URL and `soap_version="1.2"`
  2. Execute operation: `await soap.call("GetUser", {"userId": "123"})`
  3. Verify `ApiResult` is returned
  4. Verify SOAP 1.2 envelope is used
  5. Verify response contains operation result
- **Expected Result**: SOAP 1.2 operation executes successfully
- **Coverage**: `SoapClient.call()` with SOAP 1.2
- **Dependencies**: SOAP API endpoint (SOAP 1.2)

#### TC-INTEGRATION-SOAP-003: SoapClient with namespace
- **Purpose**: Verify SoapClient handles namespaces correctly
- **Preconditions**: 
  - SOAP API endpoint requiring namespace
- **Test Steps**:
  1. Create `SoapClient` with SOAP endpoint URL
  2. Execute operation with namespace: `await soap.call("GetUser", {"userId": "123"}, namespace="http://example.com/service")`
  3. Verify namespace is included in SOAP envelope
  4. Verify operation executes successfully
- **Expected Result**: Namespace is handled correctly
- **Coverage**: `SoapClient.call()` with namespace parameter
- **Dependencies**: SOAP API endpoint with namespace

#### TC-INTEGRATION-SOAP-004: SoapClient with nested body structure
- **Purpose**: Verify SoapClient handles nested body structures correctly
- **Preconditions**: 
  - SOAP API endpoint accepting nested structures
- **Test Steps**:
  1. Create `SoapClient` with SOAP endpoint URL
  2. Execute operation with nested body: `await soap.call("CreateUser", {"user": {"name": "John", "email": "john@example.com"}})`
  3. Verify nested structure is converted to XML correctly
  4. Verify operation executes successfully
- **Expected Result**: Nested structures are handled correctly
- **Coverage**: `SoapClient.call()` with nested body
- **Dependencies**: SOAP API endpoint with nested structures

### 2. SoapClient Authentication Integration

#### TC-INTEGRATION-SOAP-005: SoapClient with authentication token
- **Purpose**: Verify SoapClient includes authentication token in requests
- **Preconditions**: 
  - SOAP API endpoint requiring authentication
  - Valid authentication token
- **Test Steps**:
  1. Create `SoapClient` with SOAP endpoint URL
  2. Set authentication token using `set_auth_token("token-123")`
  3. Execute operation
  4. Verify Authorization header is included in request
  5. Verify operation executes successfully
- **Expected Result**: Authentication token is included, operation executes successfully
- **Coverage**: `SoapClient.set_auth_token()`, authentication header
- **Dependencies**: SOAP API endpoint with auth

### 3. SoapClient Error Handling Integration

#### TC-INTEGRATION-SOAP-006: SoapClient SOAP fault parsing
- **Purpose**: Verify SoapClient parses SOAP faults correctly
- **Preconditions**: 
  - SOAP API endpoint that returns SOAP faults
- **Test Steps**:
  1. Create `SoapClient` with SOAP endpoint URL
  2. Execute operation that triggers SOAP fault
  3. Get `ApiResult` from call
  4. Call `parse_soap_fault()` on result
  5. Verify fault dictionary is returned
  6. Verify fault contains expected fields (faultcode, faultstring, etc.)
- **Expected Result**: SOAP faults are parsed correctly
- **Coverage**: `SoapClient.parse_soap_fault()`
- **Dependencies**: SOAP API endpoint that returns faults

#### TC-INTEGRATION-SOAP-007: SoapClient SOAP 1.2 fault parsing
- **Purpose**: Verify SoapClient parses SOAP 1.2 faults correctly
- **Preconditions**: 
  - SOAP API endpoint (SOAP 1.2) that returns SOAP faults
- **Test Steps**:
  1. Create `SoapClient` with SOAP 1.2
  2. Execute operation that triggers SOAP fault
  3. Get `ApiResult` from call
  4. Call `parse_soap_fault()` on result
  5. Verify SOAP 1.2 fault is parsed correctly
- **Expected Result**: SOAP 1.2 faults are parsed correctly
- **Coverage**: `SoapClient.parse_soap_fault()` with SOAP 1.2
- **Dependencies**: SOAP API endpoint (SOAP 1.2) that returns faults

#### TC-INTEGRATION-SOAP-008: SoapClient handles network errors
- **Purpose**: Verify SoapClient handles network errors gracefully
- **Preconditions**: 
  - Network that can be interrupted
- **Test Steps**:
  1. Create `SoapClient` with invalid endpoint URL
  2. Execute operation
  3. Verify error is handled gracefully
  4. Verify `ApiResult` with success=False is returned
- **Expected Result**: Network errors are handled gracefully
- **Coverage**: `SoapClient` error handling
- **Dependencies**: Network interruption

### 4. SoapClient + Validators Integration

#### TC-INTEGRATION-SOAP-009: SoapClient response validation
- **Purpose**: Verify SoapClient responses can be validated using validators
- **Preconditions**: 
  - SOAP API endpoint available
  - msgspec Struct schema defined for response
- **Test Steps**:
  1. Create `SoapClient` and execute operation
  2. Get `ApiResult` from call
  3. Extract response body (may need XML parsing)
  4. Define msgspec Struct schema for response
  5. Use `validate_response()` to validate response data
  6. Verify validated data matches schema
- **Expected Result**: SOAP response validation works correctly
- **Coverage**: `SoapClient` + `validators.validate_response()`
- **Dependencies**: SOAP API endpoint, schema definition

### 5. SoapClient + ApiClient Integration

#### TC-INTEGRATION-SOAP-010: SoapClient and ApiClient side by side
- **Purpose**: Verify SoapClient and ApiClient can be used together
- **Preconditions**: 
  - Web application with both SOAP and REST endpoints
- **Test Steps**:
  1. Create `SoapClient` for SOAP endpoint
  2. Create `ApiClient` for REST endpoint
  3. Execute SOAP operation
  4. Execute REST API request
  5. Verify both work correctly
  6. Verify data consistency between SOAP and REST
- **Expected Result**: Both clients work correctly together
- **Coverage**: `SoapClient` + `ApiClient` integration
- **Dependencies**: Web application with both API types

#### TC-INTEGRATION-SOAP-011: SoapClient context manager
- **Purpose**: Verify SoapClient works as context manager
- **Preconditions**: 
  - SOAP API endpoint available
- **Test Steps**:
  1. Use `async with SoapClient(url, config) as soap:`
  2. Execute operation within context
  3. Verify operation executes successfully
  4. Exit context
  5. Verify client is closed properly
- **Expected Result**: Context manager works correctly, resources cleaned up
- **Coverage**: `SoapClient` context manager
- **Dependencies**: SOAP API endpoint

## Summary

- **Total test cases**: 11
- **Categories**: 5 (Basic integration, Authentication, Error handling, Validators, ApiClient integration)
- **Coverage**: Complete integration testing of `SoapClient` with framework components

