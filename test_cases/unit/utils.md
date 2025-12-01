# Utility Functions - Unit Test Cases

## Overview
Tests for utility functions in `py_web_automation.utils`:
- `parse_json()` - Parse JSON from response body
- `validate_response_structure()` - Validate response structure
- `extract_pagination_info()` - Extract pagination information
- `get_error_detail()` - Extract error detail from response

## parse_json() Test Cases

### 1. Parameterized Tests (TC-UTILS-001 to TC-UTILS-004)

**Примечание**: Тесты TC-UTILS-001, TC-UTILS-002, TC-UTILS-003, TC-UTILS-004 объединены в один параметризованный тест `test_parse_json()` для улучшения поддерживаемости и читаемости кода.

#### TC-UTILS-001: Parse valid JSON
- **Purpose**: Verify parse_json() parses valid JSON correctly
- **Preconditions**: Valid JSON bytes
- **Test Steps**:
  1. Call parse_json() with valid JSON bytes: b'{"key": "value", "number": 123}'
  2. Verify returned dict matches JSON content
- **Expected Result**: Returns parsed dictionary with correct values
- **Coverage**: `parse_json()` basic functionality
- **Implementation**: Параметризованный тест `test_parse_json()` с параметром `input_data={"key": "value", "number": 123}`

#### TC-UTILS-002: Parse invalid JSON returns empty dict
- **Purpose**: Verify parse_json() returns empty dict for invalid JSON
- **Preconditions**: Invalid JSON bytes
- **Test Steps**:
  1. Call parse_json() with invalid JSON bytes: b"not valid json"
  2. Verify returned dict is empty: {}
- **Expected Result**: Returns empty dictionary
- **Coverage**: `parse_json()` error handling
- **Implementation**: Параметризованный тест `test_parse_json()` с параметром `input_data=b"not valid json"`

#### TC-UTILS-003: Parse empty body returns empty dict
- **Purpose**: Verify parse_json() handles empty body
- **Preconditions**: Empty bytes
- **Test Steps**:
  1. Call parse_json() with empty bytes: b""
  2. Verify returned dict is empty: {}
- **Expected Result**: Returns empty dictionary
- **Coverage**: `parse_json()` empty input handling
- **Implementation**: Параметризованный тест `test_parse_json()` с параметром `input_data=b""`

#### TC-UTILS-004: Parse JSON with unicode characters
- **Purpose**: Verify parse_json() handles unicode characters
- **Preconditions**: JSON with unicode characters
- **Test Steps**:
  1. Call parse_json() with JSON containing unicode: b'{"message": "Привет", "emoji": "🎉"}'
  2. Verify returned dict contains unicode values correctly
- **Expected Result**: Unicode characters parsed correctly
- **Coverage**: `parse_json()` unicode handling
- **Implementation**: Параметризованный тест `test_parse_json()` с параметром `input_data={"message": "Привет", "emoji": "🎉"}`

## validate_response_structure() Test Cases

### 1. Basic Functionality Tests

#### TC-UTILS-005: Validate structure with all fields present
- **Purpose**: Verify validate_response_structure() returns True when all fields present
- **Preconditions**: Data dict with all expected fields
- **Test Steps**:
  1. Call validate_response_structure({"name": "test", "id": 123, "status": "active"}, ["name", "id", "status"])
  2. Verify returns True
- **Expected Result**: Returns True
- **Coverage**: `validate_response_structure()` success case

#### TC-UTILS-006: Validate structure with missing fields
- **Purpose**: Verify validate_response_structure() returns False when fields missing
- **Preconditions**: Data dict missing some expected fields
- **Test Steps**:
  1. Call validate_response_structure({"name": "test", "id": 123}, ["name", "id", "status", "email"])
  2. Verify returns False
- **Expected Result**: Returns False
- **Coverage**: `validate_response_structure()` failure case

#### TC-UTILS-007: Validate structure with empty expected fields
- **Purpose**: Verify validate_response_structure() returns True for empty expected fields
- **Preconditions**: Empty expected_fields list
- **Test Steps**:
  1. Call validate_response_structure({"name": "test"}, [])
  2. Verify returns True
- **Expected Result**: Returns True (all zero fields are present)
- **Coverage**: `validate_response_structure()` edge case

## extract_pagination_info() Test Cases

### 1. Basic Functionality Tests

#### TC-UTILS-008: Extract complete pagination info
- **Purpose**: Verify extract_pagination_info() extracts all pagination fields
- **Preconditions**: Data dict with complete pagination info
- **Test Steps**:
  1. Call extract_pagination_info({"count": 100, "next": "http://api.example.com/items/?page=2", "previous": None, "results": [{"id": 1}, {"id": 2}]})
  2. Verify returned dict contains count, next, previous, results
- **Expected Result**: Returns dict with all pagination fields
- **Coverage**: `extract_pagination_info()` complete data

#### TC-UTILS-009: Extract partial pagination info
- **Purpose**: Verify extract_pagination_info() handles partial pagination data
- **Preconditions**: Data dict with only count field
- **Test Steps**:
  1. Call extract_pagination_info({"count": 50})
  2. Verify returned dict has count=50, next=None, previous=None, results=[]
- **Expected Result**: Returns dict with available fields, None/[] for missing
- **Coverage**: `extract_pagination_info()` partial data

#### TC-UTILS-010: Extract pagination info from empty data
- **Purpose**: Verify extract_pagination_info() handles empty data dict
- **Preconditions**: Empty data dict
- **Test Steps**:
  1. Call extract_pagination_info({})
  2. Verify returned dict has all fields as None or []
- **Expected Result**: Returns dict with count=None, next=None, previous=None, results=[]
- **Coverage**: `extract_pagination_info()` empty input

## get_error_detail() Test Cases

### 1. Basic Functionality Tests

#### TC-UTILS-011: Extract error detail from 'detail' field
- **Purpose**: Verify get_error_detail() extracts 'detail' field
- **Preconditions**: Data dict with 'detail' field
- **Test Steps**:
  1. Call get_error_detail({"detail": "Error message"})
  2. Verify returns "Error message"
- **Expected Result**: Returns value from 'detail' field
- **Coverage**: `get_error_detail()` detail field

#### TC-UTILS-012: Extract error detail from 'error' field
- **Purpose**: Verify get_error_detail() extracts 'error' field when 'detail' missing
- **Preconditions**: Data dict with 'error' field but no 'detail'
- **Test Steps**:
  1. Call get_error_detail({"error": "Error message"})
  2. Verify returns "Error message"
- **Expected Result**: Returns value from 'error' field
- **Coverage**: `get_error_detail()` error field fallback

#### TC-UTILS-013: Extract error detail fallback to string representation
- **Purpose**: Verify get_error_detail() falls back to string representation
- **Preconditions**: Data dict without 'detail' or 'error' fields
- **Test Steps**:
  1. Call get_error_detail({"message": "Some message"})
  2. Verify returns string representation of dict
- **Expected Result**: Returns string representation of data
- **Coverage**: `get_error_detail()` fallback behavior


