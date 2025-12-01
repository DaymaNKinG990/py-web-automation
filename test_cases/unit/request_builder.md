# Unit Test Cases: Request Builder

## Overview

Test cases for RequestBuilder class implementing Builder pattern for HTTP requests.

## Test Cases

### TC-UNIT-RB-001: RequestBuilder initialization

**Description**: Test RequestBuilder initialization with ApiClient.

**Preconditions**:
- ApiClient instance available
- Config instance available

**Test Steps**:
1. Create ApiClient instance
2. Create RequestBuilder with ApiClient
3. Verify builder is initialized with default values
4. Verify _method is "GET"
5. Verify _endpoint is empty string
6. Verify _params, _headers, _data are empty/None

**Expected Result**:
- RequestBuilder is created successfully
- All default values are set correctly
- No exceptions raised

**Test Data**:
```python
config = Config(timeout=30)
api = ApiClient("https://api.example.com", config)
builder = RequestBuilder(api)
```

---

### TC-UNIT-RB-002: RequestBuilder initialization with invalid client

**Description**: Test RequestBuilder initialization fails with non-ApiClient.

**Preconditions**:
- None

**Test Steps**:
1. Create non-ApiClient object (e.g., dict, string)
2. Attempt to create RequestBuilder with invalid client
3. Verify TypeError is raised
4. Verify error message indicates expected ApiClient type

**Expected Result**:
- TypeError is raised
- Error message mentions ApiClient

**Test Data**:
```python
invalid_client = "not an ApiClient"
```

---

### TC-UNIT-RB-003: RequestBuilder GET method

**Description**: Test setting GET method and endpoint.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.get("/users")`
2. Verify method returns self (for chaining)
3. Verify _method is set to "GET"
4. Verify _endpoint is set to "/users"

**Expected Result**:
- Method returns RequestBuilder instance
- _method is "GET"
- _endpoint is "/users"

**Test Data**:
```python
builder.get("/users")
```

---

### TC-UNIT-RB-004: RequestBuilder POST method

**Description**: Test setting POST method and endpoint.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.post("/users")`
2. Verify method returns self
3. Verify _method is set to "POST"
4. Verify _endpoint is set to "/users"
5. Verify _json_body is True

**Expected Result**:
- Method returns RequestBuilder instance
- _method is "POST"
- _endpoint is "/users"
- _json_body is True

**Test Data**:
```python
builder.post("/users")
```

---

### TC-UNIT-RB-005: RequestBuilder PUT method

**Description**: Test setting PUT method and endpoint.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.put("/users/1")`
2. Verify method returns self
3. Verify _method is set to "PUT"
4. Verify _endpoint is set to "/users/1"
5. Verify _json_body is True

**Expected Result**:
- Method returns RequestBuilder instance
- _method is "PUT"
- _endpoint is "/users/1"
- _json_body is True

**Test Data**:
```python
builder.put("/users/1")
```

---

### TC-UNIT-RB-006: RequestBuilder DELETE method

**Description**: Test setting DELETE method and endpoint.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.delete("/users/1")`
2. Verify method returns self
3. Verify _method is set to "DELETE"
4. Verify _endpoint is set to "/users/1"

**Expected Result**:
- Method returns RequestBuilder instance
- _method is "DELETE"
- _endpoint is "/users/1"

**Test Data**:
```python
builder.delete("/users/1")
```

---

### TC-UNIT-RB-007: RequestBuilder PATCH method

**Description**: Test setting PATCH method and endpoint.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.patch("/users/1")`
2. Verify method returns self
3. Verify _method is set to "PATCH"
4. Verify _endpoint is set to "/users/1"
5. Verify _json_body is True

**Expected Result**:
- Method returns RequestBuilder instance
- _method is "PATCH"
- _endpoint is "/users/1"
- _json_body is True

**Test Data**:
```python
builder.patch("/users/1")
```

---

### TC-UNIT-RB-008: RequestBuilder HEAD method

**Description**: Test setting HEAD method and endpoint.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.head("/users")`
2. Verify method returns self
3. Verify _method is set to "HEAD"
4. Verify _endpoint is set to "/users"

**Expected Result**:
- Method returns RequestBuilder instance
- _method is "HEAD"
- _endpoint is "/users"

