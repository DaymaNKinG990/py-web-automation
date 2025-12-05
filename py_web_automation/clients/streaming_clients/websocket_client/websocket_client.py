"""
WebSocket API client for web automation testing.

This module provides WebSocketClient for testing WebSocket connections,
including message sending, receiving, and connection management.
"""

# Python imports
from __future__ import annotations

from asyncio import sleep, wait_for
from collections.abc import AsyncIterator, Callable
from json import dumps, loads
from json.decoder import JSONDecodeError
from time import time
from types import TracebackType
from typing import TYPE_CHECKING, Any

from websockets import connect
from websockets.asyncio.client import ClientConnection
from websockets.exceptions import WebSocketException

# Local imports
from ....config import Config
from ....exceptions import ConnectionError, OperationError, TimeoutError
from .middleware.context import _WebSocketConnectionContext, _WebSocketMessageContext
from .websocket_result import WebSocketResult

if TYPE_CHECKING:
    from .middleware.context import _WebSocketConnectionContext, _WebSocketMessageContext
    from .middleware.middleware import MiddlewareChain


class WebSocketClient:
    """
    WebSocket API client for web automation testing.

    Implements WebSocket protocol support for testing real-time communication.
    Follows the Single Responsibility Principle by focusing solely on WebSocket testing.

    Provides methods for testing WebSocket connections:
    - Connection establishment and management with retry support
    - Message sending and receiving with middleware support
    - Event handling with callbacks
    - Connection state monitoring
    - Automatic reconnection support via middleware

    Attributes:
        url: WebSocket URL (ws:// or wss://)
        config: Configuration object
        _websocket: WebSocket connection (private)
        _is_connected: Connection state flag (private)
        _message_handlers: Registered message handlers (private)
        _middleware: Middleware chain for message/connection processing (private)

    Example:
        >>> from py_web_automation.clients.websocket_client import WebSocketClient, MiddlewareChain
        >>> from py_web_automation.clients.websocket_client.middleware import LoggingMiddleware
        >>> config = Config(timeout=30)
        >>> middleware = MiddlewareChain().add(LoggingMiddleware())
        >>> async with WebSocketClient("ws://example.com/ws", config, middleware) as ws:
        ...     result = await ws.send_message({"type": "ping"})
        ...     if result.success:
        ...         message_result = await ws.receive_message()
        ...         print(message_result.message)
    """

    def __init__(
        self,
        url: str,
        config: Config | None = None,
        middleware: MiddlewareChain | None = None,
    ) -> None:
        """
        Initialize WebSocket client.

        Args:
            url: WebSocket URL (ws:// or wss://)
            config: Configuration object with timeout settings
            middleware: Optional middleware chain for message/connection processing

        Raises:
            ValueError: If URL is not a valid WebSocket URL
            TypeError: If config is not a Config object when provided

        Example:
            >>> config = Config(timeout=30)
            >>> middleware = MiddlewareChain().add(LoggingMiddleware())
            >>> ws = WebSocketClient("wss://api.example.com/ws", config, middleware)
        """
        # Validate WebSocket URL
        if not (url.startswith("ws://") or url.startswith("wss://")):
            raise ValueError(f"Invalid WebSocket URL: {url}. Must start with ws:// or wss://")
        if config is None:
            config = Config()
        elif not isinstance(config, Config):
            raise TypeError("config must be a Config object")
        self.url: str = url
        self.config: Config = config
        self._websocket: ClientConnection | None = None
        self._is_connected: bool = False
        self._message_handlers: dict[str, Callable[[dict[str, Any]], None]] = {}
        self._middleware = middleware

    async def __aenter__(self) -> WebSocketClient:
        """
        Async context manager entry.

        Returns:
            Self for use in async with statement

        Example:
            >>> async with WebSocketClient("ws://example.com/ws", config) as ws:
            ...     # Client is ready to use
            ...     pass
        """
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Async context manager exit.

        Ensures proper cleanup by calling close() method.
        """
        await self.close()

    async def connect(self) -> None:
        """
        Establish WebSocket connection with retry support via middleware.

        Raises:
            ConnectionError: If connection fails after retries

        Example:
            >>> await ws.connect()
        """
        if self._is_connected:
            return
        connection_context = _WebSocketConnectionContext(
            event_type="connect",
            url=self.url,
        )
        # Process connection through middleware
        if self._middleware:
            await self._middleware.process_connection(connection_context)
        # Retry loop for connection
        while True:
            try:
                self._websocket = await connect(
                    self.url, timeout=self.config.timeout, ping_interval=None
                )
                self._is_connected = True
                # Process successful connection
                if self._middleware:
                    await self._middleware.process_connection(connection_context)
                return
            except (WebSocketException, Exception) as e:
                # Process error through middleware
                if self._middleware:
                    error_result = await self._middleware.process_error(connection_context, e)
                    if error_result is not None:
                        # Middleware handled the error
                        continue
                    # Check if retry is needed
                    if connection_context.metadata_context.get("should_retry"):
                        delay = connection_context.metadata_context.get("retry_delay", 0)
                        if delay > 0:
                            await sleep(delay)
                        continue  # Retry connection
                # No retry, raise error
                error_msg = f"Failed to connect to WebSocket {self.url}: {e}"
                raise ConnectionError(error_msg, str(e)) from e

    async def disconnect(self) -> None:
        """
        Close WebSocket connection.

        Example:
            >>> await ws.disconnect()
        """
        if self._websocket and self._is_connected:
            connection_context = _WebSocketConnectionContext(
                event_type="disconnect",
                url=self.url,
            )
            # Process disconnection through middleware
            if self._middleware:
                await self._middleware.process_connection(connection_context)
            await self._websocket.close()
            self._websocket = None
            self._is_connected = False

    async def is_connected(self) -> bool:
        """
        Check if WebSocket is connected.

        Returns:
            True if connected, False otherwise
        """
        return self._is_connected and self._websocket is not None

    async def send_message(self, message: dict[str, Any] | str) -> WebSocketResult:
        """
        Send message through WebSocket connection with middleware support.

        Args:
            message: Message to send (dict will be JSON encoded, str sent as-is)

        Returns:
            WebSocketResult with message, timestamp, and success status

        Raises:
            ConnectionError: If not connected
            OperationError: If sending fails

        Example:
            >>> result = await ws.send_message({"type": "ping", "data": "test"})
            >>> if result.success:
            ...     print(f"Sent at {result.timestamp}")
        """
        if not await self.is_connected():
            error_msg = "Not connected to WebSocket. Call connect() first."
            raise ConnectionError(error_msg)
        timestamp = time()
        message_context = _WebSocketMessageContext(
            direction="send",
            message=message,
        )
        # Process message through middleware (may modify message)
        if self._middleware:
            await self._middleware.process_message(message_context)
        try:
            # Use message from context (may have been modified by middleware)
            processed_message = message_context.message
            if isinstance(processed_message, dict):
                message_str = dumps(processed_message)
            else:
                message_str = str(processed_message)
            if self._websocket is None:
                raise RuntimeError("WebSocket is not connected")
            await self._websocket.send(message_str)
            return WebSocketResult(
                direction="send",
                message=processed_message,
                timestamp=timestamp,
                success=True,
                error=None,
                metadata=message_context.metadata_context.copy(),
            )
        except Exception as e:
            # Process error through middleware
            if self._middleware:
                error_result = await self._middleware.process_error(message_context, e)
                if error_result is not None:
                    return error_result
            error_msg = f"Failed to send message: {e}"
            return WebSocketResult(
                direction="send",
                message=message,
                timestamp=timestamp,
                success=False,
                error=error_msg,
                metadata=message_context.metadata_context.copy(),
            )

    async def receive_message(self, timeout: float | None = None) -> WebSocketResult:
        """
        Receive message from WebSocket connection with middleware support.

        Args:
            timeout: Optional timeout in seconds (uses config timeout if not provided)

        Returns:
            WebSocketResult with received message, timestamp, and success status

        Raises:
            ConnectionError: If not connected
            TimeoutError: If no message received within timeout
            OperationError: If receiving fails

        Example:
            >>> result = await ws.receive_message(timeout=5.0)
            >>> if result.success:
            ...     print(f"Received: {result.message} at {result.timestamp}")
        """
        if not await self.is_connected():
            error_msg = "Not connected to WebSocket. Call connect() first."
            raise ConnectionError(error_msg)
        timeout = timeout or self.config.timeout
        timestamp = time()
        try:
            if self._websocket is None:
                raise RuntimeError("WebSocket is not connected")
            message_str = await wait_for(
                self._websocket.recv(),
                timeout=timeout if timeout is not None else 30.0,
            )
            # Try to parse as JSON
            try:
                # Handle bytes if needed
                if isinstance(message_str, bytes):
                    message_str = message_str.decode("utf-8", errors="replace")
                message = loads(message_str)
            except (JSONDecodeError, TypeError):
                # Ensure message_str is string for logging and return
                if isinstance(message_str, bytes):
                    message_str = message_str.decode("utf-8", errors="replace")
                message = message_str
            message_context = _WebSocketMessageContext(
                direction="receive",
                message=message,
            )
            message_context.metadata_context["receive_timestamp"] = timestamp
            # Process message through middleware (may modify message)
            if self._middleware:
                await self._middleware.process_message(message_context)
            return WebSocketResult(
                direction="receive",
                message=message_context.message,  # Use potentially modified message
                timestamp=timestamp,
                success=True,
                error=None,
                metadata=message_context.metadata_context.copy(),
            )
        except TimeoutError as e:
            error_msg = f"Timeout waiting for message: {timeout}s"
            message_context = _WebSocketMessageContext(
                direction="receive",
                message="",
            )
            if self._middleware:
                error_result = await self._middleware.process_error(
                    message_context, TimeoutError(error_msg, str(e))
                )
                if error_result is not None:
                    return error_result
            raise TimeoutError(error_msg, str(e)) from e
        except Exception as e:
            error_msg = f"Failed to receive message: {e}"
            message_context = _WebSocketMessageContext(
                direction="receive",
                message="",
            )
            if self._middleware:
                error_result = await self._middleware.process_error(message_context, e)
                if error_result is not None:
                    return error_result
            raise OperationError(error_msg, str(e)) from e

    async def listen(
        self, handler: Callable[[dict[str, Any] | str], None] | None = None
    ) -> AsyncIterator[WebSocketResult]:
        """
        Listen for incoming messages as an async iterator.

        Args:
            handler: Optional callback function to process each message

        Yields:
            WebSocketResult for each received message

        Raises:
            ConnectionError: If not connected

        Example:
            >>> async for result in ws.listen():
            ...     if result.success:
            ...         print(f"Received: {result.message}")
            ...         msg_dict = isinstance(result.message, dict)
            ...         if msg_dict and result.message.get("type") == "close":
            ...             break
        """
        if not await self.is_connected():
            error_msg = "Not connected to WebSocket. Call connect() first."
            raise ConnectionError(error_msg)
        try:
            while self._is_connected:
                result = await self.receive_message()
                if handler:
                    handler(result.message)
                yield result
        except (ConnectionError, OperationError):
            # Re-raise connection and operation errors
            raise
        except Exception as e:
            error_msg = f"Error in WebSocket listener: {e}"
            raise OperationError(error_msg, str(e)) from e

    def register_handler(
        self, message_type: str, handler: Callable[[dict[str, Any]], None]
    ) -> None:
        """
        Register message handler for specific message type.

        Args:
            message_type: Message type to handle
            handler: Handler function that receives message dict

        Example:
            >>> def handle_ping(message):
            ...     print(f"Received ping: {message}")
            >>> ws.register_handler("ping", handle_ping)
        """
        self._message_handlers[message_type] = handler

    async def close(self) -> None:
        """
        Close WebSocket connection and cleanup resources.

        This method is automatically called when exiting an async context manager.
        """
        await self.disconnect()
        self._message_handlers.clear()
