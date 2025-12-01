# Unit Test Cases: Validators

## Overview

Test cases for response validation utilities using msgspec.

## Test Cases

### TC-UNIT-VAL-001: validate_response with msgspec Struct

**Description**: Test validation of dict data against msgspec Struct schema.

**Preconditions**:
- msgspec library is installed
- Valid msgspec Struct class defined

**Test Steps**:
1. Define a msgspec Struct class (e.g., UserResponse with id, name, email)
2. Create valid data dictionary matching the schema
3. Call `validate_response(data, UserResponse)`
4. Verify returned object is instance of UserResponse
5. Verify all fields are correctly populated

**Expected Result**:
- Function returns UserResponse instance
- All fields match input data
- No exceptions raised

**Test Data**:
```python
class UserResponse(msgspec.Struct):
    id: int
    name: str
    email: str

data = {"id": 1, "name": "John", "email": "john@example.com"}
```

---

### TC-UNIT-VAL-002: validate_response with invalid data

**Description**: Test validation failure with invalid data structure.

**Preconditions**:
- msgspec library is installed
- Valid msgspec Struct class defined

**Test Steps**:
1. Define a msgspec Struct class
2. Create invalid data (missing required fields or wrong types)
3. Call `validate_response(data, UserResponse)`
4. Verify FrameworkValidationError is raised
5. Verify error message contains validation details

**Expected Result**:
- FrameworkValidationError is raised
- Error message describes validation failure
- Error details are included

**Test Data**:
```python
data = {"id": "invalid", "name": "John"}  # Missing email, wrong type for id
```

---

### TC-UNIT-VAL-003: validate_response with dict schema

**Description**: Test validation with dict type annotation.

**Preconditions**:
- None

**Test Steps**:
1. Create valid dictionary data
2. Call `validate_response(data, dict)` or `validate_response(data, Dict[str, Any])`
3. Verify same dictionary is returned
4. Test with non-dict data (e.g., list)
5. Verify FrameworkValidationError is raised for non-dict

**Expected Result**:
- Valid dict returns same dict
- Non-dict raises FrameworkValidationError

**Test Data**:
```python
data = {"key": "value"}
invalid_data = ["list", "not", "dict"]
```

---

### TC-UNIT-VAL-004: validate_response with list schema

**Description**: Test validation with list type annotation.

**Preconditions**:
- None

**Test Steps**:
1. Create valid list data
2. Call `validate_response(data, list)` or `validate_response(data, List[Any])`
3. Verify same list is returned
4. Test with non-list data (e.g., dict)
5. Verify FrameworkValidationError is raised for non-list

**Expected Result**:
- Valid list returns same list
- Non-list raises FrameworkValidationError

**Test Data**:
```python
data = [1, 2, 3]
invalid_data = {"not": "list"}
```

---

### TC-UNIT-VAL-005: validate_json_response with string

**Description**: Test validation of JSON string against schema.

**Preconditions**:
- msgspec library is installed
- Valid msgspec Struct class defined

**Test Steps**:
1. Define a msgspec Struct class
2. Create valid JSON string
3. Call `validate_json_response(json_str, UserResponse)`
4. Verify returned object is instance of UserResponse
5. Verify all fields are correctly populated

**Expected Result**:
- Function returns UserResponse instance
- All fields match JSON data
- No exceptions raised

**Test Data**:
```python
json_str = '{"id": 1, "name": "John", "email": "john@example.com"}'
```

---

### TC-UNIT-VAL-006: validate_json_response with bytes

**Description**: Test validation of JSON bytes against schema.

**Preconditions**:
- msgspec library is installed
- Valid msgspec Struct class defined

**Test Steps**:
1. Define a msgspec Struct class
2. Create valid JSON bytes
3. Call `validate_json_response(json_bytes, UserResponse)`
4. Verify returned object is instance of UserResponse
5. Verify all fields are correctly populated

**Expected Result**:
- Function returns UserResponse instance
- All fields match JSON data
- No exceptions raised

**Test Data**:
```python
json_bytes = b'{"id": 1, "name": "John", "email": "john@example.com"}'
```

---

### TC-UNIT-VAL-007: validate_json_response with invalid JSON

**Description**: Test validation failure with invalid JSON string.

**Preconditions**:
- None

**Test Steps**:
1. Create invalid JSON string (malformed)
2. Call `validate_json_response(invalid_json, UserResponse)`
3. Verify FrameworkValidationError is raised
4. Verify error message indicates JSON parsing failure

**Expected Result**:
- FrameworkValidationError is raised
- Error message mentions JSON parsing failure

