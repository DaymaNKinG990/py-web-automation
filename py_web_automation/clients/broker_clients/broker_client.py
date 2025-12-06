"""
Base broker client for message broker testing.

This module provides BaseBrokerClient abstract base class for implementing
message broker clients with common functionality.
"""

# Python imports
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from json import dumps, loads
from json.decoder import JSONDecodeError
from typing import Any

# Local imports
from ...config import Config


class BrokerClient(ABC):
    """
    Abstract base class for message broker clients.

    Provides common functionality for message broker clients:
    - Connection management
    - Message serialization/deserialization
    - Context manager support
    - Logging
    - Error handling

    Subclasses must implement:
    - connect() - Establish connection to broker
    - disconnect() - Close connection to broker
    - publish() - Publish message to broker
    - consume() - Consume messages from broker

    Attributes:
        url: Broker connection URL
        config: Configuration object
        logger: Logger instance bound to class name
        _is_connected: Connection state flag (private)

    Example:
        >>> class MyBrokerClient(BaseBrokerClient):
        ...     async def connect(self) -> None:
        ...         # Implementation
        ...     async def disconnect(self) -> None:
        ...         # Implementation
        ...     async def publish(self, *args, **kwargs) -> None:
        ...         # Implementation
        ...     async def consume(self, *args, **kwargs) -> AsyncIterator:
        ...         # Implementation
    """

    def __init__(self, url: str, config: Config | None = None) -> None:
        """
        Initialize broker client.

        Args:
            url: Broker connection URL
            config: Configuration object with timeout settings

        Raises:
            TypeError: If config is not a Config object when provided
            ValueError: If url is empty

        Example:
            >>> config = Config(timeout=30)
            >>> client = MyBrokerClient("broker://localhost", config)
        """
        if not url or not url.strip():
            raise ValueError("url cannot be empty")

        if config is None:
            config = Config()
        elif not isinstance(config, Config):
            raise TypeError("config must be a Config object")
        self.url: str = url
        self.config: Config = config
        self._is_connected: bool = False

    @abstractmethod
    async def connect(self) -> None:
        """
        Establish connection to broker.

        Must set `_is_connected = True` on success.

        Raises:
            ConnectionError: If connection fails

        Example:
            >>> await client.connect()
        """
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """
        Close connection to broker.

        Must set `_is_connected = False` on completion.

        Example:
            >>> await client.disconnect()
        """
        ...

    @abstractmethod
    async def publish(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Publish message to broker.

        Args:
            *args: Positional arguments specific to broker implementation
            **kwargs: Keyword arguments specific to broker implementation

        Raises:
            RuntimeError: If not connected
            OperationError: If publishing fails

        Example:
            >>> await client.publish("topic", {"key": "value"})
        """
        ...

    @abstractmethod
    async def consume(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any] | str]:
        """
        Consume messages from broker.

        Args:
            *args: Positional arguments specific to broker implementation
            **kwargs: Keyword arguments specific to broker implementation

        Yields:
            Message content (dict if JSON, str otherwise)

        Raises:
            RuntimeError: If not connected
            OperationError: If consumption fails

        Example:
            >>> async for message in client.consume("topic"):
            ...     print(message)
        """
        ...

    @staticmethod
    def serialize_message(message: dict[str, Any] | str | bytes) -> bytes:
        """
        Serialize message to bytes.

        Supports dict (converted to JSON), str, and bytes.

        Args:
            message: Message content (dict, str, or bytes)

        Returns:
            Serialized message as bytes

        Example:
            >>> BaseBrokerClient.serialize_message({"key": "value"})
            b'{"key": "value"}'
            >>> BaseBrokerClient.serialize_message("text")
            b'text'
            >>> BaseBrokerClient.serialize_message(b"bytes")
            b'bytes'
        """
        if isinstance(message, dict):
            return dumps(message).encode("utf-8")
        elif isinstance(message, str):
            return message.encode("utf-8")
        else:
            return message

    @staticmethod
    def deserialize_message(message_bytes: bytes) -> dict[str, Any] | str:
        """
        Deserialize message from bytes.

        Attempts to parse as JSON first, falls back to string.

        Args:
            message_bytes: Message content as bytes

        Returns:
            Deserialized message (dict if JSON, str otherwise)

        Example:
            >>> BaseBrokerClient.deserialize_message(b'{"key": "value"}')
            {'key': 'value'}
            >>> BaseBrokerClient.deserialize_message(b"text")
            'text'
        """
        message = message_bytes.decode("utf-8")
        try:
            return loads(message)
        except JSONDecodeError:
            return message

    async def close(self) -> None:
        """
        Close client and cleanup resources.

        Calls disconnect() to close connection. This method is automatically
        called when exiting an async context manager.

        Example:
            >>> async with client:
            ...     # Use client
            ...     pass
            # Client is automatically closed here
        """
        await self.disconnect()

    async def __aenter__(self) -> "BrokerClient":
        """
        Async context manager entry.

        Automatically connects to broker.

        Returns:
            Self for use in async with statement

        Example:
            >>> async with client:
            ...     await client.publish("topic", {"key": "value"})
        """
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        """
        Async context manager exit.

        Automatically closes connection and cleans up resources.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)

        Example:
            >>> async with client:
            ...     # Use client
            ...     pass
            # Client is automatically closed here
        """
        await self.close()
