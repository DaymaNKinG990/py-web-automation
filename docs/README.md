# Web Automation Framework Documentation

This directory contains comprehensive documentation for the Web Automation Framework.

## Documentation Structure

### Getting Started
- [Installation Guide](installation.md) - How to install and setup the framework
- [Quick Start Guide](quickstart.md) - Get started with the framework in minutes

### Core Documentation
- [Comprehensive Guide](comprehensive-guide.md) - **Complete guide to all functionality** ⭐
- [API Reference](api-reference.md) - Complete API documentation with all classes and methods
- [Examples](examples.md) - Detailed examples and use cases for all clients
- [Architecture](architecture.md) - Framework architecture and design decisions
- [Features](features.md) - Framework features and capabilities

### Testing & Development
- [Testing Documentation](testing.md) - Comprehensive testing guide, coverage, and best practices
- [CI/CD Setup](ci-cd-setup.md) - Continuous integration and deployment configuration

### Support
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## Framework Overview

The Web Automation Framework provides clients for testing various aspects of web applications:

### API Clients
- **HttpClient** - HTTP REST API testing with middleware support
- **GraphQLClient** - GraphQL API testing with query validation
- **GrpcClient** - gRPC service testing
- **SoapClient** - SOAP web service testing

### Streaming Clients
- **WebSocketClient** - WebSocket communication with message handling

### UI Clients
- **AsyncUiClient** - Asynchronous browser automation (Playwright)
- **SyncUiClient** - Synchronous browser automation (Playwright)

### Database Clients
- **SQLiteClient** - SQLite database operations
- **PostgreSQLClient** - PostgreSQL database operations
- **MySQLClient** - MySQL database operations

### Broker Clients
- **KafkaClient** - Apache Kafka message broker
- **RabbitMQClient** - RabbitMQ message broker

## Quick Import Examples

```python
# Configuration and Exceptions
from py_web_automation import Config
from py_web_automation.exceptions import WebAutomationError

# API Clients
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient

# UI Clients
from py_web_automation.clients.ui_clients import AsyncUiClient

# Database Clients
from py_web_automation.clients.db_clients.sqlite_client import SQLiteClient
```

## Getting Started

1. Start with the [Installation Guide](installation.md) to set up the framework
2. Follow the [Quick Start Guide](quickstart.md) for your first steps
3. Explore the [Examples](examples.md) for practical use cases
4. Refer to the [API Reference](api-reference.md) for detailed method documentation
5. Check the [Architecture](architecture.md) to understand design decisions

## Documentation Guide

- **New to the framework?** Start with [Installation](installation.md) → [Quick Start](quickstart.md) → [Examples](examples.md)
- **Looking for specific functionality?** Check [API Reference](api-reference.md) or [Comprehensive Guide](comprehensive-guide.md)
- **Having issues?** See [Troubleshooting](troubleshooting.md)
- **Want to understand the design?** Read [Architecture](architecture.md)

## Contributing

If you find any issues with the documentation or want to contribute improvements, please refer to the main project repository.
