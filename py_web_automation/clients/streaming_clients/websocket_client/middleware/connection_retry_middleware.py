"""
Connection retry middleware for WebSocket client.

This module provides ConnectionRetryMiddleware for automatic WebSocket reconnection.
"""

# Local imports
from ..retry import RetryHandler
from ..websocket_result import WebSocketResult
from .context import _WebSocketConnectionContext, _WebSocketMessageContext
from .middleware import Middleware


class ConnectionRetryMiddleware(Middleware):
    """
    Middleware for automatic WebSocket connection retry.

    Handles reconnection logic when connection fails or is lost.

    Attributes:
        retry_handler: Retry handler instance

    Example:
        >>> from py_web_automation.clients.websocket_client import WebSocketClient, MiddlewareChain
        >>> from py_web_automation.clients.websocket_client.middleware import (
        ...     ConnectionRetryMiddleware
        ... )
        >>> from py_web_automation.clients.websocket_client import RetryConfig, RetryHandler
        >>> retry_config = RetryConfig(max_attempts=3, delay=1.0, backoff=2.0)
        >>> retry_handler = RetryHandler(retry_config)
        >>> retry_middleware = ConnectionRetryMiddleware(retry_handler)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(retry_middleware)
        >>> async with WebSocketClient(
        ...     "ws://example.com/ws", config, middleware=middleware_chain
        ... ) as ws:
        ...     await ws.send_message({"type": "ping"})
    """

    def __init__(self, retry_handler: RetryHandler) -> None:
        """
        Initialize connection retry middleware.

        Args:
            retry_handler: Retry handler instance
        """
        self.retry_handler = retry_handler
        self._retry_count: int = 0
        self._should_retry: bool = False

    async def process_message(self, context: _WebSocketMessageContext) -> None:
        """
        No-op for messages.

        Args:
            context: Message context
        """
        pass

    async def process_connection(self, context: _WebSocketConnectionContext) -> None:
        """
        Track connection events and set retry flag if needed.

        Args:
            context: Connection context
        """
        if context.event_type == "connect":
            self._retry_count = 0
            self._should_retry = False
        elif context.event_type == "disconnect":
            # Check if retry is needed
            if self._retry_count < self.retry_handler.config.max_attempts:
                self._should_retry = True
                self._retry_count += 1
                context.metadata_context["should_retry"] = True
                attempt_index = self._retry_count - 1
                delay = self.retry_handler.config.calculate_delay(attempt_index)
                context.metadata_context["retry_delay"] = delay
            else:
                self._should_retry = False

    async def process_error(
        self,
        context: _WebSocketConnectionContext | _WebSocketMessageContext,
        error: Exception,
    ) -> WebSocketResult | None:
        """
        Handle connection errors and set retry metadata.

        Args:
            context: Connection or message context
            error: Exception that occurred
        """
        if isinstance(context, _WebSocketConnectionContext):
            if context.event_type == "connect":
                # Delegate to retry handler for connection errors
                result = await self.retry_handler.handle_error(context, error)
                if result is None and context.metadata_context.get("should_retry"):
                    # Retry handler set should_retry flag
                    self._retry_count = context.metadata_context.get("retry_attempt", 0)
                    self._should_retry = True
        return None
