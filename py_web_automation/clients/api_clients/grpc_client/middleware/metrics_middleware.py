"""
Metrics middleware for gRPC client.

This module provides MetricsMiddleware for collecting gRPC call metrics.
"""

# Python imports
from time import time

# Local imports
from ..grpc_result import GrpcResult
from ..metrics import Metrics
from .context import _GrpcRequestContext, _GrpcResponseContext
from .middleware import Middleware


class MetricsMiddleware(Middleware):
    """
    Middleware for collecting performance metrics for gRPC unary calls.

    Collects metrics about call latency, success rate, and error rates.

    Attributes:
        metrics: Metrics object for storing collected data

    Example:
        >>> from py_web_automation.clients.grpc_client import GrpcClient, MiddlewareChain
        >>> from py_web_automation.clients.grpc_client.middleware import MetricsMiddleware
        >>> from py_web_automation.clients.grpc_client.metrics import Metrics
        >>> metrics = Metrics()
        >>> metrics_middleware = MetricsMiddleware(metrics)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(metrics_middleware)
        >>> async with GrpcClient(
        ...     "localhost:50051", config, middleware=middleware_chain
        ... ) as client:
        ...     result = await client.unary_call("UserService", "GetUser", request)
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

    async def process_request(self, context: _GrpcRequestContext) -> None:
        """
        Record request start time.

        Args:
            context: Request context
        """
        context.metadata_context["metrics_start_time"] = time()

    async def process_response(self, context: _GrpcResponseContext) -> None:
        """
        Record response metrics.

        Args:
            context: Response context
        """
        start_time = context.metadata_context.get("metrics_start_time")
        if start_time:
            latency = context.result.response_time
            error_type = None
            if not context.result.success:
                if context.result.status_code:
                    error_type = f"grpc_status_{context.result.status_code}"
                else:
                    error_type = "grpc_error"
            self.metrics.record_request(
                success=context.result.success,
                latency=latency,
                error_type=error_type,
            )

    async def process_error(
        self, context: _GrpcRequestContext, error: Exception
    ) -> GrpcResult | None:
        """
        Record error metrics.

        Args:
            context: Request context
            error: Exception that occurred
        """
        error_type = type(error).__name__
        self.metrics.record_request(success=False, latency=0.0, error_type=error_type)
        return None
