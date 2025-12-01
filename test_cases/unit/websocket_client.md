# Unit Test Cases: WebSocket Client

## Overview

Test cases for WebSocketClient class.

## Test Cases

### TC-UNIT-WS-001: WebSocketClient initialization with valid URL

**Description**: Test WebSocketClient initialization with valid WebSocket URL.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Create WebSocketClient with "ws://example.com/ws"
2. Verify client is initialized correctly
3. Verify _websocket is None
4. Verify _is_connected is False
5. Verify _message_handlers is empty dict

**Expected Result**:
- WebSocketClient is created successfully
- All initial values are set correctly
- No exceptions raised

**Test Data**:
```python
config = Config(timeout=30)
ws = WebSocketClient("ws://example.com/ws", config)
```

---

### TC-UNIT-WS-002: WebSocketClient initialization with wss URL

**Description**: Test WebSocketClient initialization with secure WebSocket URL.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Create WebSocketClient with "wss://example.com/ws"
2. Verify client is initialized correctly
3. Verify no exceptions are raised

**Expected Result**:
- WebSocketClient is created successfully
- Secure WebSocket URL is accepted

**Test Data**:
```python
config = Config(timeout=30)
ws = WebSocketClient("wss://example.com/ws", config)
```

---

### TC-UNIT-WS-003: WebSocketClient initialization with invalid URL

**Description**: Test WebSocketClient initialization fails with non-WebSocket URL.

**Preconditions**:
- Config instance available

**Test Steps**:
1. Attempt to create WebSocketClient with "http://example.com"
2. Verify ValueError is raised
3. Verify error message indicates invalid WebSocket URL

**Expected Result**:
- ValueError is raised
- Error message mentions WebSocket URL requirement

**Test Data**:
```python
config = Config(timeout=30)
# Should raise ValueError
ws = WebSocketClient("http://example.com", config)
```

---

### TC-UNIT-WS-004: WebSocketClient is_connected when not connected

**Description**: Test is_connected returns False when not connected.

**Preconditions**:
- WebSocketClient instance (not connected)

**Test Steps**:
1. Create WebSocketClient
2. Call `await ws.is_connected()`
3. Verify returns False

**Expected Result**:
- Method returns False
- No exceptions raised

**Test Data**:
```python
ws = WebSocketClient("ws://example.com/ws", config)
connected = await ws.is_connected()  # Should be False
```

---

### TC-UNIT-WS-005: WebSocketClient send_message when not connected

**Description**: Test send_message raises ConnectionError when not connected.

**Preconditions**:
- WebSocketClient instance (not connected)

**Test Steps**:
1. Create WebSocketClient (do not connect)
2. Call `await ws.send_message({"type": "ping"})`
3. Verify ConnectionError is raised
4. Verify error message indicates not connected

**Expected Result**:
- ConnectionError is raised
- Error message mentions connection requirement

**Test Data**:
```python
ws = WebSocketClient("ws://example.com/ws", config)
# Should raise ConnectionError
await ws.send_message({"type": "ping"})
```

---

### TC-UNIT-WS-006: WebSocketClient send_message with dict

**Description**: Test sending dictionary message.

**Preconditions**:
- WebSocketClient instance (connected)
- Mocked WebSocket connection

**Test Steps**:
1. Connect WebSocketClient (mocked)
2. Call `await ws.send_message({"type": "ping", "data": "test"})`
3. Verify message is JSON encoded
4. Verify WebSocket send is called with JSON string

**Expected Result**:
- Message is sent successfully
- Message is JSON encoded
- No exceptions raised

**Test Data**:
```python
await ws.connect()  # Mocked
await ws.send_message({"type": "ping", "data": "test"})
```

---

### TC-UNIT-WS-007: WebSocketClient send_message with string

**Description**: Test sending string message.

**Preconditions**:
- WebSocketClient instance (connected)
- Mocked WebSocket connection

**Test Steps**:
1. Connect WebSocketClient (mocked)
2. Call `await ws.send_message('{"type": "ping"}')`
3. Verify message is sent as-is (not JSON encoded)
4. Verify WebSocket send is called with string

**Expected Result**:
- Message is sent successfully
- Message is sent as string
- No exceptions raised

**Test Data**:
```python
await ws.connect()  # Mocked
await ws.send_message('{"type": "ping"}')
```

---

### TC-UNIT-WS-008: WebSocketClient receive_message when not connected

**Description**: Test receive_message raises ConnectionError when not connected.

**Preconditions**:
- WebSocketClient instance (not connected)

**Test Steps**:
1. Create WebSocketClient (do not connect)
2. Call `await ws.receive_message()`
3. Verify ConnectionError is raised
4. Verify error message indicates not connected

**Expected Result**:
- ConnectionError is raised
- Error message mentions connection requirement

**Test Data**:
```python
ws = WebSocketClient("ws://example.com/ws", config)
# Should raise ConnectionError
await ws.receive_message()
```

---

### TC-UNIT-WS-009: WebSocketClient receive_message with JSON

**Description**: Test receiving JSON message.

**Preconditions**:
- WebSocketClient instance (connected)
- Mocked WebSocket connection returning JSON

**Test Steps**:
1. Connect WebSocketClient (mocked)
2. Mock WebSocket to return JSON string
3. Call `await ws.receive_message()`
4. Verify message is parsed as JSON
5. Verify returns dict

**Expected Result**:
- Message is received successfully
- Message is parsed as JSON
- Returns dict object

