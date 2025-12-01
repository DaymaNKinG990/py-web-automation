# Changelog

All notable changes to py-web-automation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Automatic retry mechanism with exponential backoff (`retry.py`)
- Request/Response middleware system (`middleware.py`)
- Response caching with TTL support (`cache.py`)
- Rate limiting with sliding window algorithm (`rate_limit.py`)
- Performance metrics collection (`metrics.py`)
- Page Object Model (POM) support (`page_objects.py`)
- Circuit breaker pattern implementation (`circuit_breaker.py`)
- Query builder for SQL queries (`query_builder.py`)
- Visual regression testing utilities (`visual_testing.py`)
- Plugin system for extending functionality (`plugins.py`)
- LICENSE file (MIT)
- CONTRIBUTING.md guide
- CHANGELOG.md

### Changed
- `ApiClient` now supports middleware, caching, and rate limiting
- `ApiResult` now includes `metadata` field for middleware communication
- Enhanced `__init__.py` exports for new modules

### Fixed
- Fixed metadata handling in middleware

## [3.2.0] - Current

### Added
- Comprehensive test coverage (95%)
- Allure test reports integration
- CI/CD setup with GitHub Actions
- Complete type annotations (100%)
- Multiple protocol support (REST, GraphQL, gRPC, SOAP, WebSocket)
- Database client with adapter pattern (PostgreSQL, MySQL, SQLite)
- Request Builder fluent API
- Response validation with msgspec
- Structured exception hierarchy

### Changed
- Refactored from TMA Framework to universal web automation framework
- Removed Telegram-specific dependencies
- Updated all documentation

## [3.1.0] - Previous

### Added
- Initial framework structure
- Basic API and UI clients
- Configuration management

## [3.0.0] - Initial Release

### Added
- Core framework functionality
- Basic clients for API and UI testing

---

## Version History

- **3.2.0**: Current stable version with comprehensive features
- **3.1.0**: Framework refactoring and improvements
- **3.0.0**: Initial release

---

## Migration Guides

### From 3.1.0 to 3.2.0

No breaking changes. All existing code should work without modifications.

### From 3.0.0 to 3.1.0

- Removed Telegram-specific features
- Updated import paths
- Changed configuration structure

---

## Deprecation Notices

None at this time.

---

## Security

Security issues should be reported privately. Please do not open public issues for security vulnerabilities.

