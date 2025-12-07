# API Reference

Complete API documentation for the Web Automation Framework.

## Importing Classes

```python
# Configuration and Exceptions
from py_web_automation import Config
from py_web_automation.exceptions import (
    WebAutomationError,
    ConfigurationError,
    ConnectionError,
    OperationError,
    TimeoutError,
    AuthenticationError,
    NotFoundError,
)

# API Clients
from py_web_automation.clients.api_clients.http_client import HttpClient, HttpResult
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient, GraphQLResult
from py_web_automation.clients.api_clients.grpc_client import GrpcClient, GrpcResult
from py_web_automation.clients.api_clients.soap_client import SoapClient, SoapResult
from py_web_automation.clients.streaming_clients.websocket_client.websocket_client import (
    WebSocketClient,
)
from py_web_automation.clients.streaming_clients.websocket_client.websocket_result import (
    WebSocketResult,
)

# UI Clients
from py_web_automation.clients.ui_clients import AsyncUiClient, SyncUiClient

# Database Clients
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient
from py_web_automation.clients.db_clients.postgresql_client import PostgreSQLClient
from py_web_automation.clients.db_clients.mysql_client import MySQLClient
```

## Core Classes

### HttpClient

Class for testing HTTP REST API endpoints.

#### Constructor

```python
HttpClient(url: str, config: Config | None = None, middleware: MiddlewareChain | None = None)
```

**Parameters:**
- `url` (str): Base URL for API
- `config` (Config | None): Configuration object (default: Config())
- `middleware` (MiddlewareChain | None): Optional middleware chain

#### Methods

##### `make_request(endpoint: str, method: HTTPMethod = HTTPMethod.GET, data: dict[str, Any] | bytes | str | None = None, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> HttpResult`

Make HTTP request to API endpoint.

**Parameters:**
- `endpoint` (str): API endpoint path
- `method` (HTTPMethod): HTTP method (GET, POST, PUT, DELETE, etc.)
- `data` (dict[str, Any] | bytes | str | None): Request data (dict=JSON, bytes/str=raw)
- `params` (dict[str, Any] | None): Query parameters
- `headers` (dict[str, str] | None): Request headers

**Returns:** `HttpResult` object

**Example:**
```python
from py_web_automation.clients.api_clients.http_client import HttpClient

async with HttpClient("https://api.example.com", config) as api:
    result = await api.make_request("/api/status", method="GET")
    print(f"Status: {result.status_code}, Success: {result.success}")
    if result.body:
        print(f"Response: {result.json()}")
```

##### `build_request() -> RequestBuilder`

Create a request builder for fluent API.

**Returns:** `RequestBuilder` instance

**Example:**
```python
builder = api.build_request()
result = await builder.get("/users").params(page=1, limit=10).execute()
```

##### `close() -> None`

Close HTTP client and cleanup resources.

**Example:**
```python
await api.close()
```

### GraphQLClient

Class for testing GraphQL API endpoints.

#### Constructor

```python
GraphQLClient(url: str, config: Config | None = None, middleware: MiddlewareChain | None = None)
```

**Parameters:**
- `url` (str): GraphQL endpoint URL
- `config` (Config | None): Configuration object (default: Config())
- `middleware` (MiddlewareChain | None): Optional middleware chain

#### Methods

##### `query(query: str, variables: dict[str, Any] | None = None, operation_name: str | None = None, headers: dict[str, str] | None = None) -> GraphQLResult`

Execute GraphQL query.

**Parameters:**
- `query` (str): GraphQL query string
- `variables` (dict[str, Any] | None): Query variables
- `operation_name` (str | None): Operation name for multi-operation queries
- `headers` (dict[str, str] | None): Request headers

**Returns:** `GraphQLResult` object

**Example:**
```python
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient

async with GraphQLClient("https://api.example.com/graphql", config) as gql:
    query = """
    query GetUser($id: ID!) {
        user(id: $id) {
            id
            name
        }
    }
    """
    result = await gql.query(query, variables={"id": "123"})
    if result.success:
        print(result.data)
    else:
        print(result.errors)
```

##### `mutate(mutation: str, variables: dict[str, Any] | None = None, operation_name: str | None = None, headers: dict[str, str] | None = None) -> GraphQLResult`

Execute GraphQL mutation.

**Parameters:**
- `mutation` (str): GraphQL mutation string
- `variables` (dict[str, Any] | None): Mutation variables
- `operation_name` (str | None): Operation name for multi-operation queries
- `headers` (dict[str, str] | None): Request headers

