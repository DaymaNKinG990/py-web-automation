"""
Rate limit middleware for HTTP client.

This module provides RateLimitMiddleware for rate limiting requests.
"""

# Local imports
from ..http_result import HttpResult
from ..rate_limit import RateLimiter
from .context import _RequestContext, _ResponseContext
from .middleware import Middleware


class RateLimitMiddleware(Middleware):
    """
    Middleware for rate limiting requests.

    Limits the rate of requests using a rate limiter to prevent
    exceeding API rate limits.

    Attributes:
        rate_limiter: Rate limiter instance

    Example:
        >>> from py_web_automation.clients.http_client.middleware.rate_limit_middleware import (
        ...     RateLimitMiddleware,
        ... )
        >>> from py_web_automation.rate_limit import RateLimiter
        >>> rate_limiter = RateLimiter(max_requests=100, window=60)
        >>> middleware = RateLimitMiddleware(rate_limiter)
        >>> # Use with HttpClient
    """

    def __init__(self, rate_limiter: "RateLimiter") -> None:
        """
        Initialize rate limit middleware.

        Args:
            rate_limiter: Rate limiter instance
        """
        self.rate_limiter = rate_limiter

    async def process_request(self, context: _RequestContext) -> None:
        """
        Acquire permission from rate limiter before request.

        Blocks if rate limit would be exceeded, waiting until a slot becomes available.

        Args:
            context: Request context
        """
        await self.rate_limiter.acquire()

    async def process_response(self, context: _ResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(self, context: _RequestContext, error: Exception) -> HttpResult | None:
        """
        No-op for errors.

        Args:
            context: Request context
            error: Exception that occurred
        """
        return None
