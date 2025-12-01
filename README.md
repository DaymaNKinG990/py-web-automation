# py-web-automation

A comprehensive Python framework for automated testing of web applications, providing clients for API testing (REST, GraphQL, gRPC, SOAP), WebSocket communication, UI testing, and database operations.

## Features

- **Multiple API Protocols**: REST, GraphQL, gRPC, SOAP, and WebSocket support
- **Browser Automation**: Playwright-based UI testing
- **Database Testing**: Support for PostgreSQL, MySQL, and SQLite with adapter pattern
- **Type Safety**: Complete type annotations with 100% coverage
- **Async-First**: Built on async/await for high performance
- **Request Builder**: Fluent API for constructing complex HTTP requests
- **Response Validation**: Fast schema validation using msgspec
- **Error Handling**: Structured exception hierarchy
- **Configuration Management**: Flexible configuration with environment variables and YAML support

## Installation

```bash
# Using uv (recommended)
uv add py-web-automation

# Or using pip
pip install py-web-automation
```

## Quick Start

### API Testing

```python
import asyncio
from py_web_automation import ApiClient, Config

async def main():
    config = Config(timeout=30)
    async with ApiClient("https://api.example.com", config) as api:
        result = await api.make_request("/users/1", method="GET")
        print(f"Status: {result.status_code}, Success: {result.success}")

asyncio.run(main())
```

### UI Testing

```python
import asyncio
from py_web_automation import UiClient, Config

async def main():
    config = Config(timeout=30)
    async with UiClient("https://example.com", config) as ui:
        await ui.setup_browser()
        await ui.page.goto("https://example.com")
        await ui.click_element("#button")
        await ui.take_screenshot("result.png")

asyncio.run(main())
```

### Database Testing

```python
import asyncio
from py_web_automation import DBClient, Config

async def main():
    config = Config()
    db = await DBClient.create(
        "https://example.com",
        config,
        db_type="postgresql",
        connection_string="postgresql://user:pass@localhost/db"
    )
    async with db:
        results = await db.execute_query("SELECT * FROM users WHERE id = :id", {"id": 1})
        print(results)

asyncio.run(main())
```

## Available Clients

- **ApiClient**: HTTP REST API testing
- **GraphQLClient**: GraphQL API testing
- **GrpcClient**: gRPC API testing
- **SoapClient**: SOAP API testing
- **WebSocketClient**: WebSocket communication
- **UiClient**: Browser automation with Playwright
- **DBClient**: Database operations with multiple backend support

## Documentation

- **[Comprehensive Guide](docs/comprehensive-guide.md)** - Полное руководство по всему функционалу ⭐
- [Quick Start Guide](docs/quickstart.md)
- [API Reference](docs/api-reference.md)
- [Architecture](docs/architecture.md)
- [Examples](docs/examples.md)
- [Testing Guide](docs/testing.md)
- [Troubleshooting](docs/troubleshooting.md)

## Requirements

- Python >= 3.13
- See `pyproject.toml` for dependencies

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

