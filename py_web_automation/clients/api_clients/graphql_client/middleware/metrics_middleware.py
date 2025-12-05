"""
Metrics middleware for GraphQL client.

This module provides MetricsMiddleware for collecting GraphQL operation metrics.
"""

# Python imports
from time import time

# Local imports
from ..graphql_result import GraphQLResult
from ..metrics import Metrics
from .context import _GraphQLRequestContext, _GraphQLResponseContext
from .middleware import Middleware


class MetricsMiddleware(Middleware):
    """
    Middleware for collecting performance metrics for GraphQL operations.

    Collects metrics about operation latency, success rate, and error rates.

    Attributes:
        metrics: Metrics object for storing collected data

    Example:
        >>> from py_web_automation.clients.graphql_client import GraphQLClient, MiddlewareChain
        >>> from py_web_automation.clients.graphql_client.middleware import MetricsMiddleware
        >>> from py_web_automation.clients.graphql_client.metrics import Metrics
        >>> metrics = Metrics()
        >>> metrics_middleware = MetricsMiddleware(metrics)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(metrics_middleware)
        >>> async with GraphQLClient(
        ...     "https://api.example.com", config, middleware=middleware_chain
        ... ) as gql:
        ...     result = await gql.query("query { user { name } }")
        ...     print(metrics.get_summary())
    """

    def __init__(self, metrics: Metrics | None = None) -> None:
        """
        Initialize metrics middleware.

        Args:
            metrics: Metrics object to use (creates new one if None)
        """
        if metrics is None:
            metrics = Metrics()
        self.metrics = metrics

    async def process_request(self, context: _GraphQLRequestContext) -> None:
        """
        Record request start time.

        Args:
            context: Request context
        """
        context.metadata["metrics_start_time"] = time()

    async def process_response(self, context: _GraphQLResponseContext) -> None:
        """
        Record response metrics.

        Args:
            context: Response context
        """
        start_time = context.metadata.get("metrics_start_time")
        if start_time:
            latency = context.result.response_time
            error_type = None
            if not context.result.success:
                if context.result.errors:
                    error_type = "graphql_error"
                else:
                    error_type = "unknown_error"
            self.metrics.record_request(
                success=context.result.success,
                latency=latency,
                error_type=error_type,
            )

    async def process_error(
        self, context: _GraphQLRequestContext, error: Exception
    ) -> GraphQLResult | None:
        """
        Record error metrics.

        Args:
            context: Request context
            error: Exception that occurred
        """
        error_type = type(error).__name__
        self.metrics.record_request(success=False, latency=0.0, error_type=error_type)
        return None
