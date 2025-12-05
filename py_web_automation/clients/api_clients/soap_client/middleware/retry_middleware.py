"""
Retry middleware for SOAP client.

This module provides RetryMiddleware for automatic retry of failed SOAP operations.
"""

# Local imports
from ..retry import RetryHandler
from ..soap_result import SoapResult
from .context import _SoapRequestContext, _SoapResponseContext
from .middleware import Middleware


class RetryMiddleware(Middleware):
    """
    Middleware for automatic retry of failed SOAP operations.

    Automatically retries operations on specific exceptions or SOAP faults
    with exponential backoff.

    Attributes:
        retry_handler: Retry handler instance

    Example:
        >>> from py_web_automation.clients.soap_client import SoapClient, MiddlewareChain
        >>> from py_web_automation.clients.soap_client.middleware import RetryMiddleware
        >>> from py_web_automation.clients.soap_client import RetryConfig, RetryHandler
        >>> retry_config = RetryConfig(max_attempts=3, delay=1.0, backoff=2.0)
        >>> retry_handler = RetryHandler(retry_config)
        >>> retry_middleware = RetryMiddleware(retry_handler)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(retry_middleware)
        >>> async with SoapClient(
        ...     "https://api.example.com/soap", config, middleware=middleware_chain
        ... ) as soap:
        ...     result = await soap.call("GetUser", {"userId": "123"})
    """

    def __init__(self, retry_handler: RetryHandler) -> None:
        """
        Initialize retry middleware.

        Args:
            retry_handler: Retry handler instance
        """
        self.retry_handler = retry_handler

    async def process_request(self, context: _SoapRequestContext) -> None:
        """
        No-op for requests.

        Args:
            context: Request context
        """
        pass

    async def process_response(self, context: _SoapResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(
        self,
        context: _SoapRequestContext,
        error: Exception,
    ) -> SoapResult | None:
        """
        Process error and determine if retry is needed.

        Delegates to retry handler to check if error should be retried
        and handles retry logic with exponential backoff.

        Args:
            context: Request context
            error: Exception that occurred

        Returns:
            None if retry should be attempted, SoapResult with error if limit exceeded
        """
        # Extract SOAP fault from error if available
        soap_fault = None
        if hasattr(error, "detail") and hasattr(error, "code"):
            soap_fault = {"faultcode": str(error.code), "faultstring": str(error)}

        return await self.retry_handler.handle_error(context, error, soap_fault)
