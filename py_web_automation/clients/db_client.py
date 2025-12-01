"""
Database client for web automation testing framework.

This module provides DBClient abstract base class and factory method
for creating database clients with support for multiple backends
(PostgreSQL, SQLite, MySQL) through pluggable adapter pattern.
"""

# Python imports
from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any

from ..config import Config

# Local imports
from .base_client import BaseClient


class DBClient(BaseClient, ABC):
    """
    Abstract base class for database clients.

    Implements the Strategy pattern through abstract methods that subclasses
    must implement, and the Factory pattern via the create() class method.

    Follows the Open/Closed Principle - open for extension (new adapters)
    but closed for modification (interface remains stable).

    Provides common interface for database operations:
    - Connection management with automatic connection handling
    - Query execution (SELECT, INSERT, UPDATE, DELETE)
    - Transaction handling with context manager support
    - Connection pooling (implemented by adapters)

    Subclasses (adapters) should implement database-specific logic
    while adhering to this interface.

    Attributes:
        connection_string: Database connection string
        _connection: Internal connection object (private)
        _is_connected: Connection state flag (private)
        _db_kwargs: Additional database-specific parameters (private)

    Example:
        >>> from py_web_automation import Config, DBClient
        >>> config = Config(api_id=12345, api_hash="hash", session_string="session")
        >>> db = DBClient.create("postgresql", "https://example.com", config,
        ...                      connection_string="postgresql://user:pass@localhost/db")
        >>> async with db:
        ...     results = await db.execute_query("SELECT * FROM users")
    """

    def __init__(
        self,
        url: str,
        config: Config | None = None,
        connection_string: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize database client.

        Args:
            url: Base URL (for BaseClient compatibility)
            config: Configuration object
            connection_string: Database connection string
            **kwargs: Additional database-specific parameters
        """
        super().__init__(url, config)
        self.connection_string = connection_string
        self._connection: Any | None = None
        self._is_connected = False
        self._db_kwargs = kwargs

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
    async def execute_command(self, command: str, params: dict[str, Any] | None = None) -> int:
        """
        Execute INSERT/UPDATE/DELETE command.

        Args:
            command: SQL command string
            params: Command parameters

        Returns:
            Number of affected rows

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

    async def is_connected(self) -> bool:
        """
        Check if client is connected to database.

        Returns:
            True if connected, False otherwise
        """
        return self._is_connected

    @classmethod
    def create(
        cls,
        db_type: str,
        url: str,
        config: Config | None = None,
        connection_string: str | None = None,
        **kwargs: Any,
    ) -> "DBClient":
        """
        Factory method to create database client by type.

        Args:
            db_type: Database type ('postgresql', 'sqlite', 'mysql', etc.)
            url: Base URL (for BaseClient compatibility)
            config: Configuration object
            connection_string: Database connection string
            **kwargs: Additional database-specific parameters

        Returns:
            DBClient instance

        Raises:
            ValueError: If db_type is not supported
            ImportError: If required database library is not installed

        Example:
            >>> # PostgreSQL
            >>> db = DBClient.create(
            ...     'postgresql',
            ...     'https://example.com',
            ...     config,
            ...     connection_string='postgresql://user:pass@localhost/db'
            ... )
            >>> # SQLite
            >>> db = DBClient.create(
            ...     'sqlite',
            ...     'https://example.com',
            ...     config,
            ...     connection_string='sqlite:///path/to/db.sqlite'
            ... )
        """
        db_type_lower = db_type.lower()

        if db_type_lower in ("postgresql", "postgres"):
            try:
                from .db_adapters.postgresql_adapter import PostgreSQLAdapter

                return PostgreSQLAdapter(url, config, connection_string, **kwargs)
            except ImportError as e:
                raise ImportError(
                    "PostgreSQL adapter requires 'asyncpg' or 'psycopg' library. Install it with: uv add asyncpg"
                ) from e

        elif db_type_lower == "sqlite":
            try:
                from .db_adapters.sqlite_adapter import SQLiteAdapter

                return SQLiteAdapter(url, config, connection_string, **kwargs)
            except ImportError as e:
                raise ImportError(
                    "SQLite adapter requires 'aiosqlite' library. Install it with: uv add aiosqlite"
                ) from e

        elif db_type_lower == "mysql":
            try:
                from .db_adapters.mysql_adapter import MySQLAdapter

                return MySQLAdapter(url, config, connection_string, **kwargs)
            except ImportError as e:
                raise ImportError(
                    "MySQL adapter requires 'aiomysql' or 'pymysql' library. Install it with: uv add aiomysql"
                ) from e

        else:
            raise ValueError(f"Unsupported database type: {db_type}. Supported types: postgresql, sqlite, mysql")
