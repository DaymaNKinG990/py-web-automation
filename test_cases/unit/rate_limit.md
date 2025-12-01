# Rate Limit Module - Unit Test Cases

## Overview
Tests for `py_web_automation.rate_limit` module - rate limiting with sliding window algorithm.

## Test Categories

### 1. RateLimiter Tests

#### TC-RL-001: RateLimiter - acquire успешно
- **Purpose**: Verify successful permission acquisition
- **Preconditions**: RateLimiter with available slots
- **Test Steps**:
  1. Create RateLimiter(max_requests=10, window=60)
  2. Call acquire() 5 times
  3. Verify all calls succeed (no blocking)
- **Expected Result**: All acquire() calls succeed
- **Coverage**: `RateLimiter.acquire` method - success path

#### TC-RL-002: RateLimiter - acquire блокирует при превышении лимита
- **Purpose**: Verify acquire blocks when limit exceeded
- **Preconditions**: RateLimiter with max_requests=2
- **Test Steps**:
  1. Create RateLimiter(max_requests=2, window=60)
  2. Call acquire() 2 times (succeeds)
  3. Call acquire() 3rd time
  4. Verify 3rd call blocks until window expires
- **Expected Result**: 3rd call blocks, then succeeds after wait
- **Coverage**: `RateLimiter.acquire` method - blocking

#### TC-RL-003: RateLimiter - try_acquire успешно
- **Purpose**: Verify try_acquire returns True when available
- **Preconditions**: RateLimiter with available slots
- **Test Steps**:
  1. Create RateLimiter(max_requests=10, window=60)
  2. Call try_acquire()
  3. Verify True returned
- **Expected Result**: True returned
- **Coverage**: `RateLimiter.try_acquire` method - success

#### TC-RL-004: RateLimiter - try_acquire при превышении лимита
- **Purpose**: Verify try_acquire returns False when limit exceeded
- **Preconditions**: RateLimiter with max_requests=1
- **Test Steps**:
  1. Create RateLimiter(max_requests=1, window=60)
  2. Call try_acquire() (succeeds)
  3. Call try_acquire() again
  4. Verify False returned
- **Expected Result**: False returned
- **Coverage**: `RateLimiter.try_acquire` method - limit exceeded

#### TC-RL-005: RateLimiter - sliding window
- **Purpose**: Verify old requests removed from window
- **Preconditions**: RateLimiter with short window
- **Test Steps**:
  1. Create RateLimiter(max_requests=2, window=1)
  2. Call acquire() 2 times
  3. Wait 2 seconds (window expires)
  4. Call acquire() again
  5. Verify 3rd call succeeds (old requests removed)
- **Expected Result**: 3rd call succeeds (sliding window works)
- **Coverage**: `RateLimiter.acquire` method - sliding window

#### TC-RL-006: RateLimiter - get_remaining
- **Purpose**: Verify remaining requests calculation
- **Preconditions**: RateLimiter with some requests
- **Test Steps**:
  1. Create RateLimiter(max_requests=10, window=60)
  2. Call acquire() 3 times
  3. Call get_remaining()
  4. Verify 7 returned
- **Expected Result**: 7 returned
- **Coverage**: `RateLimiter.get_remaining` method

#### TC-RL-007: RateLimiter - get_wait_time
- **Purpose**: Verify wait time calculation
- **Preconditions**: RateLimiter at limit
- **Test Steps**:
  1. Create RateLimiter(max_requests=1, window=60)
  2. Call acquire()
  3. Call get_wait_time()
  4. Verify wait_time > 0
- **Expected Result**: Wait time > 0
- **Coverage**: `RateLimiter.get_wait_time` method

#### TC-RL-008: RateLimiter - get_wait_time когда доступно
- **Purpose**: Verify wait_time = 0 when available
- **Preconditions**: RateLimiter with available slots
- **Test Steps**:
  1. Create RateLimiter(max_requests=10, window=60)
  2. Call get_wait_time()
  3. Verify 0.0 returned
- **Expected Result**: 0.0 returned
- **Coverage**: `RateLimiter.get_wait_time` method - available

#### TC-RL-009: RateLimiter - reset
- **Purpose**: Verify rate limiter reset
- **Preconditions**: RateLimiter with requests
- **Test Steps**:
  1. Create RateLimiter
  2. Call acquire() several times
  3. Call reset()
  4. Verify get_remaining() = max_requests
- **Expected Result**: Limiter reset, all slots available
- **Coverage**: `RateLimiter.reset` method

#### TC-RL-010: RateLimiter - burst support
- **Purpose**: Verify burst allows extra requests
- **Preconditions**: RateLimiter with burst
- **Test Steps**:
  1. Create RateLimiter(max_requests=10, window=60, burst=5)
  2. Call acquire() 15 times quickly
  3. Verify first 15 succeed (10 + 5 burst)
  4. Verify 16th blocks
- **Expected Result**: Burst allows extra requests
- **Coverage**: `RateLimiter.acquire` method - burst handling

### 2. RateLimitConfig Tests

#### TC-RL-011: RateLimitConfig - инициализация
- **Purpose**: Verify RateLimitConfig initialization
- **Preconditions**: Config parameters
- **Test Steps**:
  1. Create RateLimitConfig(max_requests=100, window=60, burst=10)
  2. Verify all fields set correctly
- **Expected Result**: Config initialized correctly
- **Coverage**: `RateLimitConfig.__init__` method

#### TC-RL-012: RateLimitConfig - default burst
- **Purpose**: Verify default burst calculation
- **Preconditions**: RateLimitConfig without burst
- **Test Steps**:
  1. Create RateLimitConfig(max_requests=100, window=60)
  2. Verify burst = 10 (10% of max_requests)
- **Expected Result**: Burst = 10
- **Coverage**: `RateLimitConfig` default burst

