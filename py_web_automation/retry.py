"""
Retry mechanism with exponential backoff for web automation framework.

This module provides decorators and utilities for automatic retry of failed operations
with configurable exponential backoff strategy.
"""

import asyncio
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from .exceptions import ConnectionError, TimeoutError

P = ParamSpec("P")
R = TypeVar("R")


def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    on_retry: Callable[[int, Exception], None] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for automatic retry with exponential backoff.

    Automatically retries a function call if it raises one of the specified exceptions.
    Uses exponential backoff to increase delay between retries.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Multiplier for exponential backoff (default: 2.0)
        exceptions: Tuple of exception types to catch and retry (default: (Exception,))
        on_retry: Optional callback function called on each retry attempt.
                 Receives (attempt_number, exception) as arguments.

    Returns:
        Decorated function with retry logic

    Example:
        >>> @retry_on_failure(max_attempts=3, delay=1.0, backoff=2.0)
        ... async def fetch_data():
        ...     # This will be retried up to 3 times with exponential backoff
        ...     return await api.make_request("/data")
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            current_delay = delay
            last_exception: Exception | None = None

            for attempt in range(max_attempts):
                try:
                    result = func(*args, **kwargs)
                    if hasattr(result, "__await__"):
                        return await result
                    return result
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        if on_retry:
                            on_retry(attempt + 1, e)
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        # Last attempt failed, raise the exception
                        raise

            # This should never be reached, but type checker needs it
            if last_exception:
                raise last_exception
            raise RuntimeError("Retry failed without exception")

        return wrapper  # type: ignore[return-value]

    return decorator


def retry_on_connection_error(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for retrying on connection errors specifically.

    Convenience decorator that retries on ConnectionError and TimeoutError.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Multiplier for exponential backoff (default: 2.0)

    Returns:
        Decorated function with retry logic for connection errors

    Example:
        >>> @retry_on_connection_error(max_attempts=5, delay=2.0)
        ... async def connect_to_api():
        ...     return await api.make_request("/status")
    """
    return retry_on_failure(
        max_attempts=max_attempts,
        delay=delay,
        backoff=backoff,
        exceptions=(ConnectionError, TimeoutError),
    )


class RetryConfig:
    """
    Configuration for retry behavior.

    Provides a structured way to configure retry parameters
    that can be reused across multiple operations.

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

    def to_dict(self) -> dict:
        """Convert configuration to dictionary for decorator."""
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
        import random

        delay = self.delay * (self.backoff**attempt)
        if self.max_delay:
            delay = min(delay, self.max_delay)
        if self.jitter:
            # Add ±10% jitter
            jitter_amount = delay * 0.1
            delay += random.uniform(-jitter_amount, jitter_amount)
            delay = max(0, delay)  # Ensure non-negative
        return delay
