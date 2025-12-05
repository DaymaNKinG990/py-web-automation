"""
Logging middleware for WebSocket client.

This module provides LoggingMiddleware for automatic WebSocket message and connection logging.
"""

# Python imports
from loguru import logger

# Local imports
from ..websocket_result import WebSocketResult
from .context import _WebSocketConnectionContext, _WebSocketMessageContext
from .middleware import Middleware


class LoggingMiddleware(Middleware):
    """
    Middleware for automatic WebSocket message and connection logging.

    Logs all messages (sent/received) and connection events.

    Example:
        >>> from py_web_automation.clients.websocket_client import WebSocketClient, MiddlewareChain
        >>> from py_web_automation.clients.websocket_client.middleware import LoggingMiddleware
        >>> logging_middleware = LoggingMiddleware()
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(logging_middleware)
        >>> async with WebSocketClient(
        ...     "ws://example.com/ws", config, middleware=middleware_chain
        ... ) as ws:
        ...     await ws.send_message({"type": "ping"})
    """

    async def process_message(self, context: _WebSocketMessageContext) -> None:
        """
        Log WebSocket message.

        Args:
            context: Message context
        """
        message_preview = (
            str(context.message)[:100] if len(str(context.message)) > 100 else str(context.message)
        )
        logger.info(f"WebSocket {context.direction}: {message_preview}")

    async def process_connection(self, context: _WebSocketConnectionContext) -> None:
        """
        Log WebSocket connection event.

        Args:
            context: Connection context
        """
        logger.info(f"WebSocket {context.event_type}: {context.url}")

    async def process_error(
        self,
        context: _WebSocketMessageContext | _WebSocketConnectionContext,
        error: Exception,
    ) -> WebSocketResult | None:
        """
        Log WebSocket error.

        Args:
            context: Message or connection context
            error: Exception that occurred
        """
        if isinstance(context, _WebSocketMessageContext):
            logger.error(f"WebSocket {context.direction} error: {error}")
        else:
            logger.error(f"WebSocket {context.event_type} error: {error}")
        return None
