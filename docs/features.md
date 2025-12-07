# Framework Features

## Response Validation

### Overview

Response validation can be done manually using `msgspec` directly, or through built-in ValidationMiddleware in specific clients (e.g., GraphQL query validation). This is useful for:
- Validating API responses against expected schemas
- Type-safe response handling
- Early detection of API contract violations
- Performance-critical validation (msgspec is 2-4x faster than Pydantic)

### Manual Validation with msgspec

```python
from msgspec import Struct, json
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

class UserResponse(Struct):
    id: int
    name: str
    email: str

config = Config(timeout=30)
async with HttpClient("https://api.example.com", config) as api:
    result = await api.make_request("/users/1", method="GET")
    if result.success and result.body:
        user_data = result.json()
        user = json.decode(json.encode(user_data), type=UserResponse)
        print(f"User: {user.name} ({user.email})")
```

### Built-in Validation

Some clients have built-in validation:
- **GraphQLClient**: Automatic query validation via ValidationMiddleware
- Other clients support custom validation through middleware

## Request Builder Pattern

### Overview

Request Builder provides a fluent API for constructing complex HTTP requests.
RequestBuilder uses Builder pattern for request construction.

### Usage

#### Basic Request

```python
from py_web_automation import Config
from py_web_automation.clients.api_clients.http_client import HttpClient

config = Config(timeout=30)
async with HttpClient("https://api.example.com", config) as api:
    builder = api.build_request()
    result = await builder.get("/users").execute()
```

#### Complex Request with Parameters

```python
builder = api.build_request()
result = await (builder
    .get("/users")
    .params(page=1, limit=10, sort="name")
    .header("X-Custom-Header", "value")
    .execute())
```

#### POST Request with Body

```python
result = await (builder
    .post("/users")
    .body({"name": "John", "email": "john@example.com"})
    .header("Content-Type", "application/json")
    .execute())
```

#### Request with Authentication

```python
result = await (builder
    .get("/protected")
    .auth("your-token-here")
    .execute())
```

#### Method Chaining

```python
# All HTTP methods supported
builder.get("/users")
builder.post("/users")
builder.put("/users/1")
builder.delete("/users/1")
builder.patch("/users/1")
builder.head("/users")
builder.options("/users")
```

#### Reset Builder

```python
builder.get("/users").execute()
builder.reset()  # Clear all settings
builder.post("/posts").execute()
```


