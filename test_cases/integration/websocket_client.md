# WebSocket Client Integration Test Cases

## Overview
Tests for integration between `WebSocketClient` and other framework components, and real WebSocket endpoints.

## Test Categories

### 1. WebSocketClient Basic Integration

#### TC-INTEGRATION-WS-001: WebSocketClient connection and messaging
- **Purpose**: Verify WebSocketClient connects and exchanges messages successfully
- **Preconditions**: 
  - WebSocket endpoint available (ws:// or wss://)
- **Test Steps**:
  1. Create `WebSocketClient` with WebSocket URL
  2. Connect using `await ws.connect()`
  3. Verify `is_connected()` returns True
  4. Send message using `await ws.send_message({"type": "ping"})`
  5. Receive message using `await ws.receive_message()`
  6. Verify message is received correctly
  7. Disconnect using `await ws.disconnect()`
- **Expected Result**: WebSocket connection and messaging works correctly
- **Coverage**: `WebSocketClient.connect()`, `WebSocketClient.send_message()`, `WebSocketClient.receive_message()`, `WebSocketClient.disconnect()`
- **Dependencies**: WebSocket endpoint

#### TC-INTEGRATION-WS-002: WebSocketClient secure connection (wss://)
- **Purpose**: Verify WebSocketClient connects to secure WebSocket endpoint
- **Preconditions**: 
  - Secure WebSocket endpoint available (wss://)
- **Test Steps**:
  1. Create `WebSocketClient` with wss:// URL
  2. Connect using `await ws.connect()`
  3. Verify connection is established
  4. Send and receive messages
  5. Verify SSL/TLS is used
- **Expected Result**: Secure WebSocket connection works correctly
- **Coverage**: `WebSocketClient` with wss://
- **Dependencies**: Secure WebSocket endpoint

#### TC-INTEGRATION-WS-003: WebSocketClient message handlers
- **Purpose**: Verify WebSocketClient message handlers work correctly
- **Preconditions**: 
  - WebSocket endpoint available
- **Test Steps**:
  1. Create `WebSocketClient` and connect
  2. Register message handler: `ws.register_handler("ping", handler_function)`
  3. Send message that triggers handler
  4. Verify handler is called with correct message
  5. Verify handler processes message correctly
- **Expected Result**: Message handlers work correctly
- **Coverage**: `WebSocketClient.register_handler()`
- **Dependencies**: WebSocket endpoint

#### TC-INTEGRATION-WS-004: WebSocketClient listen iterator
- **Purpose**: Verify WebSocketClient listen method as async iterator
- **Preconditions**: 
  - WebSocket endpoint available
- **Test Steps**:
  1. Create `WebSocketClient` and connect
  2. Use `listen()` as async iterator: `async for message in ws.listen():`
  3. Send multiple messages from server
  4. Verify messages are yielded correctly
  5. Verify iterator stops when connection closes
- **Expected Result**: Listen iterator works correctly
- **Coverage**: `WebSocketClient.listen()` as async iterator
- **Dependencies**: WebSocket endpoint

### 2. WebSocketClient + ApiClient Integration

#### TC-INTEGRATION-WS-005: WebSocketClient and ApiClient integration
- **Purpose**: Verify WebSocketClient and ApiClient work together
- **Preconditions**: 
  - Web application with WebSocket and REST endpoints
- **Test Steps**:
  1. Create `WebSocketClient` and connect
  2. Create `ApiClient` for REST endpoint
  3. Trigger event via REST API using `ApiClient.make_request()`
  4. Listen for WebSocket message
  5. Verify WebSocket receives notification
  6. Verify data consistency
- **Expected Result**: WebSocket and REST API integration works correctly
- **Coverage**: `WebSocketClient` + `ApiClient` integration
- **Dependencies**: Web application with WebSocket and REST

#### TC-INTEGRATION-WS-006: WebSocketClient real-time updates workflow
- **Purpose**: Verify complete real-time updates workflow
- **Preconditions**: 
  - Web application with WebSocket for real-time updates
  - REST API for triggering updates
- **Test Steps**:
  1. Create `WebSocketClient` and connect
  2. Start listening for messages
  3. Create `ApiClient` and trigger update via REST API
  4. Verify WebSocket receives real-time update
  5. Verify update data is correct
  6. Process update in handler
- **Expected Result**: Real-time updates workflow works correctly
- **Coverage**: `WebSocketClient` + `ApiClient` real-time integration
- **Dependencies**: Web application with real-time features

### 3. WebSocketClient Error Handling Integration

#### TC-INTEGRATION-WS-007: WebSocketClient connection timeout
- **Purpose**: Verify WebSocketClient handles connection timeout correctly
- **Preconditions**: 
  - WebSocket endpoint that times out
- **Test Steps**:
  1. Create `WebSocketClient` with short timeout
  2. Attempt to connect to slow/unreachable endpoint
  3. Verify `TimeoutError` is raised
  4. Verify error message indicates timeout
- **Expected Result**: Connection timeout is handled correctly
- **Coverage**: `WebSocketClient.connect()` timeout handling
- **Dependencies**: Slow/unreachable WebSocket endpoint

#### TC-INTEGRATION-WS-008: WebSocketClient receive timeout
- **Purpose**: Verify WebSocketClient handles receive timeout correctly
- **Preconditions**: 
  - WebSocket endpoint available
- **Test Steps**:
  1. Create `WebSocketClient` and connect
  2. Call `receive_message(timeout=1.0)` when no message arrives
  3. Verify `TimeoutError` is raised
  4. Verify error message indicates timeout
- **Expected Result**: Receive timeout is handled correctly
- **Coverage**: `WebSocketClient.receive_message()` timeout handling
- **Dependencies**: WebSocket endpoint

#### TC-INTEGRATION-WS-009: WebSocketClient connection error recovery
- **Purpose**: Verify WebSocketClient recovers from connection errors
- **Preconditions**: 
  - WebSocket endpoint that can be interrupted
- **Test Steps**:
  1. Create `WebSocketClient` and connect
  2. Simulate connection interruption
  3. Verify error is detected
  4. Reconnect using `connect()`
  5. Verify connection is re-established
  6. Verify messaging works after reconnection
- **Expected Result**: Connection error recovery works correctly
- **Coverage**: `WebSocketClient` error recovery
- **Dependencies**: WebSocket endpoint with interruption

### 4. WebSocketClient + UiClient Integration

#### TC-INTEGRATION-WS-010: WebSocketClient and UiClient integration
- **Purpose**: Verify WebSocketClient and UiClient work together
- **Preconditions**: 
  - Web application with WebSocket and UI
- **Test Steps**:
  1. Create `WebSocketClient` and connect
  2. Create `UiClient` and setup browser
  3. Navigate to application UI
  4. Trigger UI action that sends WebSocket message
  5. Verify WebSocket receives message
  6. Verify UI updates based on WebSocket response
- **Expected Result**: WebSocket and UI integration works correctly
- **Coverage**: `WebSocketClient` + `UiClient` integration
- **Dependencies**: Web application with WebSocket and UI

### 5. WebSocketClient Context Manager Integration

#### TC-INTEGRATION-WS-011: WebSocketClient context manager
- **Purpose**: Verify WebSocketClient works as context manager
- **Preconditions**: 
  - WebSocket endpoint available
- **Test Steps**:
  1. Use `async with WebSocketClient(url, config) as ws:`
  2. Verify connection is established on entry
  3. Send and receive messages within context
  4. Exit context
  5. Verify connection is closed properly
- **Expected Result**: Context manager works correctly, resources cleaned up
- **Coverage**: `WebSocketClient` context manager
- **Dependencies**: WebSocket endpoint

#### TC-INTEGRATION-WS-012: WebSocketClient multiple message types
- **Purpose**: Verify WebSocketClient handles different message types
- **Preconditions**: 
  - WebSocket endpoint available
- **Test Steps**:
  1. Create `WebSocketClient` and connect
  2. Send JSON message: `await ws.send_message({"type": "ping"})`
  3. Send string message: `await ws.send_message('{"type": "pong"}')`
  4. Receive and verify both message types are handled correctly
- **Expected Result**: Different message types are handled correctly
- **Coverage**: `WebSocketClient.send_message()` with different types
- **Dependencies**: WebSocket endpoint

## Summary

- **Total test cases**: 12
- **Categories**: 5 (Basic integration, ApiClient integration, Error handling, UiClient integration, Context manager)
- **Coverage**: Complete integration testing of `WebSocketClient` with framework components

