# Unit Test Cases: GraphQL Client

## Overview

Test cases for GraphQLClient class.

## Test Cases

### TC-UNIT-GQL-001: GraphQLClient initialization

**Description**: Test GraphQLClient initialization.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Create GraphQLClient with URL and config
2. Verify client is initialized correctly
3. Verify endpoint defaults to "/graphql"
4. Verify _auth_token is None
5. Verify _auth_token_type is "Bearer"

**Expected Result**:
- GraphQLClient is created successfully
- Default values are set correctly
- No exceptions raised

**Test Data**:
```python
config = Config(timeout=30)
gql = GraphQLClient("https://api.example.com", config)
```

---

### TC-UNIT-GQL-002: GraphQLClient initialization with custom endpoint

**Description**: Test GraphQLClient initialization with custom endpoint.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Create GraphQLClient with custom endpoint
2. Verify endpoint is set correctly
3. Verify other defaults are set correctly

**Expected Result**:
- GraphQLClient is created with custom endpoint
- Endpoint is stored correctly

**Test Data**:
```python
config = Config(timeout=30)
gql = GraphQLClient("https://api.example.com", config, endpoint="/api/graphql")
```

---

### TC-UNIT-GQL-003: GraphQLClient set_auth_token

**Description**: Test setting authentication token.

**Preconditions**:
- GraphQLClient instance

**Test Steps**:
1. Call `gql.set_auth_token("token-123")`
2. Verify _auth_token is set
3. Verify _auth_token_type is "Bearer" (default)
4. Call `gql.set_auth_token("token-456", "Custom")`
5. Verify _auth_token is updated
6. Verify _auth_token_type is "Custom"

**Expected Result**:
- Token is set correctly
- Token type is set correctly
- No exceptions raised

**Test Data**:
```python
gql.set_auth_token("token-123")
gql.set_auth_token("token-456", "Custom")
```

---

### TC-UNIT-GQL-004: GraphQLClient clear_auth_token

**Description**: Test clearing authentication token.

**Preconditions**:
- GraphQLClient instance with token set

**Test Steps**:
1. Set authentication token
2. Call `gql.clear_auth_token()`
3. Verify _auth_token is None
4. Verify _auth_token_type is "Bearer" (reset)

**Expected Result**:
- Token is cleared
- Token type is reset
- No exceptions raised

**Test Data**:
```python
gql.set_auth_token("token-123")
gql.clear_auth_token()
```

---

### TC-UNIT-GQL-005: GraphQLClient query execution

**Description**: Test executing GraphQL query.

**Preconditions**:
- GraphQLClient instance
- Mocked HTTP client

**Test Steps**:
1. Mock HTTP client response
2. Call `await gql.query("query { user { name } }")`
3. Verify HTTP POST is called with correct URL
4. Verify payload contains query
5. Verify ApiResult is returned

**Expected Result**:
- Query is executed successfully
- Correct payload is sent
- ApiResult is returned

**Test Data**:
```python
result = await gql.query("query { user { name } }")
```

---

### TC-UNIT-GQL-006: GraphQLClient query with variables

**Description**: Test executing GraphQL query with variables.

**Preconditions**:
- GraphQLClient instance
- Mocked HTTP client

**Test Steps**:
1. Mock HTTP client response
2. Call `await gql.query("query GetUser($id: ID!) { user(id: $id) { name } }", variables={"id": "1"})`
3. Verify payload contains query and variables
4. Verify ApiResult is returned

**Expected Result**:
- Query with variables is executed successfully
- Variables are included in payload
- ApiResult is returned

**Test Data**:
```python
result = await gql.query(
    "query GetUser($id: ID!) { user(id: $id) { name } }",
    variables={"id": "1"}
)
```

---

### TC-UNIT-GQL-007: GraphQLClient query with operation name

**Description**: Test executing GraphQL query with operation name.

