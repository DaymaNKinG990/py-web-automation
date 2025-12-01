# Retry Integration Test Cases

## Overview
Integration tests for retry mechanism with ApiClient and other clients.
Tests verify automatic retry on failures, exponential backoff, and retry configuration.

## Test Categories

### 1. Retry with ApiClient

#### TC-INTEGRATION-RETRY-001: Retry с ApiClient - автоматический retry при ошибках
- **Purpose**: Verify automatic retry on connection errors with ApiClient
- **Preconditions**:
  - ApiClient instance with retry enabled
  - Mock HTTP endpoint that fails initially then succeeds
- **Test Steps**:
  1. Create ApiClient with base URL and config (retry_count=3, retry_delay=1.0)
  2. Mock HTTP client to fail first 2 attempts (ConnectionError), succeed on 3rd
  3. Make request using `make_request()` with enable_auto_retry=True
  4. Verify retry behavior:
     - First attempt failed (ConnectionError)
     - Second attempt failed (ConnectionError)
     - Third attempt succeeded (status 200)
     - Total attempts = 3
  5. Verify exponential backoff delay between retries
- **Expected Result**: Request retried automatically on connection errors, succeeded on 3rd attempt
- **Coverage**: `retry_on_connection_error()`, `ApiClient.make_request()` with auto retry
- **Dependencies**: ApiClient, retry mechanism, mock HTTP client

#### TC-INTEGRATION-RETRY-002: Retry с ApiClient - превышение max_attempts
- **Purpose**: Verify retry stops after max_attempts
- **Preconditions**:
  - ApiClient instance with retry enabled
  - Mock HTTP endpoint that always fails
- **Test Steps**:
  1. Create ApiClient with base URL and config (retry_count=3, retry_delay=1.0)
  2. Mock HTTP client to always fail (ConnectionError)
  3. Make request using `make_request()` with enable_auto_retry=True
  4. Verify retry behavior:
     - All 3 attempts failed
     - Final exception raised (ConnectionError)
     - No more retries after max_attempts
  5. Verify exception contains retry information
- **Expected Result**: Retry stops after max_attempts, final exception raised
- **Coverage**: `retry_on_connection_error()` with max_attempts limit
- **Dependencies**: ApiClient, retry mechanism, mock HTTP client

#### TC-INTEGRATION-RETRY-003: Retry с ApiClient - exponential backoff
- **Purpose**: Verify exponential backoff delay between retries
- **Preconditions**:
  - ApiClient instance with retry enabled
  - Mock HTTP endpoint that fails initially
  - Time tracking capability
- **Test Steps**:
  1. Create ApiClient with base URL and config (retry_count=3, retry_delay=1.0, backoff=2.0)
  2. Mock HTTP client to fail first 2 attempts, succeed on 3rd
  3. Track time between retry attempts
  4. Make request using `make_request()` with enable_auto_retry=True
  5. Verify exponential backoff:
     - Delay between attempt 1 and 2: ~1.0s (delay)
     - Delay between attempt 2 and 3: ~2.0s (delay * backoff)
     - Total retry time: ~3.0s
- **Expected Result**: Exponential backoff delays increase correctly between retries
- **Coverage**: `retry_on_connection_error()` with exponential backoff
- **Dependencies**: ApiClient, retry mechanism, time tracking

### 2. Retry with GraphQLClient

#### TC-INTEGRATION-RETRY-004: Retry с GraphQLClient
- **Purpose**: Verify retry mechanism works with GraphQLClient
- **Preconditions**:
  - GraphQLClient instance
  - Mock GraphQL endpoint that fails initially
- **Test Steps**:
  1. Create GraphQLClient with base URL and config (retry_count=2, retry_delay=0.5)
  2. Mock HTTP client to fail first attempt (ConnectionError), succeed on 2nd
  3. Execute GraphQL query using `query()`
  4. Verify retry behavior:
     - First attempt failed
     - Second attempt succeeded
     - Query result returned successfully
- **Expected Result**: GraphQL query retried on connection errors
- **Coverage**: Retry with GraphQLClient
- **Dependencies**: GraphQLClient, retry mechanism

### 3. Retry with SoapClient

#### TC-INTEGRATION-RETRY-005: Retry с SoapClient
- **Purpose**: Verify retry mechanism works with SoapClient
- **Preconditions**:
  - SoapClient instance
  - Mock SOAP endpoint that fails initially
- **Test Steps**:
  1. Create SoapClient with base URL and config (retry_count=2, retry_delay=0.5)
  2. Mock HTTP client to fail first attempt (ConnectionError), succeed on 2nd
  3. Execute SOAP call using `call()`
  4. Verify retry behavior:
     - First attempt failed
     - Second attempt succeeded
     - SOAP response returned successfully
