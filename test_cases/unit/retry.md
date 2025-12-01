# Retry Module - Unit Test Cases

## Overview
Tests for `py_web_automation.retry` module - automatic retry mechanism with exponential backoff.

## Test Categories

### 1. retry_on_failure Decorator Tests

#### TC-RETRY-001: retry_on_failure - успешный вызов без повторов
- **Purpose**: Verify decorator doesn't affect successful calls
- **Preconditions**: Function that succeeds immediately
- **Test Steps**:
  1. Create function with `@retry_on_failure` decorator
  2. Call function successfully
  3. Verify function called exactly 1 time
- **Expected Result**: Function called 1 time, result returned
- **Coverage**: `retry_on_failure` decorator - success path

#### TC-RETRY-002: retry_on_failure - повтор при ошибке
- **Purpose**: Verify decorator retries on failure
- **Preconditions**: Function that fails 2 times, then succeeds
- **Test Steps**:
  1. Create function that raises exception 2 times, then returns value
  2. Apply `@retry_on_failure(max_attempts=3)`
  3. Call function
  4. Verify function called 3 times
- **Expected Result**: Function called 3 times, result returned on 3rd attempt
- **Coverage**: `retry_on_failure` decorator - retry logic

#### TC-RETRY-003: retry_on_failure - exponential backoff
- **Purpose**: Verify delay increases exponentially
- **Preconditions**: Function that fails multiple times
- **Test Steps**:
  1. Create function with `@retry_on_failure(delay=1.0, backoff=2.0)`
  2. Mock asyncio.sleep
  3. Call function that fails 2 times
  4. Verify sleep called with delays: 1.0, 2.0 seconds
- **Expected Result**: Delays increase exponentially (1.0, 2.0)
- **Coverage**: `retry_on_failure` decorator - exponential backoff

#### TC-RETRY-004: retry_on_failure - on_retry callback
- **Purpose**: Verify callback is called on each retry
- **Preconditions**: Function that fails, callback function
- **Test Steps**:
  1. Create callback function
  2. Apply `@retry_on_failure(on_retry=callback)`
  3. Call function that fails 2 times
  4. Verify callback called 2 times with correct parameters (attempt_number, exception)
- **Expected Result**: Callback called for each retry attempt
- **Coverage**: `retry_on_failure` decorator - on_retry callback

#### TC-RETRY-005: retry_on_failure - исключение после всех попыток
- **Purpose**: Verify exception is raised after all attempts fail
- **Preconditions**: Function that always fails
- **Test Steps**:
  1. Create function that always raises exception
  2. Apply `@retry_on_failure(max_attempts=3)`
  3. Call function
  4. Verify exception is raised after 3 attempts
- **Expected Result**: Exception raised after 3 attempts
- **Coverage**: `retry_on_failure` decorator - exception propagation

#### TC-RETRY-006: retry_on_failure - специфичные исключения
- **Purpose**: Verify only specified exceptions trigger retry
- **Preconditions**: Function that raises different exception types
- **Test Steps**:
  1. Create function that raises ValueError
  2. Apply `@retry_on_failure(exceptions=(ConnectionError,))`
  3. Call function
  4. Verify exception is raised immediately (no retry)
- **Expected Result**: Exception raised immediately, no retry
- **Coverage**: `retry_on_failure` decorator - exception filtering

### 2. retry_on_connection_error Decorator Tests

#### TC-RETRY-007: retry_on_connection_error - ConnectionError
- **Purpose**: Verify decorator retries on ConnectionError
- **Preconditions**: Function that raises ConnectionError
- **Test Steps**:
  1. Create function that raises ConnectionError 2 times, then succeeds
  2. Apply `@retry_on_connection_error(max_attempts=3)`
  3. Call function
  4. Verify function called 3 times
- **Expected Result**: Function retried on ConnectionError
- **Coverage**: `retry_on_connection_error` decorator

#### TC-RETRY-008: retry_on_connection_error - TimeoutError
- **Purpose**: Verify decorator retries on TimeoutError
- **Preconditions**: Function that raises TimeoutError
- **Test Steps**:
  1. Create function that raises TimeoutError 2 times, then succeeds
  2. Apply `@retry_on_connection_error(max_attempts=3)`
  3. Call function
  4. Verify function called 3 times
- **Expected Result**: Function retried on TimeoutError
- **Coverage**: `retry_on_connection_error` decorator

### 3. RetryConfig Tests

#### TC-RETRY-009: RetryConfig - calculate_delay
- **Purpose**: Verify delay calculation
- **Preconditions**: RetryConfig instance
- **Test Steps**:
  1. Create RetryConfig(delay=1.0, backoff=2.0)
  2. Call calculate_delay(0) - should return 1.0
  3. Call calculate_delay(1) - should return 2.0
  4. Call calculate_delay(2) - should return 4.0
- **Expected Result**: Delays calculated correctly (1.0, 2.0, 4.0)
- **Coverage**: `RetryConfig.calculate_delay` method

#### TC-RETRY-010: RetryConfig - max_delay ограничение
- **Purpose**: Verify max_delay limits delay
- **Preconditions**: RetryConfig with max_delay
- **Test Steps**:
  1. Create RetryConfig(delay=1.0, backoff=2.0, max_delay=5.0)
  2. Call calculate_delay(0) - should return 1.0
  3. Call calculate_delay(2) - should return 4.0
  4. Call calculate_delay(10) - should return 5.0 (capped)
- **Expected Result**: Delay capped at max_delay
- **Coverage**: `RetryConfig.calculate_delay` method - max_delay

#### TC-RETRY-011: RetryConfig - jitter
- **Purpose**: Verify jitter adds randomness
- **Preconditions**: RetryConfig with jitter=True
- **Test Steps**:
  1. Create RetryConfig(delay=1.0, backoff=2.0, jitter=True)
  2. Call calculate_delay(1) multiple times
  3. Verify values differ (within ±10% range)
- **Expected Result**: Delays vary due to jitter
- **Coverage**: `RetryConfig.calculate_delay` method - jitter

#### TC-RETRY-012: RetryConfig - to_dict
- **Purpose**: Verify conversion to dictionary
- **Preconditions**: RetryConfig instance
- **Test Steps**:
  1. Create RetryConfig
  2. Call to_dict()
  3. Verify dictionary contains all config values
- **Expected Result**: Dictionary contains all config values
- **Coverage**: `RetryConfig.to_dict` method

