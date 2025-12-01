# Circuit Breaker Integration Test Cases

## Overview
Integration tests for circuit breaker pattern with ApiClient and other clients.
Tests verify circuit breaker state transitions, failure handling, and recovery.

## Test Categories

### 1. CircuitBreaker with ApiClient

#### TC-INTEGRATION-CB-001: CircuitBreaker с ApiClient - защита от cascading failures
- **Purpose**: Verify CircuitBreaker protects against cascading failures
- **Preconditions**:
  - ApiClient instance
  - CircuitBreaker instance
  - Mock HTTP endpoint that fails
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create CircuitBreaker with failure_threshold=3, timeout=60.0
  3. Mock HTTP client to always return status 500 (server error)
  4. Make requests until circuit opens:
     - Request 1: fails (500), circuit CLOSED
     - Request 2: fails (500), circuit CLOSED
     - Request 3: fails (500), circuit CLOSED
     - Request 4: fails (500), circuit OPEN (threshold reached)
  5. Verify circuit breaker state:
     - Circuit state is OPEN
     - CircuitBreakerOpenError raised on subsequent requests
     - No requests sent to failing endpoint
  6. Verify circuit breaker stats:
     - failures = 4
     - state = OPEN
- **Expected Result**: Circuit breaker opens after failure threshold, blocks requests
- **Coverage**: `CircuitBreaker.__call__()`, state transitions, failure counting
- **Dependencies**: ApiClient, CircuitBreaker, mock HTTP client

#### TC-INTEGRATION-CB-002: CircuitBreaker state transitions - CLOSED → OPEN → HALF_OPEN → CLOSED
- **Purpose**: Verify circuit breaker state transitions work correctly
- **Preconditions**:
  - ApiClient instance
  - CircuitBreaker instance
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create CircuitBreaker with failure_threshold=2, timeout=1.0, success_threshold=2
  3. Verify initial state: CLOSED
  4. Mock HTTP client to fail 2 times (status 500)
  5. Make 2 requests, verify circuit opens (state = OPEN)
  6. Wait for timeout (1 second)
  7. Verify circuit transitions to HALF_OPEN
  8. Mock HTTP client to succeed
  9. Make 2 successful requests
  10. Verify circuit closes (state = CLOSED):
      - Both requests succeeded
      - Circuit state = CLOSED
      - Requests allowed again
- **Expected Result**: Circuit breaker transitions through all states correctly
- **Coverage**: State transitions, timeout handling, recovery
- **Dependencies**: ApiClient, CircuitBreaker, time manipulation

#### TC-INTEGRATION-CB-003: CircuitBreaker с GraphQLClient
- **Purpose**: Verify CircuitBreaker works with GraphQLClient
- **Preconditions**:
  - GraphQLClient instance
  - CircuitBreaker instance
  - Mock GraphQL endpoint
- **Test Steps**:
  1. Create GraphQLClient with base URL
  2. Create CircuitBreaker with failure_threshold=2
  3. Mock GraphQL endpoint to fail (status 500)
  4. Execute GraphQL queries until circuit opens
  5. Verify circuit breaker blocks GraphQL requests when OPEN
  6. Wait for timeout and verify circuit transitions to HALF_OPEN
  7. Mock GraphQL endpoint to succeed
  8. Execute successful queries to close circuit
- **Expected Result**: Circuit breaker works with GraphQLClient
- **Coverage**: CircuitBreaker with GraphQLClient
- **Dependencies**: GraphQLClient, CircuitBreaker

#### TC-INTEGRATION-CB-004: CircuitBreaker с SoapClient
- **Purpose**: Verify CircuitBreaker works with SoapClient
- **Preconditions**:
  - SoapClient instance
  - CircuitBreaker instance
  - Mock SOAP endpoint
- **Test Steps**:
  1. Create SoapClient with base URL
  2. Create CircuitBreaker with failure_threshold=2
  3. Mock SOAP endpoint to fail (SOAP fault)
  4. Execute SOAP calls until circuit opens
  5. Verify circuit breaker blocks SOAP requests when OPEN
  6. Wait for timeout and verify circuit transitions to HALF_OPEN
  7. Mock SOAP endpoint to succeed
  8. Execute successful calls to close circuit
