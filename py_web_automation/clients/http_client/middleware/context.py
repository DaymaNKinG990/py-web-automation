"""
Middleware context objects for HTTP client.

This module provides request and response context objects for middleware.
"""

# Python imports
from http import HTTPMethod
from typing import Any

# Local imports
from ..http_result import HttpResult


class _RequestContext:
    """
    Internal context object passed through middleware chain.

    Contains request information that can be modified by middleware.
    This is an internal class used only within middleware system.

    Attributes:
        method: HTTP method
        url: Request URL
        headers: Request headers (can be modified)
        data: Request body data (can be modified)
        params: Query parameters (can be modified)
        metadata: Custom metadata dictionary for middleware communication
    """

    def __init__(
        self,
        method: HTTPMethod,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, Any] | bytes | str | None = None,
        params: dict[str, Any] | None = None,
    ) -> None:
        """Initialize request context."""
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.data = data
        self.params = params or {}
        self.metadata: dict[str, Any] = {}


class _ResponseContext:
    """
    Internal context object for response processing.

    Contains response information that can be modified by middleware.
    This is an internal class used only within middleware system.

    Attributes:
        result: HttpResult object (can be modified)
        metadata: Custom metadata dictionary for middleware communication
    """

    def __init__(self, result: HttpResult) -> None:
        """Initialize response context."""
        self.result = result
        # Copy metadata from result to context for middleware communication
        self.metadata: dict[str, Any] = result.metadata.copy() if result.metadata else {}
