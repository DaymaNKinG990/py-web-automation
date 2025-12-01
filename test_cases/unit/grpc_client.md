# Unit Test Cases: gRPC Client

## Overview

Test cases for GrpcClient abstract base class and GrpcClientImpl concrete implementation.

## Test Cases

### TC-UNIT-GRPC-001: GrpcClient initialization

**Description**: Test GrpcClient abstract base class initialization.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Create GrpcClient subclass instance
2. Verify client is initialized correctly
3. Verify _channel is None
4. Verify _metadata is empty dict

**Expected Result**:
- GrpcClient subclass is created successfully
- Initial values are set correctly
- No exceptions raised

**Test Data**:
```python
config = Config(timeout=30)
# Using concrete implementation
client = GrpcClientImpl("localhost:50051", config)
```

---

### TC-UNIT-GRPC-002: GrpcClient set_metadata

**Description**: Test setting default metadata.

**Preconditions**:
- GrpcClient instance

**Test Steps**:
1. Call `client.set_metadata("authorization", "Bearer token123")`
2. Verify metadata is stored in _metadata dict
3. Call `client.set_metadata("x-custom-header", "value")`
4. Verify both metadata entries are stored

**Expected Result**:
- Metadata is stored correctly
- Multiple metadata entries can be set
- No exceptions raised

**Test Data**:
```python
client.set_metadata("authorization", "Bearer token123")
client.set_metadata("x-custom-header", "value")
```

---

### TC-UNIT-GRPC-003: GrpcClient clear_metadata

**Description**: Test clearing all metadata.

**Preconditions**:
- GrpcClient instance with metadata set

**Test Steps**:
1. Set multiple metadata entries
2. Call `client.clear_metadata()`
3. Verify _metadata is empty

**Expected Result**:
- All metadata is cleared
- _metadata is empty dict
- No exceptions raised

**Test Data**:
```python
client.set_metadata("authorization", "Bearer token123")
client.set_metadata("x-custom-header", "value")
client.clear_metadata()
```

---

### TC-UNIT-GRPC-004: GrpcClient _merge_metadata

**Description**: Test merging default metadata with call-specific metadata.

**Preconditions**:
- GrpcClient instance with default metadata

**Test Steps**:
1. Set default metadata
2. Call `_merge_metadata({"x-call-header": "call-value"})`
3. Verify merged dict contains both default and call metadata
4. Verify call metadata overrides default if key conflicts

**Expected Result**:
- Metadata is merged correctly
- Call metadata takes precedence
- No exceptions raised

**Test Data**:
```python
client.set_metadata("authorization", "Bearer default")
merged = client._merge_metadata({"authorization": "Bearer call", "x-call-header": "value"})
# Should contain: authorization="Bearer call", x-call-header="value"
```

---

### TC-UNIT-GRPC-005: GrpcClient _merge_metadata with None

**Description**: Test merging metadata with None (only default metadata).

**Preconditions**:
- GrpcClient instance with default metadata

**Test Steps**:
1. Set default metadata
2. Call `_merge_metadata(None)`
3. Verify returned dict contains only default metadata

**Expected Result**:
- Only default metadata is returned
- No exceptions raised

**Test Data**:
```python
client.set_metadata("authorization", "Bearer token123")
merged = client._merge_metadata(None)
# Should contain only: authorization="Bearer token123"
```

---

### TC-UNIT-GRPC-006: GrpcClient close method

**Description**: Test closing gRPC client.

**Preconditions**:
- GrpcClient instance (connected)

**Test Steps**:
1. Connect client (mocked)
2. Set metadata
3. Call `await client.close()`
4. Verify disconnect() is called
5. Verify _metadata is cleared

**Expected Result**:
- Client is closed successfully
- Metadata is cleared
- No exceptions raised

**Test Data**:
```python
await client.connect()  # Mocked
client.set_metadata("authorization", "Bearer token123")
await client.close()
```

---

### TC-UNIT-GRPC-007: GrpcClient context manager

**Description**: Test GrpcClient as async context manager.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Use GrpcClient in async with statement
2. Verify connect() is called on entry
3. Verify close() is called on exit
4. Verify connection is established
5. Verify connection is closed on exit

**Expected Result**:
- Context manager works correctly
- Connection is established on entry
- Connection is closed on exit

**Test Data**:
```python
async with GrpcClientImpl("localhost:50051", config) as client:
    # Connection should be established
    pass
# Connection should be closed
```

---

### TC-UNIT-GRPC-008: GrpcClientImpl connect method

**Description**: Test GrpcClientImpl connect method.

**Preconditions**:
- GrpcClientImpl instance
- Mocked gRPC connection

**Test Steps**:
1. Mock gRPC channel creation
2. Call `await client.connect()`
3. Verify _channel is set
4. Verify _is_connected is True
5. Verify connection is logged

**Expected Result**:
- Connection is established
- State is updated correctly
- No exceptions raised

**Test Data**:
```python
await client.connect()  # Mocked
```

---

### TC-UNIT-GRPC-009: GrpcClientImpl connect failure

