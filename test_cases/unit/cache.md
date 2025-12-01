# Cache Module - Unit Test Cases

## Overview
Tests for `py_web_automation.cache` module - response caching system with TTL support.

## Test Categories

### 1. ResponseCache Tests

#### TC-CACHE-001: ResponseCache - get cache hit
- **Purpose**: Verify getting cached value
- **Preconditions**: ResponseCache with cached value
- **Test Steps**:
  1. Create ResponseCache
  2. Save value through set() with method, url
  3. Get value through get() with same method, url
  4. Verify value matches
- **Expected Result**: Cached value returned
- **Coverage**: `ResponseCache.get` method - cache hit

#### TC-CACHE-002: ResponseCache - get cache miss
- **Purpose**: Verify None returned when not in cache
- **Preconditions**: Empty ResponseCache
- **Test Steps**:
  1. Create ResponseCache
  2. Get value through get() for non-existent key
  3. Verify None returned
- **Expected Result**: None returned
- **Coverage**: `ResponseCache.get` method - cache miss

#### TC-CACHE-003: ResponseCache - expired entry
- **Purpose**: Verify expired entries not returned
- **Preconditions**: ResponseCache with expired entry
- **Test Steps**:
  1. Create ResponseCache
  2. Save value with ttl=1 second
  3. Wait 2 seconds
  4. Get value through get()
  5. Verify None returned and entry removed
- **Expected Result**: None returned, expired entry removed
- **Coverage**: `ResponseCache.get` method - expired entry handling

#### TC-CACHE-004: ResponseCache - max_size ограничение
- **Purpose**: Verify max_size limits cache size
- **Preconditions**: ResponseCache with max_size=2
- **Test Steps**:
  1. Create ResponseCache(max_size=2)
  2. Save 3 values
  3. Verify cache size = 2
  4. Verify oldest value removed (FIFO)
- **Expected Result**: Cache size limited, oldest entry removed
- **Coverage**: `ResponseCache.set` method - max_size handling

#### TC-CACHE-005: ResponseCache - _make_key одинаковые параметры
- **Purpose**: Verify same parameters create same key
- **Preconditions**: ResponseCache instance
- **Test Steps**:
  1. Create ResponseCache
  2. Create key for (GET, "/test", None, None, None)
  3. Create key for (GET, "/test", None, None, None) again
  4. Verify keys match
- **Expected Result**: Keys are identical
- **Coverage**: `ResponseCache._make_key` method - key consistency

#### TC-CACHE-006: ResponseCache - _make_key разные параметры
- **Purpose**: Verify different parameters create different keys
- **Preconditions**: ResponseCache instance
- **Test Steps**:
  1. Create ResponseCache
  2. Create key for (GET, "/test1")
  3. Create key for (GET, "/test2")
  4. Verify keys differ
- **Expected Result**: Keys are different
- **Coverage**: `ResponseCache._make_key` method - key uniqueness

#### TC-CACHE-007: ResponseCache - _make_key нормализация headers
- **Purpose**: Verify sensitive headers excluded from key
- **Preconditions**: ResponseCache instance
- **Test Steps**:
  1. Create ResponseCache
  2. Create key with Authorization header
  3. Create key without Authorization header
  4. Verify keys match (Authorization excluded)
- **Expected Result**: Keys match (sensitive headers excluded)
- **Coverage**: `ResponseCache._make_key` method - header normalization

#### TC-CACHE-008: ResponseCache - _make_key с params
- **Purpose**: Verify params included in key
- **Preconditions**: ResponseCache instance
- **Test Steps**:
  1. Create ResponseCache
  2. Create key with params={"page": 1}
  3. Create key with params={"page": 2}
  4. Verify keys differ
- **Expected Result**: Keys differ (params included)
- **Coverage**: `ResponseCache._make_key` method - params handling

#### TC-CACHE-009: ResponseCache - invalidate
- **Purpose**: Verify cache invalidation
- **Preconditions**: ResponseCache with entries
- **Test Steps**:
  1. Create ResponseCache
  2. Save several values
  3. Call invalidate()
  4. Verify cache is empty
- **Expected Result**: Cache cleared
- **Coverage**: `ResponseCache.invalidate` method

#### TC-CACHE-010: ResponseCache - cleanup_expired
- **Purpose**: Verify expired entries cleanup
- **Preconditions**: ResponseCache with expired entries
- **Test Steps**:
  1. Create ResponseCache
  2. Save value with ttl=1
  3. Wait 2 seconds
  4. Call cleanup_expired()
  5. Verify expired entry removed, count returned
- **Expected Result**: Expired entry removed, count > 0
- **Coverage**: `ResponseCache.cleanup_expired` method

#### TC-CACHE-011: ResponseCache - size
- **Purpose**: Verify cache size calculation
- **Preconditions**: ResponseCache with entries
- **Test Steps**:
  1. Create ResponseCache
  2. Save 3 values
  3. Call size()
  4. Verify size = 3
- **Expected Result**: Size = 3
- **Coverage**: `ResponseCache.size` method

#### TC-CACHE-012: ResponseCache - clear
- **Purpose**: Verify cache clearing
- **Preconditions**: ResponseCache with entries
- **Test Steps**:
  1. Create ResponseCache
  2. Save several values
  3. Call clear()
  4. Verify cache is empty
- **Expected Result**: Cache cleared
- **Coverage**: `ResponseCache.clear` method

### 2. CacheEntry Tests

#### TC-CACHE-013: CacheEntry - is_expired False
- **Purpose**: Verify is_expired returns False for valid entry
- **Preconditions**: CacheEntry with ttl=300
- **Test Steps**:
  1. Create CacheEntry with ttl=300
  2. Call is_expired() immediately
  3. Verify False returned
- **Expected Result**: False returned
- **Coverage**: `CacheEntry.is_expired` method - valid entry

#### TC-CACHE-014: CacheEntry - is_expired True
- **Purpose**: Verify is_expired returns True for expired entry
- **Preconditions**: CacheEntry with ttl=1
- **Test Steps**:
  1. Create CacheEntry with ttl=1
  2. Wait 2 seconds
  3. Call is_expired()
  4. Verify True returned
- **Expected Result**: True returned
- **Coverage**: `CacheEntry.is_expired` method - expired entry

#### TC-CACHE-015: CacheEntry - timestamp
- **Purpose**: Verify timestamp set on creation
- **Preconditions**: CacheEntry creation
- **Test Steps**:
  1. Record current time
  2. Create CacheEntry
  3. Verify timestamp is recent (within 1 second)
- **Expected Result**: Timestamp set correctly
- **Coverage**: `CacheEntry` timestamp field

