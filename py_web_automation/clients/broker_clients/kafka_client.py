"""
Kafka message broker client for web automation testing.

This module provides KafkaClient for testing Kafka message brokers,
including message publishing, consuming, and topic management.
"""

# Python imports
from collections.abc import AsyncIterator, Callable
from typing import Any

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError

# Local imports
from ...config import Config
from ...exceptions import ConnectionError, OperationError
from .broker_client import BrokerClient


class KafkaClient(BrokerClient):
    """
    Kafka message broker client for web automation testing.

    Implements Kafka protocol support for testing message brokers.
    Follows the Single Responsibility Principle by focusing solely on Kafka testing.

    Provides methods for testing Kafka brokers:
    - Message publishing to topics
    - Message consuming from topics
    - Topic management
    - Consumer group management
    - Offset management

    Attributes:
        _producer: Kafka producer instance (private)
        _consumers: Active consumers dictionary (private)
        _bootstrap_servers: Kafka bootstrap servers (private)
        _is_connected: Connection state flag (private)

    Example:
        >>> from py_web_automation import Config, KafkaClient
        >>> config = Config(timeout=30)
        >>> async with KafkaClient("localhost:9092", config) as kafka:
        ...     await kafka.publish("test-topic", {"key": "value"})
        ...     async for message in kafka.consume("test-topic"):
        ...         print(f"Received: {message}")
    """

    def __init__(
        self,
        url: str,
        config: Config | None = None,
        bootstrap_servers: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize Kafka client.

        Args:
            url: Kafka broker URL (host:port format, e.g., "localhost:9092")
            config: Configuration object with timeout settings
            bootstrap_servers: Comma-separated list of Kafka brokers
                (optional, uses url if not provided)
            **kwargs: Additional Kafka client configuration (client_id, group_id, etc.)

        Raises:
            ImportError: If aiokafka library is not installed
            ValueError: If URL format is invalid

        Example:
            >>> config = Config(timeout=30)
            >>> kafka = KafkaClient("localhost:9092", config)
            >>> # Or with multiple brokers
            >>> brokers = "localhost:9092,localhost:9093"
            >>> kafka = KafkaClient("localhost:9092", config, bootstrap_servers=brokers)
        """
        # Validate URL format (host:port)
        if ":" not in url:
            raise ValueError(f"Invalid Kafka URL format: {url}. Expected format: host:port")
        super().__init__(url, config)
        self._bootstrap_servers: str = bootstrap_servers or url
        self._producer: AIOKafkaProducer | None = None
        self._consumers: dict[str, AIOKafkaConsumer] = {}
        self._kafka_kwargs = kwargs

    async def connect(self) -> None:
        """
        Establish Kafka connection.

        Creates producer instance for publishing messages.

        Raises:
            ConnectionError: If connection fails

        Example:
            >>> await kafka.connect()
        """
        if self._is_connected:
            return
        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._bootstrap_servers,
                **self._kafka_kwargs,
            )
            await self._producer.start()
            self._is_connected = True
        except KafkaError as e:
            error_msg = f"Failed to connect to Kafka broker {self._bootstrap_servers}: {e}"
            raise ConnectionError(error_msg, str(e)) from e

    async def disconnect(self) -> None:
        """
        Close Kafka connections.

        Closes all producers and consumers.

        Example:
            >>> await kafka.disconnect()
        """
        if self._producer:
            await self._producer.stop()
            self._producer = None
        for topic, consumer in list(self._consumers.items()):
            await consumer.stop()
            del self._consumers[topic]
        self._is_connected = False

    def _serialize_key(self, key: str | bytes | None) -> bytes | None:
        """Serialize message key to bytes if provided."""
        if key is None:
            return None
        if isinstance(key, str):
            return key.encode("utf-8")
        return key

    async def _get_or_create_consumer(
        self, topic: str, group_id: str | None, auto_offset_reset: str
    ) -> AIOKafkaConsumer:
        """Get existing consumer or create new one for topic."""
        if topic in self._consumers:
            return self._consumers[topic]
        consumer_kwargs = {
            "bootstrap_servers": self._bootstrap_servers,
            "auto_offset_reset": auto_offset_reset,
            **self._kafka_kwargs,
        }
        if group_id:
            consumer_kwargs["group_id"] = group_id
        consumer = AIOKafkaConsumer(topic, **consumer_kwargs)
        await consumer.start()
        self._consumers[topic] = consumer
        return consumer

    def _process_message(
        self,
        msg_value: bytes,
        handler: Callable[[dict[str, Any] | str], None] | None,
    ) -> dict[str, Any] | str:
        """Deserialize and optionally handle message."""
        parsed_message = self.deserialize_message(msg_value)
        if handler:
            handler(parsed_message)
        return parsed_message

    async def publish(
        self,
        topic: str,
        message: dict[str, Any] | str | bytes,
        key: str | bytes | None = None,
        partition: int | None = None,
    ) -> None:
        """
        Publish message to Kafka topic.

        Args:
            topic: Topic name to publish to
            message: Message content (dict, str, or bytes)
            key: Optional message key for partitioning
            partition: Optional partition number

        Raises:
            RuntimeError: If not connected
            OperationError: If publishing fails

        Example:
            >>> await kafka.publish("test-topic", {"user_id": 123, "action": "login"})
            >>> await kafka.publish("test-topic", "simple message", key="message-1")
        """
        if not self._is_connected or not self._producer:
            error_msg = "Not connected to Kafka. Call connect() first."
            raise RuntimeError(error_msg)
        try:
            message_bytes = self.serialize_message(message)
            key_bytes = self._serialize_key(key)
            await self._producer.send(
                topic=topic,
                value=message_bytes,
                key=key_bytes,
                partition=partition,
            )
        except KafkaError as e:
            error_msg = f"Failed to publish message to topic '{topic}': {e}"
            raise OperationError(error_msg, str(e)) from e

    async def consume(  # type: ignore[override]
        self,
        topic: str,
        group_id: str | None = None,
        auto_offset_reset: str = "latest",
        timeout: float | None = None,
        handler: Callable[[dict[str, Any] | str], None] | None = None,
    ) -> AsyncIterator[dict[str, Any] | str]:
        """
        Consume messages from Kafka topic.

        Args:
            topic: Topic name to consume from
            group_id: Consumer group ID (optional)
            auto_offset_reset: Offset reset policy ("earliest" or "latest", default: "latest")
            timeout: Timeout in seconds for receiving messages (uses config timeout if None)
            handler: Optional callback function to handle messages

        Yields:
            Message content (dict if JSON, str otherwise)

        Raises:
            RuntimeError: If not connected
            OperationError: If consumption fails

        Example:
            >>> async for message in kafka.consume("test-topic"):
            ...     print(f"Received: {message}")
            >>> # With handler
            >>> async def handle_message(msg):
            ...     print(f"Handled: {msg}")
            >>> async for message in kafka.consume("test-topic", handler=handle_message):
            ...     pass
        """
        if not self._is_connected:
            error_msg = "Not connected to Kafka. Call connect() first."
            raise RuntimeError(error_msg)
        consumer = await self._get_or_create_consumer(topic, group_id, auto_offset_reset)
        try:
            async for msg in consumer:
                try:
                    parsed_message = self._process_message(msg.value, handler)
                    yield parsed_message
                except Exception as e:
                    error_msg = f"Failed to process message from topic '{topic}': {e}"
                    raise OperationError(error_msg, str(e)) from e
        except KafkaError as e:
            error_msg = f"Failed to consume messages from topic '{topic}': {e}"
            raise OperationError(error_msg, str(e)) from e
