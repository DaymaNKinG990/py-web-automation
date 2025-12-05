"""
Middleware system for WebSocket message and connection interception.

This module provides a middleware/interceptor system that allows hooking into
the WebSocket lifecycle for logging, metrics, message transformation, and connection handling.
"""

# Python imports
from abc import ABC, abstractmethod

# Local imports
from ..websocket_result import WebSocketResult
from .context import _WebSocketConnectionContext, _WebSocketMessageContext


class Middleware(ABC):
    """
    Base class for WebSocket middleware implementations.

    Middleware can intercept and modify WebSocket messages before they are sent
    or after they are received, and handle connection events.

    Example:
        >>> class LoggingMiddleware(Middleware):
        ...     async def process_message(self, context: _WebSocketMessageContext) -> None:
        ...         print(f"Message: {context.direction} {context.message}")
        ...     async def process_connection(self, context: _WebSocketConnectionContext) -> None:
        ...         print(f"Connection: {context.event_type}")
    """

    @abstractmethod
    async def process_message(self, context: _WebSocketMessageContext) -> None:
        """
        Process message before sending or after receiving.

        Can modify context.message for message transformation.

        Args:
            context: Message context that can be modified
        """
        pass

    @abstractmethod
    async def process_connection(self, context: _WebSocketConnectionContext) -> None:
        """
        Process connection event (connect/disconnect).

        Args:
            context: Connection context
        """
        pass

    async def process_error(
        self,
        context: _WebSocketMessageContext | _WebSocketConnectionContext,
        error: Exception,
    ) -> WebSocketResult | None:
        """
        Process error that occurred during operation.

        Can return a WebSocketResult to replace the error response,
        or return None to let the error propagate.

        Args:
            context: Message or connection context
            error: Exception that occurred

        Returns:
            Optional WebSocketResult to replace error, or None to propagate error
        """
        return None


class MiddlewareChain:
    """
    Chain of middleware to process WebSocket messages and connections.

    Executes middleware in order for messages and connections.

    Attributes:
        _middleware: List of middleware instances

    Example:
        >>> chain = MiddlewareChain()
        >>> chain.add(LoggingMiddleware())
        >>> chain.add(MetricsMiddleware())
        >>> # Use chain in WebSocketClient
    """

    def __init__(self) -> None:
        """Initialize empty middleware chain."""
        self._middleware: list[Middleware] = []

    def add(self, middleware: Middleware) -> "MiddlewareChain":
        """
        Add middleware to the chain.

        Args:
            middleware: Middleware instance to add

        Returns:
            Self for method chaining

        Example:
            >>> chain.add(LoggingMiddleware()).add(MetricsMiddleware())
        """
        self._middleware.append(middleware)
        return self

    def remove(self, middleware: Middleware) -> "MiddlewareChain":
        """
        Remove middleware from the chain.

        Args:
            middleware: Middleware instance to remove

        Returns:
            Self for method chaining
        """
        if middleware in self._middleware:
            self._middleware.remove(middleware)
        return self

    async def process_message(self, context: _WebSocketMessageContext) -> None:
        """
        Process message through all middleware.

        Args:
            context: Message context to process
        """
        for middleware in self._middleware:
            await middleware.process_message(context)

    async def process_connection(self, context: _WebSocketConnectionContext) -> None:
        """
        Process connection event through all middleware.

        Args:
            context: Connection context to process
        """
        for middleware in self._middleware:
            await middleware.process_connection(context)

    async def process_error(
        self,
        context: _WebSocketMessageContext | _WebSocketConnectionContext,
        error: Exception,
    ) -> WebSocketResult | None:
        """
        Process error through all middleware (in reverse order).

        Args:
            context: Message or connection context
            error: Exception that occurred

        Returns:
            Optional WebSocketResult to replace error, or None
        """
        for middleware in reversed(self._middleware):
            result = await middleware.process_error(context, error)
            if result is not None:
                return result
        return None
