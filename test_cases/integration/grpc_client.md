# gRPC Client Integration Test Cases

## Overview
Tests for integration between `GrpcClient` and other framework components, and real gRPC services.

## Test Categories

### 1. GrpcClient Basic Integration

#### TC-INTEGRATION-GRPC-001: GrpcClient connection
- **Purpose**: Verify GrpcClient connects to gRPC service successfully
- **Preconditions**: 
  - gRPC service endpoint available
  - Valid gRPC service definition
- **Test Steps**:
  1. Create `GrpcClientImpl` with gRPC endpoint URL
  2. Connect using `await client.connect()`
  3. Verify connection is established
  4. Verify `_is_connected` is True
  5. Disconnect using `await client.disconnect()`
- **Expected Result**: gRPC connection works correctly
- **Coverage**: `GrpcClient.connect()`, `GrpcClient.disconnect()`
- **Dependencies**: gRPC service endpoint

#### TC-INTEGRATION-GRPC-002: GrpcClient metadata management
- **Purpose**: Verify GrpcClient manages metadata correctly
- **Preconditions**: 
  - gRPC service endpoint available
- **Test Steps**:
  1. Create `GrpcClientImpl` with gRPC endpoint URL
  2. Set metadata: `client.set_metadata("authorization", "Bearer token123")`
  3. Set additional metadata: `client.set_metadata("x-custom-header", "value")`
  4. Connect to service
  5. Verify metadata is included in requests
  6. Clear metadata: `client.clear_metadata()`
  7. Verify metadata is cleared
- **Expected Result**: Metadata management works correctly
- **Coverage**: `GrpcClient.set_metadata()`, `GrpcClient.clear_metadata()`
- **Dependencies**: gRPC service endpoint

#### TC-INTEGRATION-GRPC-003: GrpcClient metadata merging
- **Purpose**: Verify GrpcClient merges default and call-specific metadata
- **Preconditions**: 
  - gRPC service endpoint available
- **Test Steps**:
  1. Create `GrpcClientImpl` with gRPC endpoint URL
  2. Set default metadata: `client.set_metadata("authorization", "Bearer default")`
  3. Connect to service
  4. Call method with call-specific metadata (when implemented)
  5. Verify merged metadata contains both default and call metadata
  6. Verify call metadata overrides default if key conflicts
- **Expected Result**: Metadata merging works correctly
- **Coverage**: `GrpcClient._merge_metadata()`
- **Dependencies**: gRPC service endpoint

### 2. GrpcClient Error Handling Integration

#### TC-INTEGRATION-GRPC-004: GrpcClient connection failure
- **Purpose**: Verify GrpcClient handles connection failures gracefully
- **Preconditions**: 
  - Invalid or unreachable gRPC endpoint
- **Test Steps**:
  1. Create `GrpcClientImpl` with invalid endpoint URL
  2. Attempt to connect: `await client.connect()`
  3. Verify `RuntimeError` is raised
  4. Verify error message indicates connection failure
- **Expected Result**: Connection failures are handled correctly
- **Coverage**: `GrpcClient.connect()` error handling
- **Dependencies**: Invalid gRPC endpoint

#### TC-INTEGRATION-GRPC-005: GrpcClient disconnect when not connected
- **Purpose**: Verify GrpcClient handles disconnect when not connected
- **Preconditions**: 
  - GrpcClient instance (not connected)
- **Test Steps**:
  1. Create `GrpcClientImpl` (do not connect)
  2. Call `await client.disconnect()`
  3. Verify no exceptions are raised
  4. Verify method is idempotent
- **Expected Result**: Disconnect when not connected is handled gracefully
- **Coverage**: `GrpcClient.disconnect()` idempotency
- **Dependencies**: GrpcClient instance

### 3. GrpcClient Context Manager Integration

#### TC-INTEGRATION-GRPC-006: GrpcClient context manager
- **Purpose**: Verify GrpcClient works as context manager
- **Preconditions**: 
  - gRPC service endpoint available
- **Test Steps**:
  1. Use `async with GrpcClientImpl(url, config) as client:`
  2. Verify connection is established on entry
  3. Perform operations within context (when methods are implemented)
  4. Exit context
  5. Verify connection is closed properly
- **Expected Result**: Context manager works correctly, resources cleaned up
- **Coverage**: `GrpcClient` context manager
- **Dependencies**: gRPC service endpoint

### 4. GrpcClient + ApiClient Integration

#### TC-INTEGRATION-GRPC-007: GrpcClient and ApiClient side by side
- **Purpose**: Verify GrpcClient and ApiClient can be used together
- **Preconditions**: 
  - Web application with both gRPC and REST endpoints
- **Test Steps**:
  1. Create `GrpcClientImpl` for gRPC endpoint
  2. Create `ApiClient` for REST endpoint
  3. Connect to gRPC service
  4. Execute REST API request
  5. Verify both work correctly
  6. Verify data consistency between gRPC and REST
- **Expected Result**: Both clients work correctly together
- **Coverage**: `GrpcClient` + `ApiClient` integration
- **Dependencies**: Web application with both API types

## Summary

- **Total test cases**: 7
- **Categories**: 4 (Basic integration, Error handling, Context manager, ApiClient integration)
- **Coverage**: Complete integration testing of `GrpcClient` with framework components
- **Note**: Some test cases require protobuf definitions and generated client code to be fully implemented

