"""
Data models for SOAP API client.

This module provides SoapResult class for standardized SOAP operation results.
"""

# Python imports
from typing import Any

from msgspec import Struct, field


class SoapResult(Struct, frozen=True):
    """
    SOAP operation result.

    Contains complete information about a SOAP operation execution,
    including response, SOAP fault, timing information, and metadata.

    Attributes:
        operation: SOAP operation name
        response_time: Time taken to execute the operation in seconds
        success: Whether the operation completed successfully (no SOAP fault)
        response: Response object from zeep (None if operation failed)
        soap_fault: SOAP fault information (None if operation succeeded)
        headers: Response headers from SOAP response
        metadata: Custom metadata dictionary for middleware communication

    Example:
        >>> result = await soap.call("GetUser", {"userId": "123"})
        >>> if result.success:
        ...     print(result.response)
        >>> else:
        ...     print(f"SOAP Fault: {result.soap_fault}")
    """

    operation: str
    response_time: float
    success: bool
    response: Any | None = None
    soap_fault: dict[str, Any] | None = None
    headers: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def raise_for_fault(self) -> None:
        """
        Raise exception if operation has SOAP fault.

        Raises:
            Exception: If operation has SOAP fault

        Example:
            >>> result = await soap.call("GetUser", {"userId": "123"})
            >>> result.raise_for_fault()  # Raises if SOAP fault present
        """
        if not self.soap_fault:
            return

        fault_code = self.soap_fault.get("faultcode", "Unknown")
        fault_string = self.soap_fault.get("faultstring", "SOAP Fault")
        raise Exception(
            f"SOAP operation '{self.operation}' failed: {fault_string} (code: {fault_code})"
        )