**Preconditions**:
- GraphQLClient instance
- Mocked HTTP client

**Test Steps**:
1. Mock HTTP client response
2. Call `await gql.query("query GetUser { user { name } }", operation_name="GetUser")`
3. Verify payload contains operationName
4. Verify ApiResult is returned

**Expected Result**:
- Query with operation name is executed successfully
- Operation name is included in payload
- ApiResult is returned

**Test Data**:
```python
result = await gql.query(
    "query GetUser { user { name } }",
    operation_name="GetUser"
)
```

---

### TC-UNIT-GQL-008: GraphQLClient mutate execution

**Description**: Test executing GraphQL mutation.

**Preconditions**:
- GraphQLClient instance
- Mocked HTTP client

**Test Steps**:
1. Mock HTTP client response
2. Call `await gql.mutate("mutation { createUser(name: \"John\") { id } }")`
3. Verify HTTP POST is called
4. Verify payload contains mutation
5. Verify ApiResult is returned

**Expected Result**:
- Mutation is executed successfully
- Correct payload is sent
- ApiResult is returned

**Test Data**:
```python
result = await gql.mutate("mutation { createUser(name: \"John\") { id } }")
```

---

### TC-UNIT-GQL-009: GraphQLClient query with auth token

**Description**: Test query execution includes authentication token.

**Preconditions**:
- GraphQLClient instance with auth token
- Mocked HTTP client

**Test Steps**:
1. Set authentication token
2. Mock HTTP client response
3. Call `await gql.query("query { user { name } }")`
4. Verify Authorization header is included
5. Verify header format is correct

**Expected Result**:
- Authorization header is included
- Header format is "Bearer token" or custom type
- Query executes successfully

**Test Data**:
```python
gql.set_auth_token("token-123")
result = await gql.query("query { user { name } }")
```

---

### TC-UNIT-GQL-010: GraphQLClient get_errors with errors

**Description**: Test extracting errors from GraphQL response.

**Preconditions**:
- GraphQLClient instance
- ApiResult with GraphQL errors

**Test Steps**:
1. Create ApiResult with error response body
2. Call `gql.get_errors(result)`
3. Verify errors list is returned
4. Verify errors contain expected fields

**Expected Result**:
- Errors are extracted correctly
- Error list is returned
- Errors have expected structure

**Test Data**:
```python
result = ApiResult(
    endpoint="/graphql",
    method="POST",
    status_code=200,
    response_time=0.1,
    success=True,
    body=b'{"errors": [{"message": "Error message"}]}'
)
errors = gql.get_errors(result)
```

---

### TC-UNIT-GQL-011: GraphQLClient get_errors without errors

**Description**: Test extracting errors from response without errors.

**Preconditions**:
- GraphQLClient instance
- ApiResult without errors

**Test Steps**:
1. Create ApiResult with success response body
2. Call `gql.get_errors(result)`
3. Verify empty list is returned

**Expected Result**:
- Empty list is returned
- No exceptions raised

**Test Data**:
```python
result = ApiResult(
    endpoint="/graphql",
    method="POST",
    status_code=200,
    response_time=0.1,
    success=True,
    body=b'{"data": {"user": {"name": "John"}}}'
)
errors = gql.get_errors(result)  # Should be []
```

---

### TC-UNIT-GQL-012: GraphQLClient get_errors with invalid JSON

**Description**: Test extracting errors from invalid JSON response.

**Preconditions**:
- GraphQLClient instance
- ApiResult with invalid JSON

**Test Steps**:
1. Create ApiResult with invalid JSON body
2. Call `gql.get_errors(result)`
3. Verify empty list is returned (graceful handling)

**Expected Result**:
- Empty list is returned
- No exceptions raised
- Graceful error handling

**Test Data**:
```python
result = ApiResult(
    endpoint="/graphql",
    method="POST",
    status_code=200,
    response_time=0.1,
    success=True,
    body=b"Invalid JSON"
)
errors = gql.get_errors(result)  # Should be []
```

