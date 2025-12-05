"""
SQLite database client using aiosqlite.
"""

# Python imports
from typing import Any

from aiosqlite import Connection, Row, connect

# Local imports
from .db_client import DBClient


class SQLiteClient(DBClient):
    """
    SQLite database client.
    """

    def __init__(self, connection_string: str | None = None) -> None:
        """
        Initialize SQLite client.

        Args:
            connection_string: SQLite connection string (e.g., 'sqlite:///path/to/db.sqlite')
        """
        super().__init__(connection_string=connection_string)
        self._connection: Connection

    async def connect(self) -> None:
        """Establish SQLite connection."""
        if self._is_connected:
            return
        self._connection = await connect(self.connection_string)
        self._connection.row_factory = Row
        self._is_connected = True

    async def disconnect(self) -> None:
        """Close SQLite connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None
        self._is_connected = False
        self._in_transaction = False
        self._transaction_level = 0

    async def execute_query(
        self, query: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Execute SELECT query.

        Args:
            query: SQL query to execute
            params: Parameters to pass to the query

        Returns:
            List of dictionaries representing the query results
        """
        cursor = await self._connection.execute(query, params or {})
        rows = await cursor.fetchall()
        if cursor.description is None:
            return []
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row, strict=True)) for row in rows]

    async def execute_command(self, command: str, params: dict[str, Any] | None = None) -> None:
        """
        Execute INSERT/UPDATE/DELETE command.

        Args:
            command: SQL command to execute
            params: Parameters to pass to the command
        """
        await self._connection.execute(command, params or {})
        if not self._in_transaction:
            await self._connection.commit()

    async def begin_transaction(self) -> None:
        """Start transaction."""
        # SQLite doesn't support nested transactions, so we track nesting level
        # Only start a new transaction if we're not already in one
        if self._transaction_level == 0:
            await self._connection.execute("BEGIN")
            self._in_transaction = True
        self._transaction_level += 1

    async def commit_transaction(self) -> None:
        """Commit transaction."""
        if self._transaction_level > 0:
            self._transaction_level -= 1
            # Only commit if we're at the top level
            if self._transaction_level == 0 and self._connection:
                await self._connection.commit()
                self._in_transaction = False

    async def rollback_transaction(self) -> None:
        """Rollback transaction."""
        if self._transaction_level > 0:
            # In SQLite, rollback always rolls back the entire transaction
            # regardless of nesting level, so we rollback everything
            if self._connection and self._in_transaction:
                await self._connection.rollback()
                self._in_transaction = False
            # Reset transaction level to 0 (rollback affects all nested levels)
            self._transaction_level = 0
