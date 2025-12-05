"""
Retry mechanism with exponential backoff for SOAP operations.

This module provides retry handler for automatic retry of failed SOAP operations
with configurable exponential backoff strategy.
"""

# Python imports
from asyncio import sleep
from random import uniform
from typing import TYPE_CHECKING, Any

# Local imports
from ....exceptions import ConnectionError, TimeoutError

if TYPE_CHECKING:
    from .middleware.context import _SoapRequestContext
    from .soap_result import SoapResult


class RetryConfig:
    """
    Configuration for retry behavior for SOAP operations.

    Provides a structured way to configure retry parameters
    that can be reused across multiple SOAP operations.

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
    Internal retry handler for SOAP middleware system.

    Handles retry logic with exponential backoff and configurable exceptions.
    Supports retry on connection errors, timeouts, and retryable SOAP faults.

    Attributes:
        config: Retry configuration
        _attempts: Dictionary tracking retry attempts per operation key
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

    def _get_request_key(self, context: "_SoapRequestContext") -> str:
        """
        Generate unique key for SOAP operation tracking.

        Args:
            context: SOAP request context

        Returns:
            Unique key for this operation
        """
        request_id = context.metadata_context.get("request_id")
        operation_key = context.operation
        if request_id:
            return f"{operation_key}:{request_id}"
        return operation_key

    def _should_retry(self, error: Exception, soap_fault: dict[str, Any] | None = None) -> bool:
        """
        Check if error should trigger retry.

        Checks for retryable exceptions and SOAP faults.

        Args:
            error: Exception to check
            soap_fault: SOAP fault dict (if any)

        Returns:
            True if error/fault should trigger retry
        """
        # Check if error is in configured exceptions
        if isinstance(error, self.config.exceptions):
            return True
        # Check for retryable SOAP faults
        if soap_fault:
            fault_code = soap_fault.get("faultcode", "")
            # Retry on server errors (Server, Server.*)
            if "Server" in fault_code:
                return True
            # Don't retry on client errors (Client, Client.*)
            if "Client" in fault_code:
                return False
        return False

    async def handle_error(
        self,
        context: "_SoapRequestContext",
        error: Exception,
        soap_fault: dict[str, Any] | None = None,
    ) -> "SoapResult | None":
        """
        Handle error and determine if retry is needed.

        Checks if error is retryable, tracks attempts, and waits if retry is needed.
        Returns None if retry should be attempted, or SoapResult if retry limit exceeded.

        Args:
            context: SOAP request context
            error: Exception that occurred
            soap_fault: SOAP fault dict (if any)

        Returns:
            None if retry should be attempted, SoapResult with error if limit exceeded
        """
        if not self._should_retry(error, soap_fault):
            # Error is not retryable, return None to let error propagate
            return None
        request_key = self._get_request_key(context)
        current_attempt = self._attempts.get(request_key, 0)
        current_attempt += 1
        self._attempts[request_key] = current_attempt
        if current_attempt >= self.config.max_attempts:
            # Retry limit exceeded, clean up and return error result
            del self._attempts[request_key]
            # Return None to let error propagate (SoapClient will create error SoapResult)
            return None
        # Calculate delay and wait
        attempt_index = current_attempt - 1  # 0-indexed for delay calculation
        delay = self.config.calculate_delay(attempt_index)
        await sleep(delay)
        # Store retry info in metadata for SoapClient to check
        context.metadata_context["retry_attempt"] = current_attempt
        context.metadata_context["should_retry"] = True
        # Return None to indicate retry should be attempted
        # SoapClient will check metadata and retry the operation
        return None
