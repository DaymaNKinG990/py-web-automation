"""
Unit tests for query_builder module.
"""

import allure
import pytest

from py_web_automation.query_builder import QueryBuilder

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit, pytest.mark.db]


class TestQueryBuilderSelect:
    """Test QueryBuilder SELECT queries."""

    @allure.title("TC-QB-001: QueryBuilder - select")
    def test_query_builder_select(self):
        """Test SELECT query building."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build SELECT query"):
            builder.select("id", "name", "email")
            builder.from_table("users")
            sql, params = builder.build()

        with allure.step("Verify SELECT query built correctly"):
            sql_upper = sql.upper()
            assert "SELECT" in sql_upper
            assert "id" in sql.lower() or "ID" in sql_upper
            assert "name" in sql.lower() or "NAME" in sql_upper
            assert "email" in sql.lower() or "EMAIL" in sql_upper
            assert "FROM" in sql_upper and "USERS" in sql_upper

    @allure.title("TC-QB-002: QueryBuilder - select *")
    def test_query_builder_select_wildcard(self):
        """Test SELECT * query."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build SELECT * query"):
            builder.select("*")
            builder.from_table("users")
            sql, params = builder.build()

        with allure.step("Verify SELECT * query built"):
            sql_upper = sql.upper()
            assert "SELECT" in sql_upper and "*" in sql
            assert "FROM" in sql_upper and "USERS" in sql_upper

    @allure.title("TC-QB-003: QueryBuilder - from_table")
    def test_query_builder_from_table(self):
        """Test FROM clause."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with FROM"):
            builder.select("*").from_table("users")
            sql, params = builder.build()

        with allure.step("Verify FROM clause added"):
            sql_upper = sql.upper()
            assert "FROM" in sql_upper and "USERS" in sql_upper

    @allure.title("TC-QB-004: QueryBuilder - where")
    def test_query_builder_where(self):
        """Test WHERE clause."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with WHERE"):
            builder.select("*").from_table("users").where("active", "=", True)
            sql, params = builder.build()

        with allure.step("Verify WHERE clause and parameters"):
            sql_upper = sql.upper()
            assert "WHERE" in sql_upper
            assert "active" in sql.lower() or "ACTIVE" in sql_upper
            assert len(params) > 0
            assert any(v or "true" in str(v).lower() for v in params.values())

    @allure.title("TC-QB-005: QueryBuilder - multiple where")
    def test_query_builder_multiple_where(self):
        """Test multiple WHERE conditions."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with multiple WHERE"):
            builder.select("*").from_table("users").where("active", "=", True).where("age", ">=", 18)
            sql, params = builder.build()

        with allure.step("Verify both conditions in WHERE"):
            assert "WHERE" in sql.upper()
            assert "active" in sql
            assert "age" in sql
            assert "AND" in sql.upper()

    @allure.title("TC-QB-006: QueryBuilder - order_by")
    def test_query_builder_order_by(self):
        """Test ORDER BY clause."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with ORDER BY"):
            builder.select("*").from_table("users").order_by("name", "ASC")
            sql, params = builder.build()

        with allure.step("Verify ORDER BY clause in SQL"):
            assert "ORDER BY" in sql.upper()
            assert "name" in sql
            assert "ASC" in sql.upper()

    @allure.title("TC-QB-007: QueryBuilder - order_by DESC")
    def test_query_builder_order_by_desc(self):
        """Test ORDER BY DESC."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with ORDER BY DESC"):
            builder.select("*").from_table("users").order_by("created_at", "DESC")
            sql, params = builder.build()

        with allure.step("Verify ORDER BY DESC added"):
            assert "ORDER BY" in sql.upper()
            assert "created_at" in sql
            assert "DESC" in sql.upper()

    @allure.title("TC-QB-008: QueryBuilder - multiple order_by")
    def test_query_builder_multiple_order_by(self):
        """Test multiple ORDER BY columns."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with multiple ORDER BY"):
            builder.select("*").from_table("users").order_by("status", "ASC").order_by("name", "ASC")
            sql, params = builder.build()

        with allure.step("Verify both columns in ORDER BY"):
            assert "ORDER BY" in sql.upper()
            assert "status" in sql
            assert "name" in sql

    @allure.title("TC-QB-009: QueryBuilder - limit")
    def test_query_builder_limit(self):
        """Test LIMIT clause."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with LIMIT"):
            builder.select("*").from_table("users").limit(10)
            sql, params = builder.build()

        with allure.step("Verify LIMIT 10 in SQL"):
            assert "LIMIT" in sql.upper()
            assert "10" in sql

    @allure.title("TC-QB-010: QueryBuilder - offset")
    def test_query_builder_offset(self):
        """Test OFFSET clause."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with OFFSET"):
            builder.select("*").from_table("users").offset(20)
            sql, params = builder.build()

        with allure.step("Verify OFFSET 20 in SQL"):
            assert "OFFSET" in sql.upper()
            assert "20" in sql

    @allure.title("TC-QB-011: QueryBuilder - limit и offset вместе")
    def test_query_builder_limit_and_offset(self):
        """Test LIMIT and OFFSET together."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with LIMIT and OFFSET"):
            builder.select("*").from_table("users").limit(10).offset(20)
            sql, params = builder.build()

        with allure.step("Verify both LIMIT and OFFSET added"):
            assert "LIMIT" in sql.upper()
            assert "OFFSET" in sql.upper()
            assert "10" in sql
            assert "20" in sql

    @allure.title("TC-QB-012: QueryBuilder - join")
    def test_query_builder_join(self):
        """Test JOIN clause."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with JOIN"):
            builder.select("*").from_table("users").join("orders", "users.id", "orders.user_id", "LEFT")
            sql, params = builder.build()

        with allure.step("Verify LEFT JOIN clause in SQL"):
            assert "JOIN" in sql.upper()
            assert "orders" in sql
            assert "LEFT" in sql.upper()

    @allure.title("TC-QB-013: QueryBuilder - multiple joins")
    def test_query_builder_multiple_joins(self):
        """Test multiple JOINs."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with multiple JOINs"):
            builder.select("*").from_table("users")
            builder.join("orders", "users.id", "orders.user_id", "LEFT")
            builder.join("products", "orders.product_id", "products.id", "INNER")
            sql, params = builder.build()

        with allure.step("Verify both JOINs in SQL"):
            assert sql.upper().count("JOIN") == 2

    @allure.title("TC-QB-014: QueryBuilder - group_by")
    def test_query_builder_group_by(self):
        """Test GROUP BY clause."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with GROUP BY"):
            builder.select("*").from_table("users").group_by("status", "category")
            sql, params = builder.build()

        with allure.step("Verify GROUP BY clause in SQL"):
            assert "GROUP BY" in sql.upper()
            assert "status" in sql
            assert "category" in sql

    @allure.title("TC-QB-015: QueryBuilder - having")
    def test_query_builder_having(self):
        """Test HAVING clause."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build query with HAVING"):
            builder.select("*").from_table("users").group_by("status").having("COUNT(*)", ">", 10)
            sql, params = builder.build()

        with allure.step("Verify HAVING clause in SQL"):
            assert "HAVING" in sql.upper()
            assert "COUNT(*)" in sql
            assert ">" in sql


@pytest.mark.unit
class TestQueryBuilderInsert:
    """Test QueryBuilder INSERT queries."""

    @allure.title("TC-QB-016: QueryBuilder - insert")
    def test_query_builder_insert(self):
        """Test INSERT query building."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build INSERT query"):
            builder.insert("users", name="John", email="john@example.com")
            sql, params = builder.build()

        with allure.step("Verify INSERT query and parameters"):
            assert "INSERT" in sql.upper()
            assert "users" in sql
            assert "name" in sql
            assert "email" in sql
            assert len(params) >= 2
            assert "John" in str(params.values())
            assert "john@example.com" in str(params.values())

    @allure.title("TC-QB-017: QueryBuilder - insert с множеством полей")
    def test_query_builder_insert_multiple_fields(self):
        """Test INSERT with multiple fields."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build INSERT with multiple fields"):
            builder.insert("users", name="John", email="john@example.com", age=30)
            sql, params = builder.build()

        with allure.step("Verify all fields in INSERT"):
            assert "name" in sql
            assert "email" in sql
            assert "age" in sql
            assert len(params) >= 3


@pytest.mark.unit
class TestQueryBuilderUpdate:
    """Test QueryBuilder UPDATE queries."""

    @allure.title("TC-QB-018: QueryBuilder - update")
    def test_query_builder_update(self):
        """Test UPDATE query building."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build UPDATE query"):
            builder.update("users", name="Jane").where("id", "=", 1)
            sql, params = builder.build()

        with allure.step("Verify UPDATE query and parameters"):
            assert "UPDATE" in sql.upper()
            assert "users" in sql
            assert "SET" in sql.upper()
            assert "WHERE" in sql.upper()
            assert "name" in sql
            assert "id" in sql

    @allure.title("TC-QB-019: QueryBuilder - update без WHERE")
    def test_query_builder_update_no_where(self):
        """Test UPDATE without WHERE (allowed but dangerous)."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build UPDATE without WHERE"):
            builder.update("users", name="Jane")
            sql, params = builder.build()

        with allure.step("Verify UPDATE without WHERE"):
            assert "UPDATE" in sql.upper()
            assert "SET" in sql.upper()
            assert "WHERE" not in sql.upper()

    @allure.title("TC-QB-020: QueryBuilder - update с множеством полей")
    def test_query_builder_update_multiple_fields(self):
        """Test UPDATE with multiple fields."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build UPDATE with multiple fields"):
            builder.update("users", name="Jane", email="jane@example.com").where("id", "=", 1)
            sql, params = builder.build()

        with allure.step("Verify all fields in SET"):
            assert "name" in sql
            assert "email" in sql


