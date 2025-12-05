"""
Data models for gRPC API client.

This module provides GrpcResult class for standardized gRPC unary call results.
"""

# Python imports
from typing import Any

from msgspec import Struct, field


class GrpcResult(Struct, frozen=True):
    """
    gRPC unary call result.

    Contains complete information about a gRPC unary RPC call execution,
    including response, status, timing information, and metadata.

    Note: This result type is only used for unary calls (request-response).
    Streaming calls return AsyncIterator[Any] directly.

    Attributes:
        service: Service name
        method: Method name (RPC method)
        response_time: Time taken to execute the call in seconds
        success: Whether the call completed successfully
        response: Response protobuf message object (None if call failed)
        error: Error message (None if call succeeded)
        status_code: gRPC status code (None if call succeeded, int if failed)
        metadata: Response metadata from gRPC call
        request_metadata: Request metadata sent with the call

    Example:
        >>> result = await client.unary_call("UserService", "GetUser", request)
        >>> if result.success:
        ...     print(result.response)
        >>> else:
        ...     print(f"Error: {result.error} (status: {result.status_code})")
    """

    service: str
    method: str
    response_time: float
    success: bool
    response: Any | None = None
    error: str | None = None
    status_code: int | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    request_metadata: dict[str, str] = field(default_factory=dict)
    metadata_context: dict[str, Any] = field(default_factory=dict)

    def raise_for_error(self) -> None:
        """
        Raise exception if call failed.

        Raises:
            Exception: If call failed with error and status code

        Example:
            >>> result = await client.unary_call("UserService", "GetUser", request)
            >>> result.raise_for_error()  # Raises if call failed
        """
        if self.success:
            return
        error_msg = self.error or f"gRPC call failed with status code {self.status_code}"
        raise Exception(
            f"gRPC call {self.service}.{self.method} failed: {error_msg} "
            f"(status: {self.status_code})"
        )
