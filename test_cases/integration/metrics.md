# Metrics Integration Test Cases

## Overview
Integration tests for metrics collection system with ApiClient and other clients.
Tests verify metrics collection, aggregation, and integration with middleware.

## Test Categories

### 1. Metrics with ApiClient

#### TC-INTEGRATION-METRICS-001: Metrics с ApiClient - сбор метрик запросов
- **Purpose**: Verify Metrics collects request metrics with ApiClient
- **Preconditions**:
  - ApiClient instance
  - Metrics instance
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create Metrics instance
  3. Mock HTTP responses with different latencies:
     - Request 1: status 200, latency 0.3s
     - Request 2: status 200, latency 0.5s
     - Request 3: status 500, latency 0.1s
  4. Make requests and manually record metrics:
     ```python
     start_time = time.time()
     result = await api.make_request("/endpoint")
     latency = time.time() - start_time
     metrics.record_request(success=result.success, latency=latency, error_type=result.error_message)
     ```
  5. Verify metrics collected:
     - request_count = 3
     - success_count = 2
     - error_count = 1
     - total_latency = 0.9s
     - avg_latency = 0.3s
     - min_latency = 0.1s
     - max_latency = 0.5s
     - errors_by_type contains error type
- **Expected Result**: Metrics collects request metrics correctly
- **Coverage**: `Metrics.record_request()`, metrics collection
- **Dependencies**: ApiClient, Metrics, manual metrics recording

#### TC-INTEGRATION-METRICS-002: Metrics с MetricsMiddleware - автоматический сбор метрик
- **Purpose**: Verify MetricsMiddleware automatically collects metrics
- **Preconditions**:
  - ApiClient instance
  - MetricsMiddleware with Metrics instance
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create Metrics instance
  3. Create MetricsMiddleware with Metrics
  4. Create MiddlewareChain and add MetricsMiddleware
  5. Initialize ApiClient with middleware chain
  6. Mock HTTP responses:
     - Request 1: status 200, latency 0.3s
     - Request 2: status 200, latency 0.5s
     - Request 3: status 500, latency 0.1s
  7. Make 3 requests using `make_request()`
  8. Verify MetricsMiddleware automatically collected metrics:
     - request_count = 3
     - success_count = 2
     - error_count = 1
     - total_latency > 0
     - avg_latency calculated correctly
- **Expected Result**: MetricsMiddleware automatically collects metrics for all requests
- **Coverage**: MetricsMiddleware.process_request(), MetricsMiddleware.process_response()
- **Dependencies**: ApiClient, MetricsMiddleware, Metrics

### 2. Metrics with GraphQLClient

#### TC-INTEGRATION-METRICS-003: Metrics с GraphQLClient
- **Purpose**: Verify Metrics collects metrics for GraphQL queries
- **Preconditions**:
  - GraphQLClient instance
  - Metrics instance
  - Mock GraphQL endpoint
- **Test Steps**:
  1. Create GraphQLClient with base URL
  2. Create Metrics instance
  3. Mock GraphQL responses with different latencies
  4. Execute GraphQL queries and record metrics manually
  5. Verify metrics collected:
     - request_count = number of queries
     - success_count = successful queries
     - error_count = failed queries
     - Latency metrics collected
- **Expected Result**: Metrics collects metrics for GraphQL queries
- **Coverage**: Metrics with GraphQLClient
- **Dependencies**: GraphQLClient, Metrics

### 3. Metrics with SoapClient

#### TC-INTEGRATION-METRICS-004: Metrics с SoapClient
- **Purpose**: Verify Metrics collects metrics for SOAP calls
- **Preconditions**:
  - SoapClient instance
  - Metrics instance
  - Mock SOAP endpoint
- **Test Steps**:
  1. Create SoapClient with base URL
  2. Create Metrics instance
  3. Mock SOAP responses with different latencies
  4. Execute SOAP calls and record metrics manually
  5. Verify metrics collected:
     - request_count = number of calls
     - success_count = successful calls
     - error_count = failed calls
     - Latency metrics collected