**Description**: Test GrpcClientImpl connect method handles failures.

**Preconditions**:
- GrpcClientImpl instance
- Mocked gRPC connection that fails

**Test Steps**:
1. Mock gRPC channel creation to raise exception
2. Call `await client.connect()`
3. Verify RuntimeError is raised
4. Verify error message indicates connection failure

**Expected Result**:
- RuntimeError is raised
- Error message mentions connection failure
- State is not updated

**Test Data**:
```python
# Mock connection failure
# Should raise RuntimeError
await client.connect()
```

---

### TC-UNIT-GRPC-010: GrpcClientImpl disconnect method

**Description**: Test GrpcClientImpl disconnect method.

**Preconditions**:
- GrpcClientImpl instance (connected)
- Mocked gRPC connection

**Test Steps**:
1. Connect client (mocked)
2. Call `await client.disconnect()`
3. Verify _channel is set to None
4. Verify disconnect is logged

**Expected Result**:
- Connection is closed
- State is reset correctly
- No exceptions raised

**Test Data**:
```python
await client.connect()  # Mocked
await client.disconnect()
```

---

### TC-UNIT-GRPC-011: GrpcClientImpl disconnect when not connected

**Description**: Test GrpcClientImpl disconnect when not connected.

**Preconditions**:
- GrpcClientImpl instance (not connected)

**Test Steps**:
1. Create client (do not connect)
2. Call `await client.disconnect()`
3. Verify no exceptions are raised
4. Verify method is idempotent

**Expected Result**:
- No exceptions raised
- Method is idempotent
- State remains unchanged

**Test Data**:
```python
# Not connected
await client.disconnect()  # Should not raise
```

---

### TC-UNIT-GRPC-012: GrpcClientImpl unary_call not implemented

**Description**: Test GrpcClientImpl unary_call raises NotImplementedError.

**Preconditions**:
- GrpcClientImpl instance (connected)

**Test Steps**:
1. Connect client (mocked)
2. Call `await client.unary_call("Service", "Method", request)`
3. Verify NotImplementedError is raised
4. Verify error message mentions protobuf requirements

**Expected Result**:
- NotImplementedError is raised
- Error message mentions protobuf definitions

**Test Data**:
```python
await client.connect()  # Mocked
# Should raise NotImplementedError
await client.unary_call("UserService", "GetUser", request)
```

---

### TC-UNIT-GRPC-013: GrpcClientImpl unary_call when not connected

**Description**: Test GrpcClientImpl unary_call raises RuntimeError when not connected.

**Preconditions**:
- GrpcClientImpl instance (not connected)

**Test Steps**:
1. Create client (do not connect)
2. Call `await client.unary_call("Service", "Method", request)`
3. Verify RuntimeError is raised
4. Verify error message indicates not connected

**Expected Result**:
- RuntimeError is raised
- Error message mentions connection requirement

**Test Data**:
```python
# Not connected
# Should raise RuntimeError
await client.unary_call("UserService", "GetUser", request)
```

---

### TC-UNIT-GRPC-014: GrpcClientImpl server_streaming_call not implemented

**Description**: Test GrpcClientImpl server_streaming_call raises NotImplementedError.

**Preconditions**:
- GrpcClientImpl instance (connected)

**Test Steps**:
1. Connect client (mocked)
2. Call `await client.server_streaming_call("Service", "Method", request)`
3. Verify NotImplementedError is raised
4. Verify error message mentions protobuf requirements

**Expected Result**:
- NotImplementedError is raised
- Error message mentions protobuf definitions

**Test Data**:
```python
await client.connect()  # Mocked
# Should raise NotImplementedError
async for response in client.server_streaming_call("UserService", "ListUsers", request):
    pass
```

---

### TC-UNIT-GRPC-015: GrpcClientImpl server_streaming_call when not connected

**Description**: Test GrpcClientImpl server_streaming_call raises RuntimeError when not connected.

**Preconditions**:
- GrpcClientImpl instance (not connected)

**Test Steps**:
1. Create client (do not connect)
2. Call `await client.server_streaming_call("Service", "Method", request)`
3. Verify RuntimeError is raised
4. Verify error message indicates not connected

**Expected Result**:
- RuntimeError is raised
- Error message mentions connection requirement

**Test Data**:
```python
# Not connected
# Should raise RuntimeError
async for response in client.server_streaming_call("UserService", "ListUsers", request):
    pass
```

---

### TC-UNIT-GRPC-016: GrpcClient abstract methods

**Description**: Test that GrpcClient abstract methods must be implemented.

**Preconditions**:
- None

**Test Steps**:
1. Attempt to create subclass without implementing abstract methods
2. Verify TypeError is raised (cannot instantiate abstract class)
3. Verify error mentions abstract methods

**Expected Result**:
- TypeError is raised
- Error indicates abstract methods must be implemented

**Test Data**:
```python
# Should raise TypeError
class IncompleteGrpcClient(GrpcClient):
    pass

client = IncompleteGrpcClient("localhost:50051", config)
```