**Test Data**:
```python
builder.head("/users")
```

---

### TC-UNIT-RB-009: RequestBuilder OPTIONS method

**Description**: Test setting OPTIONS method and endpoint.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.options("/users")`
2. Verify method returns self
3. Verify _method is set to "OPTIONS"
4. Verify _endpoint is set to "/users"

**Expected Result**:
- Method returns RequestBuilder instance
- _method is "OPTIONS"
- _endpoint is "/users"

**Test Data**:
```python
builder.options("/users")
```

---

### TC-UNIT-RB-010: RequestBuilder params method

**Description**: Test adding query parameters.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.params(page=1, limit=10)`
2. Verify method returns self
3. Verify _params contains page=1 and limit=10
4. Call `builder.params(sort="name")`
5. Verify _params contains all three parameters

**Expected Result**:
- Method returns RequestBuilder instance
- _params dictionary contains all parameters
- Parameters are accumulated (not replaced)

**Test Data**:
```python
builder.params(page=1, limit=10)
builder.params(sort="name")
```

---

### TC-UNIT-RB-011: RequestBuilder param method

**Description**: Test adding single query parameter.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.param("page", 1)`
2. Verify method returns self
3. Verify _params contains page=1
4. Call `builder.param("limit", 10)`
5. Verify _params contains both parameters

**Expected Result**:
- Method returns RequestBuilder instance
- _params dictionary contains all parameters
- Parameters are accumulated

**Test Data**:
```python
builder.param("page", 1)
builder.param("limit", 10)
```

---

### TC-UNIT-RB-012: RequestBuilder body method

**Description**: Test setting request body.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.body({"name": "John", "email": "john@example.com"})`
2. Verify method returns self
3. Verify _data contains the body data
4. Verify _json_body is True

**Expected Result**:
- Method returns RequestBuilder instance
- _data contains body dictionary
- _json_body is True

**Test Data**:
```python
builder.body({"name": "John", "email": "john@example.com"})
```

---

### TC-UNIT-RB-013: RequestBuilder json method

**Description**: Test setting request body using json alias.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.json({"name": "John"})`
2. Verify method returns self
3. Verify _data contains the body data
4. Verify _json_body is True
5. Verify json() is alias for body()

**Expected Result**:
- Method returns RequestBuilder instance
- _data contains body dictionary
- _json_body is True
- json() behaves same as body()

**Test Data**:
```python
builder.json({"name": "John"})
```

---

### TC-UNIT-RB-014: RequestBuilder header method

**Description**: Test adding single header.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.header("X-Custom-Header", "value")`
2. Verify method returns self
3. Verify _headers contains the header
4. Call `builder.header("X-Another-Header", "another")`
5. Verify _headers contains both headers

**Expected Result**:
- Method returns RequestBuilder instance
- _headers dictionary contains all headers
- Headers are accumulated

**Test Data**:
```python
builder.header("X-Custom-Header", "value")
builder.header("X-Another-Header", "another")
```

---

### TC-UNIT-RB-015: RequestBuilder headers method