- **Expected Result**: Metrics collects metrics for SOAP calls
- **Coverage**: Metrics with SoapClient
- **Dependencies**: SoapClient, Metrics

### 4. Metrics with WebSocketClient

#### TC-INTEGRATION-METRICS-005: Metrics с WebSocketClient
- **Purpose**: Verify Metrics collects metrics for WebSocket messages
- **Preconditions**:
  - WebSocketClient instance
  - Metrics instance
  - Mock WebSocket server
- **Test Steps**:
  1. Create WebSocketClient with WebSocket URL
  2. Create Metrics instance
  3. Connect to WebSocket
  4. Send messages and record metrics manually
  5. Verify metrics collected:
     - request_count = number of messages
     - success_count = successful messages
     - error_count = failed messages
     - Latency metrics collected (if applicable)
- **Expected Result**: Metrics collects metrics for WebSocket messages
- **Coverage**: Metrics with WebSocketClient
- **Dependencies**: WebSocketClient, Metrics

### 5. Metrics with RequestBuilder

#### TC-INTEGRATION-METRICS-006: Metrics с RequestBuilder
- **Purpose**: Verify Metrics collects metrics for RequestBuilder requests
- **Preconditions**:
  - RequestBuilder with ApiClient
  - Metrics instance
  - Mock HTTP endpoint
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create Metrics instance
  3. Create RequestBuilder with ApiClient
  4. Mock HTTP responses with different latencies
  5. Execute requests using RequestBuilder and record metrics manually
  6. Verify metrics collected:
     - request_count = number of requests
     - success_count = successful requests
     - error_count = failed requests
     - Latency metrics collected
- **Expected Result**: Metrics collects metrics for RequestBuilder requests
- **Coverage**: Metrics with RequestBuilder
- **Dependencies**: RequestBuilder, ApiClient, Metrics

### 6. Metrics Aggregation

#### TC-INTEGRATION-METRICS-007: Metrics aggregation across multiple clients
- **Purpose**: Verify Metrics aggregates metrics from multiple clients
- **Preconditions**:
  - Multiple client instances (ApiClient, GraphQLClient, SoapClient)
  - Shared Metrics instance
  - Mock endpoints
- **Test Steps**:
  1. Create shared Metrics instance
  2. Create ApiClient, GraphQLClient, SoapClient
  3. Make requests from each client:
     - ApiClient: 3 requests
     - GraphQLClient: 2 queries
     - SoapClient: 1 call
  4. Record metrics for each request manually
  5. Verify aggregated metrics:
     - request_count = 6 (total from all clients)
     - success_count = sum of successes
     - error_count = sum of errors
     - total_latency = sum of all latencies
     - avg_latency = total_latency / request_count
- **Expected Result**: Metrics aggregates metrics from multiple clients correctly
- **Coverage**: Metrics aggregation, shared Metrics instance
- **Dependencies**: Multiple clients, shared Metrics instance

### 7. Metrics Export/Reporting

#### TC-INTEGRATION-METRICS-008: Metrics export/reporting
- **Purpose**: Verify Metrics can be exported and reported
- **Preconditions**:
  - ApiClient instance with Metrics
  - Metrics instance with collected data
- **Test Steps**:
  1. Create ApiClient with base URL
  2. Create Metrics instance
  3. Make multiple requests and collect metrics
  4. Export metrics to dictionary:
     ```python
     metrics_dict = {
         "request_count": metrics.request_count,
         "success_count": metrics.success_count,
         "error_count": metrics.error_count,
         "avg_latency": metrics.avg_latency,
         "min_latency": metrics.min_latency,
         "max_latency": metrics.max_latency,
         "success_rate": metrics.success_rate,
         "errors_by_type": dict(metrics.errors_by_type),
     }
     ```
  5. Verify exported metrics:
     - All metrics fields present
     - Values match collected metrics
     - success_rate calculated correctly
     - errors_by_type exported correctly
  6. Optionally export to JSON or other format
- **Expected Result**: Metrics can be exported and reported correctly
- **Coverage**: Metrics export, metrics reporting
- **Dependencies**: Metrics instance with collected data

