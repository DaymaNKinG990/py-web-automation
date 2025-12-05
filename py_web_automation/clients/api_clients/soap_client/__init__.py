"""
SOAP API client for web automation testing.

This module provides SoapClient for testing SOAP API endpoints.
"""

from .metrics import Metrics
from .middleware import (
    AuthMiddleware,
    LoggingMiddleware,
    MetricsMiddleware,
    Middleware,
    MiddlewareChain,
    RateLimitMiddleware,
    RetryMiddleware,
)
from .rate_limit import RateLimitConfig, RateLimiter
from .retry import RetryConfig, RetryHandler
from .soap_client import SoapClient
from .soap_result import SoapResult

__all__ = [
    "SoapClient",
    "SoapResult",
    "Metrics",
    "RateLimiter",
    "RateLimitConfig",
    "RetryConfig",
    "RetryHandler",
    "Middleware",
    "MiddlewareChain",
    "AuthMiddleware",
    "LoggingMiddleware",
    "MetricsMiddleware",
    "RetryMiddleware",
    "RateLimitMiddleware",
]
