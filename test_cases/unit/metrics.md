# Metrics Module - Unit Test Cases

## Overview
Tests for `py_web_automation.metrics` module - performance metrics collection.

## Test Categories

### 1. Metrics - record_request Tests

#### TC-METRICS-001: Metrics - record_request успех
- **Purpose**: Verify recording successful request
- **Preconditions**: Metrics instance
- **Test Steps**:
  1. Create Metrics
  2. Call record_request(success=True, latency=0.5)
  3. Verify request_count=1, success_count=1, error_count=0
- **Expected Result**: Success metrics recorded
- **Coverage**: `Metrics.record_request` method - success

#### TC-METRICS-002: Metrics - record_request ошибка
- **Purpose**: Verify recording error request
- **Preconditions**: Metrics instance
- **Test Steps**:
  1. Create Metrics
  2. Call record_request(success=False, latency=0.1, error_type="timeout")
  3. Verify request_count=1, error_count=1, errors_by_type["timeout"]=1
- **Expected Result**: Error metrics recorded
- **Coverage**: `Metrics.record_request` method - error

#### TC-METRICS-003: Metrics - record_request без error_type
- **Purpose**: Verify recording error without error_type
- **Preconditions**: Metrics instance
- **Test Steps**:
  1. Create Metrics
  2. Call record_request(success=False, latency=0.1)
  3. Verify error_count=1, errors_by_type empty
- **Expected Result**: Error recorded without error_type
- **Coverage**: `Metrics.record_request` method - error without type

### 2. Metrics - Properties Tests

#### TC-METRICS-004: Metrics - avg_latency
- **Purpose**: Verify average latency calculation
- **Preconditions**: Metrics with multiple requests
- **Test Steps**:
  1. Create Metrics
  2. Record requests with latency: 0.1, 0.3, 0.5
  3. Verify avg_latency = 0.3
- **Expected Result**: Average latency = 0.3
- **Coverage**: `Metrics.avg_latency` property

#### TC-METRICS-005: Metrics - avg_latency без запросов
- **Purpose**: Verify avg_latency = 0.0 when no requests
- **Preconditions**: Empty Metrics
- **Test Steps**:
  1. Create Metrics
  2. Verify avg_latency = 0.0
- **Expected Result**: 0.0 returned
- **Coverage**: `Metrics.avg_latency` property - empty

#### TC-METRICS-006: Metrics - success_rate
- **Purpose**: Verify success rate calculation
- **Preconditions**: Metrics with mixed requests
- **Test Steps**:
  1. Create Metrics
  2. Record 10 requests (7 success, 3 errors)
  3. Verify success_rate = 70.0
- **Expected Result**: Success rate = 70.0%
- **Coverage**: `Metrics.success_rate` property

#### TC-METRICS-007: Metrics - error_rate
- **Purpose**: Verify error rate calculation
- **Preconditions**: Metrics with mixed requests
- **Test Steps**:
  1. Create Metrics
  2. Record 10 requests (7 success, 3 errors)
  3. Verify error_rate = 30.0
- **Expected Result**: Error rate = 30.0%
- **Coverage**: `Metrics.error_rate` property

#### TC-METRICS-008: Metrics - min_latency и max_latency
- **Purpose**: Verify min/max latency tracking
- **Preconditions**: Metrics with requests
- **Test Steps**:
  1. Create Metrics
  2. Record requests with latency: 0.1, 0.5, 0.3
  3. Verify min_latency=0.1, max_latency=0.5
- **Expected Result**: Min/max latency correct
- **Coverage**: `Metrics.min_latency` and `max_latency` properties

#### TC-METRICS-009: Metrics - requests_per_second
- **Purpose**: Verify RPS calculation
- **Preconditions**: Metrics with requests over time
- **Test Steps**:
  1. Create Metrics
  2. Record 10 requests
  3. Wait 1 second
  4. Verify requests_per_second ≈ 10
- **Expected Result**: RPS calculated correctly
- **Coverage**: `Metrics.requests_per_second` property

#### TC-METRICS-010: Metrics - requests_per_second без запросов
- **Purpose**: Verify RPS = 0.0 when no requests
- **Preconditions**: Empty Metrics
- **Test Steps**:
  1. Create Metrics
  2. Verify requests_per_second = 0.0
- **Expected Result**: 0.0 returned
- **Coverage**: `Metrics.requests_per_second` property - empty

### 3. Metrics - Utility Methods Tests

#### TC-METRICS-011: Metrics - reset
- **Purpose**: Verify metrics reset
- **Preconditions**: Metrics with data
- **Test Steps**:
  1. Create Metrics
  2. Record several requests
  3. Call reset()
  4. Verify all metrics reset to zero/None
- **Expected Result**: All metrics reset
- **Coverage**: `Metrics.reset` method

#### TC-METRICS-012: Metrics - to_dict
- **Purpose**: Verify conversion to dictionary
- **Preconditions**: Metrics with data
- **Test Steps**:
  1. Create Metrics
  2. Record several requests
  3. Call to_dict()
  4. Verify dictionary contains all metrics
- **Expected Result**: Dictionary with all metrics
- **Coverage**: `Metrics.to_dict` method

#### TC-METRICS-013: Metrics - get_summary
- **Purpose**: Verify formatted summary
- **Preconditions**: Metrics with data
- **Test Steps**:
  1. Create Metrics
  2. Record several requests
  3. Call get_summary()
  4. Verify formatted string contains key metrics
- **Expected Result**: Formatted summary string
- **Coverage**: `Metrics.get_summary` method

#### TC-METRICS-014: Metrics - last_request_time
- **Purpose**: Verify last_request_time tracking
- **Preconditions**: Metrics instance
- **Test Steps**:
  1. Create Metrics
  2. Record request
  3. Verify last_request_time is recent
- **Expected Result**: last_request_time set correctly
- **Coverage**: `Metrics.last_request_time` field

#### TC-METRICS-015: Metrics - errors_by_type aggregation
- **Purpose**: Verify error type aggregation
- **Preconditions**: Metrics instance
- **Test Steps**:
  1. Create Metrics
  2. Record 3 errors with error_type="timeout"
  3. Record 2 errors with error_type="connection"
  4. Verify errors_by_type["timeout"]=3, errors_by_type["connection"]=2
- **Expected Result**: Errors aggregated by type
- **Coverage**: `Metrics.errors_by_type` field

