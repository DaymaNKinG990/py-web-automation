# API Reference

Complete API documentation for the Web Automation Framework.

## Importing Classes

```python
# Main imports
from py_web_automation import (
    ApiClient,
    GraphQLClient,
    GrpcClient,
    SoapClient,
    WebSocketClient,
    UiClient,
    DBClient,
    Config,
    ApiResult,
)

# Exceptions
from py_web_automation.exceptions import (
    WebAutomationError,
    ConfigurationError,
    ConnectionError,
    ValidationError,
    OperationError,
    TimeoutError,
    AuthenticationError,
    NotFoundError,
)

# Validators
from py_web_automation.validators import (
    validate_response,
    validate_json_response,
    validate_api_result,
    create_schema_from_dict,
)
```

## Core Classes

### ApiClient

Class for testing HTTP REST API endpoints.

#### Constructor

```python
ApiClient(url: str, config: Optional[Config] = None)
```

**Parameters:**
- `url` (str): Base URL for API
- `config` (Optional[Config]): Configuration object

#### Methods

##### `make_request(endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> ApiResult`

Make HTTP request to API endpoint.

**Parameters:**
- `endpoint` (str): API endpoint path
- `method` (str): HTTP method (GET, POST, PUT, DELETE, etc.)
- `data` (Optional[Dict[str, Any]]): Request data
- `params` (Optional[Dict[str, Any]]): Query parameters
- `headers` (Optional[Dict[str, str]]): Request headers

**Returns:** `ApiResult` object

**Example:**
```python
result = await api.make_request("/api/status", method="GET")
print(f"Status: {result.status_code}, Success: {result.success}")
```

##### `build_request() -> RequestBuilder`

Create a request builder for fluent API.

**Returns:** `RequestBuilder` instance

**Example:**
```python
result = await (api.build_request()
    .get("/users")
    .params(page=1, limit=10)
    .execute())
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
GraphQLClient(url: str, config: Optional[Config] = None)
```

**Parameters:**
- `url` (str): GraphQL endpoint URL
- `config` (Optional[Config]): Configuration object

#### Methods

##### `execute_query(query: str, variables: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> ApiResult`

Execute GraphQL query.

**Parameters:**
- `query` (str): GraphQL query string
- `variables` (Optional[Dict[str, Any]]): Query variables
- `headers` (Optional[Dict[str, str]]): Request headers

**Returns:** `ApiResult` object

**Example:**
```python
query = """
query GetUser($id: ID!) {
    user(id: $id) {
        id
        name
    }
}
"""
result = await client.execute_query(query, variables={"id": "123"})
```

##### `execute_mutation(mutation: str, variables: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> ApiResult`

Execute GraphQL mutation.

**Parameters:**
- `mutation` (str): GraphQL mutation string
- `variables` (Optional[Dict[str, Any]]): Mutation variables
- `headers` (Optional[Dict[str, str]]): Request headers

**Returns:** `ApiResult` object

### GrpcClient

Class for testing gRPC services.

#### Constructor

```python
GrpcClient(url: str, config: Optional[Config] = None)
```

**Parameters:**
- `url` (str): gRPC server URL
- `config` (Optional[Config]): Configuration object

#### Methods

##### `call_method(service: str, method: str, request_data: Dict[str, Any]) -> ApiResult`

Call gRPC method.

**Parameters:**
- `service` (str): Service name
- `method` (str): Method name
- `request_data` (Dict[str, Any]): Request data

**Returns:** `ApiResult` object

### SoapClient

Class for testing SOAP web services.

#### Constructor

```python
SoapClient(url: str, config: Optional[Config] = None)
```

**Parameters:**
- `url` (str): SOAP endpoint URL
- `config` (Optional[Config]): Configuration object

#### Methods

##### `call_method(method: str, params: Dict[str, Any]) -> ApiResult`

Call SOAP method.

**Parameters:**
- `method` (str): SOAP method name
- `params` (Dict[str, Any]): Method parameters

**Returns:** `ApiResult` object

### WebSocketClient

Class for testing WebSocket connections.

#### Constructor

```python
WebSocketClient(url: str, config: Optional[Config] = None)
```