---

### TC-UNIT-GQL-013: GraphQLClient close method

**Description**: Test closing GraphQL client.

**Preconditions**:
- GraphQLClient instance

**Test Steps**:
1. Call `await gql.close()`
2. Verify HTTP client is closed
3. Verify _auth_token is cleared
4. Verify _auth_token_type is reset

**Expected Result**:
- Client is closed successfully
- State is reset correctly
- No exceptions raised

**Test Data**:
```python
await gql.close()
```

---

### TC-UNIT-GQL-014: GraphQLClient context manager

**Description**: Test GraphQLClient as async context manager.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Use GraphQLClient in async with statement
2. Verify close() is called on exit
3. Verify resources are cleaned up

**Expected Result**:
- Context manager works correctly
- Resources are cleaned up on exit

**Test Data**:
```python
async with GraphQLClient("https://api.example.com", config) as gql:
    result = await gql.query("query { user { name } }")
# Client should be closed
```

---

## Parameterized Status Code Tests

### TC-GRAPHQL-STATUS-001 to TC-GRAPHQL-STATUS-009: GraphQLClient handles various HTTP status codes

**Примечание**: Тесты TC-GRAPHQL-STATUS-001 до TC-GRAPHQL-STATUS-009 объединены в один параметризованный тест `test_graphql_client_status_codes()` для систематического тестирования различных HTTP статус-кодов.

#### TC-GRAPHQL-STATUS-001: GraphQLClient handles status code 200
- **Purpose**: Verify GraphQLClient correctly handles HTTP 200 (OK) status code
- **Preconditions**: GraphQLClient instance
- **Test Steps**:
  1. Create GraphQLClient
  2. Mock HTTP response with status_code=200
  3. Execute GraphQL query
  4. Verify result.status_code == 200
  5. Verify result.success == True
- **Expected Result**: GraphQLClient correctly processes 200 status code
- **Coverage**: `GraphQLClient.query()` with successful response
- **Implementation**: Параметризованный тест `test_graphql_client_status_codes()` с параметрами `status_code=200, expected_success=True`

#### TC-GRAPHQL-STATUS-002: GraphQLClient handles status code 201
- **Purpose**: Verify GraphQLClient correctly handles HTTP 201 (Created) status code
- **Preconditions**: GraphQLClient instance
- **Test Steps**:
  1. Create GraphQLClient
  2. Mock HTTP response with status_code=201
  3. Execute GraphQL mutation
  4. Verify result.status_code == 201
  5. Verify result.success == True
- **Expected Result**: GraphQLClient correctly processes 201 status code
- **Coverage**: `GraphQLClient.mutate()` with successful creation response
- **Implementation**: Параметризованный тест `test_graphql_client_status_codes()` с параметрами `status_code=201, expected_success=True`

#### TC-GRAPHQL-STATUS-003: GraphQLClient handles status code 400
- **Purpose**: Verify GraphQLClient correctly handles HTTP 400 (Bad Request) status code
- **Preconditions**: GraphQLClient instance
- **Test Steps**:
  1. Create GraphQLClient
  2. Mock HTTP response with status_code=400
  3. Execute GraphQL query
  4. Verify result.status_code == 400
  5. Verify result.success == False
- **Expected Result**: GraphQLClient correctly processes 400 status code
- **Coverage**: `GraphQLClient.query()` with client error response
- **Implementation**: Параметризованный тест `test_graphql_client_status_codes()` с параметрами `status_code=400, expected_success=False`

#### TC-GRAPHQL-STATUS-004: GraphQLClient handles status code 401
- **Purpose**: Verify GraphQLClient correctly handles HTTP 401 (Unauthorized) status code
- **Preconditions**: GraphQLClient instance
- **Test Steps**:
  1. Create GraphQLClient
  2. Mock HTTP response with status_code=401
  3. Execute GraphQL query
  4. Verify result.status_code == 401
  5. Verify result.success == False