- **Expected Result**: Circuit breaker works with SoapClient
- **Coverage**: CircuitBreaker with SoapClient
- **Dependencies**: SoapClient, CircuitBreaker

#### TC-INTEGRATION-CB-005: CircuitBreaker с WebSocketClient
- **Purpose**: Verify CircuitBreaker works with WebSocketClient
- **Preconditions**:
  - WebSocketClient instance
  - CircuitBreaker instance
  - Mock WebSocket server
- **Test Steps**:
  1. Create WebSocketClient with WebSocket URL
  2. Create CircuitBreaker with failure_threshold=2
  3. Mock WebSocket connection to fail
  4. Attempt connections until circuit opens
  5. Verify circuit breaker blocks WebSocket connections when OPEN
  6. Wait for timeout and verify circuit transitions to HALF_OPEN
  7. Mock WebSocket connection to succeed
  8. Connect successfully to close circuit
- **Expected Result**: Circuit breaker works with WebSocketClient
- **Coverage**: CircuitBreaker with WebSocketClient
- **Dependencies**: WebSocketClient, CircuitBreaker

### 2. CircuitBreaker with DBClient

#### TC-INTEGRATION-CB-006: CircuitBreaker с DBClient - защита при DB errors
- **Purpose**: Verify CircuitBreaker protects against database errors
- **Preconditions**:
  - DBClient instance
  - CircuitBreaker instance
  - Database connection
- **Test Steps**:
  1. Create DBClient with database connection string
  2. Create CircuitBreaker with failure_threshold=2
  3. Mock database to fail (connection errors or query errors)
  4. Execute database queries until circuit opens
  5. Verify circuit breaker blocks database queries when OPEN
  6. Wait for timeout and verify circuit transitions to HALF_OPEN
  7. Mock database to succeed
  8. Execute successful queries to close circuit
- **Expected Result**: Circuit breaker protects against database errors
- **Coverage**: CircuitBreaker with DBClient
- **Dependencies**: DBClient, CircuitBreaker

### 3. CircuitBreaker with RequestBuilder

#### TC-INTEGRATION-CB-007: CircuitBreaker с RequestBuilder
- **Purpose**: Verify CircuitBreaker works with RequestBuilder
- **Preconditions**:
  - RequestBuilder with ApiClient
  - CircuitBreaker instance
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create CircuitBreaker with failure_threshold=2
  3. Create RequestBuilder with ApiClient
  4. Mock HTTP endpoint to fail (status 500)
  5. Execute requests using RequestBuilder until circuit opens
  6. Verify circuit breaker blocks RequestBuilder requests when OPEN
  7. Wait for timeout and verify circuit transitions to HALF_OPEN
  8. Mock HTTP endpoint to succeed
  9. Execute successful requests to close circuit
- **Expected Result**: Circuit breaker works with RequestBuilder
- **Coverage**: CircuitBreaker with RequestBuilder
- **Dependencies**: RequestBuilder, ApiClient, CircuitBreaker

### 4. CircuitBreaker with Retry

#### TC-INTEGRATION-CB-008: CircuitBreaker с Retry - комбинированное использование
- **Purpose**: Verify CircuitBreaker and Retry work together
- **Preconditions**:
  - ApiClient instance with retry and circuit breaker
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL and config (retry_count=2, retry_delay=0.5)
  2. Create CircuitBreaker with failure_threshold=3
  3. Mock HTTP client to fail intermittently
  4. Make requests:
     - Request 1: fails, retries, succeeds (circuit CLOSED)
     - Request 2: fails, retries, succeeds (circuit CLOSED)
     - Request 3: fails, retries, succeeds (circuit CLOSED)
  5. Verify retry works independently when circuit is CLOSED
  6. Mock HTTP client to always fail
  7. Make requests until circuit opens
  8. Verify circuit breaker blocks requests when OPEN:
     - CircuitBreakerOpenError raised immediately
     - Retry does NOT execute (circuit is OPEN)
     - No requests sent to failing endpoint
  9. Wait for timeout and verify circuit transitions to HALF_OPEN
  10. Mock HTTP client to succeed
  11. Make successful requests to close circuit
  12. Verify retry works again when circuit is CLOSED
- **Expected Result**: Circuit breaker and retry work together correctly
- **Coverage**: CircuitBreaker with Retry integration
- **Dependencies**: ApiClient, CircuitBreaker, retry mechanism

