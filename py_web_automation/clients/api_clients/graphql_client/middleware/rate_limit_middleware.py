"""
Rate limit middleware for GraphQL client.

This module provides RateLimitMiddleware for rate limiting GraphQL operations.
"""

# Local imports
from ..graphql_result import GraphQLResult
from ..rate_limit import RateLimiter
from .context import _GraphQLRequestContext, _GraphQLResponseContext
from .middleware import Middleware


class RateLimitMiddleware(Middleware):
    """
    Middleware for rate limiting GraphQL operations.

    Limits the rate of operations using a rate limiter to prevent
    exceeding API rate limits.

    Attributes:
        rate_limiter: Rate limiter instance

    Example:
        >>> from py_web_automation.clients.graphql_client import GraphQLClient, MiddlewareChain
        >>> from py_web_automation.clients.graphql_client.middleware import RateLimitMiddleware
        >>> from py_web_automation.clients.graphql_client.rate_limit import RateLimiter
        >>> rate_limiter = RateLimiter(max_requests=100, window=60)
        >>> rate_limit_middleware = RateLimitMiddleware(rate_limiter)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(rate_limit_middleware)
        >>> async with GraphQLClient(
        ...     "https://api.example.com", config, middleware=middleware_chain
        ... ) as gql:
        ...     result = await gql.query("query { user { name } }")
    """

    def __init__(self, rate_limiter: RateLimiter) -> None:
        """
        Initialize rate limit middleware.

        Args:
            rate_limiter: Rate limiter instance
        """
        self.rate_limiter = rate_limiter

    async def process_request(self, context: _GraphQLRequestContext) -> None:
        """
        Acquire permission from rate limiter before request.

        Blocks if rate limit would be exceeded, waiting until a slot becomes available.

        Args:
            context: Request context
        """
        await self.rate_limiter.acquire()

    async def process_response(self, context: _GraphQLResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(
        self, context: _GraphQLRequestContext, error: Exception
    ) -> GraphQLResult | None:
        """
        No-op for errors.

        Args:
            context: Request context
            error: Exception that occurred
        """
        return None
