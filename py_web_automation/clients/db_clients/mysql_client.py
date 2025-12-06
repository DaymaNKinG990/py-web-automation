"""
MySQL database adapter using aiomysql.
"""

# Python imports
from typing import Any

from aiomysql import Connection, DictCursor, connect

# Local imports
from .db_client import DBClient


class MySQLClient(DBClient):
    """
    MySQL database client.
    """

    def __init__(self, connection_string: str | None = None) -> None:
        """
        Initialize MySQL client.

        Args:
            connection_string: MySQL connection string
            **kwargs: Additional connection parameters (host, port, database, user, password)
        """
        super().__init__(connection_string=connection_string)
        self._connection: Connection

    async def _parse_connection_string(self) -> dict[str, Any]:
        """
        Parse MySQL connection string into a dictionary of connection parameters.

        Supports standard URL format: mysql://[user[:password]@]host[:port]/database[?params]

        Returns:
            Dictionary with connection parameters:
            - host: Database host
            - port: Database port
            - database: Database name
            - user: Username
            - password: Password
            - Additional query parameters as key-value pairs

        Example:
            >>> params = await self._parse_connection_string()
            >>> # For connection_string="mysql://user:pass@localhost:3306/mydb?charset=utf8mb4"
            >>> # Returns: {
            ... #     'host': 'localhost',
            ... #     'port': 3306,
            ... #     'database': 'mydb',
            ... #     'user': 'user',
            ... #     'password': 'pass',
            ... #     'charset': 'utf8mb4'
            ... # }
        """
        if not self.connection_string:
            return {}
        return self._parse_url_connection_string(self.connection_string)

    async def connect(self) -> None:
        """Establish MySQL connection."""
        if self._is_connected:
            return
        connection_params = await self._parse_connection_string()
        self._connection = await connect(
            host=connection_params.get("host"),
            port=connection_params.get("port"),
            db=connection_params.get("database"),
            user=connection_params.get("user"),
            password=connection_params.get("password"),
        )
        self._is_connected = True

    async def disconnect(self) -> None:
        """Close MySQL connection."""
        if self._connection:
            await self._connection.close()
            await self._connection.ensure_closed()
            self._connection = None
        self._is_connected = False

    async def execute_query(
        self,
        query: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Execute SELECT query.

        Args:
            query: SQL query to execute
            params: Parameters to pass to the query

        Returns:
            List of dictionaries representing the result rows
        """
        async with self._connection.cursor(DictCursor) as cursor:
            await cursor.execute(query, list((params or {}).values()))
            rows = await cursor.fetchall()
            return list(rows)

    async def execute_command(
        self,
        command: str,
        params: dict[str, Any] | None = None,
    ) -> None:
        """
        Execute INSERT/UPDATE/DELETE command.

        Args:
            command: SQL command to execute
            params: Parameters to pass to the command

        Returns:
            None
        """
        async with self._connection.cursor() as cursor:
            await cursor.execute(command, list((params or {}).values()))
            if not self._connection.in_transaction:
                await self._connection.commit()

    async def begin_transaction(self) -> None:
        """Start transaction."""
        await self._connection.begin()

    async def commit_transaction(self) -> None:
        """Commit transaction."""
        await self._connection.commit()

    async def rollback_transaction(self) -> None:
        """Rollback transaction."""
        await self._connection.rollback()
