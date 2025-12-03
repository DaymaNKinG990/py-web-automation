"""
Logging middleware for HTTP client.

This module provides LoggingMiddleware for logging requests and responses.
"""

# Python imports
from loguru import logger

from ..http_result import HttpResult
from .context import _RequestContext, _ResponseContext

# Local imports
from .middleware import Middleware


class LoggingMiddleware(Middleware):
    """
    Middleware for logging requests and responses.

    Logs request details before sending and response details after receiving.

    Example:
        >>> chain.add(LoggingMiddleware())
    """

    async def process_request(self, context: _RequestContext) -> None:
        """
        Log request details.

        Args:
            context: Request context
        """
        logger.info(
            f"Request: {context.method} {context.url} "
            f"headers={len(context.headers)} params={len(context.params)}"
        )

    async def process_response(self, context: _ResponseContext) -> None:
        """
        Log response details.

        Args:
            context: Response context
        """
        logger.info(
            f"Response: {context.result.status_code} "
            f"time={context.result.response_time:.3f}s "
            f"success={context.result.success}"
        )

    async def process_error(self, context: _RequestContext, error: Exception) -> HttpResult | None:
        """
        Log error details.

        Args:
            context: Request context
            error: Exception that occurred
        """
        logger.error(f"Request error: {context.method} {context.url} - {error}")
        return None
