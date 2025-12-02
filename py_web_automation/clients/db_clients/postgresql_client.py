"""
PostgreSQL database client using asyncpg.
"""

# Python imports
from typing import Any
from urllib.parse import parse_qs, urlparse
from asyncpg import connect, Connection

# Local imports
from .db_client import DBClient


class PostgreSQLClient(DBClient):
    """
    PostgreSQL database client.
    """

    def __init__(
        self,
        connection_string: str | None = None
    ) -> None:
        """
        Initialize PostgreSQL client.

        Args:
            connection_string: PostgreSQL connection string
        """
        super().__init__(
            connection_string=connection_string,
            log_file_name=self.__class__.__name__
        )
        self._connection: Connection

    async def _parse_connection_string(self) -> dict[str, Any]:
        """
        Parse PostgreSQL connection string into a dictionary of connection parameters.

        Supports standard URL format: postgresql://[user[:password]@]host[:port]/database[?params]
        Also supports 'postgres://' scheme (alias for postgresql://)

        Returns:
            Dictionary with connection parameters:
            - host: Database host
            - port: Database port (default: 5432)
            - database: Database name
            - user: Username
            - password: Password
            - Additional query parameters as key-value pairs (e.g., sslmode, application_name)

        Example:
            >>> params = await self._parse_connection_string()
            >>> # For connection_string="postgresql://user:pass@localhost:5432/mydb?sslmode=require"
            >>> # Returns: {
            ... #     'host': 'localhost',
            ... #     'port': 5432,
            ... #     'database': 'mydb',
            ... #     'user': 'user',
            ... #     'password': 'pass',
            ... #     'sslmode': 'require'
            ... # }
        """
        if not self.connection_string:
            return {}
        parsed = urlparse(self.connection_string)
        params: dict[str, Any] = {}
        if parsed.username:
            params["user"] = parsed.username
        if parsed.password:
            params["password"] = parsed.password
        if parsed.hostname:
            params["host"] = parsed.hostname
        if parsed.port:
            params["port"] = parsed.port
        if parsed.path:
            params["database"] = parsed.path.lstrip("/")
        if parsed.query:
            query_params = parse_qs(parsed.query, keep_blank_values=True)
            for key, value in query_params.items():
                params[key] = value[0] if len(value) == 1 else value
        return params

    async def connect(self) -> None:
        """Establish PostgreSQL connection."""
        if self._is_connected:
            self.logger.debug("Already connected to PostgreSQL")
            return
        connection_params = await self._parse_connection_string()
        self._connection = await connect(
            host=connection_params.get("host"),
            port=connection_params.get("port"),
            database=connection_params.get("database"),
            user=connection_params.get("user"),
            password=connection_params.get("password")
        )
        self._is_connected = True
        self.logger.debug("Connected to PostgreSQL database")

    async def disconnect(self) -> None:
        """Close PostgreSQL connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None
        self._is_connected = False
        self.logger.debug("Disconnected from PostgreSQL database")

    async def execute_query(self, query: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Execute SELECT query.

        Args:
            query: SQL query to execute
            params: Parameters to pass to the query

        Returns:
            List of dictionaries representing the query results
        """
        rows = await self._connection.fetch(query, *(params or {}).values())
        return [dict(row) for row in rows]

    async def execute_command(self, command: str, params: dict[str, Any] | None = None) -> None:
        """
        Execute INSERT/UPDATE/DELETE command.

        Args:
            command: SQL command to execute
            params: Parameters to pass to the command

        Returns:
            None
        """
        await self._connection.execute(command, *(params or {}).values())

    async def begin_transaction(self) -> None:
        """Start transaction."""
        await self._connection.execute("BEGIN")

    async def commit_transaction(self) -> None:
        """Commit transaction."""
        await self._connection.execute("COMMIT")

    async def rollback_transaction(self) -> None:
        """Rollback transaction."""
        await self._connection.execute("ROLLBACK")