- **Expected Result**: SOAP call retried on connection errors
- **Coverage**: Retry with SoapClient
- **Dependencies**: SoapClient, retry mechanism

### 4. Retry with WebSocketClient

#### TC-INTEGRATION-RETRY-006: Retry с WebSocketClient - connection retry
- **Purpose**: Verify retry mechanism works with WebSocketClient connection
- **Preconditions**:
  - WebSocketClient instance
  - Mock WebSocket server that fails initially
- **Test Steps**:
  1. Create WebSocketClient with WebSocket URL and config (retry_count=2, retry_delay=0.5)
  2. Mock WebSocket connection to fail first attempt, succeed on 2nd
  3. Connect to WebSocket using `connect()` with retry decorator
  4. Verify retry behavior:
     - First connection attempt failed
     - Second connection attempt succeeded
     - WebSocket connected successfully
- **Expected Result**: WebSocket connection retried on failures
- **Coverage**: Retry with WebSocketClient.connect()
- **Dependencies**: WebSocketClient, retry mechanism

### 5. Retry with DBClient

#### TC-INTEGRATION-RETRY-007: Retry с DBClient - connection errors
- **Purpose**: Verify retry mechanism works with DBClient connection errors
- **Preconditions**:
  - DBClient instance
  - Database that fails initially then succeeds
- **Test Steps**:
  1. Create DBClient with database connection string and config (retry_count=2, retry_delay=0.5)
  2. Mock database connection to fail first attempt (ConnectionError), succeed on 2nd
  3. Connect to database using `connect()` with retry decorator
  4. Verify retry behavior:
     - First connection attempt failed
     - Second connection attempt succeeded
     - Database connected successfully
  5. Execute query to verify connection works
- **Expected Result**: DBClient connection retried on connection errors
- **Coverage**: Retry with DBClient.connect()
- **Dependencies**: DBClient, retry mechanism

### 6. Retry with UiClient

#### TC-INTEGRATION-RETRY-008: Retry с UiClient - timeout retry
- **Purpose**: Verify retry mechanism works with UiClient timeouts
- **Preconditions**:
  - UiClient instance
  - Web page that loads slowly
- **Test Steps**:
  1. Create UiClient with base URL and config (retry_count=2, retry_delay=1.0, timeout=5.0)
  2. Mock page load to timeout first attempt, succeed on 2nd
  3. Navigate to page using `navigate()` with retry decorator
  4. Verify retry behavior:
     - First navigation attempt timed out
     - Second navigation attempt succeeded
     - Page loaded successfully
- **Expected Result**: UiClient navigation retried on timeouts
- **Coverage**: Retry with UiClient.navigate()
- **Dependencies**: UiClient, retry mechanism

### 7. Retry with RequestBuilder

#### TC-INTEGRATION-RETRY-009: Retry с RequestBuilder
- **Purpose**: Verify retry mechanism works with RequestBuilder
- **Preconditions**:
  - RequestBuilder with ApiClient
  - Mock HTTP endpoint that fails initially
- **Test Steps**:
  1. Create ApiClient with base URL and config (retry_count=2, retry_delay=0.5)
  2. Create RequestBuilder with ApiClient
  3. Mock HTTP client to fail first attempt (ConnectionError), succeed on 2nd
  4. Execute request using RequestBuilder with retry
  5. Verify retry behavior:
     - First attempt failed
     - Second attempt succeeded
     - Request result returned successfully
- **Expected Result**: RequestBuilder request retried on connection errors
- **Coverage**: Retry with RequestBuilder.execute()
- **Dependencies**: RequestBuilder, ApiClient, retry mechanism

### 8. Retry with CircuitBreaker

#### TC-INTEGRATION-RETRY-010: Retry с CircuitBreaker - комбинированное использование
- **Purpose**: Verify retry and circuit breaker work together
- **Preconditions**:
  - ApiClient with retry and circuit breaker
  - Mock HTTP endpoint that fails intermittently
- **Test Steps**:
  1. Create ApiClient with base URL and config (retry_count=2, retry_delay=0.5)
  2. Create CircuitBreaker with failure_threshold=3
  3. Mock HTTP client to fail 2 times, then succeed
  4. Make multiple requests:
     - Request 1: fails, retries, succeeds
     - Request 2: fails, retries, succeeds
     - Request 3: fails, retries, succeeds
  5. Verify circuit breaker state:
     - Circuit remains CLOSED (not enough failures)
     - Retry works independently
  6. Mock HTTP client to fail consistently
  7. Make requests until circuit opens
  8. Verify circuit breaker blocks requests when OPEN
  9. Verify retry doesn't execute when circuit is OPEN
- **Expected Result**: Retry and circuit breaker work together correctly
- **Coverage**: Retry with CircuitBreaker integration
- **Dependencies**: ApiClient, retry mechanism, CircuitBreaker

