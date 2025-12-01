"""
gRPC API client for web automation testing.

This module provides GrpcClient for testing gRPC API endpoints,
including unary calls, streaming calls, and metadata handling.
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from ..config import Config
from .base_client import BaseClient


class GrpcClient(BaseClient, ABC):
    """
    gRPC API client for web automation testing.

    Abstract base class for gRPC clients. Subclasses should implement
    protocol-specific gRPC communication (e.g., using grpclib or grpcio).

    Provides interface for testing gRPC API endpoints:
    - Unary RPC calls (request-response)
    - Server streaming RPC calls
    - Client streaming RPC calls
    - Bidirectional streaming RPC calls
    - Metadata handling
    - Error handling

    Attributes:
        _channel: gRPC channel (private, implementation-specific)
        _metadata: Default metadata for all calls (private)

    Example:
        >>> from py_web_automation import Config, GrpcClient
        >>> config = Config(timeout=30)
        >>> # Implementation would be in a concrete subclass
        >>> # client = ConcreteGrpcClient("localhost:50051", config)
    """

    def __init__(self, url: str, config: Config | None = None) -> None:
        """
        Initialize gRPC client.

        Args:
            url: gRPC server address (host:port format)
            config: Configuration object with timeout settings

        Raises:
            ValueError: If config is None (inherited from BaseClient)
        """
        super().__init__(url, config)
        self._channel: Any | None = None
        self._metadata: dict[str, str] = {}

    @abstractmethod
    async def connect(self) -> None:
        """
        Establish gRPC channel connection.

        Raises:
            RuntimeError: If connection fails
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close gRPC channel connection."""
        pass

    @abstractmethod
    async def unary_call(
        self,
        service: str,
        method: str,
        request: Any,
        metadata: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> Any:
        """
        Execute unary RPC call (request-response).

        Args:
            service: Service name
            method: Method name
            request: Request message object
            metadata: Optional metadata for this call
            timeout: Optional timeout in seconds

        Returns:
            Response message object

        Raises:
            RuntimeError: If not connected
            Exception: If RPC call fails
        """
        pass

    @abstractmethod
    async def server_streaming_call(
        self,
        service: str,
        method: str,
        request: Any,
        metadata: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> AsyncIterator[Any]:
        """
        Execute server streaming RPC call.

        Args:
            service: Service name
            method: Method name
            request: Request message object
            metadata: Optional metadata for this call
            timeout: Optional timeout in seconds

        Yields:
            Response message objects from server stream

        Raises:
            RuntimeError: If not connected
            Exception: If RPC call fails
        """
        pass

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
        self.logger.debug(f"Metadata set: {key}")

    def clear_metadata(self) -> None:
        """Clear all default metadata."""
        self._metadata.clear()
        self.logger.debug("Metadata cleared")

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

    async def __aenter__(self) -> "GrpcClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()


class GrpcClientImpl(GrpcClient):
    """
    Concrete implementation of gRPC client using grpclib.

    This is a placeholder implementation. In a real scenario, you would
    use a library like grpclib or grpcio to implement the abstract methods.

    Note: This requires protobuf definitions and generated code.
    """

    async def connect(self) -> None:
        """Establish gRPC channel connection."""
        try:
            # This would use grpclib or grpcio to create a channel
            # Example with grpclib:
            # from grpclib.client import Channel
            # self._channel = Channel(self.url.split("://")[-1].split(":")[0],
            #                         int(self.url.split(":")[-1]))
            self.logger.info(f"Connected to gRPC server at {self.url}")
        except Exception as e:
            raise RuntimeError(f"Failed to connect to gRPC server: {e}") from e

    async def disconnect(self) -> None:
        """Close gRPC channel connection."""
        if self._channel:
            # self._channel.close()  # Implementation-specific
            self._channel = None
            self.logger.info("Disconnected from gRPC server")

    async def unary_call(
        self,
        service: str,
        method: str,
        request: Any,
        metadata: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> Any:
        """
        Execute unary RPC call (request-response).

        This is a placeholder implementation. In a real scenario,
        you would use generated protobuf stubs to make the call.

        Args:
            service: Service name
            method: Method name
            request: Request message object
            metadata: Optional metadata for this call
            timeout: Optional timeout in seconds

        Returns:
            Response message object

        Raises:
            RuntimeError: If not connected
            NotImplementedError: This is a placeholder implementation
        """
        if not self._channel:
            raise RuntimeError("Not connected to gRPC server")

        # Placeholder - would use generated stub
        # stub = ServiceStub(self._channel)
        # return await getattr(stub, method)(request, metadata=self._merge_metadata(metadata))
        raise NotImplementedError(
            "gRPC client requires protobuf definitions and generated stubs. Please implement using grpclib or grpcio."
        )

    async def server_streaming_call(
        self,
        service: str,
        method: str,
        request: Any,
        metadata: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> AsyncIterator[Any]:
        """
        Execute server streaming RPC call.

        This is a placeholder implementation.

        Args:
            service: Service name
            method: Method name
            request: Request message object
            metadata: Optional metadata for this call
            timeout: Optional timeout in seconds

        Yields:
            Response message objects from server stream

        Raises:
            RuntimeError: If not connected
            NotImplementedError: This is a placeholder implementation
        """
        if not self._channel:
            raise RuntimeError("Not connected to gRPC server")

        # Placeholder - would use generated stub
        raise NotImplementedError(
            "gRPC client requires protobuf definitions and generated stubs. Please implement using grpclib or grpcio."
        )
