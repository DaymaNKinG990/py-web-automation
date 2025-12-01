"""
WebSocket API client for web automation testing.

This module provides WebSocketClient for testing WebSocket connections,
including message sending, receiving, and connection management.
"""

import json
from collections.abc import AsyncIterator, Callable
from typing import Any

try:
    from websockets import connect
    from websockets.asyncio.client import ClientConnection
    from websockets.exceptions import WebSocketException
except ImportError:
    raise ImportError("WebSocket support requires 'websockets' library. Install it with: uv add websockets") from None

import builtins

from ..config import Config
from ..exceptions import ConnectionError, OperationError, TimeoutError
from .base_client import BaseClient


class WebSocketClient(BaseClient):
    """
    WebSocket API client for web automation testing.

    Implements WebSocket protocol support for testing real-time communication.
    Follows the Single Responsibility Principle by focusing solely on WebSocket testing.

    Provides methods for testing WebSocket connections:
    - Connection establishment and management
    - Message sending and receiving
    - Event handling with callbacks
    - Connection state monitoring
    - Automatic reconnection support

    Attributes:
        _websocket: WebSocket connection (private)
        _is_connected: Connection state flag (private)
        _message_handlers: Registered message handlers (private)

    Example:
        >>> from py_web_automation import Config, WebSocketClient
        >>> config = Config(timeout=30)
        >>> async with WebSocketClient("ws://example.com/ws", config) as ws:
        ...     await ws.send_message({"type": "ping"})
        ...     message = await ws.receive_message()
        ...     print(f"Received: {message}")
    """

    def __init__(self, url: str, config: Config | None = None) -> None:
        """
        Initialize WebSocket client.

        Args:
            url: WebSocket URL (ws:// or wss://)
            config: Configuration object with timeout settings

        Raises:
            ValueError: If URL is not a valid WebSocket URL

        Example:
            >>> config = Config(timeout=30)
            >>> ws = WebSocketClient("wss://api.example.com/ws", config)
        """
        # Validate WebSocket URL
        if not (url.startswith("ws://") or url.startswith("wss://")):
            raise ValueError(f"Invalid WebSocket URL: {url}. Must start with ws:// or wss://")

        super().__init__(url, config)
        self._websocket: ClientConnection | None = None
        self._is_connected: bool = False
        self._message_handlers: dict[str, Callable[[dict[str, Any]], None]] = {}

    async def connect(self) -> None:
        """
        Establish WebSocket connection.

        Raises:
            ConnectionError: If connection fails
            TimeoutError: If connection times out

        Example:
            >>> await ws.connect()
        """
        if self._is_connected:
            self.logger.debug("Already connected to WebSocket")
            return

        try:
            self._websocket = await connect(self.url, timeout=self.config.timeout, ping_interval=None)
            self._is_connected = True
            self.logger.info(f"Connected to WebSocket: {self.url}")
        except WebSocketException as e:
            error_msg = f"Failed to connect to WebSocket {self.url}: {e}"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg, str(e)) from e
        except Exception as e:
            error_msg = f"Unexpected error connecting to WebSocket: {e}"
            self.logger.error(error_msg)
            raise ConnectionError(error_msg, str(e)) from e

    async def disconnect(self) -> None:
        """
        Close WebSocket connection.

        Example:
            >>> await ws.disconnect()
        """
        if self._websocket and self._is_connected:
            await self._websocket.close()
            self._websocket = None
            self._is_connected = False
            self.logger.info("Disconnected from WebSocket")

    async def is_connected(self) -> bool:
        """
        Check if WebSocket is connected.

        Returns:
            True if connected, False otherwise
        """
        return self._is_connected and self._websocket is not None

    async def send_message(self, message: dict[str, Any] | str) -> None:
        """
        Send message through WebSocket connection.

        Args:
            message: Message to send (dict will be JSON encoded, str sent as-is)

        Raises:
            ConnectionError: If not connected
            OperationError: If sending fails

        Example:
            >>> await ws.send_message({"type": "ping", "data": "test"})
            >>> await ws.send_message('{"type": "ping"}')
        """
        if not await self.is_connected():
            error_msg = "Not connected to WebSocket. Call connect() first."
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)

        try:
            if isinstance(message, dict):
                message_str = json.dumps(message)
            else:
                message_str = str(message)

            await self._websocket.send(message_str)  # type: ignore[union-attr]
            self.logger.debug(f"Sent message: {message_str[:100]}")
        except Exception as e:
            error_msg = f"Failed to send message: {e}"
            self.logger.error(error_msg)
            raise OperationError(error_msg, str(e)) from e

    async def receive_message(self, timeout: float | None = None) -> dict[str, Any] | str:
        """
        Receive message from WebSocket connection.

        Args:
            timeout: Optional timeout in seconds (uses config timeout if not provided)

        Returns:
            Received message (parsed as JSON if possible, otherwise as string)

        Raises:
            ConnectionError: If not connected
            TimeoutError: If no message received within timeout
            OperationError: If receiving fails

        Example:
            >>> message = await ws.receive_message(timeout=5.0)
            >>> print(f"Received: {message}")
        """
        if not await self.is_connected():
            error_msg = "Not connected to WebSocket. Call connect() first."
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)

        timeout = timeout or self.config.timeout

        try:
            import asyncio

            if self._websocket is None:
                raise RuntimeError("WebSocket is not connected")
            message_str = await asyncio.wait_for(
                self._websocket.recv(),
                timeout=timeout if timeout is not None else 30.0,
            )

            # Try to parse as JSON
            try:
                # Handle bytes if needed
                if isinstance(message_str, bytes):
                    message_str = message_str.decode("utf-8", errors="replace")
                message = json.loads(message_str)
                self.logger.debug(f"Received JSON message: {type(message)}")
                return message
            except (json.JSONDecodeError, TypeError):
                # Ensure message_str is string for logging and return
                if isinstance(message_str, bytes):
                    message_str = message_str.decode("utf-8", errors="replace")
                msg_preview = message_str[:100]
                self.logger.debug(f"Received text message: {msg_preview}")
                return message_str

        except builtins.TimeoutError as e:
            error_msg = f"Timeout waiting for message: {timeout}s"
            self.logger.error(error_msg)
            raise TimeoutError(error_msg, str(e)) from e
        except Exception as e:
            error_msg = f"Failed to receive message: {e}"
            self.logger.error(error_msg)
            raise OperationError(error_msg, str(e)) from e

    async def listen(
        self, handler: Callable[[dict[str, Any] | str], None] | None = None
    ) -> AsyncIterator[dict[str, Any] | str]:
        """
        Listen for incoming messages as an async iterator.

        Args:
            handler: Optional callback function to process each message

        Yields:
            Received messages

        Raises:
            ConnectionError: If not connected

        Example:
            >>> async for message in ws.listen():
            ...     print(f"Received: {message}")
            ...     if message.get("type") == "close":
            ...         break
        """
        if not await self.is_connected():
            error_msg = "Not connected to WebSocket. Call connect() first."
            self.logger.error(error_msg)
            raise ConnectionError(error_msg)

        try:
            while self._is_connected:
                message = await self.receive_message()
                if handler:
                    handler(message)
                yield message
        except (ConnectionError, OperationError):
            # Re-raise connection and operation errors
            raise
        except Exception as e:
            error_msg = f"Error in WebSocket listener: {e}"
            self.logger.error(error_msg)
            raise OperationError(error_msg, str(e)) from e

    def register_handler(self, message_type: str, handler: Callable[[dict[str, Any]], None]) -> None:
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
        self.logger.debug(f"Registered handler for message type: {message_type}")

    async def close(self) -> None:
        """
        Close WebSocket connection and cleanup resources.

        This method is automatically called when exiting an async context manager.
        """
        await self.disconnect()
        self._message_handlers.clear()

    async def __aenter__(self) -> "WebSocketClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()
