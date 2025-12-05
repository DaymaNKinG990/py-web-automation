"""
Rate limiting middleware for SOAP client.

This module provides RateLimitMiddleware for rate limiting SOAP operations.
"""

# Local imports
from ..rate_limit import RateLimiter
from ..soap_result import SoapResult
from .context import _SoapRequestContext, _SoapResponseContext
from .middleware import Middleware


class RateLimitMiddleware(Middleware):
    """
    Middleware for rate limiting SOAP operations.

    Limits the number of operations per time window using sliding window algorithm.

    Attributes:
        rate_limiter: RateLimiter instance

    Example:
        >>> from py_web_automation.clients.soap_client import SoapClient, MiddlewareChain
        >>> from py_web_automation.clients.soap_client.middleware import RateLimitMiddleware
        >>> from py_web_automation.clients.soap_client import RateLimiter, RateLimitConfig
        >>> rate_limiter = RateLimiter(RateLimitConfig(max_requests=100, window=60))
        >>> rate_limit_middleware = RateLimitMiddleware(rate_limiter)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(rate_limit_middleware)
        >>> async with SoapClient(
        ...     "https://api.example.com/soap", config, middleware=middleware_chain
        ... ) as soap:
        ...     result = await soap.call("GetUser", {"userId": "123"})
    """

    def __init__(self, rate_limiter: RateLimiter) -> None:
        """
        Initialize rate limit middleware.

        Args:
            rate_limiter: RateLimiter instance to use
        """
        self.rate_limiter = rate_limiter

    async def process_request(self, context: _SoapRequestContext) -> None:
        """
        Acquire rate limit slot before making operation.

        Args:
            context: Request context
        """
        await self.rate_limiter.acquire()

    async def process_response(self, context: _SoapResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(
        self, context: _SoapRequestContext, error: Exception
    ) -> SoapResult | None:
        """
        No-op for errors.

        Args:
            context: Request context
            error: Exception that occurred
        """
        return None
