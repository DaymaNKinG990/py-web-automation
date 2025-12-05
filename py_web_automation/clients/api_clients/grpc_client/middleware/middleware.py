"""
Middleware system for gRPC request/response interception and modification.

This module provides a middleware/interceptor system that allows hooking into
the gRPC unary call lifecycle for logging, metrics, validation, and modification.
"""

# Python imports
from abc import ABC, abstractmethod

# Local imports
from ..grpc_result import GrpcResult
from .context import _GrpcRequestContext, _GrpcResponseContext


class Middleware(ABC):
    """
    Base class for gRPC middleware implementations.

    Middleware can intercept and modify unary RPC calls before they are sent
    and responses after they are received.

    Note: Middleware is only applied to unary calls. Streaming calls
    bypass middleware system as they work with AsyncIterator.

    Example:
        >>> class LoggingMiddleware(Middleware):
        ...     async def process_request(self, context: _GrpcRequestContext) -> None:
        ...         print(f"Request: {context.service}.{context.method}")
        ...     async def process_response(self, context: _GrpcResponseContext) -> None:
        ...         print(f"Response: {context.result.success}")
    """

    @abstractmethod
    async def process_request(self, context: _GrpcRequestContext) -> None:
        """
        Process request before it is sent.

        Can modify context.metadata, context.request, etc.

        Args:
            context: Request context that can be modified
        """
        pass

    @abstractmethod
    async def process_response(self, context: _GrpcResponseContext) -> None:
        """
        Process response after it is received.

        Can modify context.result or access context.metadata_context.

        Args:
            context: Response context that can be modified
        """
        pass

    async def process_error(
        self, context: _GrpcRequestContext, error: Exception
    ) -> GrpcResult | None:
        """
        Process error that occurred during call.

        Can return a modified GrpcResult to replace the error response,
        or return None to let the error propagate.

        Args:
            context: Request context
            error: Exception that occurred

        Returns:
            Optional GrpcResult to replace error, or None to propagate error
        """
        return None


class MiddlewareChain:
    """
    Chain of middleware to process gRPC unary calls.

    Executes middleware in order for requests and in reverse order for responses.

    Attributes:
        _middleware: List of middleware instances

    Example:
        >>> chain = MiddlewareChain()
        >>> chain.add(LoggingMiddleware())
        >>> chain.add(MetricsMiddleware())
        >>> # Use chain in GrpcClient
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

    async def process_request(self, context: _GrpcRequestContext) -> None:
        """
        Process request through all middleware.

        Args:
            context: Request context to process
        """
        for middleware in self._middleware:
            await middleware.process_request(context)

    async def process_response(self, context: _GrpcResponseContext) -> None:
        """
        Process response through all middleware (in reverse order).

        Args:
            context: Response context to process
        """
        for middleware in reversed(self._middleware):
            await middleware.process_response(context)

    async def process_error(
        self, context: _GrpcRequestContext, error: Exception
    ) -> GrpcResult | None:
        """
        Process error through all middleware (in reverse order).

        Args:
            context: Request context
            error: Exception that occurred

        Returns:
            Optional GrpcResult to replace error, or None
        """
        for middleware in reversed(self._middleware):
            result = await middleware.process_error(context, error)
            if result is not None:
                return result
        return None
