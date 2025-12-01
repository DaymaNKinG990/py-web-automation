# Unit Test Cases: Exceptions

## Overview

Test cases for custom exception hierarchy.

## Test Cases

### TC-UNIT-EXC-001: WebAutomationError base exception

**Description**: Test base exception class initialization and string representation.

**Preconditions**:
- None

**Test Steps**:
1. Create WebAutomationError with message only
2. Verify exception message is set correctly
3. Verify details is None
4. Verify str(exception) returns message
5. Create WebAutomationError with message and details
6. Verify str(exception) returns formatted message with details

**Expected Result**:
- Exception is created successfully
- Message is stored correctly
- String representation includes details when provided

**Test Data**:
```python
error1 = WebAutomationError("Error message")
error2 = WebAutomationError("Error message", "Additional details")
```

---

### TC-UNIT-EXC-002: ConfigurationError exception

**Description**: Test ConfigurationError exception.

**Preconditions**:
- None

**Test Steps**:
1. Create ConfigurationError with message and details
2. Verify exception is instance of WebAutomationError
3. Verify exception is instance of ConfigurationError
4. Verify message and details are set correctly
5. Verify exception can be caught as WebAutomationError
6. Verify exception can be caught as ConfigurationError

**Expected Result**:
- Exception inherits from WebAutomationError
- Exception can be caught by both types
- Message and details are correct

**Test Data**:
```python
error = ConfigurationError("Invalid timeout", "Timeout must be between 1 and 300")
```

---

### TC-UNIT-EXC-003: ConnectionError exception

**Description**: Test ConnectionError exception.

**Preconditions**:
- None

**Test Steps**:
1. Create ConnectionError with message and details
2. Verify exception is instance of WebAutomationError
3. Verify exception is instance of ConnectionError
4. Verify message and details are set correctly
5. Verify exception can be caught as WebAutomationError
6. Verify exception can be caught as ConnectionError

**Expected Result**:
- Exception inherits from WebAutomationError
- Exception can be caught by both types
- Message and details are correct

**Test Data**:
```python
error = ConnectionError("Failed to connect", "Connection timeout after 30s")
```

---

### TC-UNIT-EXC-004: ValidationError exception

**Description**: Test ValidationError exception.

**Preconditions**:
- None

**Test Steps**:
1. Create ValidationError with message and details
2. Verify exception is instance of WebAutomationError
3. Verify exception is instance of ValidationError
4. Verify message and details are set correctly
5. Verify exception can be caught as WebAutomationError
6. Verify exception can be caught as ValidationError

**Expected Result**:
- Exception inherits from WebAutomationError
- Exception can be caught by both types
- Message and details are correct

**Test Data**:
```python
error = ValidationError("Invalid URL format", "URL must start with http:// or https://")
```

---

### TC-UNIT-EXC-005: OperationError exception

**Description**: Test OperationError exception.

**Preconditions**:
- None

**Test Steps**:
1. Create OperationError with message and details
2. Verify exception is instance of WebAutomationError
3. Verify exception is instance of OperationError
4. Verify message and details are set correctly
5. Verify exception can be caught as WebAutomationError
6. Verify exception can be caught as OperationError

**Expected Result**:
- Exception inherits from WebAutomationError
- Exception can be caught by both types
- Message and details are correct

**Test Data**:
```python
error = OperationError("Failed to execute query", "Table does not exist")
```

---

### TC-UNIT-EXC-006: TimeoutError exception

**Description**: Test TimeoutError exception.

**Preconditions**:
- None

**Test Steps**:
1. Create TimeoutError with message and details
2. Verify exception is instance of WebAutomationError
3. Verify exception is instance of TimeoutError
4. Verify message and details are set correctly
5. Verify exception can be caught as WebAutomationError
6. Verify exception can be caught as TimeoutError

**Expected Result**:
- Exception inherits from WebAutomationError
- Exception can be caught by both types
- Message and details are correct

**Test Data**:
```python
error = TimeoutError("Request timed out", "Operation exceeded 30 second timeout")
```

---

### TC-UNIT-EXC-007: AuthenticationError exception

**Description**: Test AuthenticationError exception.

**Preconditions**:
- None

**Test Steps**:
1. Create AuthenticationError with message and details
2. Verify exception is instance of WebAutomationError
3. Verify exception is instance of AuthenticationError
4. Verify message and details are set correctly
5. Verify exception can be caught as WebAutomationError
6. Verify exception can be caught as AuthenticationError

**Expected Result**:
- Exception inherits from WebAutomationError
- Exception can be caught by both types
- Message and details are correct

**Test Data**:
```python
error = AuthenticationError("Authentication failed", "Invalid token")
```

---

### TC-UNIT-EXC-008: NotFoundError exception

**Description**: Test NotFoundError exception.

**Preconditions**:
- None

**Test Steps**:
1. Create NotFoundError with message and details
2. Verify exception is instance of WebAutomationError
3. Verify exception is instance of NotFoundError
4. Verify message and details are set correctly
5. Verify exception can be caught as WebAutomationError
6. Verify exception can be caught as NotFoundError

**Expected Result**:
- Exception inherits from WebAutomationError
- Exception can be caught by both types
- Message and details are correct

**Test Data**:
```python
error = NotFoundError("Element not found", "Selector '#button' did not match any element")
```

---

### TC-UNIT-EXC-009: Exception hierarchy catch all

**Description**: Test catching all framework exceptions with base class.

**Preconditions**:
- None

**Test Steps**:
1. Create various exception types (ConfigurationError, ConnectionError, etc.)
2. Catch all exceptions as WebAutomationError
3. Verify all exceptions are caught correctly
4. Verify exception types are preserved

**Expected Result**:
- All exceptions can be caught as WebAutomationError
- Exception types are preserved
- Exception hierarchy works correctly

**Test Data**:
```python
exceptions = [
    ConfigurationError("Config error"),
    ConnectionError("Connection error"),
    ValidationError("Validation error"),
    OperationError("Operation error"),
    TimeoutError("Timeout error"),
    AuthenticationError("Auth error"),
    NotFoundError("Not found error"),
]
```

---

### TC-UNIT-EXC-010: Exception with None details

**Description**: Test exception with None details.

**Preconditions**:
- None

**Test Steps**:
1. Create exception with message and None details
2. Verify exception is created successfully
3. Verify details is None
4. Verify str(exception) returns only message (no ": None")

**Expected Result**:
- Exception is created successfully
- String representation shows only message when details is None

**Test Data**:
```python
error = WebAutomationError("Error message", None)
```

---

### TC-UNIT-EXC-011: Exception with empty details

**Description**: Test exception with empty string details.

**Preconditions**:
- None

**Test Steps**:
1. Create exception with message and empty string details
2. Verify exception is created successfully
3. Verify details is empty string
4. Verify str(exception) returns formatted message

**Expected Result**:
- Exception is created successfully
- String representation includes empty details

**Test Data**:
```python
error = WebAutomationError("Error message", "")
```