**Parameters:**
- `url` (str): WebSocket URL (ws:// or wss://)
- `config` (Optional[Config]): Configuration object

#### Methods

##### `send_message(message: Dict[str, Any]) -> None`

Send WebSocket message.

**Parameters:**
- `message` (Dict[str, Any]): Message to send

**Example:**
```python
await ws.send_message({"type": "ping", "data": "hello"})
```

##### `receive_message() -> Dict[str, Any]`

Receive WebSocket message.

**Returns:** Received message dictionary

**Example:**
```python
message = await ws.receive_message()
print(f"Received: {message}")
```

##### `listen() -> AsyncIterator[Dict[str, Any]]`

Async iterator for listening to messages.

**Example:**
```python
async for msg in ws.listen():
    print(f"Message: {msg}")
    if msg.get("type") == "close":
        break
```

### UiClient

Class for testing web application user interface using Playwright.

#### Constructor

```python
UiClient(url: str, config: Optional[Config] = None)
```

**Parameters:**
- `url` (str): Base URL for application
- `config` (Optional[Config]): Configuration object

#### Methods

##### `setup_browser() -> Self`

Setup Playwright browser for UI testing.

**Returns:** `Self` for method chaining

**Example:**
```python
await ui.setup_browser()
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

##### `get_element_text(selector: str) -> Optional[str]`

Get text content of an element.

**Parameters:**
- `selector` (str): CSS selector for element

**Returns:** Element text or None

##### `execute_script(script: str) -> Any`

Execute JavaScript on the page.

**Parameters:**
- `script` (str): JavaScript code to execute

**Returns:** Script result

### DBClient

Database client for testing applications with database backends.

#### Factory Method

```python
DBClient.create(
    url: str,
    config: Config,
    db_type: str,
    connection_string: Optional[str] = None,
    **kwargs: Any
) -> DBClient
```

**Parameters:**
- `url` (str): Base URL (for BaseClient compatibility)
- `config` (Config): Configuration object
- `db_type` (str): Database type ("postgresql", "sqlite", "mysql")
- `connection_string` (Optional[str]): Database connection string
- `**kwargs`: Additional database-specific parameters

**Returns:** Database client instance

**Example:**
```python
# PostgreSQL
db = await DBClient.create(
    "https://example.com/app",
    config,
    db_type="postgresql",
    connection_string="postgresql://user:pass@localhost/db"
)

# SQLite
db = await DBClient.create(
    "https://example.com/app",
    config,
    db_type="sqlite",
    connection_string="sqlite:///:memory:"
)
```

#### Methods

##### `connect() -> None`

Establish database connection.

##### `disconnect() -> None`

Close database connection.

##### `execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]`

Execute SELECT query and return results.

**Parameters:**
- `query` (str): SQL query string
- `params` (Optional[Dict[str, Any]]): Query parameters

**Returns:** List of result rows as dictionaries

##### `execute_command(command: str, params: Optional[Dict[str, Any]] = None) -> int`

Execute INSERT/UPDATE/DELETE command.

**Parameters:**
- `command` (str): SQL command string
- `params` (Optional[Dict[str, Any]]): Command parameters

**Returns:** Number of affected rows

##### `transaction() -> AsyncContextManager`

Context manager for transactions.

**Example:**
```python
async with db.transaction():
    await db.execute_command("INSERT INTO users (name) VALUES (:name)", {"name": "User 1"})
    await db.execute_command("INSERT INTO users (name) VALUES (:name)", {"name": "User 2"})
    # Transaction commits automatically on exit
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

### ApiResult

API request result model.

```python
class ApiResult(msgspec.Struct):
    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    redirect: bool
    client_error: bool
    server_error: bool
    informational: bool
    response: Optional[Response] = None
    error_message: Optional[str] = None
```

## Context Managers

All classes support context managers for automatic resource cleanup:

```python
# ApiClient
async with ApiClient(url, config) as api:
    result = await api.make_request("/api/test", method="GET")

# UiClient
async with UiClient(url, config) as ui:
    await ui.setup_browser()
    await ui.click_element("#button")

# DBClient
async with db:
    results = await db.execute_query("SELECT * FROM users")
```

## Error Handling

All methods may raise exceptions. Always use try-catch blocks:

```python
from py_web_automation.exceptions import WebAutomationError, ConnectionError

try:
    async with ApiClient(url, config) as api:
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
# ✅ Correct
result = await api.make_request("/api/test", method="GET")

# ❌ Incorrect
result = api.make_request("/api/test", method="GET")  # Returns coroutine, not result
```

## Type Hints

The framework uses type hints for better IDE support and code clarity:

```python
from typing import Optional
from py_web_automation import ApiClient, ApiResult

async def test_api(api: ApiClient) -> Optional[ApiResult]:
    try:
        return await api.make_request("/api/test", method="GET")
    except Exception:
        return None
```