**Description**: Test adding multiple headers.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.headers(X_Custom_Header="value", X_Another_Header="another")`
2. Verify method returns self
3. Verify _headers contains both headers
4. Verify header names are converted correctly (underscores to hyphens)

**Expected Result**:
- Method returns RequestBuilder instance
- _headers dictionary contains all headers
- Headers are accumulated

**Test Data**:
```python
builder.headers(X_Custom_Header="value", X_Another_Header="another")
```

---

### TC-UNIT-RB-016: RequestBuilder auth method

**Description**: Test setting authentication token.

**Preconditions**:
- RequestBuilder instance with ApiClient

**Test Steps**:
1. Call `builder.auth("token-123")`
2. Verify method returns self
3. Verify ApiClient's set_auth_token is called with token
4. Call `builder.auth("token-456", "Custom")`
5. Verify ApiClient's set_auth_token is called with token and type

**Expected Result**:
- Method returns RequestBuilder instance
- ApiClient's set_auth_token is called correctly
- Token is set on client

**Test Data**:
```python
builder.auth("token-123")
builder.auth("token-456", "Custom")
```

---

### TC-UNIT-RB-017: RequestBuilder validate with missing endpoint

**Description**: Test validation fails when endpoint is not set.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Create RequestBuilder without setting endpoint
2. Call `builder.validate()`
3. Verify ValidationError is raised
4. Verify error message indicates endpoint is required

**Expected Result**:
- ValidationError is raised
- Error message mentions endpoint requirement

**Test Data**:
```python
builder = RequestBuilder(api)
# No endpoint set
builder.validate()  # Should raise ValidationError
```

---

### TC-UNIT-RB-018: RequestBuilder validate with endpoint set

**Description**: Test validation succeeds when endpoint is set.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Call `builder.get("/users")`
2. Call `builder.validate()`
3. Verify no exceptions are raised

**Expected Result**:
- No exceptions raised
- Validation passes

**Test Data**:
```python
builder.get("/users")
builder.validate()  # Should not raise
```

---

### TC-UNIT-RB-019: RequestBuilder execute with GET request

**Description**: Test executing GET request through builder.

**Preconditions**:
- RequestBuilder instance with ApiClient
- Mocked ApiClient.make_request method

**Test Steps**:
1. Call `builder.get("/users").params(page=1)`
2. Call `await builder.execute()`
3. Verify ApiClient.make_request is called with correct parameters
4. Verify endpoint is "/users"
5. Verify method is "GET"
6. Verify params contain page=1

**Expected Result**:
- ApiClient.make_request is called
- All parameters are passed correctly
- ApiResult is returned

**Test Data**:
```python
builder.get("/users").params(page=1)
result = await builder.execute()
```

---

### TC-UNIT-RB-020: RequestBuilder execute with POST request

**Description**: Test executing POST request with body through builder.

**Preconditions**:
- RequestBuilder instance with ApiClient
- Mocked ApiClient.make_request method

**Test Steps**:
1. Call `builder.post("/users").body({"name": "John"})`
2. Call `await builder.execute()`
3. Verify ApiClient.make_request is called with correct parameters
4. Verify endpoint is "/users"
5. Verify method is "POST"
6. Verify data contains body

**Expected Result**:
- ApiClient.make_request is called
- All parameters are passed correctly
- ApiResult is returned

**Test Data**:
```python
builder.post("/users").body({"name": "John"})
result = await builder.execute()
```

---

### TC-UNIT-RB-021: RequestBuilder method chaining

**Description**: Test fluent API method chaining.

**Preconditions**:
- RequestBuilder instance

**Test Steps**:
1. Chain multiple methods: `builder.get("/users").params(page=1).header("X-Header", "value")`
2. Verify all methods return self
3. Verify all settings are applied
4. Verify chaining works correctly

**Expected Result**:
- All methods return RequestBuilder instance
- All settings are applied correctly
- Chaining works as expected

**Test Data**:
```python
builder.get("/users").params(page=1).header("X-Header", "value")
```

---

### TC-UNIT-RB-022: RequestBuilder reset method

**Description**: Test resetting builder to initial state.

**Preconditions**:
- RequestBuilder instance with some settings

**Test Steps**:
1. Set various builder properties (method, endpoint, params, headers, data)
2. Call `builder.reset()`
3. Verify method returns self
4. Verify all properties are reset to defaults
5. Verify _method is "GET"
6. Verify _endpoint is empty
7. Verify _params, _headers are empty
8. Verify _data is None

**Expected Result**:
- Method returns RequestBuilder instance
- All properties are reset to defaults
- Builder is in initial state

**Test Data**:
```python
builder.post("/users").body({"name": "John"}).params(page=1)
builder.reset()
```

---

### TC-UNIT-RB-023: RequestBuilder build_request from ApiClient

**Description**: Test creating RequestBuilder from ApiClient.build_request().

**Preconditions**:
- ApiClient instance

**Test Steps**:
1. Call `api.build_request()`
2. Verify RequestBuilder instance is returned
3. Verify builder has reference to ApiClient
4. Verify builder can be used to make requests

**Expected Result**:
- RequestBuilder instance is returned
- Builder is properly initialized
- Builder can execute requests

**Test Data**:
```python
builder = api.build_request()
```

---

## Parameterized Status Code Tests

### TC-RB-STATUS-001 to TC-RB-STATUS-010: RequestBuilder handles various HTTP status codes

**Примечание**: Тесты TC-RB-STATUS-001 до TC-RB-STATUS-010 объединены в один параметризованный тест `test_request_builder_status_codes()` для систематического тестирования различных HTTP статус-кодов.

#### TC-RB-STATUS-001: RequestBuilder handles status code 200
- **Purpose**: Verify RequestBuilder correctly handles HTTP 200 (OK) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=200
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 200
  5. Verify result.success == True
- **Expected Result**: RequestBuilder correctly processes 200 status code
- **Coverage**: `RequestBuilder.execute()` with successful response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=200, expected_success=True`

