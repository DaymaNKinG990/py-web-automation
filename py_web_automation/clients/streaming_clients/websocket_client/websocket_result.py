"""
Data models for WebSocket API client.

This module provides WebSocketResult class for standardized WebSocket message results.
"""

# Python imports
from typing import Any

from msgspec import Struct, field


class WebSocketResult(Struct, frozen=True):
    """
    WebSocket message result.

    Contains complete information about a WebSocket message operation,
    including message content, direction, timing, and metadata.

    Attributes:
        direction: Message direction ("send" or "receive")
        message: Message content (dict or str)
        timestamp: Timestamp when message was sent/received
        success: Whether the operation completed successfully
        error: Error message (None if operation succeeded)
        metadata: Custom metadata dictionary for middleware communication

    Example:
        >>> result = await ws.send_message({"type": "ping"})
        >>> if result.success:
        ...     print(f"Sent at {result.timestamp}")
        >>> else:
        ...     print(f"Error: {result.error}")
    """

    direction: str  # "send" or "receive"
    message: dict[str, Any] | str
    timestamp: float
    success: bool
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def raise_for_error(self) -> None:
        """
        Raise exception if operation failed.

        Raises:
            Exception: If operation failed with error

        Example:
            >>> result = await ws.send_message({"type": "ping"})
            >>> result.raise_for_error()  # Raises if operation failed
        """
        if not self.success and self.error:
            raise Exception(f"WebSocket {self.direction} operation failed: {self.error}")
