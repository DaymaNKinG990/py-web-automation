"""
Web automation testing framework.

A comprehensive library for automated testing of web applications,
providing clients for API testing (REST, GraphQL, gRPC, SOAP),
UI testing, and database operations.
"""

from .cache import CacheEntry, ResponseCache
from .circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitBreakerStats, CircuitState
from .clients import (
    ApiClient,
    ApiResult,
    DBClient,
    GraphQLClient,
    GrpcClient,
    SoapClient,
    UiClient,
    WebSocketClient,
)
from .config import Config
from .exceptions import (
    AuthenticationError,
    CircuitBreakerOpenError,
    ConfigurationError,
    ConnectionError,
    NotFoundError,
    OperationError,
    TimeoutError,
    ValidationError,
    WebAutomationError,
)
from .metrics import Metrics
from .middleware import (
    AuthMiddleware,
    LoggingMiddleware,
    MetricsMiddleware,
    Middleware,
    MiddlewareChain,
    RequestContext,
    ResponseContext,
    ValidationMiddleware,
)
from .page_objects import BasePage, Component, PageFactory
from .plugins import HookContext, HookType, LoggingPlugin, MetricsPlugin, Plugin, PluginManager
from .query_builder import QueryBuilder
from .rate_limit import RateLimitConfig, RateLimiter
from .retry import RetryConfig, retry_on_connection_error, retry_on_failure
from .validators import (
    create_schema_from_dict,
    validate_api_result,
    validate_json_response,
    validate_response,
)
from .visual_testing import VisualComparator, VisualDiff, take_baseline_screenshot

__all__ = [
    "Config",
    "ApiClient",
    "GraphQLClient",
    "GrpcClient",
    "SoapClient",
    "UiClient",
    "DBClient",
    "WebSocketClient",
    "ApiResult",
    # Exceptions
    "WebAutomationError",
    "ConfigurationError",
    "ConnectionError",
    "ValidationError",
    "OperationError",
    "TimeoutError",
    "AuthenticationError",
    "NotFoundError",
    "CircuitBreakerOpenError",
    # Validators
    "validate_response",
    "validate_json_response",
    "validate_api_result",
    "create_schema_from_dict",
    # Retry
    "retry_on_failure",
    "retry_on_connection_error",
    "RetryConfig",
    # Middleware
    "Middleware",
    "MiddlewareChain",
    "RequestContext",
    "ResponseContext",
    "LoggingMiddleware",
    "MetricsMiddleware",
    "AuthMiddleware",
    "ValidationMiddleware",
    # Cache
    "ResponseCache",
    "CacheEntry",
    # Rate Limiting
    "RateLimiter",
    "RateLimitConfig",
    # Metrics
    "Metrics",
    # Page Objects
    "BasePage",
    "Component",
    "PageFactory",
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitState",
    "CircuitBreakerStats",
    # Query Builder
    "QueryBuilder",
    # Visual Testing
    "VisualComparator",
    "VisualDiff",
    "take_baseline_screenshot",
    # Plugins
    "Plugin",
    "PluginManager",
    "HookType",
    "HookContext",
    "LoggingPlugin",
    "MetricsPlugin",
]
