# Framework Features

## Response Validators (msgspec)

### Overview

Response validators provide fast and efficient schema validation using `msgspec`.
This is useful for:
- Validating API responses against expected schemas
- Type-safe response handling
- Early detection of API contract violations
- Performance-critical validation (msgspec is 2-4x faster than Pydantic)

### Usage

#### Basic Validation

```python
from msgspec import Struct
from py_web_automation import ApiClient, Config
from py_web_automation.validators import validate_api_result

class UserResponse(Struct):
    id: int
    name: str
    email: str

config = Config(timeout=30)
async with ApiClient("https://api.example.com", config) as api:
    result = await api.make_request("/users/1")
    user = validate_api_result(result, UserResponse)
    print(f"User: {user.name} ({user.email})")
```

#### Dynamic Schema Creation

```python
from py_web_automation.validators import create_schema_from_dict

# Create schema at runtime
UserSchema = create_schema_from_dict(
    "User",
    {
        "id": int,
        "name": str,
        "email": str,
        "age": (int, 0),  # Optional with default
    }
)

user = UserSchema(id=1, name="John", email="john@example.com")
```

#### JSON String Validation

```python
from py_web_automation.validators import validate_json_response

json_str = '{"id": 1, "name": "John", "email": "john@example.com"}'
user = validate_json_response(json_str, UserResponse)
```

## Request Builder Pattern

### Overview

Request Builder provides a fluent API for constructing complex HTTP requests.
Similar to how `DBClient.create()` uses Factory pattern, RequestBuilder uses
Builder pattern for request construction.

### Usage

#### Basic Request

```python
from py_web_automation import ApiClient, Config

config = Config(timeout=30)
async with ApiClient("https://api.example.com", config) as api:
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


