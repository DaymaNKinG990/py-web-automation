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

### BaseClient - Base Client

All clients inherit from `BaseClient`, which provides:
- URL management
- Logging
- Context managers for automatic resource cleanup

```python
from py_web_automation.clients import BaseClient

class MyClient(BaseClient):
    async def custom_method(self):
        # Use self.url, self.config, self.logger
        pass
```

---

## Clients

### ApiClient - REST API Client

Main client for testing HTTP REST APIs.

#### Basic Usage

```python
from py_web_automation import ApiClient, Config

async def basic_api_test():
    config = Config(timeout=30)
    async with ApiClient("https://api.example.com", config) as api:
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
# Set token
api.set_auth_token("your-token-here", token_type="Bearer")

# All subsequent requests automatically include token
result = await api.make_request("/protected")

# Clear token
api.clear_auth_token()
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
    .auth("token")
    .execute())
```

#### Advanced Features

```python
from py_web_automation import (
    ApiClient, Config,
    MiddlewareChain, ResponseCache, RateLimiter,
    LoggingMiddleware, MetricsMiddleware
)

# With middleware
chain = MiddlewareChain()
chain.add(LoggingMiddleware())
chain.add(MetricsMiddleware())

# With caching
cache = ResponseCache(default_ttl=300)  # 5 minutes

# With rate limiting
rate_limiter = RateLimiter(max_requests=100, window=60)

# Create client with all features
api = ApiClient(
    "https://api.example.com",
    config,
    middleware=chain,
    cache=cache,
    rate_limiter=rate_limiter,
    enable_auto_retry=True  # Automatic retry
)
```

### GraphQLClient - GraphQL Client

Client for working with GraphQL APIs.

```python
from py_web_automation import GraphQLClient, Config

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
        
        # With authentication
        client.set_auth_token("token")
        result = await client.query("query { me { id } }")
```

### SoapClient - SOAP Client

Client for working with SOAP web services.

```python
from py_web_automation import SoapClient, Config

async def soap_test():
    config = Config(timeout=30)
    async with SoapClient("https://api.example.com/soap", config) as client:
        # SOAP call
        result = await client.call(
            method="GetUser",
            params={"id": 1},
            namespace="http://example.com/soap"
        )
        
        # With authentication
        client.set_auth_token("token")
        result = await client.call("GetUser", {"id": 1})
```

### WebSocketClient - WebSocket Client

Client for working with WebSocket connections.

```python
from py_web_automation import WebSocketClient, Config

async def websocket_test():
    config = Config(timeout=30)
    async with WebSocketClient("wss://api.example.com/ws", config) as client:
        # Connect
        await client.connect()
        
        # Send message
        await client.send_message({"type": "subscribe", "channel": "updates"})
        
        # Receive message
        message = await client.receive_message(timeout=5.0)
        print(f"Received: {message}")
        
        # Listen to messages
        async for message in client.listen():
            print(f"Message: {message}")
            if message.get("type") == "done":
                break
        
        # Register handler
        def handle_message(msg):
            print(f"Handler received: {msg}")
        
        client.register_handler(handle_message)
```

### UiClient - UI Client

Client for browser automation with Playwright.

#### Basic Usage

```python
from py_web_automation import UiClient, Config

async def ui_test():
    config = Config(timeout=30, browser_headless=True)
    async with UiClient("https://example.com", config) as ui:
        # Setup browser
        await ui.setup_browser()
        
        # Navigate
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
from py_web_automation import DBClient, Config

# PostgreSQL
db = await DBClient.create(
    "postgresql",
    "https://example.com",
    config,
    connection_string="postgresql://user:pass@localhost/db"
)

# SQLite
db = await DBClient.create(
    "sqlite",
    "https://example.com",
    config,
    connection_string="sqlite:///path/to/db.sqlite"
)

# MySQL
db = await DBClient.create(
    "mysql",
    "https://example.com",
    config,
    connection_string="mysql://user:pass@localhost/db"
)
```

#### Executing Queries

