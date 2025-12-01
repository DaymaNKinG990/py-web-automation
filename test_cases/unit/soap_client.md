# Unit Test Cases: SOAP Client

## Overview

Test cases for SoapClient class.

## Test Cases

### TC-UNIT-SOAP-001: SoapClient initialization

**Description**: Test SoapClient initialization.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Create SoapClient with URL and config
2. Verify client is initialized correctly
3. Verify soap_version defaults to "1.1"
4. Verify _auth_token is None
5. Verify _auth_token_type is "Bearer"

**Expected Result**:
- SoapClient is created successfully
- Default values are set correctly
- No exceptions raised

**Test Data**:
```python
config = Config(timeout=30)
soap = SoapClient("https://api.example.com/soap", config)
```

---

### TC-UNIT-SOAP-002: SoapClient initialization with SOAP 1.2

**Description**: Test SoapClient initialization with SOAP 1.2.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Create SoapClient with soap_version="1.2"
2. Verify soap_version is set to "1.2"
3. Verify other defaults are set correctly

**Expected Result**:
- SoapClient is created with SOAP 1.2
- Version is stored correctly

**Test Data**:
```python
config = Config(timeout=30)
soap = SoapClient("https://api.example.com/soap", config, soap_version="1.2")
```

---

### TC-UNIT-SOAP-003: SoapClient initialization with invalid version

**Description**: Test SoapClient initialization fails with invalid SOAP version.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Attempt to create SoapClient with soap_version="2.0"
2. Verify ValueError is raised
3. Verify error message indicates invalid version

**Expected Result**:
- ValueError is raised
- Error message mentions valid versions (1.1, 1.2)

**Test Data**:
```python
config = Config(timeout=30)
# Should raise ValueError
soap = SoapClient("https://api.example.com/soap", config, soap_version="2.0")
```

---

### TC-UNIT-SOAP-004: SoapClient set_auth_token

**Description**: Test setting authentication token.

**Preconditions**:
- SoapClient instance

**Test Steps**:
1. Call `soap.set_auth_token("token-123")`
2. Verify _auth_token is set
3. Verify _auth_token_type is "Bearer" (default)
4. Call `soap.set_auth_token("token-456", "Custom")`
5. Verify _auth_token is updated
6. Verify _auth_token_type is "Custom"

**Expected Result**:
- Token is set correctly
- Token type is set correctly
- No exceptions raised

**Test Data**:
```python
soap.set_auth_token("token-123")
soap.set_auth_token("token-456", "Custom")
```

---

### TC-UNIT-SOAP-005: SoapClient clear_auth_token

**Description**: Test clearing authentication token.

**Preconditions**:
- SoapClient instance with token set

**Test Steps**:
1. Set authentication token
2. Call `soap.clear_auth_token()`
3. Verify _auth_token is None
4. Verify _auth_token_type is "Bearer" (reset)

**Expected Result**:
- Token is cleared
- Token type is reset
- No exceptions raised

**Test Data**:
```python
soap.set_auth_token("token-123")
soap.clear_auth_token()
```

---

### TC-UNIT-SOAP-006: SoapClient call with SOAP 1.1

**Description**: Test executing SOAP 1.1 operation call.

**Preconditions**:
- SoapClient instance (SOAP 1.1)
- Mocked HTTP client

**Test Steps**:
1. Mock HTTP client response
2. Call `await soap.call("GetUser", {"userId": "123"})`
3. Verify SOAP envelope is built correctly
4. Verify Content-Type header is "text/xml"
5. Verify SOAPAction header is set
6. Verify ApiResult is returned

**Expected Result**:
- SOAP call is executed successfully
- Correct SOAP envelope is sent
- Headers are set correctly
- ApiResult is returned

**Test Data**:
```python
result = await soap.call("GetUser", {"userId": "123"})
```

---

### TC-UNIT-SOAP-007: SoapClient call with SOAP 1.2

**Description**: Test executing SOAP 1.2 operation call.

**Preconditions**:
- SoapClient instance (SOAP 1.2)
- Mocked HTTP client

