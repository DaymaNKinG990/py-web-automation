"""
Query builder for constructing SQL queries with fluent API.

This module provides a query builder for constructing SQL queries
in a type-safe and readable way.
"""

# Python imports
from typing import TYPE_CHECKING, Any

from .db_client import DBCommandType

if TYPE_CHECKING:
    from .db_client import DBClient


class _QueryBuilder:
    """
    Fluent query builder for SQL queries.

    Provides a fluent API for constructing SELECT, INSERT, UPDATE, DELETE queries
    in a readable and type-safe manner.

    Attributes:
        _query_type: Type of query (SELECT, INSERT, UPDATE, DELETE)
        _table: Table name
        _columns: List of columns for SELECT or INSERT
        _values: List of value dictionaries for INSERT (supports batch INSERT)
        _set_clause: SET clause for UPDATE
        _conflict_columns: Conflict columns for UPSERT operations
        _upsert_update: Update values for UPSERT operations
        _dialect: Database dialect for SQL generation
        _where_clauses: WHERE clause conditions (column, operator, value, connector)
        _order_by: ORDER BY clause
        _limit_value: LIMIT value
        _offset_value: OFFSET value
        _joins: JOIN clauses
        _group_by: GROUP BY clause
        _having: HAVING clause

    Example:
        >>> from py_web_automation import DBClient
        >>> db = DBClient.create("postgresql", "...", config)
        >>> async with db:
        ...     results = (
        ...         await db.query()
        ...         .select("id", "name")
        ...         .from_table("users")
        ...         .where("active", "=", True)
        ...         .execute(db)
        ...     )
    """

    def __init__(self) -> None:
        """Initialize empty query builder."""
        self._query_type: DBCommandType | None = None
        self._table: str | None = None
        self._columns: list[str] = []
        # List of dictionaries for batch INSERT support
        self._values: list[dict[str, Any]] = []
        self._set_clause: dict[str, Any] = {}
        # Upsert support
        self._conflict_columns: list[str] | None = None
        self._upsert_update: dict[str, Any] | None = None
        self._dialect: str | None = None  # "postgresql", "sqlite", "mysql"
        # (column, operator, value, connector) where connector is "AND" or "OR"
        self._where_clauses: list[tuple[str, str, Any, str]] = []
        self._order_by: list[tuple[str, str]] = []  # (column, direction)
        self._limit_value: int | None = None
        self._offset_value: int | None = None
        # (type, table, on_left, on_right, condition)
        self._joins: list[tuple[str, str, str, str, Any]] = []
        self._group_by: list[str] = []
        self._having: list[tuple[str, str, Any]] = []

    def select(self, *columns: str) -> "_QueryBuilder":
        """
        Start SELECT query with columns.

        Args:
            *columns: Column names to select

        Returns:
            Self for method chaining

        Example:
            >>> builder.select("id", "name", "email")
        """
        self._query_type = DBCommandType.SELECT
        self._columns = list(columns)
        return self

    def from_table(self, table: str) -> "_QueryBuilder":
        """
        Set table name for query.

        Args:
            table: Table name

        Returns:
            Self for method chaining

        Example:
            >>> builder.from_table("users")
        """
        self._table = table
        return self

    def where(self, column: str, operator: str, value: Any) -> "_QueryBuilder":
        """
        Add WHERE condition with AND connector.

        Args:
            column: Column name
            operator: Comparison operator (=, !=, <, >, <=, >=, LIKE, IN, etc.)
            value: Value to compare

        Returns:
            Self for method chaining

        Example:
            >>> builder.where("active", "=", True)
            >>> builder.where("age", ">=", 18)
            >>> builder.where("name", "LIKE", "%John%")
        """
        # First condition doesn't need connector, subsequent ones use AND
        connector = "AND" if self._where_clauses else ""
        self._where_clauses.append((column, operator, value, connector))
        return self

    def and_where(self, column: str, operator: str, value: Any) -> "_QueryBuilder":
        """
        Add AND WHERE condition (alias for where).

        Args:
            column: Column name
            operator: Comparison operator
            value: Value to compare

        Returns:
            Self for method chaining
        """
        return self.where(column, operator, value)

    def or_where(self, column: str, operator: str, value: Any) -> "_QueryBuilder":
        """
        Add OR WHERE condition.

        Args:
            column: Column name
            operator: Comparison operator
            value: Value to compare

        Returns:
            Self for method chaining

        Example:
            >>> builder.where("active", "=", True).or_where("age", ">", 65)
            >>> # Generates: WHERE active = :where_0 OR age > :where_1
        """
        if not self._where_clauses:
            # First condition doesn't need connector
            self._where_clauses.append((column, operator, value, ""))
        else:
            # Use OR connector for subsequent conditions
            self._where_clauses.append((column, operator, value, "OR"))
        return self

    def order_by(self, column: str, direction: str = "ASC") -> "_QueryBuilder":
        """
        Add ORDER BY clause.

        Args:
            column: Column name
            direction: Sort direction (ASC or DESC)

        Returns:
            Self for method chaining

        Example:
            >>> builder.order_by("created_at", "DESC")
        """
        self._order_by.append((column, direction.upper()))
        return self

    def limit(self, count: int) -> "_QueryBuilder":
        """
        Add LIMIT clause.

        Args:
            count: Maximum number of rows to return

        Returns:
            Self for method chaining

        Example:
            >>> builder.limit(10)
        """
        self._limit_value = count
        return self

    def offset(self, count: int) -> "_QueryBuilder":
        """
        Add OFFSET clause.

        Args:
            count: Number of rows to skip

        Returns:
            Self for method chaining

        Example:
            >>> builder.offset(20)
        """
        self._offset_value = count
        return self

    def join(
        self, table: str, on_left: str, on_right: str, join_type: str = "INNER"
    ) -> "_QueryBuilder":
        """
        Add JOIN clause.

        Args:
            table: Table to join
            on_left: Left side of join condition
            on_right: Right side of join condition
            join_type: Type of join (INNER, LEFT, RIGHT, FULL)

        Returns:
            Self for method chaining

        Example:
            >>> builder.join("orders", "users.id", "orders.user_id", "LEFT")
        """
        self._joins.append((join_type.upper(), table, on_left, on_right, None))
        return self

    def group_by(self, *columns: str) -> "_QueryBuilder":
        """
        Add GROUP BY clause.

        Args:
            *columns: Column names to group by

        Returns:
            Self for method chaining

        Example:
            >>> builder.group_by("status", "category")
        """
        self._group_by.extend(columns)
        return self

    def having(self, column: str, operator: str, value: Any) -> "_QueryBuilder":
        """
        Add HAVING clause.

        Args:
            column: Column name
            operator: Comparison operator
            value: Value to compare

        Returns:
            Self for method chaining

        Example:
            >>> builder.having("COUNT(*)", ">", 10)
        """
        self._having.append((column, operator, value))
        return self

    def insert(self, table: str, **values: Any) -> "_QueryBuilder":
        """
        Start INSERT query.

        Args:
            table: Table name
            **values: Optional column-value pairs to insert (first row)

        Returns:
            Self for method chaining

        Example:
            >>> builder.insert("users", name="John", email="john@example.com")
            >>> builder.insert("users").values(name="John", email="john@example.com")
        """
        self._query_type = DBCommandType.INSERT
        self._table = table
        self._values = []
        if values:
            self._values.append(values)
        return self

    def values(self, **values: Any) -> "_QueryBuilder":
        """
        Add values for batch INSERT.

        Args:
            **values: Column-value pairs for one row

        Returns:
            Self for method chaining

        Raises:
            ValueError: If not in INSERT mode or columns mismatch

        Example:
            >>> builder.insert("users")
            >>> builder.values(name="John", email="john@example.com")
            >>> builder.values(name="Jane", email="jane@example.com")
        """
        if self._query_type != DBCommandType.INSERT:
            raise ValueError("values() can only be used with INSERT queries. Call insert() first.")
        if not self._table:
            raise ValueError("Table name not set. Call insert() first.")
        # Validate column compatibility for batch INSERT
        if self._values:
            first_row_keys = set(self._values[0].keys())
            new_row_keys = set(values.keys())
            if first_row_keys != new_row_keys:
                raise ValueError(
                    f"Column mismatch in batch INSERT. "
                    f"Expected columns: {sorted(first_row_keys)}, "
                    f"got: {sorted(new_row_keys)}"
                )
        self._values.append(values)
        return self

    def on_conflict(self, *columns: str) -> "_QueryBuilder":
        """
        Specify conflict columns for UPSERT operation.

        Args:
            *columns: Column names that may conflict (for unique constraints)

        Returns:
            Self for method chaining

        Raises:
            ValueError: If not in INSERT mode

        Example:
            >>> builder.insert("users", id=1, name="John")
            >>> builder.on_conflict("id").do_update(name="John")
        """
        if self._query_type != DBCommandType.INSERT:
            raise ValueError(
                "on_conflict() can only be used with INSERT queries. Call insert() first."
            )
        if not columns:
            raise ValueError("on_conflict() requires at least one column name.")
        self._conflict_columns = list(columns)
        return self

    def do_update(self, **values: Any) -> "_QueryBuilder":
        """
        Specify update values for UPSERT operation (ON CONFLICT DO UPDATE).

        Args:
            **values: Column-value pairs to update on conflict

        Returns:
            Self for method chaining

        Raises:
            ValueError: If not in INSERT mode or conflict columns not set

        Example:
            >>> builder.insert("users", id=1, name="John", email="john@example.com")
            >>> builder.on_conflict("id").do_update(name="John", email="john@example.com")
        """
        if self._query_type != DBCommandType.INSERT:
            raise ValueError(
                "do_update() can only be used with INSERT queries. Call insert() first."
            )
        if not self._conflict_columns:
            raise ValueError("do_update() requires on_conflict() to be called first.")
        self._upsert_update = values
        return self

    def dialect(self, db_dialect: str) -> "_QueryBuilder":
        """
        Set database dialect for SQL generation.

        Args:
            db_dialect: Database dialect ("postgresql", "sqlite", "mysql")

        Returns:
            Self for method chaining

        Example:
            >>> builder.insert("users", id=1).dialect("mysql")
        """
        valid_dialects = {"postgresql", "sqlite", "mysql"}
        if db_dialect.lower() not in valid_dialects:
            raise ValueError(
                f"Invalid dialect: {db_dialect}. Must be one of: {', '.join(valid_dialects)}"
            )
        self._dialect = db_dialect.lower()
        return self

    def update(self, table: str, **values: Any) -> "_QueryBuilder":
        """
        Start UPDATE query.

        Args:
            table: Table name
            **values: Column-value pairs to update

        Returns:
            Self for method chaining

        Example:
            >>> builder.update("users", name="Jane").where("id", "=", 1)
        """
        self._query_type = DBCommandType.UPDATE
        self._table = table
        self._set_clause = values
        return self

    def delete(self, table: str) -> "_QueryBuilder":
        """
        Start DELETE query.

        Args:
            table: Table name

        Returns:
            Self for method chaining

        Example:
            >>> builder.delete("users").where("id", "=", 1)
        """
        self._query_type = DBCommandType.DELETE
        self._table = table
        return self

    def _build_in_condition(
        self,
        column: str,
        value: list[Any] | tuple[Any, ...],
        params: dict[str, Any],
        param_prefix: str,
        param_counter: int,
    ) -> tuple[str, int]:
        """Build IN condition with parameter placeholders."""
        placeholders = []
        for item in value:
            param_name = f"{param_prefix}_{param_counter}"
            params[param_name] = item
            placeholders.append(f":{param_name}")
            param_counter += 1
        condition = f"{column} IN ({', '.join(placeholders)})"
        return condition, param_counter

    def _build_simple_condition(
        self,
        column: str,
        operator: str,
        value: Any,
        params: dict[str, Any],
        param_prefix: str,
        param_counter: int,
    ) -> tuple[str, int]:
        """Build simple condition with parameter placeholder."""
        param_name = f"{param_prefix}_{param_counter}"
        params[param_name] = value
        condition = f"{column} {operator} :{param_name}"
        return condition, param_counter + 1

    def _build_condition(
        self,
        column: str,
        operator: str,
        value: Any,
        params: dict[str, Any],
        param_prefix: str,
        param_counter: int,
    ) -> tuple[str, int]:
        """Build condition with parameter placeholders."""
        if operator.upper() == "IN" and isinstance(value, (list, tuple)):
            return self._build_in_condition(
                column, value, params, param_prefix, param_counter
            )
        return self._build_simple_condition(
            column, operator, value, params, param_prefix, param_counter
        )

    def _build_where_clause(self, params: dict[str, Any], param_prefix: str = "where") -> str:
        """
        Build WHERE clause from conditions.

        Args:
            params: Parameters dictionary to populate
            param_prefix: Prefix for parameter names

        Returns:
            WHERE clause SQL string (without WHERE keyword)
        """
        if not self._where_clauses:
            return ""
        where_parts = []
        param_counter = 0
        for column, operator, value, connector in self._where_clauses:
            condition, param_counter = self._build_condition(
                column, operator, value, params, param_prefix, param_counter
            )
            if connector:
                where_parts.append(f"{connector} {condition}")
            else:
                where_parts.append(condition)
        return " ".join(where_parts)

    def _build_select_columns(self) -> str:
        """Build SELECT columns clause."""
        if self._columns:
            return ", ".join(self._columns)
        return "*"

    def _build_joins(self) -> list[str]:
        """Build JOIN clauses."""
        join_parts = []
        for join_type, join_table, on_left, on_right, _ in self._joins:
            join_parts.append(f"{join_type} JOIN {join_table} ON {on_left} = {on_right}")
        return join_parts

    def _build_group_by(self) -> list[str]:
        """Build GROUP BY clause."""
        if not self._group_by:
            return []
        return [f"GROUP BY {', '.join(self._group_by)}"]

    def _build_having(self, params: dict[str, Any]) -> list[str]:
        """Build HAVING clause."""
        if not self._having:
            return []
        having_parts = []
        for i, (column, operator, value) in enumerate(self._having):
            param_name = f"having_{i}"
            params[param_name] = value
            having_parts.append(f"{column} {operator} :{param_name}")
        return [f"HAVING {' AND '.join(having_parts)}"]

    def _build_order_limit_offset(self) -> list[str]:
        """Build ORDER BY, LIMIT, OFFSET clauses."""
        parts = []
        if self._order_by:
            order_parts = [f"{col} {dir}" for col, dir in self._order_by]
            parts.append(f"ORDER BY {', '.join(order_parts)}")
        if self._limit_value is not None:
            parts.append(f"LIMIT {self._limit_value}")
        if self._offset_value is not None:
            parts.append(f"OFFSET {self._offset_value}")
        return parts

    def _build_select_core(self, params: dict[str, Any]) -> list[str]:
        """
        Build core SELECT query parts (internal helper).

        Args:
            params: Parameters dictionary to populate

        Returns:
            List of SQL query parts
        """
        query_parts: list[str] = []
        # Build columns list
        columns = self._build_select_columns()
        query_parts.append(f"SELECT {columns}")
        query_parts.append(f"FROM {self._table}")
        # Add JOINs
        query_parts.extend(self._build_joins())
        # Add WHERE
        where_clause = self._build_where_clause(params)
        if where_clause:
            query_parts.append(f"WHERE {where_clause}")
        # Add GROUP BY
        query_parts.extend(self._build_group_by())
        # Add HAVING
        query_parts.extend(self._build_having(params))
        # Add ORDER BY, LIMIT, OFFSET
        query_parts.extend(self._build_order_limit_offset())
        return query_parts

    def _build_set_clause(
        self, values: dict[str, Any], params: dict[str, Any], prefix: str
    ) -> list[str]:
        """Build SET clause for UPDATE or UPSERT."""
        set_parts = []
        for key, value in values.items():
            param_name = f"{prefix}_{key}"
            params[param_name] = value
            set_parts.append(f"{key} = :{param_name}")
        return set_parts

    def _build_upsert_clause(self, params: dict[str, Any]) -> list[str]:
        """Build UPSERT clause based on dialect."""
        if not (self._conflict_columns and self._upsert_update):
            return []
        # Determine dialect (default to postgresql/sqlite syntax)
        db_dialect = self._dialect or "postgresql"
        update_parts = self._build_set_clause(self._upsert_update, params, "upsert")
        if db_dialect == "mysql":
            # MySQL uses ON DUPLICATE KEY UPDATE (no column specification needed)
            return [f"ON DUPLICATE KEY UPDATE {', '.join(update_parts)}"]
        else:
            # PostgreSQL/SQLite use ON CONFLICT ... DO UPDATE
            conflict_cols_str = ", ".join(self._conflict_columns)
            return [
                f"ON CONFLICT ({conflict_cols_str}) DO UPDATE SET {', '.join(update_parts)}"
            ]

    def _build_insert_query(self, params: dict[str, Any]) -> list[str]:
        """Build INSERT query with optional UPSERT clause."""
        if not self._values:
            raise ValueError(
                "INSERT query requires at least one row of values. "
                "Use insert().values() or insert(**values)"
            )
        # Get columns from first row (preserve order)
        columns = list(self._values[0].keys())
        columns_str = ", ".join(columns)
        # Build VALUES clause(s) for batch INSERT
        values_parts = []
        for row_index, row_values in enumerate(self._values):
            placeholders = []
            for col in columns:
                param_name = f"{col}_{row_index}"
                params[param_name] = row_values[col]
                placeholders.append(f":{param_name}")
            values_parts.append(f"({', '.join(placeholders)})")
        query_parts = [
            f"INSERT INTO {self._table} ({columns_str})",
            f"VALUES {', '.join(values_parts)}",
        ]
        # Add UPSERT clause if specified
        query_parts.extend(self._build_upsert_clause(params))
        return query_parts

    def _build_update_query(self, params: dict[str, Any]) -> list[str]:
        """Build UPDATE query."""
        set_parts = self._build_set_clause(self._set_clause, params, "set")
        query_parts = [
            f"UPDATE {self._table}",
            f"SET {', '.join(set_parts)}",
        ]
        # Add WHERE
        where_clause = self._build_where_clause(params)
        if where_clause:
            query_parts.append(f"WHERE {where_clause}")
        # UPDATE without WHERE is dangerous, but we allow it
        return query_parts

    def _build_delete_query(self, params: dict[str, Any]) -> list[str]:
        """Build DELETE query."""
        query_parts = [f"DELETE FROM {self._table}"]
        # Add WHERE
        where_clause = self._build_where_clause(params)
        if where_clause:
            query_parts.append(f"WHERE {where_clause}")
        # DELETE without WHERE is dangerous, but we allow it
        return query_parts

    def _build(self) -> tuple[str, dict[str, Any]]:
        """
        Build SQL query and parameters (internal method).

        Returns:
            Tuple of (SQL query string, parameters dictionary)

        Raises:
            ValueError: If query is incomplete or invalid
        """
        if not self._query_type:
            raise ValueError("Query type not set. Use select(), insert(), update(), or delete()")
        if not self._table:
            raise ValueError("Table name not set. Use from_table() or insert()/update()/delete()")
        params: dict[str, Any] = {}
        # Use dispatch table instead of if/elif chain
        query_builders = {
            DBCommandType.SELECT: self._build_select_core,
            DBCommandType.INSERT: self._build_insert_query,
            DBCommandType.UPDATE: self._build_update_query,
            DBCommandType.DELETE: self._build_delete_query,
        }
        builder_method = query_builders.get(self._query_type)
        if not builder_method:
            raise ValueError(f"Unsupported query type: {self._query_type}")
        query_parts = builder_method(params)
        query = " ".join(query_parts)
        return query, params

    async def execute(self, db_client: "DBClient") -> list[dict[str, Any]] | None:
        """
        Execute query using DBClient.

        Automatically determines query type (SELECT vs INSERT/UPDATE/DELETE)
        and calls appropriate DBClient method.

        Args:
            db_client: DBClient instance to execute query

        Returns:
            List of result rows for SELECT queries, None for INSERT/UPDATE/DELETE

        Raises:
            ValueError: If query builder is incomplete or invalid
            Exception: If query execution fails

        Example:
            >>> from py_web_automation import DBClient
            >>> db = DBClient.create("postgresql", "...", config)
            >>> builder = _QueryBuilder().select("*").from_table("users")
            >>> results = await builder.where("active", "=", True).execute(db)
        """
        query, params = self._build()
        query_type = self._query_type
        if query_type == DBCommandType.SELECT:
            return await db_client.execute_query(query, params)
        else:
            await db_client.execute_command(query, params)
            return None

    def reset(self) -> "_QueryBuilder":
        """
        Reset builder to initial state.

        Returns:
            Self for method chaining
        """
        self._query_type = None
        self._table = None
        self._columns = []
        self._values = []
        self._set_clause = {}
        self._conflict_columns = None
        self._upsert_update = None
        self._dialect = None
        self._where_clauses = []
        self._order_by = []
        self._limit_value = None
        self._offset_value = None
        self._joins = []
        self._group_by = []
        self._having = []
        return self
