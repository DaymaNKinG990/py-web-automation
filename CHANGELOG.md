# Changelog

All notable changes to py-web-automation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - Current Release

### Added

#### Core Infrastructure
- Comprehensive framework structure with modular client architecture
- Unified configuration system (`Config`) with environment variables and YAML support
- Structured exception hierarchy with specific error types
- Complete type annotations with 100% coverage
- Comprehensive test coverage (95%) with Allure reports
- CI/CD setup with GitHub Actions

#### API Clients
- **HttpClient**: HTTP REST API client with full middleware support
  - Request Builder fluent API for complex request construction
  - Response validation with msgspec
  - Custom middleware system (Auth, Logging, Metrics, Rate Limit, Retry, Validation)
  - Standardized result objects (`HttpResult`)
  
- **GraphQLClient**: GraphQL API client with query validation
  - Query and mutation execution
  - Operation name and variables support
  - Schema introspection
  - Full middleware integration
  
- **GrpcClient**: gRPC service client
  - Unary call support
  - Metadata handling
  - Service method discovery
  - Middleware support (Auth, Logging, Metrics, Rate Limit, Retry)
  
- **SoapClient**: SOAP web service client
  - SOAP 1.1 and 1.2 support
  - WSDL parsing and operation discovery
  - Namespace handling
  - Middleware support (Auth, Logging, Metrics, Rate Limit, Retry)

#### Streaming Clients
- **WebSocketClient**: WebSocket communication client
  - Bidirectional messaging
  - Secure connections (wss://)
  - Message handlers and listeners
  - Connection lifecycle management
  - Middleware support (Logging, Metrics, Rate Limit, Connection Retry)

#### UI Clients
- **AsyncUiClient**: Asynchronous browser automation with Playwright
  - Full Playwright API access
  - Page navigation and interaction
  - Screenshot and PDF generation
  - Network interception
  - Visual testing utilities
  
- **SyncUiClient**: Synchronous browser automation with Playwright
  - Same features as AsyncUiClient in synchronous mode
  
- **Page Object Model (POM)**: Structured UI testing
  - BasePage and Component classes
  - PageFactory for page initialization
  - Component reuse and composition
  
- **Visual Testing**: Visual regression testing utilities
  - Screenshot comparison
  - Hash-based change detection
  - Diff image generation

#### Database Clients
- **SQLiteClient**: SQLite database operations
- **PostgreSQLClient**: PostgreSQL database operations
- **MySQLClient**: MySQL database operations
- **QueryBuilder**: Fluent SQL query builder
  - SELECT, INSERT, UPDATE, DELETE operations
  - JOIN, WHERE, GROUP BY, HAVING, ORDER BY clauses
  - OR conditions support
  - Batch INSERT operations
  - UPSERT (INSERT ... ON CONFLICT) support
  - Transaction support

#### Message Broker Clients
- **KafkaClient**: Apache Kafka message broker client
  - Message publishing and consuming
  - Consumer groups support
  - Topic management
  
- **RabbitMQClient**: RabbitMQ message broker client
  - Queue and exchange operations
  - Message publishing and consuming
  - Routing key support

#### Middleware System
- **Middleware Architecture**: Unified middleware system across all API clients
  - Request/Response processing pipeline
  - Context-based middleware communication
  - Extensible middleware interface
  
- **Built-in Middleware**:
  - `AuthMiddleware`: Authentication handling (Bearer, Basic, API Key)
  - `LoggingMiddleware`: Request/Response logging
  - `MetricsMiddleware`: Performance metrics collection
  - `RateLimitMiddleware`: Request rate limiting (sliding window algorithm)
  - `RetryMiddleware`: Automatic retry with exponential backoff
  - `ValidationMiddleware`: Request/Response validation (GraphQL, HTTP)

#### Supporting Features
- **Retry Mechanism**: Exponential backoff retry with jitter
  - Configurable retry attempts and delays
  - Retry on specific exceptions
  - Client-specific retry handlers
  
- **Rate Limiting**: Sliding window rate limiting algorithm
  - Configurable rate limits per client
  - Request throttling
  - Burst handling
  
- **Metrics Collection**: Performance metrics tracking
  - Request/response times
  - Success/failure rates
  - Client-specific metrics
  
- **Request Builder**: Fluent API for HTTP request construction
  - Method chaining
  - Header and query parameter management
  - Body serialization
  
- **Response Validation**: Fast schema validation using msgspec
  - Runtime type checking
  - Custom validator support

### Changed

#### Architecture Refactoring
- Removed universal `BaseClient` inheritance in favor of specialized client classes
- Introduced client categorization (API, Streaming, UI, Database, Broker)
- Unified middleware system across all API clients
- Standardized result objects for each client type
- Separated sync and async UI clients

#### Client Structure
- All clients now use standardized context objects (Request/Response Context)
- Middleware integration through constructor configuration
- Consistent error handling across all clients
- Improved resource management with context managers

#### Documentation
- Complete documentation overhaul
- Comprehensive guides for all clients
- Updated examples with current API
- Architecture documentation
- Troubleshooting guide

### Fixed

- Cyclomatic complexity reduction across all clients (all methods rated 'A')
- Eliminated code duplication through middleware system
- Improved error messages and exception handling
- Fixed type hints and type checking issues
- Resolved resource cleanup issues in clients

### Removed

- Universal `BaseClient` base class (replaced with specialized client classes)
- `CircuitBreaker` pattern implementation (removed as not necessary for QA automation)
- Plugin system (functionality integrated into middleware)
- Response caching (not implemented)
- `validators` module (replaced with msgspec validation and ValidationMiddleware)

## Migration Guides

### From Previous Versions

#### Client Imports

**Old (deprecated):**
```python
from py_web_automation import ApiClient, UiClient, DBClient
```

**New:**
```python
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.ui_clients import AsyncUiClient
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient
```

#### Client Instantiation

**Old:**
```python
async with ApiClient(url, config) as client:
    result = await client.make_request("/endpoint")
```

**New:**
```python
async with HttpClient(url, config) as client:
    result = await client.get("/endpoint")
```

#### GraphQL Client

**Old:**
```python
result = await client.execute_query(query, variables)
```

**New:**
```python
result = await client.query(query, variables=variables)
```

#### Database Client

**Old:**
```python
db = await DBClient.create(url, config, db_type="postgresql", connection_string=conn_str)
```

**New:**
```python
from py_web_automation.clients.db_clients.postgresql_client import PostgreSQLClient
db = PostgreSQLClient(connection_string=conn_str, config=config)
```

#### Result Objects

**Old:**
```python
result.success  # boolean
result.response  # response data
```

**New:**
```python
result.success  # boolean
result.json()  # or result.body for HTTP client
result.status_code  # HTTP status code
```

## Deprecation Notices

None at this time.

## Security

Security issues should be reported privately. Please do not open public issues for security vulnerabilities.

## Version History

- **1.0.0**: Current stable release with comprehensive features
