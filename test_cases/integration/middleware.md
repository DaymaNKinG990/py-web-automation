# Middleware Integration Test Cases

## Overview
Integration tests for middleware system with ApiClient and other clients.
Tests verify request/response processing, middleware chains, and error handling.

## Test Categories

### 1. MiddlewareChain with ApiClient

#### TC-INTEGRATION-MW-001: MiddlewareChain с ApiClient - базовый workflow
- **Purpose**: Verify basic middleware chain integration with ApiClient
- **Preconditions**:
  - ApiClient instance
  - MiddlewareChain with at least one middleware
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create MiddlewareChain and add LoggingMiddleware
  3. Initialize ApiClient with middleware chain
  4. Mock HTTP response (status 200)
  5. Make request using `make_request()`
  6. Verify request was processed through middleware
  7. Verify response was processed through middleware
- **Expected Result**: Request and response processed through middleware chain
- **Coverage**: `MiddlewareChain.process_request()`, `MiddlewareChain.process_response()`, `ApiClient.make_request()` with middleware
- **Dependencies**: ApiClient, MiddlewareChain, LoggingMiddleware

#### TC-INTEGRATION-MW-002: Multiple middleware в цепочке
- **Purpose**: Verify multiple middleware in chain execute in correct order
- **Preconditions**:
  - ApiClient instance
  - Multiple middleware instances (LoggingMiddleware, MetricsMiddleware, AuthMiddleware)
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create MiddlewareChain and add multiple middleware:
     - LoggingMiddleware (first)
     - MetricsMiddleware (second)
     - AuthMiddleware (third)
  3. Initialize ApiClient with middleware chain
  4. Mock HTTP response (status 200)
  5. Make request using `make_request()`
  6. Verify middleware executed in correct order (request processing)
  7. Verify middleware executed in reverse order (response processing)
  8. Verify all middleware processed request/response
- **Expected Result**: All middleware execute in correct order for request and reverse order for response
- **Coverage**: MiddlewareChain ordering, multiple middleware execution
- **Dependencies**: ApiClient, MiddlewareChain, multiple middleware types

#### TC-INTEGRATION-MW-003: MiddlewareChain с GraphQLClient
- **Purpose**: Verify middleware chain integration with GraphQLClient
- **Preconditions**:
  - GraphQLClient instance
  - MiddlewareChain with LoggingMiddleware
  - Mock GraphQL endpoint
- **Test Steps**:
  1. Create GraphQLClient with base URL
  2. Create MiddlewareChain and add LoggingMiddleware
  3. Mock GraphQL response (status 200, valid GraphQL response)
  4. Execute GraphQL query using `query()`
  5. Verify request was processed through middleware
  6. Verify response was processed through middleware
- **Expected Result**: GraphQL request/response processed through middleware
- **Coverage**: MiddlewareChain with GraphQLClient
- **Dependencies**: GraphQLClient, MiddlewareChain, LoggingMiddleware

#### TC-INTEGRATION-MW-004: MiddlewareChain с SoapClient
- **Purpose**: Verify middleware chain integration with SoapClient
- **Preconditions**:
  - SoapClient instance
  - MiddlewareChain with LoggingMiddleware
  - Mock SOAP endpoint
- **Test Steps**:
  1. Create SoapClient with base URL
  2. Create MiddlewareChain and add LoggingMiddleware
  3. Mock SOAP response (status 200, valid SOAP envelope)
  4. Execute SOAP call using `call()`
  5. Verify request was processed through middleware
  6. Verify response was processed through middleware
- **Expected Result**: SOAP request/response processed through middleware
- **Coverage**: MiddlewareChain with SoapClient
- **Dependencies**: SoapClient, MiddlewareChain, LoggingMiddleware

#### TC-INTEGRATION-MW-005: MiddlewareChain с WebSocketClient
- **Purpose**: Verify middleware chain integration with WebSocketClient
- **Preconditions**:
  - WebSocketClient instance
  - MiddlewareChain with LoggingMiddleware
  - Mock WebSocket server
- **Test Steps**:
  1. Create WebSocketClient with WebSocket URL
  2. Create MiddlewareChain and add LoggingMiddleware
  3. Connect to WebSocket using `connect()`
  4. Send message using `send()`
  5. Verify request was processed through middleware (if applicable)
  6. Receive message and verify response was processed through middleware
  7. Disconnect from WebSocket
- **Expected Result**: WebSocket messages processed through middleware
- **Coverage**: MiddlewareChain with WebSocketClient
- **Dependencies**: WebSocketClient, MiddlewareChain, LoggingMiddleware

### 2. LoggingMiddleware Integration

