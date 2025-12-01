# Circuit Breaker Module - Unit Test Cases

## Overview
Tests for `py_web_automation.circuit_breaker` module - circuit breaker pattern implementation.

## Test Categories

### 1. CircuitBreaker Tests

#### TC-CB-001: CircuitBreaker - инициализация
- **Purpose**: Verify CircuitBreaker initialization
- **Preconditions**: Configuration parameters
- **Test Steps**:
  1. Create CircuitBreaker with default config
  2. Verify config and stats initialized
- **Expected Result**: CircuitBreaker initialized correctly
- **Coverage**: `CircuitBreaker.__init__` method

#### TC-CB-002: CircuitBreaker - call успешный
- **Purpose**: Verify successful call through circuit breaker
- **Preconditions**: CircuitBreaker in CLOSED state
- **Test Steps**:
  1. Create CircuitBreaker
  2. Call call() with successful function
  3. Verify function result returned
- **Expected Result**: Function result returned, success recorded
- **Coverage**: `CircuitBreaker.call` method - success

#### TC-CB-003: CircuitBreaker - call открывает circuit при ошибках
- **Purpose**: Verify circuit opens after failure threshold
- **Preconditions**: CircuitBreaker with low failure_threshold
- **Test Steps**:
  1. Create CircuitBreaker(failure_threshold=2)
  2. Call call() with failing function 2 times
  3. Verify circuit state = OPEN
- **Expected Result**: Circuit opens after threshold
- **Coverage**: `CircuitBreaker.call` method - opening circuit

#### TC-CB-004: CircuitBreaker - call блокирует при OPEN
- **Purpose**: Verify call blocked when circuit is OPEN
- **Preconditions**: CircuitBreaker in OPEN state
- **Test Steps**:
  1. Create CircuitBreaker in OPEN state
  2. Call call() with function
  3. Verify ConnectionError raised
- **Expected Result**: ConnectionError raised
- **Coverage**: `CircuitBreaker.call` method - open circuit

#### TC-CB-005: CircuitBreaker - переход в HALF_OPEN
- **Purpose**: Verify transition to HALF_OPEN after timeout
- **Preconditions**: CircuitBreaker in OPEN state
- **Test Steps**:
  1. Create CircuitBreaker in OPEN state
  2. Wait for timeout
  3. Call call() with function
  4. Verify state = HALF_OPEN
- **Expected Result**: State transitions to HALF_OPEN
- **Coverage**: `CircuitBreaker.call` method - half-open transition

#### TC-CB-006: CircuitBreaker - закрытие из HALF_OPEN
- **Purpose**: Verify circuit closes from HALF_OPEN after successes
- **Preconditions**: CircuitBreaker in HALF_OPEN state
- **Test Steps**:
  1. Create CircuitBreaker in HALF_OPEN state
  2. Call call() with successful function success_threshold times
  3. Verify state = CLOSED
- **Expected Result**: Circuit closes after success threshold
- **Coverage**: `CircuitBreaker._record_success` method

#### TC-CB-007: CircuitBreaker - возврат в OPEN из HALF_OPEN
- **Purpose**: Verify circuit reopens on failure in HALF_OPEN
- **Preconditions**: CircuitBreaker in HALF_OPEN state
- **Test Steps**:
  1. Create CircuitBreaker in HALF_OPEN state
  2. Call call() with failing function
  3. Verify state = OPEN
- **Expected Result**: Circuit reopens on failure
- **Coverage**: `CircuitBreaker._record_failure` method

#### TC-CB-008: CircuitBreaker - reset
- **Purpose**: Verify manual reset
- **Preconditions**: CircuitBreaker in OPEN state
- **Test Steps**:
  1. Create CircuitBreaker in OPEN state
  2. Call reset()
  3. Verify state = CLOSED, stats reset
- **Expected Result**: Circuit reset to CLOSED
- **Coverage**: `CircuitBreaker.reset` method

#### TC-CB-009: CircuitBreaker - get_state и get_stats
- **Purpose**: Verify state and stats retrieval
- **Preconditions**: CircuitBreaker with some history
- **Test Steps**:
  1. Create CircuitBreaker
  2. Record some successes/failures
  3. Call get_state() and get_stats()
  4. Verify correct values returned
- **Expected Result**: State and stats returned correctly
- **Coverage**: `CircuitBreaker.get_state` and `get_stats` methods

### 2. CircuitBreakerConfig Tests

#### TC-CB-010: CircuitBreakerConfig - инициализация
- **Purpose**: Verify CircuitBreakerConfig initialization
- **Preconditions**: Config parameters
- **Test Steps**:
  1. Create CircuitBreakerConfig
  2. Verify all fields set correctly
- **Expected Result**: Config initialized correctly
- **Coverage**: `CircuitBreakerConfig.__init__` method

### 3. CircuitBreakerStats Tests

#### TC-CB-011: CircuitBreakerStats - инициализация
- **Purpose**: Verify CircuitBreakerStats initialization
- **Preconditions**: Stats creation
- **Test Steps**:
  1. Create CircuitBreakerStats
  2. Verify default values
- **Expected Result**: Stats initialized with defaults
- **Coverage**: `CircuitBreakerStats.__init__` method