**Returns:** `GraphQLResult` object

**Example:**
```python
mutation = """
mutation CreateUser($input: UserInput!) {
    createUser(input: $input) {
        id
        name
    }
}
"""
result = await gql.mutate(mutation, variables={"input": {"name": "John"}})
```

### GrpcClient

Class for testing gRPC services.

#### Constructor

```python
GrpcClient(url: str, config: Config | None = None, middleware: MiddlewareChain | None = None)
```

**Parameters:**
- `url` (str): gRPC server address (host:port format, e.g., "localhost:50051")
- `config` (Config | None): Configuration object (default: Config())
- `middleware` (MiddlewareChain | None): Optional middleware chain

#### Methods

##### `unary_call(service: str, method: str, request: Any, metadata: dict[str, str] | None = None) -> GrpcResult`

Call gRPC unary method (request-response).

**Parameters:**
- `service` (str): Service name
- `method` (str): Method name
- `request` (Any): Protobuf request message
- `metadata` (dict[str, str] | None): Optional metadata

**Returns:** `GrpcResult` object

**Example:**
```python
from py_web_automation.clients.api_clients.grpc_client import GrpcClient

async with GrpcClient("localhost:50051", config) as grpc:
    await grpc.connect()
    # result = await grpc.unary_call("UserService", "GetUser", request)
```

##### `connect() -> None`

Connect to gRPC server.

##### `disconnect() -> None`

Disconnect from gRPC server.

##### `set_metadata(key: str, value: str) -> None`

Set metadata for all subsequent calls.

### SoapClient

Class for testing SOAP web services.

#### Constructor

```python
SoapClient(url: str, config: Config | None = None, wsdl_url: str | None = None, soap_version: str = "1.1", middleware: MiddlewareChain | None = None)
```

**Parameters:**
- `url` (str): SOAP endpoint URL
- `config` (Config | None): Configuration object (default: Config())
- `wsdl_url` (str | None): WSDL URL (optional)
- `soap_version` (str): SOAP version ("1.1" or "1.2", default: "1.1")
- `middleware` (MiddlewareChain | None): Optional middleware chain

#### Methods

##### `call(operation: str, body: dict[str, Any] | None = None, namespace: str | None = None, headers: dict[str, str] | None = None) -> SoapResult`

Call SOAP operation.

**Parameters:**
- `operation` (str): SOAP operation name
- `body` (dict[str, Any] | None): Operation body data
- `namespace` (str | None): SOAP namespace (optional, ignored when using WSDL)
- `headers` (dict[str, str] | None): Custom request headers

**Returns:** `SoapResult` object

**Example:**
```python
from py_web_automation.clients.api_clients.soap_client import SoapClient

async with SoapClient(url, config, wsdl_url=wsdl_url) as soap:
    result = await soap.call("GetUser", body={"userId": "123"})
    if result.success:
        print(result.response)
```

### WebSocketClient

Class for testing WebSocket connections.

#### Constructor

```python
WebSocketClient(url: str, config: Config | None = None, middleware: MiddlewareChain | None = None)
```

