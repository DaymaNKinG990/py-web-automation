"""
Middleware context objects for WebSocket client.

This module provides message and connection context objects for WebSocket middleware.
"""

# Python imports
from typing import Any


class _WebSocketMessageContext:
    """
    Internal context object for WebSocket message middleware.

    Contains message information that can be modified by middleware.
    This is an internal class used only within middleware system.

    Attributes:
        direction: Message direction ("send" or "receive")
        message: Message content (can be modified)
        metadata_context: Custom metadata dictionary for middleware communication
    """

    def __init__(
        self,
        direction: str,
        message: dict[str, Any] | str,
    ) -> None:
        """Initialize WebSocket message context."""
        self.direction = direction
        self.message = message
        self.metadata_context: dict[str, Any] = {}


class _WebSocketConnectionContext:
    """
    Internal context object for WebSocket connection middleware.

    Contains connection information for connect/disconnect events.
    This is an internal class used only within middleware system.

    Attributes:
        event_type: Connection event type ("connect" or "disconnect")
        url: WebSocket URL
        metadata_context: Custom metadata dictionary for middleware communication
    """

    def __init__(
        self,
        event_type: str,
        url: str,
    ) -> None:
        """Initialize WebSocket connection context."""
        self.event_type = event_type  # "connect" or "disconnect"
        self.url = url
        self.metadata_context: dict[str, Any] = {}
