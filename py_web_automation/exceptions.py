"""
Custom exception hierarchy for web automation testing framework.

This module provides a structured exception hierarchy following
best practices for error handling and debugging.
"""


class WebAutomationError(Exception):
    """
    Base exception for all web automation framework errors.

    All framework-specific exceptions should inherit from this class
    to allow catching all framework errors with a single exception type.

    Attributes:
        message: Error message
        details: Optional additional error details

    Example:
        >>> try:
        ...     # Framework operation
        ...     pass
        ... except WebAutomationError as e:
        ...     print(f"Framework error: {e}")
    """

    def __init__(self, message: str, details: str | None = None) -> None:
        """
        Initialize base exception.

        Args:
            message: Error message
            details: Optional additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Return formatted error message."""
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class ConfigurationError(WebAutomationError):
    """
    Exception raised for configuration-related errors.

    Raised when configuration validation fails or required
    configuration values are missing or invalid.

    Example:
        >>> raise ConfigurationError("Invalid timeout value", "Timeout must be between 1 and 300")
    """

    pass


class OperationError(WebAutomationError):
    """
    Exception raised for operation execution errors.

    Raised when an operation (API call, database query, UI action) fails
    due to business logic or execution errors.

    Example:
        >>> raise OperationError("Failed to execute query", "Table does not exist")
    """

    pass


class ConnectionError(WebAutomationError):
    """
    Exception raised for connection-related errors.

    Raised when connection to external services (database, API, browser)
    fails or cannot be established.

    Example:
        >>> raise ConnectionError("Failed to connect to database", "Connection timeout after 30s")
    """

    pass


class TimeoutError(WebAutomationError):
    """
    Exception raised for timeout errors.

    Raised when an operation exceeds the configured timeout period.

    Example:
        >>> raise TimeoutError("Request timed out", "Operation exceeded 30 second timeout")
    """

    pass


class AuthenticationError(WebAutomationError):
    """
    Exception raised for authentication-related errors.

    Raised when authentication fails or credentials are invalid.

    Example:
        >>> raise AuthenticationError("Authentication failed", "Invalid token")
    """

    pass


class NotFoundError(WebAutomationError):
    """
    Exception raised when a requested resource is not found.

    Raised when an entity, endpoint, or resource cannot be located.

    Example:
        >>> raise NotFoundError("Element not found", "Selector '#button' did not match any element")
    """

    pass


class CircuitBreakerOpenError(WebAutomationError):
    """
    Exception raised when circuit breaker is open.

    Raised when circuit breaker prevents a request because the service
    is currently failing.

    Example:
        >>> raise CircuitBreakerOpenError("Circuit breaker is open", "Service unavailable")
    """

    pass
