# Rate Limit Integration Test Cases

## Overview
Integration tests for rate limiting system with ApiClient and other clients.
Tests verify rate limiting behavior, request throttling, and rate limit configuration.

## Test Categories

### 1. RateLimiter with ApiClient

#### TC-INTEGRATION-RL-001: RateLimiter с ApiClient - ограничение частоты запросов
- **Purpose**: Verify RateLimiter limits request rate with ApiClient
- **Preconditions**:
  - ApiClient instance
  - RateLimiter instance with max_requests=5, window=60
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create RateLimiter with max_requests=5, window=60
  3. Initialize ApiClient with rate_limiter
  4. Mock HTTP response (status 200)
  5. Make 5 requests using `make_request()` with skip_rate_limit=False
  6. Verify all 5 requests succeed immediately
  7. Make 6th request
  8. Verify rate limiter blocks request:
     - Request delayed (wait for rate limit window)
     - Request eventually succeeds after delay
- **Expected Result**: RateLimiter limits request rate, blocks requests exceeding limit
- **Coverage**: `RateLimiter.acquire()`, `ApiClient.make_request()` with rate limiter
- **Dependencies**: ApiClient, RateLimiter, mock HTTP client

#### TC-INTEGRATION-RL-002: RateLimiter с ApiClient - burst handling
- **Purpose**: Verify RateLimiter handles burst requests correctly
- **Preconditions**:
  - ApiClient instance
  - RateLimiter instance with max_requests=10, window=60, burst=5
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create RateLimiter with max_requests=10, window=60, burst=5
  3. Initialize ApiClient with rate_limiter
  4. Mock HTTP response (status 200)
  5. Make burst of 15 requests (10 normal + 5 burst)
  6. Verify burst handling:
     - First 10 requests succeed immediately
     - Next 5 requests (burst) succeed immediately
     - Request 16 is blocked (exceeds limit + burst)
- **Expected Result**: RateLimiter allows burst requests up to burst limit
- **Coverage**: RateLimiter burst handling
- **Dependencies**: ApiClient, RateLimiter

#### TC-INTEGRATION-RL-003: RateLimiter с ApiClient - skip_rate_limit
- **Purpose**: Verify skip_rate_limit parameter bypasses rate limiting
- **Preconditions**:
  - ApiClient instance with RateLimiter
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL and RateLimiter (max_requests=2, window=60)
  2. Mock HTTP response (status 200)
  3. Make 2 requests (rate limit reached)
  4. Make 3rd request with skip_rate_limit=True
  5. Verify request succeeds immediately (bypasses rate limit)
  6. Make 4th request with skip_rate_limit=False
  7. Verify request is blocked (rate limit still applies)
- **Expected Result**: skip_rate_limit bypasses rate limiting for specific requests
- **Coverage**: `ApiClient.make_request()` with skip_rate_limit parameter
- **Dependencies**: ApiClient, RateLimiter

### 2. RateLimiter with GraphQLClient

#### TC-INTEGRATION-RL-004: RateLimiter с GraphQLClient
- **Purpose**: Verify RateLimiter works with GraphQLClient
- **Preconditions**:
  - GraphQLClient instance
  - RateLimiter instance
  - Mock GraphQL endpoint
- **Test Steps**:
  1. Create GraphQLClient with base URL
  2. Create RateLimiter with max_requests=3, window=60
  3. Mock GraphQL response (status 200)
  4. Execute 3 GraphQL queries
  5. Verify all queries succeed
  6. Execute 4th query
  7. Verify rate limiter blocks query (if integrated)
- **Expected Result**: RateLimiter works with GraphQLClient (if integrated)
- **Coverage**: RateLimiter with GraphQLClient
- **Dependencies**: GraphQLClient, RateLimiter

### 3. RateLimiter with SoapClient

#### TC-INTEGRATION-RL-005: RateLimiter с SoapClient
- **Purpose**: Verify RateLimiter works with SoapClient
- **Preconditions**:
  - SoapClient instance
  - RateLimiter instance
  - Mock SOAP endpoint
- **Test Steps**:
  1. Create SoapClient with base URL
  2. Create RateLimiter with max_requests=3, window=60
  3. Mock SOAP response (status 200)
  4. Execute 3 SOAP calls
  5. Verify all calls succeed
  6. Execute 4th call
  7. Verify rate limiter blocks call (if integrated)
- **Expected Result**: RateLimiter works with SoapClient (if integrated)
- **Coverage**: RateLimiter with SoapClient
- **Dependencies**: SoapClient, RateLimiter

### 4. RateLimiter with WebSocketClient

#### TC-INTEGRATION-RL-006: RateLimiter с WebSocketClient
- **Purpose**: Verify RateLimiter works with WebSocketClient
- **Preconditions**:
  - WebSocketClient instance
  - RateLimiter instance
  - Mock WebSocket server
- **Test Steps**:
  1. Create WebSocketClient with WebSocket URL
  2. Create RateLimiter with max_requests=3, window=60
  3. Connect to WebSocket
  4. Send 3 messages
  5. Verify all messages sent successfully
  6. Send 4th message
  7. Verify rate limiter blocks message (if integrated)
- **Expected Result**: RateLimiter works with WebSocketClient (if integrated)
- **Coverage**: RateLimiter with WebSocketClient
- **Dependencies**: WebSocketClient, RateLimiter

### 5. RateLimiter with RequestBuilder

#### TC-INTEGRATION-RL-007: RateLimiter с RequestBuilder
- **Purpose**: Verify RateLimiter works with RequestBuilder
- **Preconditions**:
  - RequestBuilder with ApiClient
  - RateLimiter instance
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL and RateLimiter (max_requests=3, window=60)
  2. Create RequestBuilder with ApiClient
  3. Mock HTTP response (status 200)
  4. Execute 3 requests using RequestBuilder
  5. Verify all requests succeed
  6. Execute 4th request
  7. Verify rate limiter blocks request
- **Expected Result**: RateLimiter works with RequestBuilder
- **Coverage**: RateLimiter with RequestBuilder
- **Dependencies**: RequestBuilder, ApiClient, RateLimiter

### 6. RateLimiter with Middleware

#### TC-INTEGRATION-RL-008: Rate limit middleware
- **Purpose**: Verify rate limiting can be implemented as middleware
- **Preconditions**:
  - ApiClient instance
  - Custom RateLimitMiddleware
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create RateLimitMiddleware that implements rate limiting logic
  3. Create MiddlewareChain and add RateLimitMiddleware
  4. Initialize ApiClient with middleware chain
  5. Mock HTTP response (status 200)
  6. Make requests using `make_request()`
  7. Verify RateLimitMiddleware enforces rate limits:
     - Requests within limit succeed
     - Requests exceeding limit are blocked/delayed
- **Expected Result**: Rate limit middleware enforces rate limits correctly
- **Coverage**: RateLimitMiddleware implementation, middleware-based rate limiting
- **Dependencies**: ApiClient, MiddlewareChain, RateLimitMiddleware

