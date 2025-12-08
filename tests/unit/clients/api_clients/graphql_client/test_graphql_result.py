"""
Unit tests for GraphQLResult.
"""

# Python imports
from typing import Callable
from allure import title, description, step
from pytest import mark
from graphql import GraphQLError

# Local imports
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.clients.api_clients.graphql_client.graphql_result import GraphQLResult
from py_web_automation.config import Config

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestGraphQLResult:
    """Test GraphQLResult class."""

    @mark.asyncio
    @title("GraphQLResult contains errors from response")
    @description("Test GraphQLResult contains errors from response.")
    async def test_graphql_result_contains_errors(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test GraphQLResult contains errors from response."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to raise GraphQLError"):
                    mock_graphql_execute_operation(
                        client,
                        side_effect=GraphQLError("Error 1", extensions={"code": "ERROR1"}),
                    )
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify errors in result"):
                    assert result.success is False
                    assert len(result.errors) >= 1
                    assert result.errors[0]["message"] == "Error 1"

    @mark.asyncio
    @title("GraphQLResult returns empty errors list on success")
    @description("Test GraphQLResult returns empty errors list on success.")
    async def test_graphql_result_no_errors(
        self, valid_config: Config, mock_graphql_execute_operation
    ) -> None:
        """Test GraphQLResult returns empty errors list on success."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={"users": []})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify no errors in result"):
                    assert result.success is True
                    assert result.errors == []

    @mark.asyncio
    @title("GraphQLResult handles multiple errors")
    @description("Test GraphQLResult handles multiple errors.")
    async def test_graphql_result_multiple_errors(
        self, valid_config: Config, mock_graphql_execute_operation
    ) -> None:
        """Test GraphQLResult handles multiple errors."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to raise GraphQLError"):
                    mock_graphql_execute_operation(
                        client, side_effect=GraphQLError("Multiple errors occurred")
                    )
                with step("Execute query with invalid fields"):
                    result = await client.query("{ invalidField1 invalidField2 }")
                with step("Verify multiple errors handling"):
                    assert result.success is False
                    assert len(result.errors) >= 1

    @mark.asyncio
    @title("GraphQLResult raise_for_errors raises on errors")
    @description("Test GraphQLResult.raise_for_errors() raises exception when errors present.")
    async def test_graphql_result_raise_for_errors(self) -> None:
        """Test GraphQLResult.raise_for_errors() raises exception when errors present."""
        with step("Create GraphQLResult with errors"):
            result = GraphQLResult(
                operation_name="TestQuery",
                operation_type="query",
                response_time=0.1,
                success=False,
                data=None,
                errors=[{"message": "Error 1"}, {"message": "Error 2"}],
            )
        with step("Verify raise_for_errors raises exception"):
            from pytest import raises

            with raises(Exception, match="GraphQL operation 'TestQuery' failed"):
                result.raise_for_errors()

    @mark.asyncio
    @title("GraphQLResult raise_for_errors does not raise on success")
    @description("Test GraphQLResult.raise_for_errors() does not raise when no errors.")
    async def test_graphql_result_raise_for_errors_no_errors(self) -> None:
        """Test GraphQLResult.raise_for_errors() does not raise when no errors."""
        with step("Create GraphQLResult without errors"):
            result = GraphQLResult(
                operation_name="TestQuery",
                operation_type="query",
                response_time=0.1,
                success=True,
                data={"users": []},
                errors=[],
            )
        with step("Verify raise_for_errors does not raise"):
            result.raise_for_errors()  # Should not raise