**Test Data**:
```python
await ws.connect()  # Mocked
# Mock returns: '{"type": "pong", "data": "response"}'
message = await ws.receive_message()  # Should be dict
```

---

### TC-UNIT-WS-010: WebSocketClient receive_message with text

**Description**: Test receiving text message.

**Preconditions**:
- WebSocketClient instance (connected)
- Mocked WebSocket connection returning text

**Test Steps**:
1. Connect WebSocketClient (mocked)
2. Mock WebSocket to return plain text string
3. Call `await ws.receive_message()`
4. Verify message is returned as string (not parsed as JSON)
5. Verify returns string

**Expected Result**:
- Message is received successfully
- Message is returned as string
- No JSON parsing attempted

**Test Data**:
```python
await ws.connect()  # Mocked
# Mock returns: "Plain text message"
message = await ws.receive_message()  # Should be string
```

---

### TC-UNIT-WS-011: WebSocketClient receive_message timeout

**Description**: Test receive_message raises TimeoutError on timeout.

**Preconditions**:
- WebSocketClient instance (connected)
- Mocked WebSocket connection that times out

**Test Steps**:
1. Connect WebSocketClient (mocked)
2. Mock WebSocket to timeout
3. Call `await ws.receive_message(timeout=1.0)`
4. Verify TimeoutError is raised
5. Verify error message mentions timeout

**Expected Result**:
- TimeoutError is raised
- Error message mentions timeout duration

**Test Data**:
```python
await ws.connect()  # Mocked
# Mock times out
# Should raise TimeoutError
await ws.receive_message(timeout=1.0)
```

---

### TC-UNIT-WS-012: WebSocketClient register_handler

**Description**: Test registering message handler.

**Preconditions**:
- WebSocketClient instance

**Test Steps**:
1. Create handler function
2. Call `ws.register_handler("ping", handler)`
3. Verify handler is stored in _message_handlers
4. Verify handler is associated with "ping" type

**Expected Result**:
- Handler is registered successfully
- Handler is stored correctly
- No exceptions raised

**Test Data**:
```python
def handle_ping(message):
    print(f"Received ping: {message}")

ws.register_handler("ping", handle_ping)
```

---

### TC-UNIT-WS-013: WebSocketClient disconnect

**Description**: Test disconnecting WebSocket.

**Preconditions**:
- WebSocketClient instance (connected)
- Mocked WebSocket connection

**Test Steps**:
1. Connect WebSocketClient (mocked)
2. Call `await ws.disconnect()`
3. Verify _websocket is set to None
4. Verify _is_connected is False
5. Verify WebSocket close is called

**Expected Result**:
- Connection is closed successfully
- State is reset correctly
- No exceptions raised

**Test Data**:
```python
await ws.connect()  # Mocked
await ws.disconnect()
```

---

### TC-UNIT-WS-014: WebSocketClient context manager

**Description**: Test WebSocketClient as async context manager.

**Preconditions**:
- Config instance available
- Mocked WebSocket connection

**Test Steps**:
1. Use WebSocketClient in async with statement
2. Verify connect() is called on entry
3. Verify disconnect() is called on exit
4. Verify connection is established
5. Verify connection is closed on exit

**Expected Result**:
- Context manager works correctly
- Connection is established on entry
- Connection is closed on exit

**Test Data**:
```python
async with WebSocketClient("ws://example.com/ws", config) as ws:
    # Connection should be established
    await ws.send_message({"type": "ping"})
# Connection should be closed
```

---

### TC-UNIT-WS-015: WebSocketClient listen iterator

**Description**: Test listen method as async iterator.

**Preconditions**:
- WebSocketClient instance (connected)
- Mocked WebSocket connection

**Test Steps**:
1. Connect WebSocketClient (mocked)
2. Mock WebSocket to return multiple messages
3. Use listen() as async iterator
4. Verify messages are yielded correctly
5. Verify iterator stops when connection closes

**Expected Result**:
- Iterator yields messages correctly
- Iterator stops appropriately
- No exceptions raised

**Test Data**:
```python
await ws.connect()  # Mocked
async for message in ws.listen():
    print(f"Received: {message}")
    if message.get("type") == "close":
        break
```

---

### TC-UNIT-WS-016: WebSocketClient listen with handler

**Description**: Test listen method with handler callback.

**Preconditions**:
- WebSocketClient instance (connected)
- Mocked WebSocket connection

**Test Steps**:
1. Connect WebSocketClient (mocked)
2. Create handler function
3. Call listen() with handler
4. Verify handler is called for each message
5. Verify messages are still yielded

**Expected Result**:
- Handler is called for each message
- Messages are yielded correctly
- No exceptions raised

**Test Data**:
```python
def handler(message):
    print(f"Handler: {message}")

await ws.connect()  # Mocked
async for message in ws.listen(handler=handler):
    pass
```

---

### TC-UNIT-WS-017: WebSocketClient close method

**Description**: Test close method cleanup.

**Preconditions**:
- WebSocketClient instance (connected)
- Mocked WebSocket connection

**Test Steps**:
1. Connect WebSocketClient (mocked)
2. Register message handlers
3. Call `await ws.close()`
4. Verify disconnect() is called
5. Verify _message_handlers is cleared

**Expected Result**:
- Connection is closed
- Handlers are cleared
- State is reset

**Test Data**:
```python
await ws.connect()  # Mocked
ws.register_handler("ping", handler)
await ws.close()
```