**Test Steps**:
1. Mock HTTP client response
2. Call `await soap.call("GetUser", {"userId": "123"})`
3. Verify SOAP 1.2 envelope is built correctly
4. Verify SOAPAction header is empty (SOAP 1.2 doesn't use it)
5. Verify ApiResult is returned

**Expected Result**:
- SOAP 1.2 call is executed successfully
- Correct SOAP 1.2 envelope is sent
- Headers are set correctly
- ApiResult is returned

**Test Data**:
```python
soap = SoapClient("https://api.example.com/soap", config, soap_version="1.2")
result = await soap.call("GetUser", {"userId": "123"})
```

---

### TC-UNIT-SOAP-008: SoapClient call with namespace

**Description**: Test executing SOAP call with namespace.

**Preconditions**:
- SoapClient instance
- Mocked HTTP client

**Test Steps**:
1. Mock HTTP client response
2. Call `await soap.call("GetUser", {"userId": "123"}, namespace="http://example.com/service")`
3. Verify namespace is included in SOAP envelope
4. Verify ApiResult is returned

**Expected Result**:
- Namespace is included in envelope
- SOAP call executes successfully
- ApiResult is returned

**Test Data**:
```python
result = await soap.call(
    "GetUser",
    {"userId": "123"},
    namespace="http://example.com/service"
)
```

---

### TC-UNIT-SOAP-009: SoapClient call with nested body

**Description**: Test executing SOAP call with nested body structure.

**Preconditions**:
- SoapClient instance
- Mocked HTTP client

**Test Steps**:
1. Mock HTTP client response
2. Call `await soap.call("CreateUser", {"user": {"name": "John", "email": "john@example.com"}})`
3. Verify nested structure is converted to XML correctly
4. Verify ApiResult is returned

**Expected Result**:
- Nested structure is converted correctly
- SOAP call executes successfully
- ApiResult is returned

**Test Data**:
```python
result = await soap.call(
    "CreateUser",
    {"user": {"name": "John", "email": "john@example.com"}}
)
```

---

### TC-UNIT-SOAP-010: SoapClient call with list in body

**Description**: Test executing SOAP call with list in body.

**Preconditions**:
- SoapClient instance
- Mocked HTTP client

**Test Steps**:
1. Mock HTTP client response
2. Call `await soap.call("GetUsers", {"userIds": [1, 2, 3]})`
3. Verify list is converted to XML correctly
4. Verify ApiResult is returned

**Expected Result**:
- List is converted correctly
- SOAP call executes successfully
- ApiResult is returned

**Test Data**:
```python
result = await soap.call("GetUsers", {"userIds": [1, 2, 3]})
```

---

### TC-UNIT-SOAP-011: SoapClient call with auth token

**Description**: Test SOAP call execution includes authentication token.

**Preconditions**:
- SoapClient instance with auth token
- Mocked HTTP client

**Test Steps**:
1. Set authentication token
2. Mock HTTP client response
3. Call `await soap.call("GetUser", {"userId": "123"})`
4. Verify Authorization header is included
5. Verify header format is correct

**Expected Result**:
- Authorization header is included
- Header format is "Bearer token" or custom type
- SOAP call executes successfully

**Test Data**:
```python
soap.set_auth_token("token-123")
result = await soap.call("GetUser", {"userId": "123"})
```

---

### TC-UNIT-SOAP-012: SoapClient parse_soap_fault with fault

**Description**: Test parsing SOAP fault from response.

**Preconditions**:
- SoapClient instance
- ApiResult with SOAP fault

**Test Steps**:
1. Create ApiResult with SOAP fault in body
2. Call `soap.parse_soap_fault(result)`
3. Verify fault dictionary is returned
4. Verify fault contains expected fields (faultcode, faultstring, etc.)

**Expected Result**:
- Fault is parsed correctly
- Fault dictionary is returned
- Fault fields are accessible

**Test Data**:
```python
result = ApiResult(
    endpoint="/soap",
    method="POST",
    status_code=500,
    response_time=0.1,
    success=False,
    body=b'<soap:Envelope><soap:Body><soap:Fault><faultcode>Server</faultcode><faultstring>Error</faultstring></soap:Fault></soap:Body></soap:Envelope>'
)
fault = soap.parse_soap_fault(result)
```

---

### TC-UNIT-SOAP-013: SoapClient parse_soap_fault without fault

**Description**: Test parsing SOAP fault from response without fault.

**Preconditions**:
- SoapClient instance
- ApiResult without SOAP fault

**Test Steps**:
1. Create ApiResult with success response body
2. Call `soap.parse_soap_fault(result)`
3. Verify None is returned

**Expected Result**:
- None is returned
- No exceptions raised

**Test Data**:
```python
result = ApiResult(
    endpoint="/soap",
    method="POST",
    status_code=200,
    response_time=0.1,
    success=True,
    body=b'<soap:Envelope><soap:Body><GetUserResponse>...</GetUserResponse></soap:Body></soap:Envelope>'
)
fault = soap.parse_soap_fault(result)  # Should be None
```

---

### TC-UNIT-SOAP-014: SoapClient parse_soap_fault SOAP 1.2

**Description**: Test parsing SOAP 1.2 fault.

**Preconditions**:
- SoapClient instance (SOAP 1.2)
- ApiResult with SOAP 1.2 fault

**Test Steps**:
1. Create SoapClient with SOAP 1.2
2. Create ApiResult with SOAP 1.2 fault
3. Call `soap.parse_soap_fault(result)`
4. Verify fault is parsed correctly
5. Verify fault dictionary is returned

**Expected Result**:
- SOAP 1.2 fault is parsed correctly
- Fault dictionary is returned
- No exceptions raised

**Test Data**:
```python
soap = SoapClient("https://api.example.com/soap", config, soap_version="1.2")
result = ApiResult(..., body=b'<soap12:Envelope>...<soap12:Fault>...</soap12:Fault>...</soap12:Envelope>')
fault = soap.parse_soap_fault(result)
```

---

### TC-UNIT-SOAP-015: SoapClient close method

**Description**: Test closing SOAP client.

**Preconditions**:
- SoapClient instance

**Test Steps**:
1. Call `await soap.close()`
2. Verify HTTP client is closed
3. Verify _auth_token is cleared
4. Verify _auth_token_type is reset

**Expected Result**:
- Client is closed successfully
- State is reset correctly
- No exceptions raised

**Test Data**:
```python
await soap.close()
```

---

### TC-UNIT-SOAP-016: SoapClient context manager

**Description**: Test SoapClient as async context manager.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Use SoapClient in async with statement
2. Verify close() is called on exit
3. Verify resources are cleaned up

**Expected Result**:
- Context manager works correctly
- Resources are cleaned up on exit

**Test Data**:
```python
async with SoapClient("https://api.example.com/soap", config) as soap:
    result = await soap.call("GetUser", {"userId": "123"})
# Client should be closed
```

