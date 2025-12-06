"""
Web automation testing framework.

A comprehensive library for automated testing of web applications,
providing clients for API testing (REST, GraphQL, gRPC, SOAP),
UI testing, and database operations.
"""

# Local imports
from .config import Config
from .exceptions import (
    AuthenticationError,
    ConfigurationError,
    ConnectionError,
    NotFoundError,
    OperationError,
    TimeoutError,
    WebAutomationError,
)

__all__ = [
    "Config",
    # Exceptions
    "WebAutomationError",
    "ConfigurationError",
    "ConnectionError",
    "OperationError",
    "TimeoutError",
    "AuthenticationError",
    "NotFoundError"
]
