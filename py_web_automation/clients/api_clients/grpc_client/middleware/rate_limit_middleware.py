"""
Rate limiting middleware for gRPC client.

This module provides RateLimitMiddleware for rate limiting gRPC unary calls.
"""

# Local imports
from ..grpc_result import GrpcResult
from ..rate_limit import RateLimiter
from .context import _GrpcRequestContext, _GrpcResponseContext
from .middleware import Middleware


class RateLimitMiddleware(Middleware):
    """
    Middleware for rate limiting gRPC unary calls.

    Limits the number of calls per time window using sliding window algorithm.

    Attributes:
        rate_limiter: Rate limiter instance

    Example:
        >>> from py_web_automation.clients.grpc_client import GrpcClient, MiddlewareChain
        >>> from py_web_automation.clients.grpc_client.middleware import RateLimitMiddleware
        >>> from py_web_automation.clients.grpc_client.rate_limit import RateLimiter
        >>> rate_limiter = RateLimiter(max_requests=100, window=60)
        >>> rate_limit_middleware = RateLimitMiddleware(rate_limiter)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(rate_limit_middleware)
        >>> async with GrpcClient(
        ...     "localhost:50051", config, middleware=middleware_chain
        ... ) as client:
        ...     result = await client.unary_call("UserService", "GetUser", request)
    """

    def __init__(self, rate_limiter: RateLimiter) -> None:
        """
        Initialize rate limit middleware.

        Args:
            rate_limiter: RateLimiter instance to use
        """
        self.rate_limiter = rate_limiter

    async def process_request(self, context: _GrpcRequestContext) -> None:
        """
        Acquire rate limit slot before making call.

        Args:
            context: Request context
        """
        await self.rate_limiter.acquire()

    async def process_response(self, context: _GrpcResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(
        self, context: _GrpcRequestContext, error: Exception
    ) -> GrpcResult | None:
        """
        No-op for errors.

        Args:
            context: Request context
            error: Exception that occurred
        """
        return None
