"""
HTTP client for HTTP requests and REST API testing.

This module provides HttpClient class for making HTTP requests to REST APIs
and RequestBuilder for constructing complex HTTP requests with a fluent API.
"""

# Local imports
from .http_client import HttpClient
from .http_result import HttpResult
from .metrics import Metrics
from .middleware import (
    AuthMiddleware,
    LoggingMiddleware,
    MetricsMiddleware,
    Middleware,
    MiddlewareChain,
    RateLimitMiddleware,
    RetryMiddleware,
    ValidationMiddleware,
)
from .rate_limit import RateLimitConfig, RateLimiter
from .retry import RetryConfig, RetryHandler

__all__ = [
    "HttpClient",
    "HttpResult",
    "AuthMiddleware",
    "LoggingMiddleware",
    "MetricsMiddleware",
    "Middleware",
    "MiddlewareChain",
    "RateLimitMiddleware",
    "RetryMiddleware",
    "ValidationMiddleware",
    "RetryConfig",
    "RetryHandler",
    "RateLimitConfig",
    "RateLimiter",
    "Metrics",
]
