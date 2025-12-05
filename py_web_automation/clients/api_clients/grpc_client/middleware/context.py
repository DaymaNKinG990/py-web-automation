"""
Middleware context objects for gRPC client.

This module provides request and response context objects for gRPC middleware.
"""

# Python imports
from typing import Any

# Local imports
from ..grpc_result import GrpcResult


class _GrpcRequestContext:
    """
    Internal context object passed through gRPC middleware chain for unary calls.

    Contains gRPC request information that can be modified by middleware.
    This is an internal class used only within middleware system.

    Attributes:
        service: Service name
        method: Method name (RPC method)
        request: Request protobuf message object
        metadata: Request metadata (can be modified) - gRPC metadata equivalent to headers
        timeout: Optional timeout for this call
        metadata_context: Custom metadata dictionary for middleware communication
    """

    def __init__(
        self,
        service: str,
        method: str,
        request: Any,
        metadata: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> None:
        """Initialize gRPC request context."""
        self.service = service
        self.method = method
        self.request = request
        self.metadata = metadata or {}
        self.timeout = timeout
        self.metadata_context: dict[str, Any] = {}


class _GrpcResponseContext:
    """
    Internal context object for gRPC response processing.

    Contains gRPC response information that can be modified by middleware.
    This is an internal class used only within middleware system.

    Attributes:
        result: GrpcResult object (can be modified)
        metadata_context: Custom metadata dictionary for middleware communication
    """

    def __init__(self, result: GrpcResult) -> None:
        """Initialize gRPC response context."""
        self.result = result
        # Copy metadata from result to context for middleware communication
        self.metadata_context: dict[str, Any] = (
            result.metadata_context.copy() if result.metadata_context else {}
        )
