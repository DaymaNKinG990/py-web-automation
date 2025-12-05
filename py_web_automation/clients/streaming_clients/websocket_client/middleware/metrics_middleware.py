"""
Metrics middleware for WebSocket client.

This module provides MetricsMiddleware for collecting WebSocket metrics.
"""

# Python imports
from time import time

# Local imports
from ..metrics import Metrics
from ..websocket_result import WebSocketResult
from .context import _WebSocketConnectionContext, _WebSocketMessageContext
from .middleware import Middleware


class MetricsMiddleware(Middleware):
    """
    Middleware for collecting performance metrics for WebSocket operations.

    Collects metrics about messages sent/received, connection lifetime, and errors.

    Attributes:
        metrics: Metrics object for storing collected data

    Example:
        >>> from py_web_automation.clients.websocket_client import WebSocketClient, MiddlewareChain
        >>> from py_web_automation.clients.websocket_client.middleware import MetricsMiddleware
        >>> from py_web_automation.clients.websocket_client import Metrics
        >>> metrics = Metrics()
        >>> metrics_middleware = MetricsMiddleware(metrics)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(metrics_middleware)
        >>> async with WebSocketClient(
        ...     "ws://example.com/ws", config, middleware=middleware_chain
        ... ) as ws:
        ...     await ws.send_message({"type": "ping"})
        ...     print(metrics.get_summary())
    """

    def __init__(self, metrics: Metrics | None = None) -> None:
        """
        Initialize metrics middleware.

        Args:
            metrics: Metrics object to use (creates new one if None)
        """
        if metrics is None:
            metrics = Metrics()
        self.metrics = metrics
        self._connection_start_time: float | None = None

    async def process_message(self, context: _WebSocketMessageContext) -> None:
        """
        Record message metrics.

        Args:
            context: Message context
        """
        # For sent messages, record immediately
        if context.direction == "send":
            self.metrics.record_request(success=True, latency=0.0, error_type=None)
        # For received messages, track timestamp
        elif context.direction == "receive":
            context.metadata_context["receive_timestamp"] = time()
            self.metrics.record_request(success=True, latency=0.0, error_type=None)

    async def process_connection(self, context: _WebSocketConnectionContext) -> None:
        """
        Record connection metrics.

        Args:
            context: Connection context
        """
        if context.event_type == "connect":
            self._connection_start_time = time()
            context.metadata_context["connection_start_time"] = self._connection_start_time
        elif context.event_type == "disconnect" and self._connection_start_time:
            connection_duration = time() - self._connection_start_time
            # Record connection lifetime as latency
            self.metrics.record_request(success=True, latency=connection_duration, error_type=None)
            self._connection_start_time = None

    async def process_error(
        self,
        context: _WebSocketMessageContext | _WebSocketConnectionContext,
        error: Exception,
    ) -> WebSocketResult | None:
        """
        Record error metrics.

        Args:
            context: Message or connection context
            error: Exception that occurred
        """
        error_type = type(error).__name__
        self.metrics.record_request(success=False, latency=0.0, error_type=error_type)
        return None
