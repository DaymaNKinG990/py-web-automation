"""
Unit tests for middleware context classes.
"""

# Python imports
from allure import title, description, step
from pytest import mark

# Local imports
from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
    _GraphQLRequestContext,
    _GraphQLResponseContext,
)
from py_web_automation.clients.api_clients.graphql_client.graphql_result import GraphQLResult

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestGraphQLRequestContext:
    """Test _GraphQLRequestContext class."""

    @mark.asyncio
    @title("Request context initialization")
    @description("Test _GraphQLRequestContext initializes correctly.")
    async def test_request_context_init(self) -> None:
        """Test _GraphQLRequestContext initializes correctly."""
        with step("Create request context"):
            context = _GraphQLRequestContext(
                query="{ users { id } }",
                operation_type="query",
                variables={"limit": 10},
                operation_name="GetUsers",
                headers={"Authorization": "Bearer token"},
            )
        with step("Verify context attributes"):
            assert context.query == "{ users { id } }"
            assert context.operation_type == "query"
            assert context.variables == {"limit": 10}
            assert context.operation_name == "GetUsers"
            assert context.headers == {"Authorization": "Bearer token"}
            assert isinstance(context.metadata, dict)

    @mark.asyncio
    @title("Request context with defaults")
    @description("Test _GraphQLRequestContext initializes with default values.")
    async def test_request_context_defaults(self) -> None:
        """Test _GraphQLRequestContext initializes with default values."""
        with step("Create request context with minimal params"):
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query"
            )
        with step("Verify default values"):
            assert context.variables == {}
            assert context.operation_name is None
            assert context.headers == {}
            assert isinstance(context.metadata, dict)


class TestGraphQLResponseContext:
    """Test _GraphQLResponseContext class."""

    @mark.asyncio
    @title("Response context initialization")
    @description("Test _GraphQLResponseContext initializes correctly.")
    async def test_response_context_init(self) -> None:
        """Test _GraphQLResponseContext initializes correctly."""
        with step("Create GraphQLResult"):
            result = GraphQLResult(
                operation_name="GetUsers",
                operation_type="query",
                response_time=0.5,
                success=True,
                data={"users": []},
                metadata={"key": "value"},
            )
        with step("Create response context"):
            context = _GraphQLResponseContext(result)
        with step("Verify context attributes"):
            assert context.result == result
            assert context.metadata == {"key": "value"}
            assert context.metadata is not result.metadata  # Should be a copy

    @mark.asyncio
    @title("Response context metadata copy")
    @description("Test _GraphQLResponseContext copies metadata from result.")
    async def test_response_context_metadata_copy(self) -> None:
        """Test _GraphQLResponseContext copies metadata from result."""
        with step("Create GraphQLResult with metadata"):
            result = GraphQLResult(
                operation_name="GetUsers",
                operation_type="query",
                response_time=0.5,
                success=True,
                data={},
                metadata={"original": "value"},
            )
        with step("Create response context"):
            context = _GraphQLResponseContext(result)
        with step("Modify context metadata"):
            context.metadata["new"] = "value"
        with step("Verify result metadata unchanged"):
            assert "new" not in result.metadata
            assert context.metadata["new"] == "value"
