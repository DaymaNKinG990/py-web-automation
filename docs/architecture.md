# Architecture

This document describes the architecture and design decisions of the Web Automation Framework.

## Overview

The Web Automation Framework is designed as a comprehensive library for automated testing of web applications. It provides separate classes for different testing concerns, following the Single Responsibility Principle and SOLID principles.

## Core Principles

### 1. Separation of Concerns

The framework separates different testing responsibilities:

- **ApiClient**: HTTP REST API testing
- **GraphQLClient**: GraphQL API testing
- **GrpcClient**: gRPC API testing
- **SoapClient**: SOAP API testing
- **WebSocketClient**: WebSocket communication
- **UiClient**: Browser-based UI testing with Playwright
- **DBClient**: Database client with support for multiple backends (PostgreSQL, MySQL, SQLite)

### 2. Async-First Design

All operations are asynchronous to support:
- Non-blocking HTTP requests
- Concurrent testing scenarios
- Better performance with I/O operations
- Efficient resource utilization

### 3. High Performance

Uses `msgspec` for:
- Fast data serialization/deserialization (2-4x faster than Pydantic)
- Efficient validation (2-3x faster)
- Lower memory usage compared to alternatives
- Runtime type checking

### 4. Simple Configuration

Configuration is handled through:
- Environment variables
- YAML files
- Config objects with sensible defaults
- Type-safe configuration with validation

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ApiClient     │    │ GraphQLClient   │    │   GrpcClient    │    │   SoapClient    │
│                 │    │                 │    │                 │    │                 │
│ • HTTP Client   │    │ • GraphQL       │    │ • gRPC          │    │ • SOAP          │
│ • REST API      │    │ • Queries       │    │ • Protobuf       │    │ • XML           │
│ • Validation    │    │ • Mutations     │    │ • Streaming     │    │ • WSDL          │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         └───────────────────────┼───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   BaseClient    │
                    │                 │
                    │ • URL           │
                    │ • Config        │
                    │ • Logging       │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ WebSocketClient │    │   UiClient      │    │   DBClient      │
│                 │    │                 │    │                 │
│ • WebSocket     │    │ • Playwright    │    │ • PostgreSQL    │
│ • Messages      │    │ • Browser       │    │ • SQLite        │
│ • Handlers      │    │ • UI Testing    │    │ • MySQL         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Config      │
                    │                 │
                    │ • Timeouts      │
                    │ • Retry         │
                    │ • Logging       │
                    │ • Browser       │
                    └─────────────────┘
```

## Class Responsibilities

### ApiClient

**Purpose**: Test HTTP REST API endpoints

**Responsibilities**:
- HTTP request handling
- Response analysis
- Error handling
- Request/response logging

**Dependencies**:
- `httpx` for HTTP client
- `Config` for configuration

**Key Methods**:
- `make_request()` - Make HTTP requests
- `build_request()` - Create request builder

### GraphQLClient

**Purpose**: Test GraphQL API endpoints

**Responsibilities**:
- GraphQL query execution
- Mutation execution
- Variable handling
- Response parsing

**Dependencies**:
- `httpx` for HTTP client
- `Config` for configuration

### GrpcClient

**Purpose**: Test gRPC services

**Responsibilities**:
- gRPC method calls
- Protobuf serialization/deserialization
- Streaming support
- Service discovery

**Dependencies**:
- `grpclib` for gRPC client
- `Config` for configuration

### SoapClient

**Purpose**: Test SOAP web services

**Responsibilities**:
- SOAP request construction
- WSDL parsing
- XML serialization
- SOAP fault handling

**Dependencies**:
- `zeep` for SOAP client
- `Config` for configuration

### WebSocketClient

**Purpose**: Test WebSocket connections

**Responsibilities**:
- WebSocket connection management
- Message sending and receiving
- Async message listening
- Message handler registration

**Dependencies**:
- `websockets` for WebSocket client
- `Config` for configuration

**Key Methods**:
- `send_message()` - Send WebSocket message
- `receive_message()` - Receive WebSocket message
- `listen()` - Async iterator for messages

### UiClient

**Purpose**: Test web application user interface

**Responsibilities**:
- Browser automation
- UI element interaction
- Screenshot capture
- JavaScript execution
- Form handling

**Dependencies**:
- `playwright` for browser automation
- `Config` for configuration

**Key Methods**:
- `setup_browser()` - Initialize browser
- `click_element()` - Click elements
- `fill_input()` - Fill form fields
- `take_screenshot()` - Capture screenshots
- `execute_script()` - Execute JavaScript

**Design Decisions**:
- Uses Playwright for modern browser automation
- Supports headless and headed modes
- Focused on UI testing only

### DBClient

**Purpose**: Database client for testing applications with database backends

**Responsibilities**:
- Database connection management
- Query execution (SELECT, INSERT, UPDATE, DELETE)
- Transaction handling
- Support for multiple database backends

**Dependencies**:
- Database-specific libraries (asyncpg, psycopg, aiosqlite, aiomysql, pymysql)
- `Config` for configuration

**Supported Backends**:
- **PostgreSQL**: via `asyncpg` or `psycopg`
- **SQLite**: via `aiosqlite`
- **MySQL**: via `aiomysql` or `pymysql`

**Key Methods**:
- `connect()` - Establish database connection
- `disconnect()` - Close database connection
- `execute_query()` - Execute SELECT queries
- `execute_command()` - Execute INSERT/UPDATE/DELETE commands
- `begin_transaction()` - Start transaction
- `commit_transaction()` - Commit transaction
- `rollback_transaction()` - Rollback transaction
- `transaction()` - Context manager for transactions

**Factory Method**:
- `DBClient.create()` - Create database client instance based on `db_type`

**Design Decisions**:
- Pluggable adapter pattern for different database backends
- Automatic adapter detection based on available libraries
- Unified interface across all database backends
- Support for both connection strings and keyword arguments

### Config

**Purpose**: Centralized configuration management

**Responsibilities**:
- Environment variable handling
- Configuration validation
- Default value management
- YAML file loading

**Dependencies**:
- `msgspec` for data validation
- `loguru` for logging configuration

**Key Features**:
- Type-safe configuration
- Environment variable support
- YAML file support
- Validation with helpful error messages

## Data Models

### msgspec Integration

All data models use `msgspec.Struct` for:

**Benefits**:
- 2-4x faster serialization than Pydantic
- 2-3x faster validation
- 2-3x less memory usage
- Runtime type checking
- Zero-cost validation

**Models**:
- `ApiResult` - API request results
- Response models for different clients

## Error Handling Strategy

### Exception Hierarchy

```
Exception
├── WebAutomationError (Base)
│   ├── ConfigurationError
│   ├── ConnectionError
│   ├── ValidationError
│   ├── OperationError
│   ├── TimeoutError
│   ├── AuthenticationError
│   └── NotFoundError
```

### Error Handling Patterns

1. **Explicit Exception Raising**: Methods raise specific exceptions instead of returning None
2. **Error Context**: All exceptions include both message and details
3. **Proper Exception Chaining**: Using `from e` for exception chaining
4. **Structured Error Information**: Error details provide context

## Resource Management

### Context Managers

All classes implement context managers for proper resource cleanup:

```python
async with ApiClient(url, config) as api:
    # Automatic cleanup on exit
    result = await api.make_request("/endpoint")
