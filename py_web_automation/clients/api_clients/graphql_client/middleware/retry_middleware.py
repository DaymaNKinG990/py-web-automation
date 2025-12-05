"""
Retry middleware for GraphQL client.

This module provides RetryMiddleware for automatic retry of failed GraphQL operations.
"""

# Local imports
from ..graphql_result import GraphQLResult
from ..retry import RetryHandler
from .context import _GraphQLRequestContext, _GraphQLResponseContext
from .middleware import Middleware


class RetryMiddleware(Middleware):
    """
    Middleware for automatic retry of failed GraphQL operations.

    Automatically retries operations on specific exceptions with exponential backoff.
    Uses RetryHandler to manage retry logic.

    Attributes:
        retry_handler: Retry handler instance

    Example:
        >>> from py_web_automation.clients.graphql_client import GraphQLClient, MiddlewareChain
        >>> from py_web_automation.clients.graphql_client.middleware import RetryMiddleware
        >>> from py_web_automation.clients.graphql_client.retry import (
        ...     RetryConfig,
        ...     RetryHandler,
        ... )
        >>> retry_config = RetryConfig(
        ...     max_attempts=3,
        ...     delay=1.0,
        ...     backoff=2.0,
        ... )
        >>> retry_handler = RetryHandler(retry_config)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(RetryMiddleware(retry_handler))
        >>> async with GraphQLClient(
        ...     "https://api.example.com", config, middleware=middleware_chain
        ... ) as gql:
        ...     result = await gql.query("query { user { name } }")
    """

    def __init__(self, retry_handler: RetryHandler) -> None:
        """
        Initialize retry middleware.

        Args:
            retry_handler: Retry handler instance
        """
        self.retry_handler = retry_handler

    async def process_request(self, context: _GraphQLRequestContext) -> None:
        """
        No-op for requests.

        Args:
            context: Request context
        """
        pass

    async def process_response(self, context: _GraphQLResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(
        self,
        context: _GraphQLRequestContext,
        error: Exception,
    ) -> GraphQLResult | None:
        """
        Process error and determine if retry is needed.

        Delegates to retry handler to check if error should be retried
        and handles retry logic with exponential backoff.

        Args:
            context: Request context
            error: Exception that occurred

        Returns:
            None if retry should be attempted, GraphQLResult with error if limit exceeded
        """
        return await self.retry_handler.handle_error(context, error)