@pytest.mark.unit
class TestQueryBuilderDelete:
    """Test QueryBuilder DELETE queries."""

    @allure.title("TC-QB-021: QueryBuilder - delete")
    def test_query_builder_delete(self):
        """Test DELETE query building."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build DELETE query"):
            builder.delete("users").where("id", "=", 1)
            sql, params = builder.build()

        with allure.step("Verify DELETE query and parameters"):
            assert "DELETE" in sql.upper()
            sql_upper = sql.upper()
            assert "FROM" in sql_upper and ("USERS" in sql_upper or "users" in sql)
            assert "WHERE" in sql.upper()
            assert "id" in sql

    @allure.title("TC-QB-022: QueryBuilder - delete без WHERE")
    def test_query_builder_delete_no_where(self):
        """Test DELETE without WHERE (allowed but dangerous)."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build DELETE without WHERE"):
            builder.delete("users")
            sql, params = builder.build()

        with allure.step("Verify DELETE without WHERE"):
            assert "DELETE" in sql.upper()
            sql_upper = sql.upper()
            assert "FROM" in sql_upper and ("USERS" in sql_upper or "users" in sql)
            assert "WHERE" not in sql.upper()


@pytest.mark.unit
class TestQueryBuilderErrors:
    """Test QueryBuilder error handling."""

    @allure.title("TC-QB-023: QueryBuilder - build без query_type")
    def test_query_builder_build_no_query_type(self):
        """Test error when build called without query type."""
        with allure.step("Create empty QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Call build and expect error"):
            with pytest.raises((ValueError, AttributeError)):
                builder.build()

    @allure.title("TC-QB-024: QueryBuilder - build без table")
    def test_query_builder_build_no_table(self):
        """Test error when build called without table."""
        with allure.step("Create QueryBuilder with select"):
            builder = QueryBuilder()
            builder.select("*")

        with allure.step("Call build and expect error"):
            with pytest.raises((ValueError, AttributeError)):
                builder.build()


