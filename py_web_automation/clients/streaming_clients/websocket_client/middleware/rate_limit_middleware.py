"""
Rate limiting middleware for WebSocket client.

This module provides RateLimitMiddleware for rate limiting WebSocket message sending.
"""

# Local imports
from ..rate_limit import RateLimiter
from ..websocket_result import WebSocketResult
from .context import _WebSocketConnectionContext, _WebSocketMessageContext
from .middleware import Middleware


class RateLimitMiddleware(Middleware):
    """
    Middleware for rate limiting WebSocket message sending.

    Limits the number of messages sent per time window using sliding window algorithm.
    Only applies to "send" direction messages.

    Attributes:
        rate_limiter: RateLimiter instance

    Example:
        >>> from py_web_automation.clients.websocket_client import WebSocketClient, MiddlewareChain
        >>> from py_web_automation.clients.websocket_client.middleware import RateLimitMiddleware
        >>> from py_web_automation.clients.websocket_client import RateLimiter, RateLimitConfig
        >>> rate_limiter = RateLimiter(RateLimitConfig(max_requests=100, window=60))
        >>> rate_limit_middleware = RateLimitMiddleware(rate_limiter)
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(rate_limit_middleware)
        >>> async with WebSocketClient(
        ...     "ws://example.com/ws", config, middleware=middleware_chain
        ... ) as ws:
        ...     await ws.send_message({"type": "ping"})
    """

    def __init__(self, rate_limiter: RateLimiter) -> None:
        """
        Initialize rate limit middleware.

        Args:
            rate_limiter: RateLimiter instance to use
        """
        self.rate_limiter = rate_limiter

    async def process_message(self, context: _WebSocketMessageContext) -> None:
        """
        Acquire rate limit slot before sending message.

        Only applies to "send" direction.

        Args:
            context: Message context
        """
        if context.direction == "send":
            await self.rate_limiter.acquire()

    async def process_connection(self, context: _WebSocketConnectionContext) -> None:
        """
        No-op for connections.

        Args:
            context: Connection context
        """
        pass

    async def process_error(
        self,
        context: _WebSocketMessageContext | _WebSocketConnectionContext,
        error: Exception,
    ) -> WebSocketResult | None:
        """
        No-op for errors.

        Args:
            context: Message or connection context
            error: Exception that occurred
        """
        return None
