# Middleware Module - Unit Test Cases

## Overview
Tests for `py_web_automation.middleware` module - request/response interception and modification system.

## Test Categories

### 1. MiddlewareChain Tests

#### TC-MW-001: MiddlewareChain - add middleware
- **Purpose**: Verify adding middleware to chain
- **Preconditions**: MiddlewareChain instance, middleware instance
- **Test Steps**:
  1. Create MiddlewareChain
  2. Create middleware instance
  3. Call chain.add(middleware)
  4. Verify middleware is in chain
- **Expected Result**: Middleware added to chain
- **Coverage**: `MiddlewareChain.add` method

#### TC-MW-002: MiddlewareChain - remove middleware
- **Purpose**: Verify removing middleware from chain
- **Preconditions**: MiddlewareChain with middleware
- **Test Steps**:
  1. Create MiddlewareChain with middleware
  2. Call chain.remove(middleware)
  3. Verify middleware is removed
- **Expected Result**: Middleware removed from chain
- **Coverage**: `MiddlewareChain.remove` method

#### TC-MW-003: MiddlewareChain - process_request
- **Purpose**: Verify processing request through all middleware
- **Preconditions**: MiddlewareChain with multiple middleware
- **Test Steps**:
  1. Create MiddlewareChain with 2 middleware
  2. Create RequestContext
  3. Call process_request(context)
  4. Verify all middleware process_request called
- **Expected Result**: All middleware process_request called in order
- **Coverage**: `MiddlewareChain.process_request` method

#### TC-MW-004: MiddlewareChain - process_response (обратный порядок)
- **Purpose**: Verify response processed in reverse order
- **Preconditions**: MiddlewareChain with multiple middleware
- **Test Steps**:
  1. Create MiddlewareChain with 2 middleware (track call order)
  2. Create ResponseContext
  3. Call process_response(context)
  4. Verify middleware called in reverse order
- **Expected Result**: Middleware called in reverse order (last added, first called)
- **Coverage**: `MiddlewareChain.process_response` method

#### TC-MW-005: MiddlewareChain - process_error
- **Purpose**: Verify error processing through chain
- **Preconditions**: MiddlewareChain with middleware that returns ApiResult
- **Test Steps**:
  1. Create MiddlewareChain with middleware that returns ApiResult in process_error
  2. Create RequestContext
  3. Call process_error(context, Exception())
  4. Verify ApiResult returned
- **Expected Result**: ApiResult returned from middleware
- **Coverage**: `MiddlewareChain.process_error` method

#### TC-MW-006: MiddlewareChain - process_error возвращает None
- **Purpose**: Verify error propagates when middleware returns None
- **Preconditions**: MiddlewareChain with middleware that returns None
- **Test Steps**:
  1. Create MiddlewareChain with middleware that returns None
  2. Create RequestContext
  3. Call process_error(context, Exception())
  4. Verify None returned
- **Expected Result**: None returned (error propagates)
- **Coverage**: `MiddlewareChain.process_error` method

### 2. LoggingMiddleware Tests

#### TC-MW-007: LoggingMiddleware - process_request
- **Purpose**: Verify request logging
- **Preconditions**: LoggingMiddleware, RequestContext, logger capture
- **Test Steps**:
  1. Create LoggingMiddleware
  2. Create RequestContext with method, url
  3. Call process_request(context)
  4. Verify request is logged
- **Expected Result**: Request logged: "Request: {method} {url} headers={...} params={...}"
- **Coverage**: `LoggingMiddleware.process_request` method

#### TC-MW-008: LoggingMiddleware - process_response
- **Purpose**: Verify response logging
- **Preconditions**: LoggingMiddleware, ResponseContext with ApiResult, logger capture
- **Test Steps**:
  1. Create LoggingMiddleware
  2. Create ResponseContext with ApiResult (status_code=200, response_time=0.5)
  3. Call process_response(context)
  4. Verify response is logged
- **Expected Result**: Response logged: "Response: {status_code} time={...}s success={...}"
- **Coverage**: `LoggingMiddleware.process_response` method

#### TC-MW-009: LoggingMiddleware - process_error
- **Purpose**: Verify error logging
- **Preconditions**: LoggingMiddleware, RequestContext, logger capture
- **Test Steps**:
  1. Create LoggingMiddleware
  2. Create RequestContext
  3. Call process_error(context, Exception("test error"))
  4. Verify error is logged
- **Expected Result**: Error logged: "Request error: {method} {url} - {error}"
- **Coverage**: `LoggingMiddleware.process_error` method

### 3. MetricsMiddleware Tests

#### TC-MW-010: MetricsMiddleware - process_request
- **Purpose**: Verify start_time recorded in metadata
- **Preconditions**: MetricsMiddleware with Metrics, RequestContext
- **Test Steps**:
  1. Create MetricsMiddleware with Metrics
  2. Create RequestContext
  3. Call process_request(context)
  4. Verify start_time in context.metadata
- **Expected Result**: start_time recorded in context.metadata
- **Coverage**: `MetricsMiddleware.process_request` method

#### TC-MW-011: MetricsMiddleware - process_response успех
- **Purpose**: Verify metrics recorded for successful response
- **Preconditions**: MetricsMiddleware with Metrics, ResponseContext with success=True
- **Test Steps**:
  1. Create MetricsMiddleware with Metrics
  2. Create ResponseContext with ApiResult (success=True, latency=0.5)
  3. Call process_response(context)
  4. Verify metrics.record_request called with success=True, latency=0.5
- **Expected Result**: Metrics recorded correctly
- **Coverage**: `MetricsMiddleware.process_response` method