# HTTP client automatically closed
```

### Resource Lifecycle

1. **Initialization**: Create objects with configuration
2. **Setup**: Initialize resources (browser, HTTP client, database connection)
3. **Usage**: Perform testing operations
4. **Cleanup**: Automatic resource cleanup via context managers

## Design Patterns

### Factory Pattern

**Location**: `DBClient.create()`

**Purpose**: Create database clients based on type string

**Benefits**:
- Decouples client creation from concrete implementations
- Easy to add new database types
- Centralized creation logic

### Strategy Pattern

**Location**: Database adapters, HTTP request handling

**Purpose**: Interchangeable algorithms for different database backends

**Benefits**:
- Easy to switch between database implementations
- Consistent interface across different backends

### Adapter Pattern

**Location**: `db_adapters/` directory

**Purpose**: Adapt different database libraries to common interface

**Benefits**:
- Support for multiple database libraries
- Automatic detection of available libraries
- Unified interface for all backends

### Template Method Pattern

**Location**: `BaseClient` and its subclasses

**Purpose**: Define skeleton of algorithm in base class

**Benefits**:
- Common behavior in base class
- Specific behavior in subclasses
- Consistent structure across clients

### Builder Pattern

**Location**: `RequestBuilder`

**Purpose**: Fluent API for constructing complex HTTP requests

**Benefits**:
- Readable request construction
- Method chaining
- Reusable builder instances

## Performance Considerations

### HTTP Client Optimization

- Connection pooling with `httpx.Limits`
- Keep-alive connections
- Configurable timeouts
- Retry logic with exponential backoff

### Browser Optimization

- Headless mode for faster execution
- Single browser instance per test session
- Efficient element selection
- Screenshot optimization

### Memory Management

- `msgspec` for efficient serialization
- Automatic cleanup via context managers
- Minimal object creation
- Efficient data structures

## Testing Strategy

### Unit Testing

- Each class tested independently
- Mock external dependencies
- Test error conditions
- Validate configuration

### Integration Testing

- Test class interactions
- Real HTTP requests (with test endpoints)
- Browser automation tests
- End-to-end scenarios

### Performance Testing

- Benchmark serialization/deserialization
- Measure HTTP request times
- Browser automation performance
- Memory usage monitoring

## Security Considerations

### Authentication

- Secure credential storage
- Environment variable support
- No sensitive data in logs
- Secure transmission

### Browser Security

- Headless mode for security
- No sensitive data in screenshots
- Secure file handling
- Sandboxed execution

## Extensibility

### Plugin Architecture

The framework is designed for easy extension:

1. **Custom Validators**: Add custom validation logic
2. **Custom Clients**: Implement custom HTTP clients
3. **Custom Browsers**: Add support for other browsers
4. **Custom Models**: Extend data models

### Configuration Extensions

- Custom configuration sources
- Environment-specific settings
- Dynamic configuration updates
- Validation rule extensions

## Future Considerations

### Potential Enhancements

1. **Parallel Testing**: Support for concurrent test execution
2. **Test Reporting**: Integration with test reporting tools
3. **Mock Servers**: Built-in mock server for testing
4. **CI/CD Integration**: Better CI/CD pipeline support

### Scalability

- Horizontal scaling support
- Distributed testing capabilities
- Resource pooling
- Load balancing

## Design Trade-offs

### Simplicity vs. Features

**Chosen**: Simplicity
- Focused on core functionality
- Easy to understand and use
- Minimal dependencies
- Clear separation of concerns

### Performance vs. Flexibility

**Chosen**: Performance
- `msgspec` over Pydantic
- Optimized HTTP client
- Efficient browser usage
- Minimal overhead

### Synchronous vs. Asynchronous

**Chosen**: Asynchronous
- Better I/O performance
- Support for concurrent operations
- Modern Python patterns
- Future-proof design