```python
async with db:
    # SELECT query
    results = await db.execute_query(
        "SELECT * FROM users WHERE active = :active",
        {"active": True}
    )
    
    # INSERT command
    rows_affected = await db.execute_command(
        "INSERT INTO users (name, email) VALUES (:name, :email)",
        {"name": "John", "email": "john@example.com"}
    )
    
    # UPDATE command
    rows_affected = await db.execute_command(
        "UPDATE users SET name = :name WHERE id = :id",
        {"name": "Jane", "id": 1}
    )
    
    # DELETE command
    rows_affected = await db.execute_command(
        "DELETE FROM users WHERE id = :id",
        {"id": 1}
    )
```

#### Transactions

```python
# Using context manager
async with db.transaction():
    await db.execute_command("INSERT INTO users ...")
    await db.execute_command("INSERT INTO profiles ...")
    # Automatic commit on success

# Manual management
await db.begin_transaction()
try:
    await db.execute_command("INSERT INTO users ...")
    await db.commit_transaction()
except Exception:
    await db.rollback_transaction()
```

#### Query Builder for Database

```python
from py_web_automation import QueryBuilder

# Building SELECT query
builder = QueryBuilder()
query, params = (builder
    .select("id", "name", "email")
    .from_table("users")
    .where("active", "=", True)
    .where("age", ">=", 18)
    .order_by("name", "ASC")
    .limit(10)
    .offset(0)
    .build())

results = await db.execute_query(query, params)

# INSERT query
query, params = (builder
    .insert("users", name="John", email="john@example.com")
    .build())

rows_affected = await db.execute_command(query, params)

# UPDATE query
query, params = (builder
    .update("users", name="Jane")
    .where("id", "=", 1)
    .build())

rows_affected = await db.execute_command(query, params)

# DELETE query
query, params = (builder
    .delete("users")
    .where("id", "=", 1)
    .build())

rows_affected = await db.execute_command(query, params)
```

---

## Advanced Features

### Retry Mechanism

Automatic request retry with exponential backoff.

```python
from py_web_automation import retry_on_failure, retry_on_connection_error

# Decorator for automatic retry
@retry_on_failure(
    max_attempts=3,
    delay=1.0,
    backoff=2.0,
    exceptions=(ConnectionError, TimeoutError)
)
async def fetch_data():
    return await api.make_request("/data")

# Special decorator for connection errors
@retry_on_connection_error(max_attempts=5, delay=2.0)
async def connect_to_api():
    return await api.make_request("/status")

# Retry configuration
from py_web_automation import RetryConfig

retry_config = RetryConfig(
    max_attempts=5,
    delay=1.0,
    backoff=2.0,
    max_delay=30.0,
    jitter=True
)
```

### Middleware System

Intercept and modify requests/responses.

```python
from py_web_automation import (
    Middleware, MiddlewareChain,
    RequestContext, ResponseContext,
    LoggingMiddleware, MetricsMiddleware,
    AuthMiddleware, ValidationMiddleware
)

# Create custom middleware
class CustomMiddleware(Middleware):
    async def process_request(self, context: RequestContext):
        # Modify request
        context.headers["X-Custom-Header"] = "value"
        context.metadata["request_id"] = generate_id()
    
    async def process_response(self, context: ResponseContext):
        # Handle response
        if context.result.status_code == 401:
            # Refresh token
            refresh_token()
    
    async def process_error(self, context: RequestContext, error):
        # Handle errors
        log_error(context, error)
        return None  # Allow error to propagate

# Usage
chain = MiddlewareChain()
chain.add(LoggingMiddleware())
chain.add(MetricsMiddleware(metrics))
chain.add(AuthMiddleware(token="abc123"))
chain.add(CustomMiddleware())

api = ApiClient("https://api.example.com", config, middleware=chain)
```

### Caching

Response caching for improved performance.

```python
from py_web_automation import ResponseCache

# Create cache
cache = ResponseCache(
    default_ttl=300,  # 5 minutes
    max_size=1000     # Maximum 1000 entries
)

# Use with ApiClient
api = ApiClient("https://api.example.com", config, cache=cache)

# Request with caching (GET only)
result = await api.make_request("/users", method="GET", use_cache=True)

# Invalidate cache
cache.invalidate(method="GET", url_pattern="/users/*")

# Cleanup expired entries
expired_count = cache.cleanup_expired()
```