#### TC-INTEGRATION-MW-006: LoggingMiddleware с ApiClient - логирование запросов
- **Purpose**: Verify LoggingMiddleware logs requests and responses
- **Preconditions**:
  - ApiClient instance
  - LoggingMiddleware instance
  - Logger configured to capture logs
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create MiddlewareChain and add LoggingMiddleware
  3. Initialize ApiClient with middleware chain
  4. Mock HTTP response (status 200)
  5. Capture logs using logger
  6. Make request using `make_request()`
  7. Verify request was logged (method, URL, headers)
  8. Verify response was logged (status code, response time)
- **Expected Result**: Request and response logged by LoggingMiddleware
- **Coverage**: LoggingMiddleware.process_request(), LoggingMiddleware.process_response()
- **Dependencies**: ApiClient, LoggingMiddleware, logger

### 3. MetricsMiddleware Integration

#### TC-INTEGRATION-MW-007: MetricsMiddleware с ApiClient - сбор метрик
- **Purpose**: Verify MetricsMiddleware collects request metrics
- **Preconditions**:
  - ApiClient instance
  - MetricsMiddleware with Metrics instance
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create Metrics instance
  3. Create MiddlewareChain and add MetricsMiddleware with Metrics
  4. Initialize ApiClient with middleware chain
  5. Mock HTTP response (status 200, response time 0.5s)
  6. Make multiple requests using `make_request()` (3 requests)
  7. Verify Metrics collected:
     - request_count = 3
     - success_count = 3
     - total_latency > 0
     - avg_latency calculated correctly
  8. Make request that fails (status 500)
  9. Verify Metrics collected error:
     - error_count = 1
     - errors_by_type contains error type
- **Expected Result**: MetricsMiddleware collects request metrics correctly
- **Coverage**: MetricsMiddleware.process_request(), MetricsMiddleware.process_response(), Metrics.record_request()
- **Dependencies**: ApiClient, MetricsMiddleware, Metrics

### 4. AuthMiddleware Integration

#### TC-INTEGRATION-MW-008: AuthMiddleware с ApiClient - автоматическая авторизация
- **Purpose**: Verify AuthMiddleware automatically adds authentication headers
- **Preconditions**:
  - ApiClient instance
  - AuthMiddleware with auth token
  - Mock HTTP endpoint requiring authentication
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create AuthMiddleware with auth token "test_token_123"
  3. Create MiddlewareChain and add AuthMiddleware
  4. Initialize ApiClient with middleware chain
  5. Mock HTTP response (status 200)
  6. Make request using `make_request()` without setting auth token
  7. Verify AuthMiddleware added Authorization header:
     - Header "Authorization" exists
     - Header value is "Bearer test_token_123"
  8. Verify request succeeded (status 200)
- **Expected Result**: AuthMiddleware automatically adds authentication headers
- **Coverage**: AuthMiddleware.process_request(), automatic header injection
- **Dependencies**: ApiClient, AuthMiddleware

### 5. ValidationMiddleware Integration

#### TC-INTEGRATION-MW-009: ValidationMiddleware с ApiClient - валидация ответов
- **Purpose**: Verify ValidationMiddleware validates response schemas
- **Preconditions**:
  - ApiClient instance
  - ValidationMiddleware with schema validator
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create ValidationMiddleware with JSON schema validator
  3. Create MiddlewareChain and add ValidationMiddleware
  4. Initialize ApiClient with middleware chain
  5. Mock HTTP response (status 200, valid JSON matching schema)
  6. Make request using `make_request()`
  7. Verify ValidationMiddleware validated response:
     - Response matches schema
     - Request succeeded
  8. Mock HTTP response (status 200, invalid JSON not matching schema)
  9. Make request using `make_request()`
  10. Verify ValidationMiddleware rejected response:
      - ValidationError raised
      - Request failed with validation error
- **Expected Result**: ValidationMiddleware validates response schemas correctly
- **Coverage**: ValidationMiddleware.process_response(), schema validation
- **Dependencies**: ApiClient, ValidationMiddleware, schema validator

### 6. Middleware Error Handling

#### TC-INTEGRATION-MW-010: Middleware error handling - обработка ошибок в middleware
- **Purpose**: Verify middleware chain handles errors in middleware gracefully
- **Preconditions**:
  - ApiClient instance
  - MiddlewareChain with middleware that raises exception
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create custom middleware that raises exception in process_request()
  3. Create MiddlewareChain and add error-raising middleware
  4. Initialize ApiClient with middleware chain
  5. Mock HTTP response (status 200)
  6. Make request using `make_request()`
  7. Verify error was handled:
     - Exception caught by middleware chain
     - Error processed through process_error()
     - Request failed with appropriate error
  8. Create custom middleware that raises exception in process_response()
  9. Repeat steps 4-7
  10. Verify response error was handled correctly
- **Expected Result**: Middleware errors handled gracefully, error processing works
- **Coverage**: MiddlewareChain.process_error(), error handling in middleware chain
- **Dependencies**: ApiClient, MiddlewareChain, custom error-raising middleware

