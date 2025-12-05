"""
Logging middleware for GraphQL client.

This module provides LoggingMiddleware for automatic request/response logging.
"""

# Python imports
from loguru import logger

# Local imports
from ..graphql_result import GraphQLResult
from .context import _GraphQLRequestContext, _GraphQLResponseContext
from .middleware import Middleware


class LoggingMiddleware(Middleware):
    """
    Middleware for automatic request and response logging.

    Logs GraphQL operations, their execution time, and results.

    Example:
        >>> from py_web_automation.clients.graphql_client import GraphQLClient, MiddlewareChain
        >>> from py_web_automation.clients.graphql_client.middleware import LoggingMiddleware
        >>> logging_middleware = LoggingMiddleware()
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(logging_middleware)
        >>> async with GraphQLClient(
        ...     "https://api.example.com", config, middleware=middleware_chain
        ... ) as gql:
        ...     result = await gql.query("query { user { name } }")
    """

    async def process_request(self, context: _GraphQLRequestContext) -> None:
        """
        Log GraphQL request.

        Args:
            context: Request context
        """
        operation_info = f"{context.operation_type} {context.operation_name or 'unnamed'}"
        logger.info(f"GraphQL Request: {operation_info}")
        logger.debug(f"Query: {context.query}")
        if context.variables:
            logger.debug(f"Variables: {context.variables}")

    async def process_response(self, context: _GraphQLResponseContext) -> None:
        """
        Log GraphQL response.

        Args:
            context: Response context
        """
        result = context.result
        operation_info = f"{result.operation_type} {result.operation_name or 'unnamed'}"
        if result.success:
            logger.info(
                f"GraphQL Response: {operation_info} - Success (time: {result.response_time:.3f}s)"
            )
        else:
            logger.error(
                f"GraphQL Response: {operation_info} - Failed "
                f"(time: {result.response_time:.3f}s, errors: {len(result.errors)})"
            )
            for error in result.errors:
                logger.error(f"GraphQL Error: {error}")

    async def process_error(
        self, context: _GraphQLRequestContext, error: Exception
    ) -> GraphQLResult | None:
        """
        Log GraphQL error.

        Args:
            context: Request context
            error: Exception that occurred
        """
        operation_info = f"{context.operation_type} {context.operation_name or 'unnamed'}"
        logger.error(f"GraphQL Error: {operation_info} - {error}")
        return None
