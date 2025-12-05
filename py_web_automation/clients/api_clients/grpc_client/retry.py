"""
Retry mechanism with exponential backoff for gRPC operations.

This module provides retry handler for automatic retry of failed gRPC operations
with configurable exponential backoff strategy.
"""

# Python imports
import asyncio
from typing import TYPE_CHECKING

from loguru import logger

# Local imports
from py_web_automation.exceptions import ConnectionError, TimeoutError

if TYPE_CHECKING:
    from .grpc_result import GrpcResult
    from .middleware.context import _GrpcRequestContext


class RetryConfig:
    """
    Configuration for retry behavior for gRPC operations.

    Provides a structured way to configure retry parameters
    that can be reused across multiple gRPC operations.

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
        >>> retry_handler = RetryHandler(config)
        >>> # Use with RetryMiddleware
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

    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay for a specific attempt.

        Args:
            attempt: Attempt number (0-indexed)

        Returns:
            Delay in seconds for this attempt
        """
        from random import uniform

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
    Internal retry handler for gRPC middleware system.

    Handles retry logic with exponential backoff and configurable exceptions
    for gRPC operations.

    Attributes:
        config: Retry configuration
        _attempts: Dictionary tracking retry attempts per call key
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

    def _get_request_key(self, context: "_GrpcRequestContext") -> str:
        """
        Generate unique key for gRPC call tracking.

        Args:
            context: gRPC request context

        Returns:
            Unique key for this call
        """
        request_id = context.metadata_context.get("request_id")
        call_key = f"{context.service}:{context.method}"
        if request_id:
            return f"{call_key}:{request_id}"
        return call_key

    def _should_retry(self, error: Exception) -> bool:
        """
        Check if error should trigger retry.

        Args:
            error: Exception to check

        Returns:
            True if error should trigger retry
        """
        # Check if error is in configured exceptions
        if isinstance(error, self.config.exceptions):
            return True

        # Check for gRPC status codes that are retryable
        # Common retryable gRPC status codes:
        # - UNAVAILABLE (14): Service unavailable
        # - DEADLINE_EXCEEDED (4): Deadline exceeded
        # - RESOURCE_EXHAUSTED (8): Resource exhausted (rate limiting)
        if hasattr(error, "status"):
            status_code = getattr(error.status, "code", None)
            if status_code in (4, 8, 14):  # DEADLINE_EXCEEDED, RESOURCE_EXHAUSTED, UNAVAILABLE
                return True

        return False

    async def handle_error(
        self,
        context: "_GrpcRequestContext",
        error: Exception,
    ) -> "GrpcResult | None":
        """
        Handle error and determine if retry is needed.

        Checks if error is retryable, tracks attempts, and waits if retry is needed.
        Returns None if retry should be attempted, or GrpcResult if retry limit exceeded.

        Args:
            context: gRPC request context
            error: Exception that occurred

        Returns:
            None if retry should be attempted, GrpcResult with error if limit exceeded
        """
        if not self._should_retry(error):
            # Error is not retryable, return None to let error propagate
            return None

        request_key = self._get_request_key(context)
        current_attempt = self._attempts.get(request_key, 0)
        current_attempt += 1
        self._attempts[request_key] = current_attempt

        logger.debug(
            f"Retry attempt {current_attempt}/{self.config.max_attempts} "
            f"for {context.service}.{context.method}: {error}"
        )

        if current_attempt >= self.config.max_attempts:
            # Retry limit exceeded, clean up and return error result
            del self._attempts[request_key]
            logger.error(
                f"Retry limit exceeded after {current_attempt} attempts "
                f"for {context.service}.{context.method}"
            )
            # Return None to let error propagate (GrpcClient will create error GrpcResult)
            return None

        # Calculate delay and wait
        attempt_index = current_attempt - 1  # 0-indexed for delay calculation
        delay = self.config.calculate_delay(attempt_index)
        logger.debug(f"Waiting {delay:.2f}s before retry attempt {current_attempt + 1}")
        await asyncio.sleep(delay)

        # Store retry info in metadata for GrpcClient to check
        context.metadata_context["retry_attempt"] = current_attempt
        context.metadata_context["should_retry"] = True

        # Return None to indicate retry should be attempted
        # GrpcClient will check metadata and retry the call
        return None
