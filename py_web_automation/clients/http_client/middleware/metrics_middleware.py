"""
Metrics middleware for HTTP client.

This module provides MetricsMiddleware for collecting performance metrics.
"""

# Python imports
from time import time
from typing import Optional

from ..http_result import HttpResult
from ..metrics import Metrics
from .context import _RequestContext, _ResponseContext

# Local imports
from .middleware import Middleware


class MetricsMiddleware(Middleware):
    """
    Middleware for collecting performance metrics.

    Collects metrics about request latency, success rate, and error rates.

    Attributes:
        metrics: Metrics object for storing collected data

    Example:
        >>> metrics = Metrics()
        >>> chain.add(MetricsMiddleware(metrics))
    """

    def __init__(self, metrics: Optional["Metrics"] = None) -> None:
        """
        Initialize metrics middleware.

        Args:
            metrics: Metrics object to use (creates new one if None)
        """
        if metrics is None:
            metrics = Metrics()
        self.metrics = metrics

    async def process_request(self, context: _RequestContext) -> None:
        """
        Record request start time.

        Args:
            context: Request context
        """
        context.metadata["start_time"] = time()

    async def process_response(self, context: _ResponseContext) -> None:
        """
        Record response metrics.

        Args:
            context: Response context
        """
        start_time = context.metadata.get("start_time")
        if start_time:
            latency = context.result.response_time
            error_type = None
            if not context.result.success:
                if context.result.client_error:
                    error_type = "client_error"
                elif context.result.server_error:
                    error_type = "server_error"
                else:
                    error_type = "unknown_error"
            self.metrics.record_request(
                success=context.result.success,
                latency=latency,
                error_type=error_type,
            )

    async def process_error(
        self, context: _RequestContext, error: Exception
    ) -> HttpResult | None:
        """
        Record error metrics.

        Args:
            context: Request context
            error: Exception that occurred
        """
        error_type = type(error).__name__
        self.metrics.record_request(success=False, latency=0.0, error_type=error_type)
        return None