### Rate Limiting

Request rate limiting.

```python
from py_web_automation import RateLimiter

# Create rate limiter
limiter = RateLimiter(
    max_requests=100,  # Maximum 100 requests
    window=60,         # Within 60 seconds
    burst=10           # Allow 10 additional requests
)

# Use with ApiClient
api = ApiClient("https://api.example.com", config, rate_limiter=limiter)

# Manual usage
await limiter.acquire()  # Blocks if limit exceeded
result = await api.make_request("/endpoint")

# Non-blocking attempt
if await limiter.try_acquire():
    result = await api.make_request("/endpoint")
else:
    print("Rate limit exceeded")

# Check remaining requests
remaining = limiter.get_remaining()
wait_time = limiter.get_wait_time()
```

### Metrics

Performance metrics collection.

```python
from py_web_automation import Metrics

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
from py_web_automation import MetricsMiddleware

chain = MiddlewareChain()
chain.add(MetricsMiddleware(metrics))
api = ApiClient("https://api.example.com", config, middleware=chain)
```

### Circuit Breaker

Protection against cascading failures.

```python
from py_web_automation import CircuitBreaker

# Create circuit breaker
breaker = CircuitBreaker(
    failure_threshold=5,   # Open after 5 errors
    timeout=60.0,          # Try to close after 60 seconds
    success_threshold=2    # Close after 2 successful requests
)

# Usage
try:
    result = await breaker.call(
        api.make_request,
        "/endpoint",
        method="GET"
    )
except ConnectionError as e:
    print(f"Circuit is open: {e}")

# Check state
state = breaker.get_state()  # CLOSED, OPEN, HALF_OPEN
stats = breaker.get_stats()
```

### Page Object Model

Page Object Model pattern for UI tests.

```python
from py_web_automation import BasePage, Component, PageFactory
from py_web_automation import UiClient, Config

# Create page
class LoginPage(BasePage):
    def __init__(self, ui_client: UiClient):
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
    def __init__(self, ui_client: UiClient):
        super().__init__(ui_client, "nav.main-nav")
    
    async def click_home(self):
        await self.click_element("a.home")
    
    async def click_about(self):
        await self.click_element("a.about")

# Usage
config = Config()
async with UiClient("https://example.com", config) as ui:
    factory = PageFactory(ui)
    login_page = factory.create_page(LoginPage)
    
    await login_page.navigate()
    await login_page.login("user", "pass")
```

### Visual Regression Testing

Visual regression testing.

```python
from py_web_automation import VisualComparator, take_baseline_screenshot
from py_web_automation import UiClient, Config

# Create comparator
comparator = VisualComparator(threshold=0.01)  # 1% threshold

# Create baseline
config = Config()
async with UiClient("https://example.com", config) as ui:
    await ui.setup_browser()
    await take_baseline_screenshot(ui, "baseline.png")

# Compare
diff = await comparator.compare("baseline.png", "current.png", "diff.png")

if diff.is_different:
    print(f"Visual difference: {diff.diff_percentage:.2f}%")
    print(f"Diff image: {diff.diff_image_path}")

# Quick hash comparison
identical = await comparator.compare_hashes("baseline.png", "current.png")
```

### Plugin System

Extend functionality through plugins.

```python
from py_web_automation import Plugin, PluginManager, HookType, HookContext

# Create plugin
class CustomPlugin(Plugin):
    def get_name(self) -> str:
        return "custom"
    
    def on_before_request(self, context: HookContext):
        print(f"Request: {context.data.get('method')} {context.data.get('url')}")
    
    def on_after_request(self, context: HookContext):
        print(f"Response: {context.data.get('status_code')}")

# Register plugin
manager = PluginManager()
manager.register(CustomPlugin())
manager.register(LoggingPlugin())

# Usage (plugins integrate automatically)
# through middleware or directly in clients
```

### Response Validation