**Test Data**:
```python
invalid_json = '{"id": 1, "name": "John"'  # Missing closing brace
```

---

### TC-UNIT-VAL-008: validate_api_result with valid response

**Description**: Test validation of ApiResult body against schema.

**Preconditions**:
- msgspec library is installed
- Valid msgspec Struct class defined
- ApiResult instance with valid JSON body

**Test Steps**:
1. Define a msgspec Struct class
2. Create ApiResult with valid JSON body
3. Call `validate_api_result(result, UserResponse)`
4. Verify returned object is instance of UserResponse
5. Verify all fields are correctly populated

**Expected Result**:
- Function returns UserResponse instance
- All fields match response data
- No exceptions raised

**Test Data**:
```python
result = ApiResult(
    endpoint="/users/1",
    method="GET",
    status_code=200,
    response_time=0.1,
    success=True,
    redirect=False,
    client_error=False,
    server_error=False,
    informational=False,
    body=b'{"id": 1, "name": "John", "email": "john@example.com"}'
)
```

---

### TC-UNIT-VAL-009: validate_api_result with invalid ApiResult type

**Description**: Test validation failure when non-ApiResult is passed.

**Preconditions**:
- None

**Test Steps**:
1. Create non-ApiResult object (e.g., dict)
2. Call `validate_api_result(invalid_result, UserResponse)`
3. Verify FrameworkValidationError is raised
4. Verify error message indicates wrong type

**Expected Result**:
- FrameworkValidationError is raised
- Error message mentions expected ApiResult type

**Test Data**:
```python
invalid_result = {"not": "ApiResult"}
```

---

### TC-UNIT-VAL-010: validate_api_result with non-JSON body

**Description**: Test validation failure when ApiResult body is not JSON.

**Preconditions**:
- ApiResult instance with non-JSON body

**Test Steps**:
1. Create ApiResult with non-JSON body (e.g., plain text)
2. Call `validate_api_result(result, UserResponse)`
3. Verify FrameworkValidationError is raised
4. Verify error message indicates JSON parsing failure

**Expected Result**:
- FrameworkValidationError is raised
- Error message mentions JSON parsing failure

**Test Data**:
```python
result = ApiResult(
    endpoint="/users/1",
    method="GET",
    status_code=200,
    response_time=0.1,
    success=True,
    redirect=False,
    client_error=False,
    server_error=False,
    informational=False,
    body=b"Plain text response"
)
```

---

### TC-UNIT-VAL-011: create_schema_from_dict with basic fields

**Description**: Test dynamic schema creation from dictionary.

**Preconditions**:
- msgspec library is installed

**Test Steps**:
1. Define field dictionary with types
2. Call `create_schema_from_dict("User", fields)`
3. Verify returned class is msgspec Struct
4. Create instance of returned class
5. Verify instance has correct fields

**Expected Result**:
- Function returns msgspec Struct class
- Class can be instantiated with correct fields
- Fields have correct types

**Test Data**:
```python
fields = {"id": int, "name": str, "email": str}
```

---

### TC-UNIT-VAL-012: create_schema_from_dict with optional fields

**Description**: Test dynamic schema creation with optional fields.

**Preconditions**:
- msgspec library is installed

**Test Steps**:
1. Define field dictionary with optional fields (tuple format)
2. Call `create_schema_from_dict("User", fields)`
3. Verify returned class is msgspec Struct
4. Create instance without optional fields
5. Verify default values are used

**Expected Result**:
- Function returns msgspec Struct class
- Optional fields use default values
- Instance can be created without optional fields

**Test Data**:
```python
fields = {
    "id": int,
    "name": str,
    "age": (int, 0),  # Optional with default
    "email": (str, ""),  # Optional with default
}
```

---

### TC-UNIT-VAL-013: create_schema_from_dict with frozen struct

**Description**: Test dynamic schema creation with frozen struct.

**Preconditions**:
- msgspec library is installed

**Test Steps**:
1. Define field dictionary
2. Call `create_schema_from_dict("User", fields, frozen=True)`
3. Verify returned class is frozen
4. Create instance
5. Attempt to modify field
6. Verify AttributeError is raised

**Expected Result**:
- Function returns frozen msgspec Struct class
- Attempting to modify fields raises AttributeError

**Test Data**:
```python
fields = {"id": int, "name": str}
```

---

### TC-UNIT-VAL-014: create_schema_from_dict with mutable struct

**Description**: Test dynamic schema creation with mutable struct.

**Preconditions**:
- msgspec library is installed

**Test Steps**:
1. Define field dictionary
2. Call `create_schema_from_dict("User", fields, frozen=False)`
3. Verify returned class is not frozen
4. Create instance
5. Modify field
6. Verify modification succeeds

