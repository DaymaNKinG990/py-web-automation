"""
Retry mechanism with exponential backoff for WebSocket connections.

This module provides retry handler for automatic retry of failed WebSocket connections
with configurable exponential backoff strategy.
"""

# Python imports
from asyncio import sleep
from random import uniform
from typing import TYPE_CHECKING, Any

# Local imports
from ....exceptions import ConnectionError, TimeoutError

if TYPE_CHECKING:
    from .middleware.context import _WebSocketConnectionContext
    from .websocket_result import WebSocketResult


class RetryConfig:
    """
    Configuration for retry behavior for WebSocket connections.

    Provides a structured way to configure retry parameters
    that can be reused across multiple connection attempts.

    Attributes:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for exponential backoff
        exceptions: Tuple of exception types to catch and retry
        max_delay: Maximum delay between retries (caps exponential backoff)
        jitter: Random jitter to add to delay (prevents thundering herd)

    Example:
        >>> config = RetryConfig(
        ...     max_attempts=5,
        ...     delay=1.0,
        ...     backoff=2.0,
        ...     max_delay=30.0
        ... )
        >>> @retry_on_failure(**config.to_dict())
        ... async def operation():
        ...     pass
    """

    def __init__(
        self,
        max_attempts: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: tuple[type[Exception], ...] = (Exception,),
        max_delay: float | None = None,
        jitter: bool = False,
    ) -> None:
        """
        Initialize retry configuration.

        Args:
            max_attempts: Maximum number of retry attempts
            delay: Initial delay between retries in seconds
            backoff: Multiplier for exponential backoff
            exceptions: Tuple of exception types to catch and retry
            max_delay: Maximum delay between retries (None = no limit)
            jitter: Add random jitter to delay to prevent thundering herd
        """
        self.max_attempts = max_attempts
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions
        self.max_delay = max_delay
        self.jitter = jitter

    @property
    def to_dict(self) -> dict[str, Any]:
        """
        Convert configuration to dictionary for decorator.

        Returns:
            Dictionary representation of configuration
        """
        return {
            "max_attempts": self.max_attempts,
            "delay": self.delay,
            "backoff": self.backoff,
            "exceptions": self.exceptions,
        }

    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for a specific attempt.

        Args:
            attempt: Attempt number (0-indexed)

        Returns:
            Delay in seconds for this attempt
        """

        delay = self.delay * (self.backoff**attempt)
        if self.max_delay:
            delay = min(delay, self.max_delay)
        if self.jitter:
            # Add ±10% jitter
            jitter_amount = delay * 0.1
            delay += uniform(-jitter_amount, jitter_amount)
            delay = max(0, delay)  # Ensure non-negative
        return delay


class RetryHandler:
    """
    Internal retry handler for WebSocket connection middleware system.

    Handles retry logic with exponential backoff and configurable exceptions.
    Supports retry on connection errors and timeouts.

    Attributes:
        config: Retry configuration
        _attempts: Dictionary tracking retry attempts per connection key
    """

    def __init__(self, config: RetryConfig | None = None) -> None:
        """
        Initialize retry handler.

        Args:
            config: Retry configuration (creates default if None)
        """
        if config is None:
            config = RetryConfig(
                max_attempts=3,
                delay=1.0,
                backoff=2.0,
                exceptions=(ConnectionError, TimeoutError),
            )
        self.config = config
        self._attempts: dict[str, int] = {}

    def _get_request_key(self, context: "_WebSocketConnectionContext") -> str:
        """
        Generate unique key for WebSocket connection tracking.

        Args:
            context: WebSocket connection context

        Returns:
            Unique key for this connection
        """
        # Use URL as key, with connection ID if available
        connection_id = context.metadata_context.get("connection_id")
        if connection_id:
            return f"{context.url}:{connection_id}"
        return context.url

    def _should_retry(self, error: Exception) -> bool:
        """
        Check if error should trigger retry.

        Args:
            error: Exception to check

        Returns:
            True if error should trigger retry
        """
        return isinstance(error, self.config.exceptions)

    async def handle_error(
        self,
        context: "_WebSocketConnectionContext",
        error: Exception,
    ) -> "WebSocketResult" | None:
        """
        Handle error and determine if retry is needed.

        Checks if error is retryable, tracks attempts, and waits if retry is needed.
        Returns None if retry should be attempted, or WebSocketResult if retry limit exceeded.

        Args:
            context: WebSocket connection context
            error: Exception that occurred

        Returns:
            None if retry should be attempted, WebSocketResult with error if limit exceeded
        """
        if not self._should_retry(error):
            # Error is not retryable, return None to let error propagate
            return None
        request_key = self._get_request_key(context)
        current_attempt = self._attempts.get(request_key, 0)
        current_attempt += 1
        self._attempts[request_key] = current_attempt
        if current_attempt >= self.config.max_attempts:
            # Retry limit exceeded, clean up and return error result
            del self._attempts[request_key]
            # Return None to let error propagate (WebSocketClient will create error WebSocketResult)
            return None
        # Calculate delay and wait
        attempt_index = current_attempt - 1  # 0-indexed for delay calculation
        delay = self.config.calculate_delay(attempt_index)
        await sleep(delay)
        # Store retry info in metadata for WebSocketClient to check
        context.metadata_context["retry_attempt"] = current_attempt
        context.metadata_context["should_retry"] = True
        # Return None to indicate retry should be attempted
        # WebSocketClient will check metadata and retry the connection
        return None
