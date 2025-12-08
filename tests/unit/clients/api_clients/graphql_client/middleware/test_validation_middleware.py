"""
Unit tests for ValidationMiddleware.
"""

# Python imports
from typing import Callable
from allure import title, description, step
from pytest import mark
from pytest_mock import MockerFixture
from graphql import GraphQLError, build_schema

# Local imports
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.clients.api_clients.graphql_client.middleware import (
    ValidationMiddleware,
    MiddlewareChain,
)
from py_web_automation.config import Config

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestValidationMiddleware:
    """Test ValidationMiddleware class."""

    @mark.asyncio
    @title("ValidationMiddleware validates valid query")
    @description("Test ValidationMiddleware validates valid GraphQL query.")
    async def test_validation_middleware_validates_valid_query(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test ValidationMiddleware validates valid GraphQL query."""
        with step("Setup ValidationMiddleware with schema"):
            url = "https://api.example.com/graphql"
            schema = build_schema(
                """
                type Query {
                    users: [User!]!
                }
                type User {
                    id: ID!
                    name: String!
                }
                """
            )
            validation_middleware = ValidationMiddleware(schema=schema, enabled=True)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(validation_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={"users": []})
                with step("Execute valid query"):
                    result = await client.query("{ users { id name } }")
                with step("Verify query was validated and executed"):
                    assert result.success is True

    @mark.asyncio
    @title("ValidationMiddleware rejects invalid query")
    @description("Test ValidationMiddleware rejects invalid GraphQL query.")
    async def test_validation_middleware_rejects_invalid_query(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test ValidationMiddleware rejects invalid GraphQL query."""
        with step("Setup ValidationMiddleware with schema"):
            url = "https://api.example.com/graphql"
            schema = build_schema(
                """
                type Query {
                    users: [User!]!
                }
                type User {
                    id: ID!
                    name: String!
                }
                """
            )
            validation_middleware = ValidationMiddleware(schema=schema, enabled=True)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(validation_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Execute invalid query"):
                    from pytest import raises

                    with raises(GraphQLError):
                        await client.query("{ invalidField { id } }")

    @mark.asyncio
    @title("ValidationMiddleware skips when disabled")
    @description("Test ValidationMiddleware skips validation when disabled.")
    async def test_validation_middleware_skips_when_disabled(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test ValidationMiddleware skips validation when disabled."""
        with step("Setup ValidationMiddleware disabled"):
            url = "https://api.example.com/graphql"
            schema = build_schema("type Query { users: [User!]! } type User { id: ID! }")
            validation_middleware = ValidationMiddleware(schema=schema, enabled=False)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(validation_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query (validation should be skipped)"):
                    result = await client.query("{ invalidField { id } }")
                with step("Verify query executed without validation"):
                    assert result.success is True

    @mark.asyncio
    @title("ValidationMiddleware uses schema from metadata")
    @description("Test ValidationMiddleware._get_schema() uses schema from context metadata.")
    async def test_validation_middleware_uses_schema_from_metadata(self) -> None:
        """Test ValidationMiddleware._get_schema() uses schema from context metadata."""
        from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
            _GraphQLRequestContext,
        )
        from graphql import build_schema

        with step("Create ValidationMiddleware without schema"):
            validation_middleware = ValidationMiddleware(schema=None, enabled=True)
        with step("Create request context with schema in metadata"):
            schema = build_schema("type Query { users: [User!]! } type User { id: ID! }")
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query"
            )
            context.metadata["schema"] = schema
        with step("Get schema from middleware"):
            retrieved_schema = validation_middleware._get_schema(context)
        with step("Verify schema from metadata is returned"):
            assert retrieved_schema is schema

    @mark.asyncio
    @title("ValidationMiddleware skips when schema is None")
    @description("Test ValidationMiddleware.process_request() skips validation when schema is None.")
    async def test_validation_middleware_skips_when_schema_none(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test ValidationMiddleware.process_request() skips validation when schema is None."""
        with step("Setup ValidationMiddleware without schema"):
            url = "https://api.example.com/graphql"
            validation_middleware = ValidationMiddleware(schema=None, enabled=True)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(validation_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query (should skip validation)"):
                    result = await client.query("{ invalidField { id } }")
                with step("Verify query executed without validation"):
                    assert result.success is True

    @mark.asyncio
    @title("ValidationMiddleware handles non-GraphQLError exceptions")
    @description("Test ValidationMiddleware.process_request() handles non-GraphQLError exceptions gracefully.")
    async def test_validation_middleware_handles_non_graphql_errors(
        self, valid_config: Config, mock_graphql_execute_operation: Callable, mocker: MockerFixture
    ) -> None:
        """Test ValidationMiddleware.process_request() handles non-GraphQLError exceptions gracefully."""
        from graphql import build_schema

        with step("Setup ValidationMiddleware with schema"):
            url = "https://api.example.com/graphql"
            schema = build_schema("type Query { users: [User!]! } type User { id: ID! }")
            validation_middleware = ValidationMiddleware(schema=schema, enabled=True)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(validation_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _get_schema to raise non-GraphQLError"):
                    # Mock _get_schema to raise ValueError (non-GraphQLError)
                    mocker.patch.object(
                        validation_middleware,
                        "_get_schema",
                        side_effect=ValueError("Schema error"),
                    )
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query (should handle exception gracefully)"):
                    result = await client.query("{ users { id } }")
                with step("Verify query executed despite exception"):
                    assert result.success is True

    @mark.asyncio
    @title("ValidationMiddleware process_error returns None")
    @description("Test ValidationMiddleware.process_error() returns None.")
    async def test_validation_middleware_process_error(self) -> None:
        """Test ValidationMiddleware.process_error() returns None."""
        from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
            _GraphQLRequestContext,
        )

        with step("Create ValidationMiddleware"):
            validation_middleware = ValidationMiddleware(schema=None, enabled=True)
        with step("Create request context"):
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query"
            )
        with step("Process error"):
            result = await validation_middleware.process_error(context, Exception("Test error"))
        with step("Verify returns None"):
            assert result is None
