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
from enum import StrEnum
from types import TracebackType
from typing import Any
from urllib.parse import parse_qs, urlparse

# Local imports
from .query_builder import _QueryBuilder


class DBCommandType(StrEnum):
    """Database command type."""

    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


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

    @staticmethod
    def _parse_url_components(parsed: Any) -> dict[str, Any]:
        """Parse URL components (user, password, host, port, database) into params."""
        url_component_mapping = {
            "user": ("username", lambda x: x),
            "password": ("password", lambda x: x),
            "host": ("hostname", lambda x: x),
            "port": ("port", lambda x: x),
            "database": ("path", lambda x: x.lstrip("/")),
        }
        return {
            param_key: transform(getattr(parsed, attr_name))
            for param_key, (attr_name, transform) in url_component_mapping.items()
            if getattr(parsed, attr_name, None)
        }

    @staticmethod
    def _parse_url_query_params(parsed: Any) -> dict[str, Any]:
        """Parse URL query parameters into params."""
        if not parsed.query:
            return {}
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        return {
            key: value[0] if len(value) == 1 else value
            for key, value in query_params.items()
        }

    @staticmethod
    def _parse_url_connection_string(connection_string: str) -> dict[str, Any]:
        """
        Parse database connection URL into parameters.

        Supports standard URL format: scheme://[user[:password]@]host[:port]/database[?params]

        Args:
            connection_string: Database connection URL string

        Returns:
            Dictionary with connection parameters:
            - host: Database host
            - port: Database port
            - database: Database name
            - user: Username
            - password: Password
            - Additional query parameters as key-value pairs

        Example:
            >>> params = DBClient._parse_url_connection_string(
            ...     "postgresql://user:pass@localhost:5432/mydb?sslmode=require"
            ... )
            >>> # Returns: {
            ... #     'host': 'localhost',
            ... #     'port': 5432,
            ... #     'database': 'mydb',
            ... #     'user': 'user',
            ... #     'password': 'pass',
            ... #     'sslmode': 'require'
            ... # }
        """
        if not connection_string:
            return {}
        parsed = urlparse(connection_string)
        params = DBClient._parse_url_components(parsed)
        params.update(DBClient._parse_url_query_params(parsed))
        return params

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
    async def execute_query(
        self, query: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
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
        await self.begin_transaction()
        try:
            yield
            await self.commit_transaction()
        except Exception:
            await self.rollback_transaction()
            raise

    async def close(self) -> None:
        """Close database connection."""
        await self.disconnect()

    async def __aenter__(self) -> "DBClient":
        """
        Async context manager entry - automatically connects to database.

        Returns:
            Self for use in async with statement
        """
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
        await self.close()

    async def is_connected(self) -> bool:
        """
        Check if client is connected to database.

        Returns:
            True if connected, False otherwise
        """
        return self._is_connected

    def query(self) -> _QueryBuilder:
        """
        Create _QueryBuilder instance for this database client.

        Returns:
            _QueryBuilder configured for this database

        Example:
            >>> builder = db.query().select("*").from_table("users")
            >>> results = await builder.where("active", "=", True).execute(db)
        """
        return _QueryBuilder()