- **Expected Result**: GraphQLClient correctly processes 401 status code
- **Coverage**: `GraphQLClient.query()` with authentication error response
- **Implementation**: Параметризованный тест `test_graphql_client_status_codes()` с параметрами `status_code=401, expected_success=False`

#### TC-GRAPHQL-STATUS-005: GraphQLClient handles status code 403
- **Purpose**: Verify GraphQLClient correctly handles HTTP 403 (Forbidden) status code
- **Preconditions**: GraphQLClient instance
- **Test Steps**:
  1. Create GraphQLClient
  2. Mock HTTP response with status_code=403
  3. Execute GraphQL query
  4. Verify result.status_code == 403
  5. Verify result.success == False
- **Expected Result**: GraphQLClient correctly processes 403 status code
- **Coverage**: `GraphQLClient.query()` with authorization error response
- **Implementation**: Параметризованный тест `test_graphql_client_status_codes()` с параметрами `status_code=403, expected_success=False`

#### TC-GRAPHQL-STATUS-006: GraphQLClient handles status code 404
- **Purpose**: Verify GraphQLClient correctly handles HTTP 404 (Not Found) status code
- **Preconditions**: GraphQLClient instance
- **Test Steps**:
  1. Create GraphQLClient
  2. Mock HTTP response with status_code=404
  3. Execute GraphQL query
  4. Verify result.status_code == 404
  5. Verify result.success == False
- **Expected Result**: GraphQLClient correctly processes 404 status code
- **Coverage**: `GraphQLClient.query()` with not found error response
- **Implementation**: Параметризованный тест `test_graphql_client_status_codes()` с параметрами `status_code=404, expected_success=False`

#### TC-GRAPHQL-STATUS-007: GraphQLClient handles status code 500
- **Purpose**: Verify GraphQLClient correctly handles HTTP 500 (Internal Server Error) status code
- **Preconditions**: GraphQLClient instance
- **Test Steps**:
  1. Create GraphQLClient
  2. Mock HTTP response with status_code=500
  3. Execute GraphQL query
  4. Verify result.status_code == 500
  5. Verify result.success == False
- **Expected Result**: GraphQLClient correctly processes 500 status code
- **Coverage**: `GraphQLClient.query()` with server error response
- **Implementation**: Параметризованный тест `test_graphql_client_status_codes()` с параметрами `status_code=500, expected_success=False`

#### TC-GRAPHQL-STATUS-008: GraphQLClient handles status code 502
- **Purpose**: Verify GraphQLClient correctly handles HTTP 502 (Bad Gateway) status code
- **Preconditions**: GraphQLClient instance
- **Test Steps**:
  1. Create GraphQLClient
  2. Mock HTTP response with status_code=502
  3. Execute GraphQL query
  4. Verify result.status_code == 502
  5. Verify result.success == False
- **Expected Result**: GraphQLClient correctly processes 502 status code
- **Coverage**: `GraphQLClient.query()` with gateway error response
- **Implementation**: Параметризованный тест `test_graphql_client_status_codes()` с параметрами `status_code=502, expected_success=False`

#### TC-GRAPHQL-STATUS-009: GraphQLClient handles status code 503
- **Purpose**: Verify GraphQLClient correctly handles HTTP 503 (Service Unavailable) status code
- **Preconditions**: GraphQLClient instance
- **Test Steps**:
  1. Create GraphQLClient
  2. Mock HTTP response with status_code=503
  3. Execute GraphQL query
  4. Verify result.status_code == 503
  5. Verify result.success == False
- **Expected Result**: GraphQLClient correctly processes 503 status code
- **Coverage**: `GraphQLClient.query()` with service unavailable error response
- **Implementation**: Параметризованный тест `test_graphql_client_status_codes()` с параметрами `status_code=503, expected_success=False`