**Expected Result**:
- Function returns mutable msgspec Struct class
- Fields can be modified after creation

**Test Data**:
```python
fields = {"id": int, "name": str}
```

---

### TC-UNIT-VAL-015: validate_response with nested structures

**Description**: Test validation of nested data structures.

**Preconditions**:
- msgspec library is installed
- Nested msgspec Struct classes defined

**Test Steps**:
1. Define nested Struct classes (e.g., Address within User)
2. Create data with nested structure
3. Call `validate_response(data, UserResponse)`
4. Verify nested objects are correctly validated
5. Verify nested fields are accessible

**Expected Result**:
- Function returns UserResponse instance
- Nested Address object is correctly validated
- Nested fields are accessible

**Test Data**:
```python
class Address(msgspec.Struct):
    street: str
    city: str
    zip_code: str

class UserResponse(msgspec.Struct):
    id: int
    name: str
    address: Address

data = {
    "id": 1,
    "name": "John",
    "address": {"street": "123 Main St", "city": "NYC", "zip_code": "10001"}
}
```

---

### TC-VAL-DICT-001: validate_response with dict schema and non-dict data

**Description**: Test validation failure when dict schema is used with non-dict data.

**Preconditions**:
- None

**Test Steps**:
1. Create non-dict data (e.g., list, string, int)
2. Call `validate_response(data, dict)` or `validate_response(data, Dict[str, Any])`
3. Verify FrameworkValidationError is raised
4. Verify error message indicates expected dict type

**Expected Result**:
- FrameworkValidationError is raised
- Error message: "Expected dict, got {type}"

**Test Data**:
```python
invalid_data = ["list", "not", "dict"]
invalid_data2 = "string"
invalid_data3 = 123
```

---

### TC-VAL-LIST-001: validate_response with list schema and non-list data

**Description**: Test validation failure when list schema is used with non-list data.

**Preconditions**:
- None

**Test Steps**:
1. Create non-list data (e.g., dict, string, int)
2. Call `validate_response(data, list)` or `validate_response(data, List[Any])`
3. Verify FrameworkValidationError is raised
4. Verify error message indicates expected list type

**Expected Result**:
- FrameworkValidationError is raised
- Error message: "Expected list, got {type}"

**Test Data**:
```python
invalid_data = {"not": "list"}
invalid_data2 = "string"
invalid_data3 = 123
```

---

### TC-VAL-ERROR-001: validate_response with msgspec.ValidationError without errors() method

**Description**: Test error handling when msgspec.ValidationError doesn't have errors() method.

**Preconditions**:
- msgspec library is installed
- Mock msgspec.ValidationError without errors() method

**Test Steps**:
1. Create mock ValidationError without errors() method
2. Call `validate_response(invalid_data, UserResponse)`
3. Verify FrameworkValidationError is raised
4. Verify error message uses str(e) fallback

**Expected Result**:
- FrameworkValidationError is raised
- Error message uses str(e) when errors() is not available

**Test Data**:
```python
# Mock ValidationError without errors() method
```

---

### TC-VAL-ERROR-002: validate_response with msgspec.ValidationError with non-iterable errors()

**Description**: Test error handling when msgspec.ValidationError.errors() returns non-iterable.

**Preconditions**:
- msgspec library is installed
- Mock msgspec.ValidationError with errors() returning non-iterable

**Test Steps**:
1. Create mock ValidationError with errors() returning non-iterable (e.g., None, int)
2. Call `validate_response(invalid_data, UserResponse)`
3. Verify FrameworkValidationError is raised
4. Verify TypeError is caught and str(e) is used

**Expected Result**:
- FrameworkValidationError is raised
- TypeError from errors() is caught
- Error message uses str(e) fallback

**Test Data**:
```python
# Mock ValidationError with errors() returning None or int
```

---

### TC-VAL-ERROR-003: validate_response with msgspec.ValidationError with AttributeError on errors()

**Description**: Test error handling when AttributeError occurs while accessing errors().

**Preconditions**:
- msgspec library is installed
- Mock msgspec.ValidationError that raises AttributeError on errors() access

**Test Steps**:
1. Create mock ValidationError that raises AttributeError when errors() is accessed
2. Call `validate_response(invalid_data, UserResponse)`
3. Verify FrameworkValidationError is raised
4. Verify AttributeError is caught and str(e) is used

**Expected Result**:
- FrameworkValidationError is raised
- AttributeError is caught
- Error message uses str(e) fallback

**Test Data**:
```python
# Mock ValidationError that raises AttributeError on errors() access
```