#### TC-MW-012: MetricsMiddleware - process_response ошибка
- **Purpose**: Verify metrics recorded for error response
- **Preconditions**: MetricsMiddleware with Metrics, ResponseContext with success=False
- **Test Steps**:
  1. Create MetricsMiddleware with Metrics
  2. Create ResponseContext with ApiResult (success=False, client_error=True)
  3. Call process_response(context)
  4. Verify metrics.record_request called with success=False, error_type="client_error"
- **Expected Result**: Error metrics recorded correctly
- **Coverage**: `MetricsMiddleware.process_response` method

#### TC-MW-013: MetricsMiddleware - process_error
- **Purpose**: Verify error metrics recorded
- **Preconditions**: MetricsMiddleware with Metrics, RequestContext
- **Test Steps**:
  1. Create MetricsMiddleware with Metrics
  2. Create RequestContext
  3. Call process_error(context, ConnectionError("test"))
  4. Verify metrics.record_request called with success=False, error_type="ConnectionError"
- **Expected Result**: Error metrics recorded
- **Coverage**: `MetricsMiddleware.process_error` method

### 4. AuthMiddleware Tests

#### TC-MW-014: AuthMiddleware - process_request добавляет Authorization header
- **Purpose**: Verify Authorization header added to request
- **Preconditions**: AuthMiddleware with token, RequestContext without Authorization
- **Test Steps**:
  1. Create AuthMiddleware(token="abc123", token_type="Bearer")
  2. Create RequestContext without Authorization header
  3. Call process_request(context)
  4. Verify Authorization header = "Bearer abc123"
- **Expected Result**: Authorization header added
- **Coverage**: `AuthMiddleware.process_request` method

#### TC-MW-015: AuthMiddleware - не перезаписывает существующий header
- **Purpose**: Verify existing Authorization header not overwritten
- **Preconditions**: AuthMiddleware with token, RequestContext with Authorization
- **Test Steps**:
  1. Create AuthMiddleware(token="abc123")
  2. Create RequestContext with Authorization="Bearer existing"
  3. Call process_request(context)
  4. Verify Authorization header = "Bearer existing" (not overwritten)
- **Expected Result**: Existing header preserved
- **Coverage**: `AuthMiddleware.process_request` method

#### TC-MW-016: AuthMiddleware - custom token_type
- **Purpose**: Verify custom token type used
- **Preconditions**: AuthMiddleware with custom token_type
- **Test Steps**:
  1. Create AuthMiddleware(token="abc123", token_type="ApiKey")
  2. Create RequestContext
  3. Call process_request(context)
  4. Verify Authorization header = "ApiKey abc123"
- **Expected Result**: Custom token type used
- **Coverage**: `AuthMiddleware.process_request` method

### 5. ValidationMiddleware Tests

#### TC-MW-017: ValidationMiddleware - process_response валидный ответ
- **Purpose**: Verify validation of valid response
- **Preconditions**: ValidationMiddleware with schema, ResponseContext with valid ApiResult
- **Test Steps**:
  1. Create ValidationMiddleware with User schema
  2. Create ResponseContext with ApiResult containing valid User data
  3. Call process_response(context)
  4. Verify no validation error in metadata
- **Expected Result**: No validation error
- **Coverage**: `ValidationMiddleware.process_response` method

#### TC-MW-018: ValidationMiddleware - process_response невалидный ответ
- **Purpose**: Verify validation error recorded
- **Preconditions**: ValidationMiddleware with schema, ResponseContext with invalid ApiResult
- **Test Steps**:
  1. Create ValidationMiddleware with User schema
  2. Create ResponseContext with ApiResult containing invalid data
  3. Call process_response(context)
  4. Verify validation_error in context.metadata
- **Expected Result**: Validation error recorded in metadata
- **Coverage**: `ValidationMiddleware.process_response` method

#### TC-MW-019: ValidationMiddleware - только для успешных ответов
- **Purpose**: Verify validation only for successful responses
- **Preconditions**: ValidationMiddleware, ResponseContext with success=False
- **Test Steps**:
  1. Create ValidationMiddleware
  2. Create ResponseContext with ApiResult (success=False)
  3. Call process_response(context)
  4. Verify validation not performed
- **Expected Result**: Validation skipped for unsuccessful responses
- **Coverage**: `ValidationMiddleware.process_response` method

### 6. RequestContext Tests

#### TC-MW-020: RequestContext - инициализация
- **Purpose**: Verify RequestContext initialization
- **Preconditions**: Method, URL, optional headers/params/data
- **Test Steps**:
  1. Create RequestContext(method="GET", url="/test")
  2. Verify method, url, headers, params, data, metadata initialized
- **Expected Result**: RequestContext initialized correctly
- **Coverage**: `RequestContext.__init__` method

#### TC-MW-021: RequestContext - модификация headers
- **Purpose**: Verify headers can be modified
- **Preconditions**: RequestContext instance
- **Test Steps**:
  1. Create RequestContext
  2. Modify context.headers["X-Custom"] = "value"
  3. Verify header modified
- **Expected Result**: Headers can be modified
- **Coverage**: `RequestContext` headers modification

### 7. ResponseContext Tests

#### TC-MW-022: ResponseContext - инициализация
- **Purpose**: Verify ResponseContext initialization
- **Preconditions**: ApiResult instance
- **Test Steps**:
  1. Create ApiResult
  2. Create ResponseContext(result)
  3. Verify result, metadata initialized
- **Expected Result**: ResponseContext initialized correctly
- **Coverage**: `ResponseContext.__init__` method

#### TC-MW-023: ResponseContext - модификация result
- **Purpose**: Verify result can be modified
- **Preconditions**: ResponseContext instance
- **Test Steps**:
  1. Create ResponseContext with ApiResult
  2. Create new ApiResult
  3. Modify context.result = new_result
  4. Verify result modified
- **Expected Result**: Result can be modified
- **Coverage**: `ResponseContext` result modification

