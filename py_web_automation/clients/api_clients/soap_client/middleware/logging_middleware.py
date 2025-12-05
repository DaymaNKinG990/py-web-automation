"""
Logging middleware for SOAP client.

This module provides LoggingMiddleware for automatic SOAP operation logging.
"""

# Python imports
from loguru import logger

# Local imports
from ..soap_result import SoapResult
from .context import _SoapRequestContext, _SoapResponseContext
from .middleware import Middleware


class LoggingMiddleware(Middleware):
    """
    Middleware for automatic SOAP operation logging.

    Logs SOAP operations, their execution time, and results.

    Example:
        >>> from py_web_automation.clients.soap_client import SoapClient, MiddlewareChain
        >>> from py_web_automation.clients.soap_client.middleware import LoggingMiddleware
        >>> logging_middleware = LoggingMiddleware()
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(logging_middleware)
        >>> async with SoapClient(
        ...     "https://api.example.com/soap", config, middleware=middleware_chain
        ... ) as soap:
        ...     result = await soap.call("GetUser", {"userId": "123"})
    """

    async def process_request(self, context: _SoapRequestContext) -> None:
        """
        Log SOAP request.

        Args:
            context: Request context
        """
        logger.info(f"SOAP Request: {context.operation}")
        if context.headers:
            logger.debug(f"Headers: {list(context.headers.keys())}")

    async def process_response(self, context: _SoapResponseContext) -> None:
        """
        Log SOAP response.

        Args:
            context: Response context
        """
        result = context.result
        if result.success:
            logger.info(
                f"SOAP Response: {result.operation} - Success (time: {result.response_time:.3f}s)"
            )
        else:
            logger.error(
                f"SOAP Response: {result.operation} - Failed (time: {result.response_time:.3f}s)"
            )
            if result.soap_fault:
                logger.error(f"SOAP Fault: {result.soap_fault}")

    async def process_error(
        self, context: _SoapRequestContext, error: Exception
    ) -> SoapResult | None:
        """
        Log SOAP error.

        Args:
            context: Request context
            error: Exception that occurred
        """
        logger.error(f"SOAP Error: {context.operation} - {error}")
        return None