API response validation using msgspec.

```python
from py_web_automation import validate_response, validate_api_result, create_schema_from_dict
from msgspec import Struct

# Create schema
class User(Struct):
    id: int
    name: str
    email: str

# Validate response
result = await api.make_request("/users/1")
user = validate_api_result(result, User)

# Dynamic schema creation
UserSchema = create_schema_from_dict(
    "User",
    {
        "id": int,
        "name": str,
        "email": str,
        "age": (int, 0)  # Optional with default
    }
)

# JSON string validation
from py_web_automation import validate_json_response

json_str = '{"id": 1, "name": "John", "email": "john@example.com"}'
user = validate_json_response(json_str, User)
```

---

## Patterns and Practices

### Combining Clients

```python
# API + Database
async with ApiClient("https://api.example.com", config) as api:
    result = await api.make_request("/users/1")
    user_data = result.json()
    
    async with DBClient.create("postgresql", "...", config, ...) as db:
        await db.execute_command(
            "INSERT INTO users_cache (id, data) VALUES (:id, :data)",
            {"id": user_data["id"], "data": json.dumps(user_data)}
        )

# UI + API
async with UiClient("https://example.com", config) as ui:
    await ui.setup_browser()
    await ui.fill_input("#search", "test")
    await ui.click_element("#search-button")
    
    # Get data through API
    async with ApiClient("https://api.example.com", config) as api:
        result = await api.make_request("/search?q=test")
```

### Error Handling

```python
from py_web_automation.exceptions import (
    WebAutomationError,
    ConnectionError,
    TimeoutError,
    NotFoundError,
    ValidationError
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
3. **Validate responses**: Use `validate_api_result` for type-safe data handling
4. **Use middleware**: For reusable logic (logging, metrics)
5. **Cache requests**: For improved performance
6. **Limit rate**: To protect against API rate limit violations
7. **Use retry**: For handling temporary failures
8. **Page Object Model**: For structuring UI tests

---

## Usage Examples

### Complete Example: E2E Test

```python
import asyncio
from py_web_automation import (
    ApiClient, UiClient, DBClient, Config,
    MiddlewareChain, ResponseCache, RateLimiter,
    LoggingMiddleware, MetricsMiddleware, Metrics
)

async def e2e_test():
    config = Config(timeout=30, retry_count=3)
    metrics = Metrics()
    
    # Setup middleware
    chain = MiddlewareChain()
    chain.add(LoggingMiddleware())
    chain.add(MetricsMiddleware(metrics))
    
    # Setup cache and rate limiting
    cache = ResponseCache(default_ttl=300)
    limiter = RateLimiter(max_requests=100, window=60)
    
    # API testing
    async with ApiClient(
        "https://api.example.com",
        config,
        middleware=chain,
        cache=cache,
        rate_limiter=limiter
    ) as api:
        # Create user via API
        result = await api.make_request(
            "/users",
            method="POST",
            data={"name": "Test User", "email": "test@example.com"}
        )
        user_id = result.json()["id"]
        
        # UI testing
        async with UiClient("https://example.com", config) as ui:
            await ui.setup_browser()
            await ui.page.goto("https://example.com/login")
            await ui.fill_input("#username", "test@example.com")
            await ui.fill_input("#password", "password")
            await ui.click_element("#login")
            await ui.wait_for_element("#dashboard")
            
            # Verify via API
            result = await api.make_request(f"/users/{user_id}")
            assert result.json()["email"] == "test@example.com"
            
            # Verify via database
            async with DBClient.create("postgresql", "...", config, ...) as db:
                results = await db.execute_query(
                    "SELECT * FROM users WHERE id = :id",
                    {"id": user_id}
                )
                assert len(results) == 1
    
    # Output metrics
    print(metrics.get_summary())

asyncio.run(e2e_test())
```

---

## Conclusion

This guide covers all the main features of the framework. For more detailed information, see:

- [API Reference](api-reference.md) - Complete API documentation
- [Examples](examples.md) - Additional examples
- [Architecture](architecture.md) - Framework architecture
- [Testing](testing.md) - Testing guide
