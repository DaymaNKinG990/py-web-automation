"""
Rate limiting system for SOAP client.

This module provides rate limiting functionality using sliding window algorithm
to prevent exceeding SOAP API rate limits.
"""

# Python imports
from asyncio import Lock, sleep
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class RateLimitConfig:
    """
    Configuration for rate limiting SOAP operations.

    Attributes:
        max_requests: Maximum number of operations allowed
        window: Time window in seconds
        burst: Maximum burst size (allows short bursts above max_requests)
    """

    max_requests: int = 100
    window: int = 60  # 1 minute
    burst: int = 10  # Allow 10 extra operations in burst


class RateLimiter:
    """
    Rate limiter using sliding window algorithm for SOAP operations.

    Tracks SOAP operations in a sliding time window and blocks operations
    that would exceed the rate limit.

    Attributes:
        config: Rate limit configuration
        requests: Deque of operation timestamps
        _lock: Async lock for thread safety
    """

    def __init__(
        self,
        max_requests: int = 100,
        window: int = 60,
        burst: int | None = None,
    ) -> None:
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum number of operations allowed in window
            window: Time window in seconds
            burst: Maximum burst size (default: 10% of max_requests)
        """
        self.config = RateLimitConfig(
            max_requests=max_requests,
            window=window,
            burst=burst or max(1, max_requests // 10),
        )
        self.requests: deque[datetime] = deque()
        self._lock = Lock()

    async def acquire(self) -> None:
        """
        Acquire permission to make a SOAP operation.

        Blocks if rate limit would be exceeded, waiting until a slot becomes available.

        Example:
            >>> from py_web_automation.clients.soap_client import (
            ...     SoapClient,
            ...     MiddlewareChain,
            ... )
            >>> from py_web_automation.clients.soap_client.middleware import (
            ...     RateLimitMiddleware,
            ... )
            >>> from py_web_automation.clients.soap_client.rate_limit import RateLimiter
            >>> rate_limiter = RateLimiter(max_requests=100, window=60)
            >>> middleware = MiddlewareChain().add(RateLimitMiddleware(rate_limiter))
            >>> async with SoapClient(
            ...     "https://api.example.com/soap", config, middleware=middleware
            ... ) as soap:
            ...     result = await soap.call("GetUser", {"userId": "123"})
            ...     # acquire() is called automatically by RateLimitMiddleware
        """
        async with self._lock:
            self._cleanup_old_requests()

            if self._is_rate_limit_exceeded():
                await self._wait_for_slot()
                self._cleanup_old_requests()

            self.requests.append(datetime.now())

    def _cleanup_old_requests(self) -> None:
        """Remove operations outside the time window."""
        now = datetime.now()
        window_start = now - timedelta(seconds=self.config.window)
        while self.requests and self.requests[0] < window_start:
            self.requests.popleft()

    def _is_rate_limit_exceeded(self) -> bool:
        """Check if rate limit is exceeded."""
        return len(self.requests) >= self.config.max_requests

    async def _wait_for_slot(self) -> None:
        """Wait until a slot becomes available."""
        oldest_request = self.requests[0]
        wait_until = oldest_request + timedelta(seconds=self.config.window)
        wait_time = (wait_until - datetime.now()).total_seconds()
        if wait_time > 0:
            await sleep(wait_time)

    async def try_acquire(self) -> bool:
        """
        Try to acquire permission without blocking.

        Returns:
            True if permission granted, False if rate limit exceeded

        Example:
            >>> from py_web_automation.clients.soap_client import (
            ...     SoapClient,
            ...     MiddlewareChain,
            ... )
            >>> from py_web_automation.clients.soap_client.middleware import (
            ...     RateLimitMiddleware,
            ... )
            >>> from py_web_automation.clients.soap_client.rate_limit import RateLimiter
            >>> rate_limiter = RateLimiter(max_requests=5, window=10)
            >>> middleware = MiddlewareChain().add(RateLimitMiddleware(rate_limiter))
            >>> async with SoapClient(
            ...     "https://api.example.com/soap", config, middleware=middleware
            ... ) as soap:
            ...     if await rate_limiter.try_acquire():
            ...         result = await soap.call("GetUser", {"userId": "123"})
            ...     else:
            ...         print("Rate limit exceeded, skipping operation")
        """
        async with self._lock:
            now = datetime.now()
            window_start = now - timedelta(seconds=self.config.window)
            # Remove requests outside the window
            while self.requests and self.requests[0] < window_start:
                self.requests.popleft()
            # Check if we can make a request
            if len(self.requests) >= self.config.max_requests:
                return False
            # Record this request
            self.requests.append(now)
            return True

    def reset(self) -> None:
        """Reset rate limiter (clear all request history)."""
        self.requests.clear()

    def get_remaining(self) -> int:
        """
        Get remaining operations in current window.

        Returns:
            Number of operations that can be made without waiting
        """
        now = datetime.now()
        window_start = now - timedelta(seconds=self.config.window)
        # Remove requests outside the window
        while self.requests and self.requests[0] < window_start:
            self.requests.popleft()
        return max(0, self.config.max_requests - len(self.requests))

    def get_wait_time(self) -> float:
        """
        Get time to wait before next operation can be made.

        Returns:
            Seconds to wait (0 if no wait needed)
        """
        if len(self.requests) < self.config.max_requests:
            return 0.0
        now = datetime.now()
        oldest_request = self.requests[0]
        wait_until = oldest_request + timedelta(seconds=self.config.window)
        wait_time = (wait_until - now).total_seconds()
        return max(0.0, wait_time)
