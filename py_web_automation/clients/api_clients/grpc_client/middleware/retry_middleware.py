"""
Retry middleware for gRPC client.

This module provides RetryMiddleware for automatic retry of failed gRPC unary calls.
"""

# Local imports
from ..grpc_result import GrpcResult
from ..retry import RetryHandler
from .context import _GrpcRequestContext, _GrpcResponseContext
from .middleware import Middleware


class RetryMiddleware(Middleware):
    """
    Middleware for automatic retry of failed gRPC unary calls.

    Automatically retries calls on specific exceptions or gRPC status codes
    with exponential backoff. Uses RetryHandler to manage retry logic.

    Attributes:
        retry_handler: Retry handler instance

    Example:
        >>> from py_web_automation.clients.grpc_client import GrpcClient, MiddlewareChain
        >>> from py_web_automation.clients.grpc_client.middleware import RetryMiddleware
        >>> from py_web_automation.clients.grpc_client.retry import (
        ...     RetryConfig,
        ...     RetryHandler,
        ... )
        >>> retry_config = RetryConfig(max_attempts=3, delay=1.0, backoff=2.0)
        >>> retry_handler = RetryHandler(retry_config)
        >>> retry_middleware = RetryMiddleware(retry_handler)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(retry_middleware)
        >>> async with GrpcClient(
        ...     "localhost:50051", config, middleware=middleware_chain
        ... ) as client:
        ...     result = await client.unary_call("UserService", "GetUser", request)
    """

    def __init__(self, retry_handler: RetryHandler) -> None:
        """
        Initialize retry middleware.

        Args:
            retry_handler: Retry handler instance
        """
        self.retry_handler = retry_handler

    async def process_request(self, context: _GrpcRequestContext) -> None:
        """
        No-op for requests.

        Args:
            context: Request context
        """
        pass

    async def process_response(self, context: _GrpcResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(
        self,
        context: _GrpcRequestContext,
        error: Exception,
    ) -> GrpcResult | None:
        """
        Process error and determine if retry is needed.

        Delegates to retry handler to check if error should be retried
        and handles retry logic with exponential backoff.

        Args:
            context: Request context
            error: Exception that occurred

        Returns:
            None if retry should be attempted, GrpcResult with error if limit exceeded
        """
        return await self.retry_handler.handle_error(context, error)
