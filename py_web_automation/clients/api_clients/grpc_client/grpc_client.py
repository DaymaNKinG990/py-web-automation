"""
gRPC API client for web automation testing.

This module provides GrpcClient for testing gRPC API endpoints,
including unary calls, streaming calls, and metadata handling.
"""

# Python imports
from __future__ import annotations

from collections.abc import AsyncIterator
from time import time
from types import TracebackType
from typing import TYPE_CHECKING, Any

from grpclib.client import Channel
from grpclib.exceptions import GRPCError

# Local imports
from ....config import Config
from ....exceptions import ConnectionError, OperationError
from .grpc_result import GrpcResult
from .middleware.context import _GrpcRequestContext, _GrpcResponseContext

if TYPE_CHECKING:
    from .middleware.middleware import MiddlewareChain


class GrpcClient:
    """
    gRPC API client for web automation testing.

    Implements gRPC communication using grpclib for async gRPC communication.
    Requires protobuf definitions and generated stubs.

    Provides middleware support for unary calls, including:
    - Authentication via AuthMiddleware
    - Logging via LoggingMiddleware
    - Metrics via MetricsMiddleware
    - Retry via RetryMiddleware
    - Rate limiting via RateLimitMiddleware

    Attributes:
        url: gRPC server address
        config: Configuration object
        _channel: gRPC channel (private)
        _metadata: Default metadata for all calls (private)
        _middleware: Middleware chain for unary calls (private)

    Example:
        >>> from py_web_automation.clients.grpc_client import GrpcClient
        >>> from py_web_automation.clients.grpc_client.middleware import (
        ...     MiddlewareChain, AuthMiddleware, LoggingMiddleware
        ... )
        >>> config = Config(timeout=30)
        >>> middleware = MiddlewareChain()
        >>> middleware.add(AuthMiddleware(token="token123"))
        >>> middleware.add(LoggingMiddleware())
        >>> async with GrpcClient(
        ...     "localhost:50051", config, middleware=middleware
        ... ) as client:
        ...     result = await client.unary_call("UserService", "GetUser", request)
        ...     if result.success:
        ...         print(result.response)
    """

    def __init__(
        self,
        url: str,
        config: Config | None = None,
        middleware: MiddlewareChain | None = None,
    ) -> None:
        """
        Initialize gRPC client.

        Args:
            url: gRPC server address (host:port format, e.g., "localhost:50051")
            config: Configuration object with timeout settings
            middleware: Optional middleware chain for unary call processing

        Raises:
            ValueError: If url is empty or config is invalid
            ImportError: If grpclib is not installed

        Example:
            >>> from py_web_automation.clients.grpc_client.middleware import MiddlewareChain
            >>> chain = MiddlewareChain().add(LoggingMiddleware())
            >>> client = GrpcClient("localhost:50051", config, middleware=chain)
        """
        if not url.strip():
            raise ValueError("url cannot be empty")
        if config is None:
            config = Config()
        elif not isinstance(config, Config):
            raise TypeError("config must be a Config object")
        self.url: str = url
        self.config: Config = config
        self._channel: Channel | None = None
        self._metadata: dict[str, str] = {}
        self._middleware = middleware
        self._host: str = ""
        self._port: int = 0

    async def connect(self) -> None:
        """
        Establish gRPC channel connection using grpclib.

        Raises:
            ConnectionError: If connection fails
        """
        try:
            # Parse URL to extract host and port
            if "://" in self.url:
                # Remove protocol prefix if present
                address = self.url.split("://")[-1]
            else:
                address = self.url
            if ":" in address:
                self._host, port_str = address.rsplit(":", 1)
                self._port = int(port_str)
            else:
                self._host = address
                self._port = 50051  # Default gRPC port
            # Create grpclib channel (timeout is passed per-call, not in constructor)
            self._channel = Channel(self._host, self._port)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to gRPC server: {e}") from e

    async def disconnect(self) -> None:
        """Close gRPC channel connection."""
        if self._channel:
            self._channel.close()
            self._channel = None

    def set_metadata(self, key: str, value: str) -> None:
        """
        Set default metadata for all RPC calls.

        Args:
            key: Metadata key
            value: Metadata value

        Example:
            >>> client.set_metadata("authorization", "Bearer token123")
        """
        self._metadata[key] = value

    def clear_metadata(self) -> None:
        """Clear all default metadata."""
        self._metadata.clear()

    def _merge_metadata(self, metadata: dict[str, str] | None = None) -> dict[str, str]:
        """
        Merge default metadata with call-specific metadata.

        Args:
            metadata: Call-specific metadata (optional)

        Returns:
            Merged metadata dictionary
        """
        merged = self._metadata.copy()
        if metadata:
            merged.update(metadata)
        return merged

    async def close(self) -> None:
        """
        Close gRPC client and cleanup resources.

        Closes the gRPC channel and clears metadata.
        This method is automatically called when exiting an async context manager.
        """
        await self.disconnect()
        self._metadata.clear()

    async def __aenter__(self) -> GrpcClient:
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Async context manager exit."""
        await self.close()

    async def _prepare_request_context(
        self,
        service: str,
        method: str,
        request: Any,
        metadata: dict[str, str] | None,
        timeout: float | None,
    ) -> _GrpcRequestContext:
        """
        Prepare request context with middleware.

        Args:
            service: Service name
            method: Method name
            request: Request protobuf message
            metadata: Optional call-specific metadata
            timeout: Optional timeout

        Returns:
            _GrpcRequestContext with middleware applied
        """
        # Merge default and call-specific metadata
        merged_metadata = self._merge_metadata(metadata)

        request_context = _GrpcRequestContext(
            service=service,
            method=method,
            request=request,
            metadata=merged_metadata,
            timeout=timeout,
        )
        # Process through middleware
        if self._middleware:
            await self._middleware.process_request(request_context)
        return request_context

    async def _process_response(
        self, result: GrpcResult, request_context: _GrpcRequestContext
    ) -> GrpcResult:
        """
        Process response through middleware.

        Args:
            result: GrpcResult from call
            request_context: Original request context

        Returns:
            Processed GrpcResult (may be modified by middleware)
        """
        if self._middleware:
            response_context = _GrpcResponseContext(result)
            # Copy metadata_context from request to result
            response_context.metadata_context = request_context.metadata_context.copy()
            result = result.__class__(
                service=result.service,
                method=result.method,
                response_time=result.response_time,
                success=result.success,
                response=result.response,
                error=result.error,
                status_code=result.status_code,
                metadata=result.metadata,
                request_metadata=result.request_metadata,
                metadata_context=response_context.metadata_context,
            )
            await self._middleware.process_response(response_context)
            # Create new result from potentially modified context
            result = response_context.result

        return result

    async def _handle_call_error(
        self,
        error: Exception,
        service: str,
        method: str,
        request_context: _GrpcRequestContext,
        start_time: float,
    ) -> GrpcResult:
        """
        Handle error during gRPC call execution.

        Args:
            error: Exception that occurred
            service: Service name
            method: Method name
            request_context: Request context
            start_time: Call start time

        Returns:
            GrpcResult representing the error
        """
        response_time = time() - start_time

        # Process error through middleware
        if self._middleware:
            error_result = await self._middleware.process_error(request_context, error)
            if error_result is not None:
                return error_result

        # Extract gRPC status code if available
        status_code = None
        error_message = str(error)
        if isinstance(error, GRPCError):
            status_code = getattr(error.status, "code", None)
            error_message = error.message or str(error)

        # Create error result
        return GrpcResult(
            service=service,
            method=method,
            response_time=response_time,
            success=False,
            response=None,
            error=error_message,
            status_code=status_code,
            metadata={},
            request_metadata=request_context.metadata,
            metadata_context=request_context.metadata_context.copy(),
        )

    async def unary_call(
        self,
        service: str,
        method: str,
        request: Any,
        metadata: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> GrpcResult:
        """
        Execute unary RPC call (request-response) using grpclib.

        This method supports middleware processing and returns GrpcResult.

        Args:
            service: Service name (used for method path construction)
            method: Method name
            request: Request message object (protobuf message)
            metadata: Optional metadata for this call
            timeout: Optional timeout in seconds (overrides config timeout)

        Returns:
            GrpcResult with response, status, and metadata

        Raises:
            RuntimeError: If not connected
            OperationError: If RPC call fails after retries

        Example:
            >>> result = await client.unary_call("UserService", "GetUser", request)
            >>> if result.success:
            ...     print(result.response)
            >>> else:
            ...     result.raise_for_error()
        """
        if not self._channel:
            raise RuntimeError("Not connected to gRPC server. Call connect() first.")

        # Retry loop for unary calls
        while True:
            start_time = time()
            request_context = await self._prepare_request_context(
                service=service,
                method=method,
                request=request,
                metadata=metadata,
                timeout=timeout,
            )
            request_context.metadata_context["start_time"] = start_time

            try:
                # Construct method path
                method_path = f"/{service}/{method}"

                # Use grpclib's low-level API for unary calls
                from typing import Never

                from grpclib.client import UnaryUnaryMethod

                # Create method handler
                # Response type is unknown at runtime, so we use Never as placeholder
                method_handler: UnaryUnaryMethod[Any, Any] = UnaryUnaryMethod(
                    self._channel,
                    method_path,
                    request.__class__,
                    Never,
                )

                # Use metadata from context (may have been modified by middleware)
                call_timeout = request_context.timeout
                if call_timeout is None:
                    call_timeout = self.config.timeout if self.config else None

                # Execute call
                response = await method_handler(
                    request, metadata=request_context.metadata, timeout=call_timeout
                )

                response_time = time() - start_time

                # Create result
                result = GrpcResult(
                    service=service,
                    method=method,
                    response_time=response_time,
                    success=True,
                    response=response,
                    error=None,
                    status_code=None,
                    metadata={},  # Response metadata not easily accessible in grpclib
                    request_metadata=request_context.metadata.copy(),
                    metadata_context=request_context.metadata_context.copy(),
                )

                # Process response through middleware
                result = await self._process_response(result, request_context)
                return result

            except Exception as e:
                error_result = await self._handle_call_error(
                    e, service, method, request_context, start_time
                )

                # Check if retry is needed (delay already handled by RetryHandler)
                if request_context.metadata_context.get("should_retry"):
                    continue  # Retry the call

                return error_result

    async def server_streaming_call(
        self,
        service: str,
        method: str,
        request: Any,
        metadata: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> AsyncIterator[Any]:
        """
        Execute server streaming RPC call using grpclib.

        Note: Streaming calls do not use middleware system and return
        AsyncIterator[Any] directly.

        Args:
            service: Service name (used for method path construction)
            method: Method name
            request: Request message object (protobuf message)
            metadata: Optional metadata for this call
            timeout: Optional timeout in seconds (overrides config timeout)

        Yields:
            Response message objects from server stream

        Raises:
            RuntimeError: If not connected
            OperationError: If RPC call fails

        Example:
            >>> async for response in client.server_streaming_call(
            ...     "UserService", "ListUsers", request
            ... ):
            ...     print(response)
        """
        if not self._channel:
            raise RuntimeError("Not connected to gRPC server. Call connect() first.")

        # Merge metadata (streaming doesn't use middleware)
        merged_metadata = self._merge_metadata(metadata)

        # Construct method path
        method_path = f"/{service}/{method}"

        try:
            # Use grpclib's low-level API for streaming calls
            from typing import Never

            from grpclib.client import UnaryStreamMethod

            # Create method handler
            # Response type is unknown at runtime, so we use Never as placeholder
            method_handler: UnaryStreamMethod[Any, Any] = UnaryStreamMethod(
                self._channel,
                method_path,
                request.__class__,
                Never,
            )

            # Execute streaming call
            async with method_handler.open(metadata=merged_metadata, timeout=timeout) as stream:
                await stream.send_message(request)
                await stream.end()
                async for response in stream:
                    yield response
        except GRPCError as e:
            raise OperationError(f"gRPC streaming call failed: {e.message}") from e
        except Exception as e:
            raise OperationError(f"gRPC streaming call failed: {e}") from e
