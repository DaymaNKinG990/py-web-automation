# Cache Integration Test Cases

## Overview
Integration tests for response caching system with ApiClient and other clients.
Tests verify cache hit/miss behavior, TTL expiration, and cache invalidation.

## Test Categories

### 1. ResponseCache with ApiClient

#### TC-INTEGRATION-CACHE-001: ResponseCache с ApiClient - кэширование GET запросов
- **Purpose**: Verify ResponseCache caches GET requests with ApiClient
- **Preconditions**:
  - ApiClient instance
  - ResponseCache instance
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create ResponseCache with default_ttl=300
  3. Initialize ApiClient with cache
  4. Mock HTTP response (status 200, JSON data)
  5. Make first GET request using `make_request()` with use_cache=True
  6. Verify cache miss:
     - Request sent to HTTP endpoint
     - Response cached
     - Cache entry created
  7. Make second GET request with same endpoint and parameters
  8. Verify cache hit:
     - Request NOT sent to HTTP endpoint
     - Response returned from cache
     - Response matches first request
- **Expected Result**: GET requests cached, subsequent requests return cached response
- **Coverage**: `ResponseCache.get()`, `ResponseCache.set()`, `ApiClient.make_request()` with cache
- **Dependencies**: ApiClient, ResponseCache, mock HTTP client

#### TC-INTEGRATION-CACHE-002: Cache invalidation при POST/PUT/DELETE
- **Purpose**: Verify cache is invalidated on non-GET requests
- **Preconditions**:
  - ApiClient instance with ResponseCache
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL and ResponseCache
  2. Mock HTTP response (status 200)
  3. Make GET request and verify cached
  4. Make POST request to same endpoint using `make_request()` with method="POST"
  5. Verify cache invalidation:
     - POST request sent to HTTP endpoint
     - Cache entry invalidated (if applicable)
  6. Make GET request again
  7. Verify cache miss (cache was invalidated):
     - Request sent to HTTP endpoint
     - New response cached
- **Expected Result**: Cache invalidated on POST/PUT/DELETE requests
- **Coverage**: Cache invalidation logic, non-GET request handling
- **Dependencies**: ApiClient, ResponseCache

#### TC-INTEGRATION-CACHE-003: Cache TTL expiration
- **Purpose**: Verify cache entries expire after TTL
- **Preconditions**:
  - ApiClient instance with ResponseCache
  - Mock HTTP endpoint
  - Time manipulation capability
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create ResponseCache with default_ttl=1 (1 second for testing)
  3. Initialize ApiClient with cache
  4. Mock HTTP response (status 200)
  5. Make GET request and verify cached
  6. Make second GET request immediately (within TTL)
  7. Verify cache hit (response from cache)
  8. Wait for TTL to expire (1 second)
  9. Make third GET request after TTL expiration
  10. Verify cache miss:
      - Request sent to HTTP endpoint
      - New response cached
      - Old cache entry expired
- **Expected Result**: Cache entries expire after TTL, expired entries not returned
- **Coverage**: `CacheEntry.is_expired()`, TTL expiration logic
- **Dependencies**: ApiClient, ResponseCache, time manipulation

### 2. ResponseCache with GraphQLClient

#### TC-INTEGRATION-CACHE-004: ResponseCache с GraphQLClient - кэширование queries
- **Purpose**: Verify ResponseCache caches GraphQL queries
- **Preconditions**:
  - GraphQLClient instance
  - ResponseCache instance
  - Mock GraphQL endpoint
- **Test Steps**:
  1. Create GraphQLClient with base URL
  2. Create ResponseCache with default_ttl=300
  3. Mock GraphQL response (status 200, valid GraphQL data)
  4. Execute GraphQL query using `query()` (if cache supported)
  5. Verify query cached (if applicable)
  6. Execute same query again
  7. Verify cache hit (if applicable):
     - Query result returned from cache
     - No HTTP request made
- **Expected Result**: GraphQL queries cached (if supported)
- **Coverage**: ResponseCache with GraphQLClient
- **Dependencies**: GraphQLClient, ResponseCache

### 3. Cache with RequestBuilder

#### TC-INTEGRATION-CACHE-005: ResponseCache с RequestBuilder
- **Purpose**: Verify ResponseCache works with RequestBuilder
- **Preconditions**:
  - RequestBuilder with ApiClient
  - ResponseCache instance
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL and ResponseCache
  2. Create RequestBuilder with ApiClient
  3. Mock HTTP response (status 200)
  4. Execute GET request using RequestBuilder
  5. Verify request cached
  6. Execute same request again using RequestBuilder
  7. Verify cache hit:
     - Response returned from cache
     - No HTTP request made
- **Expected Result**: RequestBuilder requests cached correctly
- **Coverage**: ResponseCache with RequestBuilder
- **Dependencies**: RequestBuilder, ApiClient, ResponseCache

### 4. Cache with Middleware

#### TC-INTEGRATION-CACHE-006: Cache middleware - кэширование через middleware
- **Purpose**: Verify cache can be implemented as middleware
- **Preconditions**:
  - ApiClient instance
  - Custom CacheMiddleware
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create CacheMiddleware that implements caching logic
  3. Create MiddlewareChain and add CacheMiddleware
  4. Initialize ApiClient with middleware chain
  5. Mock HTTP response (status 200)
  6. Make GET request using `make_request()`
  7. Verify CacheMiddleware cached response
  8. Make second GET request with same parameters
  9. Verify CacheMiddleware returned cached response:
     - Request intercepted by middleware
     - Cached response returned
     - No HTTP request made
- **Expected Result**: Cache middleware caches responses correctly
- **Coverage**: CacheMiddleware implementation, middleware-based caching
- **Dependencies**: ApiClient, MiddlewareChain, CacheMiddleware

