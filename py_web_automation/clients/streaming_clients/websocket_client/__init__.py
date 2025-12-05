"""
WebSocket API client for web automation testing.

This module provides WebSocketClient for testing WebSocket connections.
"""

from .metrics import Metrics
from .middleware import (
    ConnectionRetryMiddleware,
    LoggingMiddleware,
    MetricsMiddleware,
    Middleware,
    MiddlewareChain,
    RateLimitMiddleware,
)
from .rate_limit import RateLimitConfig, RateLimiter
from .retry import RetryConfig, RetryHandler
from .websocket_client import WebSocketClient
from .websocket_result import WebSocketResult

__all__ = [
    "WebSocketClient",
    "WebSocketResult",
    "Metrics",
    "RateLimiter",
    "RateLimitConfig",
    "RetryConfig",
    "RetryHandler",
    "Middleware",
    "MiddlewareChain",
    "LoggingMiddleware",
    "MetricsMiddleware",
    "RateLimitMiddleware",
    "ConnectionRetryMiddleware",
]