@pytest.mark.unit
class TestQueryBuilderUtility:
    """Test QueryBuilder utility methods."""

    @allure.title("TC-QB-025: QueryBuilder - reset")
    def test_query_builder_reset(self):
        """Test builder reset."""
        with allure.step("Create QueryBuilder with query"):
            builder = QueryBuilder()
            builder.select("*").from_table("users")

        with allure.step("Reset builder"):
            builder.reset()

        with allure.step("Verify builder is empty"):
            # After reset, build should fail (no query type)
            with pytest.raises((ValueError, AttributeError)):
                builder.build()

    @allure.title("TC-QB-026: QueryBuilder - method chaining")
    def test_query_builder_method_chaining(self):
        """Test method chaining works."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Chain methods"):
            builder.select("*").from_table("users").where("active", "=", True).order_by("name")
            sql, params = builder.build()

        with allure.step("Verify query built correctly"):
            sql_upper = sql.upper()
            assert "SELECT" in sql_upper
            assert "FROM" in sql_upper and "USERS" in sql_upper
            assert "WHERE" in sql_upper
            assert "ORDER BY" in sql_upper

    @allure.title("TC-QB-027: QueryBuilder - параметры в build")
    def test_query_builder_build_parameters(self):
        """Test parameters returned in build."""
        with allure.step("Create QueryBuilder with where"):
            builder = QueryBuilder()
            builder.select("*").from_table("users").where("id", "=", 1)

        with allure.step("Build query"):
            sql, params = builder.build()

        with allure.step("Verify parameters dict contains value"):
            assert isinstance(params, dict)
            assert len(params) > 0
            assert 1 in params.values() or any("1" in str(v) for v in params.values())

    @allure.title("TC-QB-028: QueryBuilder - сложный запрос")
    def test_query_builder_complex_query(self):
        """Test complex query building."""
        with allure.step("Create QueryBuilder"):
            builder = QueryBuilder()

        with allure.step("Build complex query"):
            builder.select("users.id", "users.name", "orders.total")
            builder.from_table("users")
            builder.join("orders", "users.id", "orders.user_id", "LEFT")
            builder.where("users.active", "=", True)
            builder.group_by("users.id", "users.name")
            builder.having("COUNT(orders.id)", ">", 0)
            builder.order_by("users.name", "ASC")
            builder.limit(10).offset(20)
            sql, params = builder.build()

        with allure.step("Verify all clauses in correct order"):
            sql_upper = sql.upper()
            assert "SELECT" in sql_upper
            assert "FROM" in sql_upper and "USERS" in sql_upper
            assert "JOIN" in sql_upper
            assert "WHERE" in sql_upper
            assert "GROUP BY" in sql_upper
            assert "HAVING" in sql_upper
            assert "ORDER BY" in sql_upper
            assert "LIMIT" in sql_upper
            assert "OFFSET" in sql_upper