#### TC-RB-STATUS-002: RequestBuilder handles status code 201
- **Purpose**: Verify RequestBuilder correctly handles HTTP 201 (Created) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=201
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 201
  5. Verify result.success == True
- **Expected Result**: RequestBuilder correctly processes 201 status code
- **Coverage**: `RequestBuilder.execute()` with successful creation response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=201, expected_success=True`

#### TC-RB-STATUS-003: RequestBuilder handles status code 204
- **Purpose**: Verify RequestBuilder correctly handles HTTP 204 (No Content) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=204
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 204
  5. Verify result.success == True
- **Expected Result**: RequestBuilder correctly processes 204 status code
- **Coverage**: `RequestBuilder.execute()` with successful no-content response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=204, expected_success=True`

#### TC-RB-STATUS-004: RequestBuilder handles status code 400
- **Purpose**: Verify RequestBuilder correctly handles HTTP 400 (Bad Request) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=400
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 400
  5. Verify result.success == False
- **Expected Result**: RequestBuilder correctly processes 400 status code
- **Coverage**: `RequestBuilder.execute()` with client error response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=400, expected_success=False`

#### TC-RB-STATUS-005: RequestBuilder handles status code 401
- **Purpose**: Verify RequestBuilder correctly handles HTTP 401 (Unauthorized) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=401
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 401
  5. Verify result.success == False
- **Expected Result**: RequestBuilder correctly processes 401 status code
- **Coverage**: `RequestBuilder.execute()` with authentication error response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=401, expected_success=False`

#### TC-RB-STATUS-006: RequestBuilder handles status code 403
- **Purpose**: Verify RequestBuilder correctly handles HTTP 403 (Forbidden) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=403
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 403
  5. Verify result.success == False
- **Expected Result**: RequestBuilder correctly processes 403 status code
- **Coverage**: `RequestBuilder.execute()` with authorization error response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=403, expected_success=False`

#### TC-RB-STATUS-007: RequestBuilder handles status code 404
- **Purpose**: Verify RequestBuilder correctly handles HTTP 404 (Not Found) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=404
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 404
  5. Verify result.success == False
- **Expected Result**: RequestBuilder correctly processes 404 status code
- **Coverage**: `RequestBuilder.execute()` with not found error response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=404, expected_success=False`

#### TC-RB-STATUS-008: RequestBuilder handles status code 500
- **Purpose**: Verify RequestBuilder correctly handles HTTP 500 (Internal Server Error) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=500
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 500
  5. Verify result.success == False
- **Expected Result**: RequestBuilder correctly processes 500 status code
- **Coverage**: `RequestBuilder.execute()` with server error response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=500, expected_success=False`

#### TC-RB-STATUS-009: RequestBuilder handles status code 502
- **Purpose**: Verify RequestBuilder correctly handles HTTP 502 (Bad Gateway) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=502
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 502
  5. Verify result.success == False
- **Expected Result**: RequestBuilder correctly processes 502 status code
- **Coverage**: `RequestBuilder.execute()` with gateway error response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=502, expected_success=False`

#### TC-RB-STATUS-010: RequestBuilder handles status code 503
- **Purpose**: Verify RequestBuilder correctly handles HTTP 503 (Service Unavailable) status code
- **Preconditions**: ApiClient and RequestBuilder instances
- **Test Steps**:
  1. Create ApiClient and RequestBuilder
  2. Mock HTTP response with status_code=503
  3. Execute request using RequestBuilder
  4. Verify result.status_code == 503
  5. Verify result.success == False
- **Expected Result**: RequestBuilder correctly processes 503 status code
- **Coverage**: `RequestBuilder.execute()` with service unavailable error response
- **Implementation**: Параметризованный тест `test_request_builder_status_codes()` с параметрами `status_code=503, expected_success=False`

