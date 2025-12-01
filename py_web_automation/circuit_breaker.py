"""
Circuit breaker pattern implementation for web automation framework.

This module provides circuit breaker functionality to prevent cascading failures
by stopping requests to a failing service until it recovers.
"""

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation, requests allowed
    OPEN = "open"  # Service failing, requests blocked
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """
    Configuration for circuit breaker.

    Attributes:
        failure_threshold: Number of failures before opening circuit
        timeout: Time in seconds before attempting to close circuit
        success_threshold: Number of successes needed to close circuit from half-open
        expected_exception: Exception type that counts as failure (default: Exception)
    """

    failure_threshold: int = 5
    timeout: float = 60.0
    success_threshold: int = 2
    expected_exception: type[Exception] = Exception


@dataclass
class CircuitBreakerStats:
    """
    Statistics for circuit breaker.

    Attributes:
        failures: Number of failures
        successes: Number of successes
        state: Current circuit state
        last_failure_time: Timestamp of last failure
        last_success_time: Timestamp of last success
    """

    failures: int = 0
    successes: int = 0
    state: CircuitState = CircuitState.CLOSED
    last_failure_time: datetime | None = None
    last_success_time: datetime | None = None
    opened_at: datetime | None = None


class CircuitBreaker:
    """
    Circuit breaker for preventing cascading failures.

    Monitors request failures and opens the circuit when threshold is reached,
    preventing further requests until the service recovers.

    Attributes:
        config: Circuit breaker configuration
        stats: Current statistics
        _lock: Async lock for thread safety

    Example:
        >>> breaker = CircuitBreaker(failure_threshold=5, timeout=60.0)
        >>> try:
        ...     result = await breaker.call(api.make_request, "/endpoint")
        ... except CircuitBreakerOpenError:
        ...     print("Circuit is open, service unavailable")
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        success_threshold: int = 2,
        expected_exception: type[Exception] = Exception,
    ) -> None:
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Time in seconds before attempting to close circuit
            success_threshold: Number of successes needed to close circuit
            expected_exception: Exception type that counts as failure
        """
        self.config = CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            timeout=timeout,
            success_threshold=success_threshold,
            expected_exception=expected_exception,
        )
        self.stats = CircuitBreakerStats()
        self._lock = asyncio.Lock()

    async def call(self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Execute function through circuit breaker.

        Args:
            func: Function to execute
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function

        Returns:
            Function result

        Raises:
            CircuitBreakerOpenError: If circuit is open
            Exception: If function raises exception (and circuit is closed)
        """
        async with self._lock:
            # Check circuit state
            if self.stats.state == CircuitState.OPEN:
                # Check if timeout has passed
                if self.stats.opened_at:
                    elapsed = (datetime.now() - self.stats.opened_at).total_seconds()
                    if elapsed >= self.config.timeout:
                        # Transition to half-open
                        self.stats.state = CircuitState.HALF_OPEN
                        self.stats.successes = 0
                    else:
                        # Still open, raise error
                        from .exceptions import ConnectionError

                        raise ConnectionError(
                            f"Circuit breaker is OPEN. Service unavailable. "
                            f"Retry after {self.config.timeout - elapsed:.1f}s"
                        )

        # Execute function
        try:
            result = func(*args, **kwargs)
            if hasattr(result, "__await__"):
                result = await result
            await self._record_success()
            return result
        except self.config.expected_exception:
            await self._record_failure()
            raise

    async def _record_success(self) -> None:
        """Record successful request."""
        async with self._lock:
            self.stats.successes += 1
            self.stats.last_success_time = datetime.now()

            if self.stats.state == CircuitState.HALF_OPEN:
                if self.stats.successes >= self.config.success_threshold:
                    # Close circuit
                    self.stats.state = CircuitState.CLOSED
                    self.stats.failures = 0
                    self.stats.opened_at = None
            elif self.stats.state == CircuitState.CLOSED:
                # Reset failure count on success
                self.stats.failures = 0

    async def _record_failure(self) -> None:
        """Record failed request."""
        async with self._lock:
            self.stats.failures += 1
            self.stats.last_failure_time = datetime.now()

            if self.stats.state == CircuitState.CLOSED:
                if self.stats.failures >= self.config.failure_threshold:
                    # Open circuit
                    self.stats.state = CircuitState.OPEN
                    self.stats.opened_at = datetime.now()
            elif self.stats.state == CircuitState.HALF_OPEN:
                # Back to open on failure
                self.stats.state = CircuitState.OPEN
                self.stats.opened_at = datetime.now()
                self.stats.successes = 0

    def reset(self) -> None:
        """Manually reset circuit breaker to closed state."""
        self.stats = CircuitBreakerStats()

    def get_state(self) -> CircuitState:
        """Get current circuit state."""
        return self.stats.state

    def get_stats(self) -> CircuitBreakerStats:
        """Get current statistics."""
        return self.stats
