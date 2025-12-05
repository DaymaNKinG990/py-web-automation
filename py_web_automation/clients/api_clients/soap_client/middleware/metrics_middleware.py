"""
Metrics middleware for SOAP client.

This module provides MetricsMiddleware for collecting SOAP operation metrics.
"""

# Python imports
from time import time

# Local imports
from ..metrics import Metrics
from ..soap_result import SoapResult
from .context import _SoapRequestContext, _SoapResponseContext
from .middleware import Middleware


class MetricsMiddleware(Middleware):
    """
    Middleware for collecting performance metrics for SOAP operations.

    Collects metrics about operation latency, success rate, and error rates.

    Attributes:
        metrics: Metrics object for storing collected data

    Example:
        >>> from py_web_automation.clients.soap_client import SoapClient, MiddlewareChain
        >>> from py_web_automation.clients.soap_client.middleware import MetricsMiddleware
        >>> from py_web_automation.clients.soap_client import Metrics
        >>> metrics = Metrics()
        >>> metrics_middleware = MetricsMiddleware(metrics)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(metrics_middleware)
        >>> async with SoapClient(
        ...     "https://api.example.com/soap", config, middleware=middleware_chain
        ... ) as soap:
        ...     result = await soap.call("GetUser", {"userId": "123"})
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

    async def process_request(self, context: _SoapRequestContext) -> None:
        """
        Record request start time.

        Args:
            context: Request context
        """
        context.metadata_context["metrics_start_time"] = time()

    async def process_response(self, context: _SoapResponseContext) -> None:
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
                if context.result.soap_fault:
                    fault_code = context.result.soap_fault.get("faultcode", "unknown")
                    error_type = f"soap_fault_{fault_code}"
                else:
                    error_type = "soap_error"
            self.metrics.record_request(
                success=context.result.success,
                latency=latency,
                error_type=error_type,
            )

    async def process_error(
        self, context: _SoapRequestContext, error: Exception
    ) -> SoapResult | None:
        """
        Record error metrics.

        Args:
            context: Request context
            error: Exception that occurred
        """
        error_type = type(error).__name__
        self.metrics.record_request(success=False, latency=0.0, error_type=error_type)
        return None
