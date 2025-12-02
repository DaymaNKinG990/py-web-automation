"""
Base class for web automation testing clients.

This module provides the BaseClient abstract base class that implements
common functionality for all client types, following the Template Method pattern.
"""

# Python imports
from types import TracebackType

from loguru import Logger, logger

# Local imports
from ..config import Config


class BaseClient:
    """
    Base class for web automation testing clients.

    Implements the Template Method pattern by providing common functionality
    for all client types while allowing subclasses to override specific behaviors.

    This class follows the Single Responsibility Principle by focusing solely
    on common client infrastructure (URL management, configuration, logging).

    Provides common functionality for all client types:
    - URL management and validation
    - Configuration handling
    - Logging setup with context binding
    - Context manager support for resource cleanup

    Attributes:
        url: Base URL for the application under test
        config: Configuration object
        logger: Logger instance bound to class name

    Example:
        >>> from py_web_automation import Config
        >>> from py_web_automation.clients import BaseClient
        >>> config = Config(timeout=30)
        >>> client = BaseClient("https://example.com", config)
        >>> async with client:
        ...     # Use client
        ...     pass
    """

    def __init__(self, url: str, config: Config) -> None:
        """
        Initialize base client.

        Args:
            url: Base URL for the application (must be a non-empty string)
            config: Configuration object

        Raises:
            TypeError: If url is not a string
            ValueError: If url is empty

        Example:
            >>> config = Config(timeout=60)
            >>> client = BaseClient("https://example.com", config)
            >>> # Or use default config
            >>> client = BaseClient("https://example.com")
        """
        if not url.strip():
            raise ValueError("url cannot be empty")
        self.url: str = url
        self.config: Config = config
        self.logger: Logger = logger.bind(name=self.__class__.__name__)

    async def __aenter__(self) -> "BaseClient":
        """
        Async context manager entry.

        Returns:
            Self for use in async with statement

        Example:
            >>> async with client:
            ...     # Client is ready to use
            ...     pass
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Async context manager exit.

        Ensures proper cleanup by calling close() method.
        Subclasses should override close() to implement specific cleanup logic.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        await self.close()

    async def close(self) -> None:
        """
        Close resources and perform cleanup.

        This method should be overridden in subclasses to implement
        specific cleanup logic (e.g., closing HTTP connections, browser instances).

        The base implementation only logs the cleanup action.
        """
        self.logger.debug("Closing resources")
