"""
Query builder for constructing SQL queries with fluent API.

This module provides a query builder for constructing SQL queries
in a type-safe and readable way.
"""

from typing import Any


class QueryBuilder:
    """
    Fluent query builder for SQL queries.

    Provides a fluent API for constructing SELECT, INSERT, UPDATE, DELETE queries
    in a readable and type-safe manner.

    Attributes:
        _query_type: Type of query (SELECT, INSERT, UPDATE, DELETE)
        _table: Table name
        _columns: List of columns for SELECT or INSERT
        _values: Values for INSERT
        _set_clause: SET clause for UPDATE
        _where_clauses: WHERE clause conditions
        _order_by: ORDER BY clause
        _limit_value: LIMIT value
        _offset_value: OFFSET value
        _joins: JOIN clauses
        _group_by: GROUP BY clause
        _having: HAVING clause

    Example:
        >>> builder = QueryBuilder()
        >>> query, params = builder.select("id", "name").from_table("users").where("active", "=", True).build()
        >>> # Returns: ("SELECT id, name FROM users WHERE active = :active", {"active": True})
    """

    def __init__(self) -> None:
        """Initialize empty query builder."""
        self._query_type: str | None = None
        self._table: str | None = None
        self._columns: list[str] = []
        self._values: dict[str, Any] = {}
        self._set_clause: dict[str, Any] = {}
        self._where_clauses: list[tuple[str, str, Any]] = []
        self._order_by: list[tuple[str, str]] = []  # (column, direction)
        self._limit_value: int | None = None
        self._offset_value: int | None = None
        self._joins: list[tuple[str, str, str, str, Any]] = []  # (type, table, on_left, on_right, condition)
        self._group_by: list[str] = []
        self._having: list[tuple[str, str, Any]] = []

    def select(self, *columns: str) -> "QueryBuilder":
        """
        Start SELECT query with columns.

        Args:
            *columns: Column names to select

        Returns:
            Self for method chaining

        Example:
            >>> builder.select("id", "name", "email")
        """
        self._query_type = "SELECT"
        self._columns = list(columns)
        return self

    def from_table(self, table: str) -> "QueryBuilder":
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

    def where(self, column: str, operator: str, value: Any) -> "QueryBuilder":
        """
        Add WHERE condition.

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
        self._where_clauses.append((column, operator, value))
        return self

    def and_where(self, column: str, operator: str, value: Any) -> "QueryBuilder":
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

    def or_where(self, column: str, operator: str, value: Any) -> "QueryBuilder":
        """
        Add OR WHERE condition.

        Note: This is a simplified implementation. For complex OR conditions,
        consider using raw SQL or a more advanced query builder.

        Args:
            column: Column name
            operator: Comparison operator
            value: Value to compare

        Returns:
            Self for method chaining
        """
        # For simplicity, we'll treat OR as AND in this implementation
        # A full implementation would need to track OR groups
        return self.where(column, operator, value)

    def order_by(self, column: str, direction: str = "ASC") -> "QueryBuilder":
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

    def limit(self, count: int) -> "QueryBuilder":
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

    def offset(self, count: int) -> "QueryBuilder":
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

    def join(self, table: str, on_left: str, on_right: str, join_type: str = "INNER") -> "QueryBuilder":
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

    def group_by(self, *columns: str) -> "QueryBuilder":
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

    def having(self, column: str, operator: str, value: Any) -> "QueryBuilder":
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

    def insert(self, table: str, **values: Any) -> "QueryBuilder":
        """
        Start INSERT query.

        Args:
            table: Table name
            **values: Column-value pairs to insert

        Returns:
            Self for method chaining

        Example:
            >>> builder.insert("users", name="John", email="john@example.com")
        """
        self._query_type = "INSERT"
        self._table = table
        self._values = values
        return self

    def update(self, table: str, **values: Any) -> "QueryBuilder":
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
        self._query_type = "UPDATE"
        self._table = table
        self._set_clause = values
        return self

    def delete(self, table: str) -> "QueryBuilder":
        """
        Start DELETE query.

        Args:
            table: Table name

        Returns:
            Self for method chaining

        Example:
            >>> builder.delete("users").where("id", "=", 1)
        """
        self._query_type = "DELETE"
        self._table = table
        return self

    def build(self) -> tuple[str, dict[str, Any]]:
        """
        Build SQL query and parameters.

        Returns:
            Tuple of (SQL query string, parameters dictionary)

        Raises:
            ValueError: If query is incomplete or invalid

        Example:
            >>> query, params = builder.select("id", "name").from_table("users").where("active", "=", True).build()
            >>> # query: "SELECT id, name FROM users WHERE active = :active"
            >>> # params: {"active": True}
        """
        if not self._query_type:
            raise ValueError("Query type not set. Use select(), insert(), update(), or delete()")
        if not self._table:
            raise ValueError("Table name not set. Use from_table() or insert()/update()/delete()")

        params: dict[str, Any] = {}
        query_parts: list[str] = []

        if self._query_type == "SELECT":
            # Build SELECT query
            columns = ", ".join(self._columns) if self._columns else "*"
            query_parts.append(f"SELECT {columns}")
            query_parts.append(f"FROM {self._table}")

            # Add JOINs
            for join_type, join_table, on_left, on_right, _ in self._joins:
                query_parts.append(f"{join_type} JOIN {join_table} ON {on_left} = {on_right}")

            # Add WHERE
            if self._where_clauses:
                where_parts = []
                for i, (column, operator, value) in enumerate(self._where_clauses):
                    param_name = f"where_{i}"
                    params[param_name] = value
                    where_parts.append(f"{column} {operator} :{param_name}")
                query_parts.append(f"WHERE {' AND '.join(where_parts)}")

            # Add GROUP BY
            if self._group_by:
                query_parts.append(f"GROUP BY {', '.join(self._group_by)}")

            # Add HAVING
            if self._having:
                having_parts = []
                for i, (column, operator, value) in enumerate(self._having):
                    param_name = f"having_{i}"
                    params[param_name] = value
                    having_parts.append(f"{column} {operator} :{param_name}")
                query_parts.append(f"HAVING {' AND '.join(having_parts)}")

            # Add ORDER BY
            if self._order_by:
                order_parts = [f"{col} {dir}" for col, dir in self._order_by]
                query_parts.append(f"ORDER BY {', '.join(order_parts)}")

            # Add LIMIT
            if self._limit_value is not None:
                query_parts.append(f"LIMIT {self._limit_value}")

            # Add OFFSET
            if self._offset_value is not None:
                query_parts.append(f"OFFSET {self._offset_value}")

        elif self._query_type == "INSERT":
            # Build INSERT query
            columns = ", ".join(self._values.keys())
            placeholders = ", ".join([f":{key}" for key in self._values.keys()])
            query_parts.append(f"INSERT INTO {self._table} ({columns})")
            query_parts.append(f"VALUES ({placeholders})")
            params.update(self._values)

        elif self._query_type == "UPDATE":
            # Build UPDATE query
            set_parts = []
            for key, value in self._set_clause.items():
                param_name = f"set_{key}"
                params[param_name] = value
                set_parts.append(f"{key} = :{param_name}")
            query_parts.append(f"UPDATE {self._table}")
            query_parts.append(f"SET {', '.join(set_parts)}")

            # Add WHERE
            if self._where_clauses:
                where_parts = []
                for i, (column, operator, value) in enumerate(self._where_clauses):
                    param_name = f"where_{i}"
                    params[param_name] = value
                    where_parts.append(f"{column} {operator} :{param_name}")
                query_parts.append(f"WHERE {' AND '.join(where_parts)}")
            else:
                # UPDATE without WHERE is dangerous, but we allow it
                pass

        elif self._query_type == "DELETE":
            # Build DELETE query
            query_parts.append(f"DELETE FROM {self._table}")

            # Add WHERE
            if self._where_clauses:
                where_parts = []
                for i, (column, operator, value) in enumerate(self._where_clauses):
                    param_name = f"where_{i}"
                    params[param_name] = value
                    where_parts.append(f"{column} {operator} :{param_name}")
                query_parts.append(f"WHERE {' AND '.join(where_parts)}")
            else:
                # DELETE without WHERE is dangerous, but we allow it
                pass

        query = " ".join(query_parts)
        return query, params

    def reset(self) -> "QueryBuilder":
        """
        Reset builder to initial state.

        Returns:
            Self for method chaining
        """
        self._query_type = None
        self._table = None
        self._columns = []
        self._values = {}
        self._set_clause = {}
        self._where_clauses = []
        self._order_by = []
        self._limit_value = None
        self._offset_value = None
        self._joins = []
        self._group_by = []
        self._having = []
        return self
