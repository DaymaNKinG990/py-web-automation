# Examples

This document provides comprehensive examples of using the Web Automation Framework for various testing scenarios.

## Table of Contents

- [Basic Usage](#basic-usage)
- [API Testing](#api-testing)
- [GraphQL Testing](#graphql-testing)
- [gRPC Testing](#grpc-testing)
- [SOAP Testing](#soap-testing)
- [WebSocket Testing](#websocket-testing)
- [UI Testing](#ui-testing)
- [Database Testing](#database-testing)
- [Request Builder](#request-builder)
- [Response Validation](#response-validation)
- [Error Handling](#error-handling)
- [Configuration Examples](#configuration-examples)
- [Advanced Patterns](#advanced-patterns)
- [Real-world Scenarios](#real-world-scenarios)

## Basic Usage

### Simple API Test

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

async def basic_api_test():
    config = Config(timeout=30)
    
    async with HttpClient("https://api.example.com", config) as api:
        result = await api.make_request("/api/status", method="GET")
        print(f"Status: {result.status_code}")
        print(f"Success: {result.success}")
        print(f"Response time: {result.response_time:.3f}s")

asyncio.run(basic_api_test())
```

## API Testing

### Basic API Testing

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

async def basic_api_test():
    config = Config(timeout=30)

    async with HttpClient("https://api.example.com", config) as api:
        # Test GET endpoint
        result = await api.make_request("/api/status", method="GET")
        print(f"Status: {result.status_code}")
        print(f"Success: {result.success}")
        print(f"Response time: {result.response_time:.3f}s")

        if result.error_message:
            print(f"Error: {result.error_message}")

asyncio.run(basic_api_test())
```

### POST Request with Data

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

async def post_request_example():
    config = Config(timeout=30)

    async with HttpClient("https://api.example.com", config) as api:
        # Test POST endpoint with data
        data = {
            "username": "test_user",
            "email": "test@example.com",
            "preferences": {
                "theme": "dark",
                "notifications": True
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer token123"
        }

        result = await api.make_request(
            "/api/users",
            method="POST",
            data=data,
            headers=headers
        )

        print(f"Response: {result.status_code}")
        print(f"Success: {result.success}")

asyncio.run(post_request_example())
```

### Multiple API Endpoints

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

async def multiple_endpoints_example():
    config = Config(timeout=30)

    endpoints = [
        ("/api/health", "GET"),
        ("/api/users", "GET"),
        ("/api/profile", "GET"),
        ("/api/settings", "GET"),
    ]

    async with HttpClient("https://api.example.com", config) as api:
        results = []

        for endpoint, method in endpoints:
            result = await api.make_request(endpoint, method=method)
            results.append({
                "endpoint": endpoint,
                "method": method,
                "status": result.status_code,
                "success": result.success,
                "time": result.response_time
            })

        # Print results
        for result in results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['method']} {result['endpoint']} - "
                  f"{result['status']} ({result['time']:.3f}s)")

asyncio.run(multiple_endpoints_example())
```

## GraphQL Testing

### Basic GraphQL Query

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient

async def graphql_query_example():
    config = Config(timeout=30)
    
    async with GraphQLClient("https://api.example.com/graphql", config) as client:
        query = """
        query GetUser($id: ID!) {
            user(id: $id) {
                id
                name
                email
            }
        }
        """
        
        variables = {"id": "123"}
        result = await client.query(query, variables=variables)
        print(f"Success: {result.success}")
        print(f"Data: {result.data}")

asyncio.run(graphql_query_example())
```

### GraphQL Mutation

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient

async def graphql_mutation_example():
    config = Config(timeout=30)
    
    async with GraphQLClient("https://api.example.com/graphql", config) as client:
        mutation = """
        mutation CreateUser($input: UserInput!) {
            createUser(input: $input) {
                id
                name
                email
            }
        }
        """
        
        variables = {
            "input": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
        
        result = await client.mutate(mutation, variables=variables)
        print(f"Success: {result.success}")
        print(f"Data: {result.data}")

asyncio.run(graphql_mutation_example())
```

## gRPC Testing

### Basic gRPC Call

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.grpc_client import GrpcClient

async def grpc_example():
    config = Config(timeout=30)
    
    async with GrpcClient("localhost:50051", config) as client:
        # Call gRPC method
        await client.connect()
        # result = await client.unary_call("UserService", "GetUser", request)
        # if result.success:
        #     print(result.response)
        print("gRPC call executed (conceptual example)")

asyncio.run(grpc_example())
```

## SOAP Testing

### Basic SOAP Request

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.soap_client import SoapClient

async def soap_example():
    config = Config(timeout=30)
    
    async with SoapClient("https://api.example.com/soap", config) as client:
        # Call SOAP method
        result = await client.call(
            operation="GetUser",
            body={"userId": "123"}
        )
        print(f"Success: {result.success}")
        print(f"Response: {result.response}")

asyncio.run(soap_example())
```

## WebSocket Testing

### Basic WebSocket Communication

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.streaming_clients.websocket_client.websocket_client import (
    WebSocketClient,
)

async def websocket_example():
    config = Config(timeout=30)
    
    async with WebSocketClient("ws://example.com/ws", config) as ws:
        # Connect first
        await ws.connect()
        
        # Send message
        result = await ws.send_message({"type": "ping", "data": "hello"})
        if result.success:
            print(f"Sent at {result.timestamp}")
        
        # Receive message
        received_result = await ws.receive_message(timeout=5.0)
        if received_result.success:
            print(f"Received: {received_result.message}")
        
        # Listen to messages
        async for result in ws.listen():
            if result.success:
                print(f"Message: {result.message}")
                if isinstance(result.message, dict) and result.message.get("type") == "close":
                    break

asyncio.run(websocket_example())
```

## UI Testing

### Basic UI Testing

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.ui_clients import AsyncUiClient

async def basic_ui_test():
    config = Config(timeout=30)

    async with AsyncUiClient("https://example.com", config) as ui:
        # Setup browser and navigate
        await ui.setup_browser()
        await ui.page.goto("https://example.com", wait_until="networkidle")

        # Take initial screenshot
        await ui.take_screenshot("initial_state.png")

        # Get page information
        title = await ui.get_page_title()
        url = await ui.get_page_url()
        print(f"Page: {title} - {url}")

asyncio.run(basic_ui_test())
```

### Form Interaction

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.ui_clients import AsyncUiClient

async def form_interaction_example():
    config = Config(timeout=30)

    async with AsyncUiClient("https://example.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://example.com", wait_until="networkidle")

        # Fill form fields
        await ui.fill_input("#username", "test_user")
        await ui.fill_input("#email", "test@example.com")
        await ui.fill_input("#password", "secure_password")

        # Select dropdown option
        await ui.select_option("#country", "US")

        # Check checkbox
        await ui.check_checkbox("#terms")

        # Take screenshot before submission
        await ui.take_screenshot("form_filled.png")

        # Submit form
        await ui.click_element("#submit-button")

        # Wait for success message
        await ui.wait_for_element("#success-message", timeout=10000)

        # Take final screenshot
        await ui.take_screenshot("form_submitted.png")

asyncio.run(form_interaction_example())
```

### Advanced UI Interactions

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.ui_clients import AsyncUiClient

async def advanced_ui_interactions():
    config = Config(timeout=30)

    async with AsyncUiClient("https://example.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://example.com", wait_until="networkidle")

        # Mouse interactions
        await ui.hover_element("#menu-item")
        await ui.double_click_element("#file-item")
        await ui.right_click_element("#context-menu-target")

        # Keyboard interactions
        await ui.type_text("Hello, World!")
        await ui.press_key("Enter")
        await ui.press_key("Tab")
        await ui.press_key("Escape")

        # File upload
        await ui.upload_file("#file-input", "test_file.txt")

        # Scroll to element
        await ui.scroll_to_element("#footer")

        # Wait for navigation
        await ui.wait_for_navigation(timeout=5000)

        # Execute JavaScript
        result = await ui.execute_script("return document.title;")
        print(f"Page title via JS: {result}")

        # Get element information
        element_text = await ui.get_element_text("h1")
        element_class = await ui.get_element_attribute_value("button", "class")

        print(f"Element text: {element_text}")
        print(f"Element class: {element_class}")

asyncio.run(advanced_ui_interactions())
```

## Database Testing

### Basic Database Operations

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient

async def basic_database_test():
    config = Config()

    # SQLite example
    async with SQLiteClient(connection_string="sqlite:///:memory:") as db:

        # Create table
        await db.execute_command(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
        )

        # Insert data
        await db.execute_command(
            "INSERT INTO users (name, email) VALUES (:name, :email)",
            params={"name": "Test User", "email": "test@example.com"}
        )

        # Query data
        users = await db.execute_query("SELECT * FROM users")
        print(f"Users: {users}")

        # Update data
        await db.execute_command(
            "UPDATE users SET email = :email WHERE name = :name",
            params={"email": "updated@example.com", "name": "Test User"}
        )
        print("Updated rows")

        # Delete data
        await db.execute_command(
            "DELETE FROM users WHERE name = :name",
            params={"name": "Test User"}
        )
        print("Deleted rows")

asyncio.run(basic_database_test())
```

### Database Transactions

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient

async def database_transactions():
    config = Config()

    # SQLite example with transactions
    async with SQLiteClient(connection_string="sqlite:///:memory:") as db:
        await db.execute_command(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"
        )

        # Use transaction context manager
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

asyncio.run(database_transactions())
```

## Request Builder

### Fluent API for Requests

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

async def request_builder_example():
    config = Config(timeout=30)
    
    async with HttpClient("https://api.example.com", config) as api:
        # Build request with fluent API
        result = await (api.build_request()
            .get("/users")
            .params(page=1, limit=10, sort="name")
            .header("X-Custom-Header", "value")
            .auth("bearer-token")
            .execute())
        
        print(f"Status: {result.status_code}")
        
        # POST request with body
        result = await (api.build_request()
            .post("/users")
            .body({"name": "John", "email": "john@example.com"})
            .header("Content-Type", "application/json")
            .execute())
        
        print(f"Created: {result.success}")

asyncio.run(request_builder_example())
```

## Response Validation

Response validation is available through ValidationMiddleware for each client.
Validation is handled internally and validates requests/responses according to
the client's specific requirements (e.g., GraphQL query validation).

For manual validation, you can use msgspec directly:

```python
import asyncio
from msgspec import Struct, json

from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

class UserResponse(Struct):
    id: int
    name: str
    email: str

async def validation_example():
    config = Config(timeout=30)
    
    async with HttpClient("https://api.example.com", config) as api:
        result = await api.make_request("/users/1", method="GET")
        
        if result.success and result.body:
            # Manual validation using msgspec
            user_data = result.json()
            user = json.decode(json.encode(user_data), type=UserResponse)
            print(f"User: {user.name} ({user.email})")

asyncio.run(validation_example())
```

## Error Handling

### Robust API Testing

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.exceptions import WebAutomationError, ConnectionError

async def robust_api_testing():
    config = Config(timeout=30)

    endpoints = [
        "/api/health",
        "/api/users",
        "/api/nonexistent",
        "/api/error"
    ]

    async with HttpClient("https://api.example.com", config) as api:
        for endpoint in endpoints:
            try:
                result = await api.make_request(endpoint, method="GET")

                if result.success:
                    print(f"✅ {endpoint}: {result.status_code}")
                else:
                    print(f"❌ {endpoint}: {result.status_code} - {result.error_message}")

            except ConnectionError as e:
                print(f"🔌 {endpoint}: Connection error - {e}")
            except WebAutomationError as e:
                print(f"⚠️ {endpoint}: Framework error - {e}")
            except Exception as e:
                print(f"💥 {endpoint}: Exception - {e}")

asyncio.run(robust_api_testing())
```

### Retry Logic

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

async def retry_logic_example():
    config = Config(timeout=30, retry_count=3, retry_delay=1.0)

    async with HttpClient("https://api.example.com", config) as api:
        max_retries = 3
        retry_delay = 1.0

        for attempt in range(max_retries):
            try:
                result = await api.make_request("/api/unstable", method="GET")

                if result.success:
                    print(f"✅ Success on attempt {attempt + 1}")
                    break
                else:
                    print(f"❌ Attempt {attempt + 1} failed: {result.error_message}")

            except Exception as e:
                print(f"💥 Attempt {attempt + 1} exception: {e}")

            if attempt < max_retries - 1:
                print(f"⏳ Waiting {retry_delay}s before retry...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
        else:
            print("❌ All retry attempts failed")

asyncio.run(retry_logic_example())
```

## Configuration Examples

### Environment-based Configuration

```python
from py_web_automation import Config

# Using environment variables
config = Config.from_env()

# Or create manually
config = Config(
    timeout=30,
    retry_count=3,
    retry_delay=1.0,
    log_level="INFO"
)
```

### YAML Configuration

```python
from py_web_automation import Config

# Load from YAML file
config = Config.from_yaml("config.yaml")
```

## Advanced Patterns

### Parallel Testing

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

async def parallel_api_testing():
    config = Config(timeout=30)

    endpoints = [
        "/api/health",
        "/api/users",
        "/api/profile",
        "/api/settings",
        "/api/notifications"
    ]

    async def test_endpoint(endpoint: str):
        async with HttpClient("https://api.example.com", config) as api:
            result = await api.make_request(endpoint, method="GET")
            return {
                "endpoint": endpoint,
                "status": result.status_code,
                "success": result.success,
                "time": result.response_time
            }

    # Run all tests in parallel
    tasks = [test_endpoint(endpoint) for endpoint in endpoints]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    for result in results:
        if isinstance(result, Exception):
            print(f"💥 Exception: {result}")
        else:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['endpoint']} - "
                  f"{result['status']} ({result['time']:.3f}s)")

asyncio.run(parallel_api_testing())
```

## Real-world Scenarios

### E-commerce Application Testing

```python
import asyncio
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.ui_clients import AsyncUiClient

async def ecommerce_testing():
    config = Config(timeout=30)

    # Test product API
    async with HttpClient("https://api.shop.com", config) as api:
        # Test product listing
        products = await api.make_request("/api/products", method="GET")
        print(f"Products API: {products.status_code}")

        # Test product details
        product = await api.make_request("/api/products/123", method="GET")
        print(f"Product details: {product.status_code}")

        # Test add to cart
        cart_data = {"product_id": 123, "quantity": 2}
        cart = await api.make_request("/api/cart", method="POST", data=cart_data)
        print(f"Add to cart: {cart.status_code}")

    # Test shopping flow UI
    async with AsyncUiClient("https://shop.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://shop.com", wait_until="networkidle")

        # Browse products
        await ui.click_element("#products-tab")
        await ui.wait_for_element(".product-item", timeout=10000)

        # Select product
        await ui.click_element(".product-item:first-child")
        await ui.wait_for_element("#product-details", timeout=5000)

        # Add to cart
        await ui.click_element("#add-to-cart")
        await ui.wait_for_element("#cart-notification", timeout=5000)

        # Take screenshot
        await ui.take_screenshot("cart_added.png")

asyncio.run(ecommerce_testing())
```

These examples demonstrate the flexibility and power of the Web Automation Framework for testing various types of web applications. The framework's separation of concerns allows you to focus on API testing, UI testing, or both, depending on your needs.
