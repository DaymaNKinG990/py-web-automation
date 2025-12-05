"""
Middleware context objects for SOAP client.

This module provides request and response context objects for SOAP middleware.
"""

# Python imports
from typing import Any

# Local imports
from ..soap_result import SoapResult


class _SoapRequestContext:
    """
    Internal context object passed through SOAP middleware chain.

    Contains SOAP request information that can be modified by middleware.
    This is an internal class used only within middleware system.

    Attributes:
        operation: SOAP operation name
        body: Operation body data (can be modified)
        headers: Request headers (can be modified) - SOAP headers
        namespace: SOAP namespace (optional)
        metadata_context: Custom metadata dictionary for middleware communication
    """

    def __init__(
        self,
        operation: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        namespace: str | None = None,
    ) -> None:
        """Initialize SOAP request context."""
        self.operation = operation
        self.body = body or {}
        self.headers = headers or {}
        self.namespace = namespace
        self.metadata_context: dict[str, Any] = {}


class _SoapResponseContext:
    """
    Internal context object for SOAP response processing.

    Contains SOAP response information that can be modified by middleware.
    This is an internal class used only within middleware system.

    Attributes:
        result: SoapResult object (can be modified)
        metadata_context: Custom metadata dictionary for middleware communication
    """

    def __init__(self, result: SoapResult) -> None:
        """Initialize SOAP response context."""
        self.result = result
        # Copy metadata from result to context for middleware communication
        self.metadata_context: dict[str, Any] = result.metadata.copy() if result.metadata else {}
