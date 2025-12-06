"""
RabbitMQ message broker client for web automation testing.

This module provides RabbitMQClient for testing RabbitMQ message brokers,
including message publishing, consuming, and queue management.
"""

# Python imports
from collections.abc import AsyncIterator, Callable
from typing import Any

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractQueue, AbstractRobustConnection
from aio_pika.exceptions import AMQPError

# Local imports
from ...config import Config
from ...exceptions import ConnectionError, OperationError
from .broker_client import BrokerClient


class RabbitMQClient(BrokerClient):
    """
    RabbitMQ message broker client for web automation testing.

    Implements RabbitMQ protocol support for testing message brokers.
    Follows the Single Responsibility Principle by focusing solely on RabbitMQ testing.

    Provides methods for testing RabbitMQ brokers:
    - Message publishing to exchanges/queues
    - Message consuming from queues
    - Queue and exchange management
    - Routing key support
    - Message acknowledgment

    Attributes:
        _connection: RabbitMQ connection (private)
        _channel: RabbitMQ channel (private)
        _queues: Active queues dictionary (private)
        _is_connected: Connection state flag (private)

    Example:
        >>> from py_web_automation import Config, RabbitMQClient
        >>> config = Config(timeout=30)
        >>> async with RabbitMQClient("amqp://guest:guest@localhost/", config) as rmq:
        ...     await rmq.publish("test-queue", {"key": "value"})
        ...     async for message in rmq.consume("test-queue"):
        ...         print(f"Received: {message}")
    """

    def __init__(
        self,
        url: str,
        config: Config | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize RabbitMQ client.

        Args:
            url: RabbitMQ connection URL (amqp://user:pass@host:port/vhost format)
            config: Configuration object with timeout settings
            **kwargs: Additional RabbitMQ connection parameters

        Raises:
            ImportError: If aio-pika library is not installed
            ValueError: If URL format is invalid

        Example:
            >>> config = Config(timeout=30)
            >>> rmq = RabbitMQClient("amqp://guest:guest@localhost/", config)
            >>> # Or with vhost
            >>> rmq = RabbitMQClient("amqp://guest:guest@localhost/my_vhost", config)
        """
        # Validate URL format
        if not url.startswith("amqp://") and not url.startswith("amqps://"):
            raise ValueError(
                f"Invalid RabbitMQ URL format: {url}. Expected format: amqp://user:pass@host:port/vhost"
            )
        super().__init__(url, config)
        self._connection: AbstractRobustConnection | None = None
        self._channel: Any | None = None
        self._queues: dict[str, AbstractQueue] = {}
        self._rmq_kwargs = kwargs
        # Explicitly declare inherited attribute for type checking
        self._is_connected: bool

    async def connect(self) -> None:
        """
        Establish RabbitMQ connection.

        Creates connection and channel for publishing/consuming messages.

        Raises:
            ConnectionError: If connection fails

        Example:
            >>> await rmq.connect()
        """
        if self._is_connected:
            return
        try:
            self._connection = await connect_robust(self.url, **self._rmq_kwargs)
            self._channel = await self._connection.channel()
            self._is_connected = True
        except AMQPError as e:
            error_msg = f"Failed to connect to RabbitMQ broker {self.url}: {e}"
            raise ConnectionError(error_msg, str(e)) from e

    async def disconnect(self) -> None:
        """
        Close RabbitMQ connections.

        Closes all channels and connection.

        Example:
            >>> await rmq.disconnect()
        """
        if self._channel:
            await self._channel.close()
            self._channel = None
        if self._connection:
            await self._connection.close()
            self._connection = None
        self._queues.clear()
        self._is_connected = False

    async def _get_or_create_queue(self, queue: str, durable: bool) -> AbstractQueue:
        """Get existing queue or create new one."""
        if queue in self._queues:
            return self._queues[queue]
        if self._channel is None:
            error_msg = "Channel is not available. Call connect() first."
            raise RuntimeError(error_msg)
        declared_queue = await self._channel.declare_queue(queue, durable=durable)
        self._queues[queue] = declared_queue
        return declared_queue

    def _get_routing_key(self, routing_key: str | None, queue: str) -> str:
        """Get routing key, using queue name as fallback."""
        return routing_key or queue

    async def _process_rabbitmq_message(
        self,
        message: Message,
        handler: Callable[[dict[str, Any] | str], None] | None,
        auto_ack: bool,
    ) -> dict[str, Any] | str:
        """Process RabbitMQ message and return parsed content."""
        parsed_message = self.deserialize_message(message.body)
        if handler:
            handler(parsed_message)
        if not auto_ack:
            await message.ack()
        return parsed_message

    async def _handle_message_error(
        self, message: Message, queue: str, error: Exception, auto_ack: bool
    ) -> None:
        """Handle error during message processing."""
        error_msg = f"Failed to process message from queue '{queue}': {error}"
        if not auto_ack:
            await message.nack(requeue=True)
        raise OperationError(error_msg, str(error)) from error

    async def _process_message_stream(
        self,
        queue_iter: AsyncIterator[Message],
        queue: str,
        handler: Callable[[dict[str, Any] | str], None] | None,
        auto_ack: bool,
    ) -> AsyncIterator[dict[str, Any] | str]:
        """Process stream of messages from queue iterator."""
        async for message in queue_iter:
            try:
                parsed_message = await self._process_rabbitmq_message(message, handler, auto_ack)
                yield parsed_message
            except Exception as e:
                await self._handle_message_error(message, queue, e, auto_ack)

    async def publish(
        self,
        queue: str,
        message: dict[str, Any] | str | bytes,
        exchange: str = "",
        routing_key: str | None = None,
        durable: bool = True,
    ) -> None:
        """
        Publish message to RabbitMQ queue or exchange.

        Args:
            queue: Queue name to publish to
            message: Message content (dict, str, or bytes)
            exchange: Exchange name (default: empty string for default exchange)
            routing_key: Routing key (default: queue name)
            durable: Whether queue should be durable (default: True)

        Raises:
            RuntimeError: If not connected
            OperationError: If publishing fails

        Example:
            >>> await rmq.publish("test-queue", {"user_id": 123, "action": "login"})
            >>> await rmq.publish("test-queue", "simple message", routing_key="test.key")
        """
        if not self._is_connected or not self._channel:
            error_msg = "Not connected to RabbitMQ. Call connect() first."
            raise RuntimeError(error_msg)
        try:
            await self._get_or_create_queue(queue, durable)
            message_body = self.serialize_message(message)
            routing = self._get_routing_key(routing_key, queue)
            await self._channel.default_exchange.publish(
                Message(message_body),
                routing_key=routing,
            )
        except AMQPError as e:
            error_msg = f"Failed to publish message to queue '{queue}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def consume(  # type: ignore[override]
        self,
        queue: str,
        durable: bool = True,
        timeout: float | None = None,
        handler: Callable[[dict[str, Any] | str], None] | None = None,
        auto_ack: bool = False,
    ) -> AsyncIterator[dict[str, Any] | str]:
        """
        Consume messages from RabbitMQ queue.

        Args:
            queue: Queue name to consume from
            durable: Whether queue should be durable (default: True)
            timeout: Timeout in seconds for receiving messages (uses config timeout if None)
            handler: Optional callback function to handle messages
            auto_ack: Automatically acknowledge messages (default: False)

        Yields:
            Message content (dict if JSON, str otherwise)

        Raises:
            RuntimeError: If not connected
            OperationError: If consumption fails

        Example:
            >>> async for message in rmq.consume("test-queue"):
            ...     print(f"Received: {message}")
            >>> # With handler
            >>> async def handle_message(msg):
            ...     print(f"Handled: {msg}")
            >>> async for message in rmq.consume("test-queue", handler=handle_message):
            ...     pass
        """
        if not self._is_connected or not self._channel:
            error_msg = "Not connected to RabbitMQ. Call connect() first."
            raise RuntimeError(error_msg)
        try:
            declared_queue = await self._get_or_create_queue(queue, durable)
            async with declared_queue.iterator() as queue_iter:
                async for parsed_message in self._process_message_stream(
                    queue_iter, queue, handler, auto_ack
                ):
                    yield parsed_message
        except AMQPError as e:
            error_msg = f"Failed to consume messages from queue '{queue}': {e}"
            raise OperationError(error_msg, str(e)) from e