**Parameters:**
- `url` (str): WebSocket URL (ws:// or wss://)
- `config` (Config | None): Configuration object (default: Config())
- `middleware` (MiddlewareChain | None): Optional middleware chain

#### Methods

##### `connect() -> WebSocketResult`

Connect to WebSocket server.

**Returns:** `WebSocketResult` object

##### `send_message(message: dict[str, Any] | str) -> WebSocketResult`

Send WebSocket message.

**Parameters:**
- `message` (dict[str, Any] | str): Message to send (dict=JSON, str=raw)

**Returns:** `WebSocketResult` object

**Example:**
```python
from py_web_automation.clients.streaming_clients.websocket_client.websocket_client import (
    WebSocketClient,
)

async with WebSocketClient("wss://api.example.com/ws", config) as ws:
    await ws.connect()
    result = await ws.send_message({"type": "ping", "data": "hello"})
    if result.success:
        print(f"Sent at {result.timestamp}")
```

##### `receive_message(timeout: float | None = None) -> WebSocketResult`

Receive WebSocket message.

**Parameters:**
- `timeout` (float | None): Optional timeout in seconds

**Returns:** `WebSocketResult` object

**Example:**
```python
result = await ws.receive_message(timeout=5.0)
if result.success:
    print(f"Received: {result.message} at {result.timestamp}")
```

##### `listen(handler: Callable | None = None) -> AsyncIterator[WebSocketResult]`

Async iterator for listening to messages.

**Parameters:**
- `handler` (Callable | None): Optional callback function

**Yields:** `WebSocketResult` objects

**Example:**
```python
async for result in ws.listen():
    if result.success:
        print(f"Message: {result.message}")
        if isinstance(result.message, dict) and result.message.get("type") == "close":
            break
```

##### `disconnect() -> None`

Disconnect from WebSocket server.

### AsyncUiClient

Asynchronous UI client for testing web application user interface using Playwright.

#### Constructor

```python
AsyncUiClient(url: str, config: Config | None = None)
```

**Parameters:**
- `url` (str): Base URL for application
- `config` (Config | None): Configuration object (default: Config())

#### Methods

##### `setup_browser() -> AsyncUiClient`

Setup Playwright browser for UI testing.

**Returns:** `Self` for method chaining

**Example:**
```python
from py_web_automation.clients.ui_clients import AsyncUiClient

async with AsyncUiClient("https://example.com", config) as ui:
    await ui.setup_browser()
    if ui.page:
        await ui.page.goto("https://example.com")
```

##### `click_element(selector: str) -> None`

Click element in web application.

**Parameters:**
- `selector` (str): CSS selector for element

**Example:**
```python
await ui.click_element("#submit-button")
```

##### `fill_input(selector: str, text: str) -> None`

Fill input field in web application.

**Parameters:**
- `selector` (str): CSS selector for input
- `text` (str): Text to fill

**Example:**
```python
await ui.fill_input("#username", "test_user")
```

##### `wait_for_element(selector: str, timeout: int = 5000) -> None`

Wait for element to appear.

**Parameters:**
- `selector` (str): CSS selector for element
- `timeout` (int): Timeout in milliseconds

##### `take_screenshot(path: str) -> None`

Take screenshot of the current page.

**Parameters:**
- `path` (str): Path to save screenshot

##### `get_element_text(selector: str) -> str | None`

Get text content of an element.

**Parameters:**
- `selector` (str): CSS selector for element

**Returns:** Element text or None

##### `execute_script(script: str) -> Any`

Execute JavaScript on the page.

**Parameters:**
- `script` (str): JavaScript code to execute

**Returns:** Script result

**Note:** Also available as `SyncUiClient` for synchronous usage.

### Database Clients

Database clients for testing applications with database backends.

#### SQLiteClient

```python
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient

db = SQLiteClient(connection_string="sqlite:///path/to/db.sqlite")
```

#### PostgreSQLClient

```python
from py_web_automation.clients.db_clients.postgresql_client import PostgreSQLClient

db = PostgreSQLClient(connection_string="postgresql://user:pass@localhost/db")
```

#### MySQLClient

```python
from py_web_automation.clients.db_clients.mysql_client import MySQLClient

db = MySQLClient(connection_string="mysql://user:pass@localhost/db")
```

#### Common Methods

All database clients share the same interface:

##### `connect() -> None`

Establish database connection.

##### `disconnect() -> None`

Close database connection.

##### `execute_query(query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]`

Execute SELECT query and return results.

**Parameters:**
- `query` (str): SQL query string
- `params` (dict[str, Any] | None): Query parameters

**Returns:** List of result rows as dictionaries

##### `execute_command(command: str, params: dict[str, Any] | None = None) -> None`

Execute INSERT/UPDATE/DELETE command.

**Parameters:**
- `command` (str): SQL command string
- `params` (dict[str, Any] | None): Command parameters

##### `transaction() -> AsyncContextManager`

Context manager for transactions.

**Example:**
```python
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient

async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
    async with db.transaction():
        await db.execute_command(
            "INSERT INTO users (name) VALUES (:name)",
            params={"name": "User 1"}
        )
        await db.execute_command(
            "INSERT INTO users (name) VALUES (:name)",
            params={"name": "User 2"}
        )
        # Transaction commits automatically on exit
```

##### `query() -> QueryBuilder`

Create a query builder for fluent SQL query construction.

**Example:**
```python
query, params = (db.query()
    .select("id", "name", "email")
    .from_table("users")
    .where("active", "=", True)
    ._build())
results = await db.execute_query(query, params)
```

### Config

Configuration class for the framework.

#### Constructor

```python
Config(
    base_url: Optional[str] = None,
    timeout: int = 30,
    retry_count: int = 3,
    retry_delay: float = 1.0,
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
    browser_headless: bool = True,
    browser_timeout: int = 30000
)
```

**Parameters:**
- `base_url` (Optional[str]): Base URL for application
- `timeout` (int): Request timeout in seconds (1-300)
- `retry_count` (int): Number of retry attempts (0-10)
- `retry_delay` (float): Delay between retries in seconds (0.1-10.0)
- `log_level` (str): Logging level
- `browser_headless` (bool): Run browser in headless mode
- `browser_timeout` (int): Browser operation timeout in milliseconds

#### Class Methods

##### `from_env() -> Config`

Create configuration from environment variables.

**Returns:** `Config` object

**Example:**
```python
config = Config.from_env()
```

##### `from_yaml(file_path: str) -> Config`

Create configuration from YAML file.

**Parameters:**
- `file_path` (str): Path to YAML file

**Returns:** `Config` object

## Data Models

### HttpResult

HTTP request result model.

```python
class HttpResult(msgspec.Struct, frozen=True):
    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    redirect: bool
    client_error: bool
    server_error: bool
    informational: bool
    headers: dict[str, str]
    body: bytes
    content_type: str | None
    reason: str | None
    error_message: str | None
    metadata: dict[str, Any]
    
    def json(self) -> dict[str, Any]:  # Parse JSON from body
```

### GraphQLResult

GraphQL operation result model.

```python
class GraphQLResult(msgspec.Struct, frozen=True):
    operation_name: str | None
    operation_type: str
    response_time: float
    success: bool
    data: dict[str, Any] | None
    errors: list[dict[str, Any]]
    headers: dict[str, str]
    metadata: dict[str, Any]
```

### SoapResult

SOAP operation result model.

```python
class SoapResult(msgspec.Struct, frozen=True):
    operation: str
    response_time: float
    success: bool
    status_code: int
    response: Any | None
    fault: dict[str, Any] | None
    headers: dict[str, str]
    metadata: dict[str, Any]
```

### GrpcResult

gRPC call result model.

```python
class GrpcResult(msgspec.Struct, frozen=True):
    service: str
    method: str
    response_time: float
    success: bool
    response: Any | None
    error: str | None
    status_code: int
    metadata: dict[str, Any]
```

### WebSocketResult

WebSocket message result model.

```python
class WebSocketResult(msgspec.Struct, frozen=True):
    direction: str  # "send" or "receive"
    message: dict[str, Any] | str
    timestamp: float
    success: bool
    error_message: str | None
```

## Context Managers

All classes support context managers for automatic resource cleanup:

```python
# HttpClient
from py_web_automation.clients.api_clients.http_client import HttpClient

async with HttpClient(url, config) as api:
    result = await api.make_request("/api/test", method="GET")

# AsyncUiClient
from py_web_automation.clients.ui_clients import AsyncUiClient

async with AsyncUiClient(url, config) as ui:
    await ui.setup_browser()
    await ui.click_element("#button")

# Database Client
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient

async with SQLiteClient(connection_string="sqlite:///db.sqlite") as db:
    results = await db.execute_query("SELECT * FROM users")
```

## Error Handling

All methods may raise exceptions. Always use try-catch blocks:

```python
from py_web_automation.exceptions import WebAutomationError, ConnectionError
from py_web_automation.clients.api_clients.http_client import HttpClient

try:
    async with HttpClient(url, config) as api:
        result = await api.make_request("/api/test", method="GET")
        if result.success:
            print("✅ Success")
        else:
            print(f"❌ Failed: {result.error_message}")
except ConnectionError as e:
    print(f"🔌 Connection error: {e}")
except WebAutomationError as e:
    print(f"⚠️ Framework error: {e}")
except Exception as e:
    print(f"💥 Exception: {e}")
```

## Async/Await

All framework methods are async and must be awaited:

```python
from py_web_automation.clients.api_clients.http_client import HttpClient

# ✅ Correct
async with HttpClient(url, config) as api:
    result = await api.make_request("/api/test", method="GET")

# ❌ Incorrect
result = api.make_request("/api/test", method="GET")  # Returns coroutine, not result
```

## Type Hints

The framework uses type hints for better IDE support and code clarity:

```python
from py_web_automation.clients.api_clients.http_client import HttpClient, HttpResult

async def test_api(api: HttpClient) -> HttpResult | None:
    try:
        return await api.make_request("/api/test", method="GET")
    except Exception:
        return None
```
