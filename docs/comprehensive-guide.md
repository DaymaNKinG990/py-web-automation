# Comprehensive Guide to py-web-automation

Complete guide to using all features of the py-web-automation framework.

## Table of Contents

1. [Introduction](#introduction)
2. [Basic Concepts](#basic-concepts)
3. [Clients](#clients)
4. [Advanced Features](#advanced-features)
5. [Patterns and Practices](#patterns-and-practices)
6. [Usage Examples](#usage-examples)

---

## Introduction

`py-web-automation` is a comprehensive framework for automated testing of web applications, supporting multiple protocols and testing patterns.

### Key Features

- **Multiple Protocols**: REST, GraphQL, gRPC, SOAP, WebSocket
- **UI Testing**: Playwright-based browser automation
- **Databases**: PostgreSQL, MySQL, SQLite
- **Extensibility**: Middleware, plugins, interceptors
- **Reliability**: Retry, circuit breaker, rate limiting
- **Performance**: Caching, metrics, optimization

---

## Basic Concepts

### Config - Configuration

All clients use a unified configuration system through the `Config` class.

```python
from py_web_automation import Config

# Create configuration
config = Config(
    timeout=30,           # Request timeout in seconds
    retry_count=3,        # Number of retry attempts
    retry_delay=1.0,      # Delay between attempts
    log_level="INFO",     # Logging level
    browser_headless=True, # Browser mode
    browser_timeout=30000  # Browser timeout in milliseconds
)

# From environment variables
config = Config.from_env()

# From YAML file
config = Config.from_yaml("config.yaml")
```

### Client Structure

All clients follow a consistent structure:
- Configuration through `Config` object
- Context managers for automatic resource cleanup
- Async/await support for all operations

Each client is independent and can be used separately based on your testing needs.

---

## Clients

### HttpClient - REST API Client

Main client for testing HTTP REST APIs.

#### Basic Usage

```python
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

async def basic_api_test():
    config = Config(timeout=30)
    async with HttpClient("https://api.example.com", config) as api:
        # Simple GET request
        result = await api.make_request("/users/1", method="GET")
        print(f"Status: {result.status_code}")
        print(f"Data: {result.json()}")
        
        # POST request with data
        result = await api.make_request(
            "/users",
            method="POST",
            data={"name": "John", "email": "john@example.com"}
        )
```

#### Authentication

```python
from py_web_automation.clients.api_clients.http_client.middleware import (
    AuthMiddleware,
    MiddlewareChain,
)

# Setup authentication middleware
auth_middleware = AuthMiddleware(token="your-token-here", token_type="Bearer")
chain = MiddlewareChain()
chain.add(auth_middleware)

async with HttpClient("https://api.example.com", config, middleware=chain) as api:
    # All requests automatically include token
    result = await api.make_request("/protected", method="GET")
    
    # Clear token
    auth_middleware.clear_token()
```

#### Request Builder - Fluent API

```python
# Building complex requests
builder = api.build_request()
result = await (builder
    .get("/users")
    .params(page=1, limit=10, sort="name")
    .header("X-Custom-Header", "value")
    .execute())

# POST with body
result = await (builder
    .post("/users")
    .body({"name": "Jane", "email": "jane@example.com"})
    .execute())
```

#### Advanced Features

```python
from py_web_automation.clients.api_clients.http_client.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    MiddlewareChain,
    RateLimitMiddleware,
)
from py_web_automation.clients.api_clients.http_client.rate_limit import RateLimiter

# With middleware
chain = MiddlewareChain()
chain.add(LoggingMiddleware())
chain.add(MetricsMiddleware(metrics))

# With rate limiting
rate_limiter = RateLimiter(max_requests=100, window=60)
chain.add(RateLimitMiddleware(rate_limiter))

# Create client with middleware
api = HttpClient(
    "https://api.example.com",
    config,
    middleware=chain
)
```

### GraphQLClient - GraphQL Client

Client for working with GraphQL APIs.

```python
from py_web_automation import Config
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient

async def graphql_test():
    config = Config(timeout=30)
    async with GraphQLClient("https://api.example.com/graphql", config) as client:
        # Query
        result = await client.query(
            """
            query GetUser($id: ID!) {
                user(id: $id) {
                    id
                    name
                    email
                }
            }
            """,
            variables={"id": "1"}
        )
        
        # Mutation
        result = await client.mutate(
            """
            mutation CreateUser($input: UserInput!) {
                createUser(input: $input) {
                    id
                    name
                }
            }
            """,
            variables={"input": {"name": "John", "email": "john@example.com"}}
        )
```

### SoapClient - SOAP Client

Client for working with SOAP web services.

```python
from py_web_automation import Config
from py_web_automation.clients.api_clients.soap_client import SoapClient

async def soap_test():
    config = Config(timeout=30)
    async with SoapClient(
        "https://api.example.com/soap", 
        config,
        wsdl_url="https://api.example.com/soap?WSDL"
    ) as client:
        # SOAP call
        result = await client.call(
            operation="GetUser",
            body={"id": 1}
        )
```

### WebSocketClient - WebSocket Client

Client for working with WebSocket connections.

```python
from py_web_automation import Config
from py_web_automation.clients.streaming_clients.websocket_client.websocket_client import (
    WebSocketClient,
)

async def websocket_test():
    config = Config(timeout=30)
    async with WebSocketClient("wss://api.example.com/ws", config) as client:
        # Connect
        await client.connect()
        
        # Send message
        result = await client.send_message({"type": "subscribe", "channel": "updates"})
        
        # Receive message
        result = await client.receive_message(timeout=5.0)
        if result.success:
            print(f"Received: {result.message}")
        
        # Listen to messages
        async for result in client.listen():
            if result.success:
                print(f"Message: {result.message}")
                if isinstance(result.message, dict) and result.message.get("type") == "done":
                    break
        
        # Register handler
        def handle_message(msg):
            print(f"Handler received: {msg}")
        
        client.register_handler("message", handle_message)
```

### AsyncUiClient - UI Client

Client for browser automation with Playwright.

#### Basic Usage

```python
from py_web_automation import Config
from py_web_automation.clients.ui_clients import AsyncUiClient

async def ui_test():
    config = Config(timeout=30, browser_headless=True)
    async with AsyncUiClient("https://example.com", config) as ui:
        # Setup browser
        await ui.setup_browser()
        
        # Navigate
        if ui.page:
            await ui.page.goto("https://example.com")
        
        # Interact with elements
        await ui.fill_input("#username", "testuser")
        await ui.fill_input("#password", "password123")
        await ui.click_element("#login-button")
        
        # Wait for element
        await ui.wait_for_element("#dashboard", timeout=5000)
        
        # Get data
        title = await ui.get_page_title()
        url = await ui.get_page_url()
        text = await ui.get_element_text("#welcome-message")
        
        # Screenshot
        await ui.take_screenshot("result.png")
```

#### Advanced Operations

```python
# JavaScript execution
result = await ui.execute_script("return document.title")

# Scroll
await ui.scroll_to_element("#footer")

# Hover
await ui.hover_element("#menu-item")

# Double click
await ui.double_click_element("#button")

# Right click
await ui.right_click_element("#context-menu")

# Select option
await ui.select_option("#dropdown", "option-value")

# Checkboxes
await ui.check_checkbox("#agree")
await ui.uncheck_checkbox("#newsletter")

# File upload
await ui.upload_file("#file-input", "path/to/file.pdf")

# Keyboard
await ui.press_key("#input", "Enter")
await ui.type_text("#input", "Hello World")
```

### DBClient - Database Client

Client for working with databases.

#### Creating Client

```python
from py_web_automation import Config
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient
from py_web_automation.clients.db_clients.postgresql_client import PostgreSQLClient
from py_web_automation.clients.db_clients.mysql_client import MySQLClient

# SQLite
db = SQLiteClient(connection_string="sqlite:///path/to/db.sqlite")

# PostgreSQL
db = PostgreSQLClient(connection_string="postgresql://user:pass@localhost/db")

# MySQL
db = MySQLClient(connection_string="mysql://user:pass@localhost/db")
```

#### Executing Queries

```python
async with db:
    # SELECT query
    results = await db.execute_query(
        "SELECT * FROM users WHERE active = :active",
        params={"active": True}
    )
    
    # INSERT command
    await db.execute_command(
        "INSERT INTO users (name, email) VALUES (:name, :email)",
        params={"name": "John", "email": "john@example.com"}
    )
    
    # UPDATE command
    await db.execute_command(
        "UPDATE users SET name = :name WHERE id = :id",
        params={"name": "Jane", "id": 1}
    )
    
    # DELETE command
    await db.execute_command(
        "DELETE FROM users WHERE id = :id",
        params={"id": 1}
    )
```

#### Transactions

```python
# Using context manager
async with db.transaction():
    await db.execute_command("INSERT INTO users ...")
    await db.execute_command("INSERT INTO profiles ...")
    # Automatic commit on success

# All transactions use context manager
# Manual transaction management is not available
```

#### Query Builder for Database

```python
# QueryBuilder is now integrated into DBClient
async with SQLiteClient(connection_string="sqlite:///db.sqlite") as db:
    # Building SELECT query
    query, params = (db.query()
        .select("id", "name", "email")
        .from_table("users")
        .where("active", "=", True)
        .where("age", ">=", 18)
        .order_by("name", "ASC")
        .limit(10)
        .offset(0)
        ._build())

    results = await db.execute_query(query, params)

    # INSERT query
    query, params = (db.query()
        .insert("users", name="John", email="john@example.com")
        ._build())

    await db.execute_command(query, params)

    # UPDATE query
    query, params = (db.query()
        .update("users", name="Jane")
        .where("id", "=", 1)
        ._build())

    await db.execute_command(query, params)

    # DELETE query
    query, params = (db.query()
        .delete("users")
        .where("id", "=", 1)
        ._build())

    await db.execute_command(query, params)
```

---

## Advanced Features

### Retry Mechanism

Automatic request retry with exponential backoff via RetryMiddleware.

```python
from py_web_automation.clients.api_clients.http_client.middleware import (
    RetryMiddleware,
    MiddlewareChain,
)
from py_web_automation.clients.api_clients.http_client.retry import (
    RetryConfig,
    RetryHandler,
)

# Create retry middleware
retry_config = RetryConfig(
    max_attempts=5,
    delay=1.0,
    backoff=2.0,
)
retry_handler = RetryHandler(retry_config)
retry_middleware = RetryMiddleware(retry_handler)

# Add to middleware chain
chain = MiddlewareChain()
chain.add(retry_middleware)

# Use with HttpClient
api = HttpClient("https://api.example.com", config, middleware=chain)
```

### Middleware System

Intercept and modify requests/responses.

```python
from py_web_automation.clients.api_clients.http_client.middleware import (
    Middleware,
    MiddlewareChain,
    LoggingMiddleware,
    MetricsMiddleware,
    AuthMiddleware,
)
from py_web_automation.clients.api_clients.http_client.middleware.context import (
    _HttpRequestContext,
    _HttpResponseContext,
)

# Create custom middleware
class CustomMiddleware(Middleware):
    async def process_request(self, context: _HttpRequestContext):
        # Modify request
        context.headers["X-Custom-Header"] = "value"
        context.metadata["request_id"] = generate_id()
    
    async def process_response(self, context: _HttpResponseContext):
        # Handle response
        if context.result.status_code == 401:
            # Refresh token
            refresh_token()
    
    async def process_error(self, context: _HttpRequestContext, error):
        # Handle errors
        log_error(context, error)
        return None  # Allow error to propagate

# Usage
chain = MiddlewareChain()
chain.add(LoggingMiddleware())
chain.add(MetricsMiddleware(metrics))
chain.add(AuthMiddleware(token="abc123", token_type="Bearer"))
chain.add(CustomMiddleware())

api = HttpClient("https://api.example.com", config, middleware=chain)
```

### Caching

Response caching for improved performance.


### Rate Limiting

Request rate limiting via RateLimitMiddleware.

```python
from py_web_automation.clients.api_clients.http_client.middleware import (
    RateLimitMiddleware,
    MiddlewareChain,
)
from py_web_automation.clients.api_clients.http_client.rate_limit import RateLimiter

# Create rate limiter
limiter = RateLimiter(
    max_requests=100,  # Maximum 100 requests
    window=60,         # Within 60 seconds
    burst=10           # Allow 10 additional requests
)

# Add to middleware chain
chain = MiddlewareChain()
chain.add(RateLimitMiddleware(limiter))

# Use with HttpClient
api = HttpClient("https://api.example.com", config, middleware=chain)
```

### Metrics

Performance metrics collection.

```python
from py_web_automation.clients.api_clients.http_client.metrics import Metrics
from py_web_automation.clients.api_clients.http_client.middleware import (
    MetricsMiddleware,
    MiddlewareChain,
)

# Create metrics
metrics = Metrics()

# Record metric
metrics.record_request(
    success=True,
    latency=0.5,
    error_type=None
)

# Get statistics
print(f"Success rate: {metrics.success_rate:.1f}%")
print(f"Avg latency: {metrics.avg_latency:.3f}s")
print(f"RPS: {metrics.requests_per_second:.2f}")

# Export to dictionary
stats = metrics.to_dict()

# Reset metrics
metrics.reset()

# Use with middleware
chain = MiddlewareChain()
chain.add(MetricsMiddleware(metrics))
api = HttpClient("https://api.example.com", config, middleware=chain)
```

### Retry and Error Handling

All clients support retry logic through `RetryMiddleware` to handle transient failures.
For more advanced error handling patterns, you can implement custom middleware.

### Page Object Model

Page Object Model pattern for UI tests.

```python
from py_web_automation import Config
from py_web_automation.clients.ui_clients import AsyncUiClient
from py_web_automation.clients.ui_clients.async_ui_client.page_objects import (
    BasePage,
    Component,
    PageFactory,
)

# Create page
class LoginPage(BasePage):
    def __init__(self, ui_client: AsyncUiClient):
        super().__init__(ui_client, "https://example.com/login")
    
    async def is_loaded(self) -> bool:
        return await self.is_element_visible("#login-form")
    
    async def login(self, username: str, password: str):
        await self.fill_input("#username", username)
        await self.fill_input("#password", password)
        await self.click_element("#submit")
        await self.wait_for_navigation()

# Create component
class NavigationComponent(Component):
    def __init__(self, ui_client: AsyncUiClient):
        super().__init__(ui_client, "nav.main-nav")
    
    async def click_home(self):
        await self.click_element("a.home")
    
    async def click_about(self):
        await self.click_element("a.about")

# Usage
config = Config()
async with AsyncUiClient("https://example.com", config) as ui:
    factory = PageFactory(ui)
    login_page = factory.create_page(LoginPage)
    
    await login_page.navigate()
    await login_page.login("user", "pass")
```

### Visual Regression Testing

Visual regression testing.

```python
from py_web_automation import Config
from py_web_automation.clients.ui_clients import AsyncUiClient
from py_web_automation.clients.ui_clients.visual_testing import (
    VisualComparator,
    take_baseline_screenshot,
)

# Create comparator
comparator = VisualComparator(threshold=0.01)  # 1% threshold

# Create baseline
config = Config()
async with AsyncUiClient("https://example.com", config) as ui:
    await ui.setup_browser()
    await take_baseline_screenshot(ui, "baseline.png")

# Compare
diff = await comparator.compare("baseline.png", "current.png", diff_path="diff.png")

if diff.is_different:
    print(f"Visual difference: {diff.diff_percentage:.2f}%")
    print(f"Diff image: {diff.diff_image_path}")

# Quick hash comparison
identical = await comparator.compare_hashes("baseline.png", "current.png")
```

### Custom Middleware

Extend functionality through custom middleware.

```python
from py_web_automation.clients.api_clients.http_client.middleware import (
    Middleware,
    MiddlewareChain,
)
from py_web_automation.clients.api_clients.http_client.middleware.context import (
    _HttpRequestContext,
    _HttpResponseContext,
)

# Create custom middleware
class CustomMiddleware(Middleware):
    async def process_request(self, context: _HttpRequestContext):
        # Modify request
        context.headers["X-Custom-Header"] = "value"
    
    async def process_response(self, context: _HttpResponseContext):
        # Handle response
        if context.result.status_code == 401:
            # Handle authentication error
            pass

# Register middleware
chain = MiddlewareChain()
chain.add(CustomMiddleware())
```

### Response Validation

Response validation is available through ValidationMiddleware for each client.
Validation is handled internally (e.g., GraphQL query validation).

For manual validation, you can use msgspec directly:

```python
from msgspec import Struct, json
from py_web_automation.clients.api_clients.http_client import HttpClient

# Create schema
class User(Struct):
    id: int
    name: str
    email: str

# Validate response manually
result = await api.make_request("/users/1", method="GET")
if result.success and result.body:
    user_data = result.json()
    user = json.decode(json.encode(user_data), type=User)
    print(f"User: {user.name}")
```

---

## Patterns and Practices

### Combining Clients

```python
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient
from py_web_automation.clients.ui_clients import AsyncUiClient
import json

# API + Database
async with HttpClient("https://api.example.com", config) as api:
    result = await api.make_request("/users/1", method="GET")
    user_data = result.json()
    
            async with SQLiteClient(connection_string="sqlite:///cache.db") as db:
        await db.execute_command(
            "INSERT INTO users_cache (id, data) VALUES (:id, :data)",
            params={"id": user_data["id"], "data": json.dumps(user_data)}
        )

# UI + API
async with AsyncUiClient("https://example.com", config) as ui:
    await ui.setup_browser()
    await ui.fill_input("#search", "test")
    await ui.click_element("#search-button")
    
    # Get data through API
    async with HttpClient("https://api.example.com", config) as api:
        result = await api.make_request("/search?q=test", method="GET")
```

### Error Handling

```python
from py_web_automation.exceptions import (
    WebAutomationError,
    ConnectionError,
    TimeoutError,
    NotFoundError,
)

try:
    result = await api.make_request("/endpoint")
except ConnectionError as e:
    print(f"Connection failed: {e}")
except TimeoutError as e:
    print(f"Request timed out: {e}")
except NotFoundError as e:
    print(f"Resource not found: {e}")
except WebAutomationError as e:
    print(f"Framework error: {e}")
```

### Best Practices

1. **Use context managers**: Always use `async with` for automatic resource cleanup
2. **Configure logging**: Use `Config` to set logging level
3. **Validate responses**: Use msgspec directly for type-safe data handling
4. **Use middleware**: For reusable logic (logging, metrics)
6. **Limit rate**: To protect against API rate limit violations
7. **Use retry**: For handling temporary failures
8. **Page Object Model**: For structuring UI tests

---

## Usage Examples

### Complete Example: E2E Test

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.api_clients.http_client.metrics import Metrics
from py_web_automation.clients.api_clients.http_client.middleware import (
    LoggingMiddleware,
    MetricsMiddleware,
    MiddlewareChain,
    RateLimitMiddleware,
)
from py_web_automation.clients.api_clients.http_client.rate_limit import RateLimiter
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient
from py_web_automation.clients.ui_clients import AsyncUiClient

async def e2e_test():
    config = Config(timeout=30, retry_count=3)
    metrics = Metrics()
    
    # Setup middleware
    chain = MiddlewareChain()
    chain.add(LoggingMiddleware())
    chain.add(MetricsMiddleware(metrics))
    
    # Setup rate limiting
    limiter = RateLimiter(max_requests=100, window=60)
    chain.add(RateLimitMiddleware(limiter))
    
    # API testing
    async with HttpClient(
        "https://api.example.com",
        config,
        middleware=chain
    ) as api:
        # Create user via API
        result = await api.make_request(
            "/users",
            method="POST",
            data={"name": "Test User", "email": "test@example.com"}
        )
        user_data = result.json()
        user_id = user_data["id"]
        
        # UI testing
        async with AsyncUiClient("https://example.com", config) as ui:
            await ui.setup_browser()
            if ui.page:
                await ui.page.goto("https://example.com/login")
            await ui.fill_input("#username", "test@example.com")
            await ui.fill_input("#password", "password")
            await ui.click_element("#login")
            await ui.wait_for_element("#dashboard")
            
            # Verify via API
            result = await api.make_request(f"/users/{user_id}", method="GET")
            assert result.json()["email"] == "test@example.com"
            
            # Verify via database
            async with SQLiteClient(connection_string="sqlite:///test.db") as db:
                results = await db.execute_query(
                    "SELECT * FROM users WHERE id = :id",
                    params={"id": user_id}
                )
                assert len(results) == 1
    
    # Output metrics
    print(metrics.to_dict())

asyncio.run(e2e_test())
```

---

## Conclusion

This guide covers all the main features of the framework. For more detailed information, see:

- [API Reference](api-reference.md) - Complete API documentation
- [Examples](examples.md) - Additional examples
- [Architecture](architecture.md) - Framework architecture
- [Testing](testing.md) - Testing guide
