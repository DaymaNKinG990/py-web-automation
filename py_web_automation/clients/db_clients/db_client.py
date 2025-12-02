"""
Database client for web automation testing framework.

This module provides DBClient abstract base class and factory method
for creating database clients with support for multiple backends
(PostgreSQL, SQLite, MySQL) through pluggable adapter pattern.

Follows Open/Closed Principle (OCP) - new adapters can be registered
via DBAdapterRegistry without modifying existing code.
"""

# Python imports
from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from types import TracebackType
from typing import Any, TYPE_CHECKING
from urllib.parse import urlparse, parse_qs
from loguru import logger


if TYPE_CHECKING:
    from loguru._logger import Logger


class DBClient(ABC):
    """
    Abstract base class for database clients.

    Defines common interface for database operations through a combination of
    abstract methods (which subclasses must implement) and concrete methods
    (which provide shared functionality for all database clients).

    Abstract methods (must be implemented by subclasses):
    - connect() - Establish database connection
    - disconnect() - Close database connection
    - execute_query() - Execute SELECT queries
    - execute_command() - Execute INSERT/UPDATE/DELETE commands
    - begin_transaction() - Start a transaction
    - commit_transaction() - Commit current transaction
    - rollback_transaction() - Rollback current transaction

    Concrete methods (already implemented, can be used by all subclasses):
    - transaction() - Context manager for transactions with automatic rollback
    - close() - Close connection wrapper
    - __aenter__() / __aexit__() - Async context manager support
    - is_connected() - Check connection status

    Provides common interface for database operations:
    - Connection management with automatic connection handling via context manager
    - Query execution (SELECT, INSERT, UPDATE, DELETE)
    - Transaction handling with context manager support and automatic rollback
    - Connection pooling (implemented by adapters)

    Subclasses (adapters) should implement database-specific logic
    for abstract methods while inheriting concrete methods.

    Attributes:
        connection_string: Database connection string
        _connection: Internal connection object (private)
        _is_connected: Connection state flag (private)
        _db_kwargs: Additional database-specific parameters (private)

    Example:
        >>> from py_web_automation.clients.db_adapters.sqlite_adapter import SQLiteAdapter
        >>> db = SQLiteAdapter(connection_string="sqlite:///path/to/db.sqlite")
        >>> async with db:
        ...     results = await db.execute_query("SELECT * FROM users")
        >>> # Using transaction context manager
        >>> async with db.transaction():
        ...     await db.execute_command("INSERT INTO users (name) VALUES ('Alice')")
        ...     await db.execute_command("INSERT INTO users (name) VALUES ('Bob')")
    """

    def __init__(
        self,
        connection_string: str | None = None,
        log_file_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize database client.

        Args:
            connection_string: Database connection string
            **kwargs: Additional database-specific parameters
        """
        self.connection_string: str | None = connection_string
        self._connection: Any | None = None
        self._is_connected: bool = False
        self.logger: "Logger" = logger.bind(
            name=self.__class__.__name__ if log_file_name is None else log_file_name
        )

    @abstractmethod
    async def connect(self) -> None:
        """
        Establish database connection.

        Raises:
            Exception: If connection fails
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close database connection."""
        pass

    @abstractmethod
    async def execute_query(self, query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Execute SELECT query and return results.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            List of result rows as dictionaries

        Raises:
            Exception: If query execution fails
        """
        pass

    @abstractmethod
    async def execute_command(self, command: str, params: dict[str, Any] | None = None) -> None:
        """
        Execute INSERT/UPDATE/DELETE command.

        Args:
            command: SQL command string
            params: Command parameters

        Returns:
            None

        Raises:
            Exception: If command execution fails
        """
        pass

    @abstractmethod
    async def begin_transaction(self) -> None:
        """Start a database transaction."""
        pass

    @abstractmethod
    async def commit_transaction(self) -> None:
        """Commit current transaction."""
        pass

    @abstractmethod
    async def rollback_transaction(self) -> None:
        """Rollback current transaction."""
        pass

    @asynccontextmanager  # type: ignore[arg-type]
    async def transaction(self) -> "AbstractAsyncContextManager[None]":  # type: ignore[misc]
        """
        Context manager for database transactions.

        Provides automatic transaction management with rollback on exception.
        Ensures data consistency by committing only if all operations succeed.

        Yields:
            None (used for transaction scope)

        Raises:
            Exception: Re-raises any exception that occurs, after rollback

        Example:
            >>> async with db.transaction():
            ...     await db.execute_command("INSERT INTO users (name) VALUES ('Alice')")
            ...     await db.execute_command("INSERT INTO users (name) VALUES ('Bob')")
            # Transaction is committed if no exceptions, rolled back otherwise
        """
        self.logger.debug("Starting transaction")
        await self.begin_transaction()
        try:
            yield
            self.logger.debug("Transaction committed")
            await self.commit_transaction()
        except Exception:
            self.logger.debug("Transaction rolled back")
            await self.rollback_transaction()
            raise
        finally:
            self.logger.debug("Transaction ended")

    async def close(self) -> None:
        """Close database connection."""
        self.logger.debug("Closing database connection")
        await self.disconnect()

    async def __aenter__(self) -> "DBClient":
        """
        Async context manager entry - automatically connects to database.

        Returns:
            Self for use in async with statement
        """
        self.logger.debug("Connecting to database")
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Async context manager exit - automatically disconnects from database.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        self.logger.debug("Disconnecting from database")
        await self.close()

    async def is_connected(self) -> bool:
        """
        Check if client is connected to database.

        Returns:
            True if connected, False otherwise
        """
        return self._is_connected
