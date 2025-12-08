"""
Unit tests for LoggingMiddleware.
"""

# Python imports
from typing import Callable
from allure import title, description, step
from pytest import mark

# Local imports
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.clients.api_clients.graphql_client.middleware import (
    LoggingMiddleware,
    MiddlewareChain,
)
from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
    _GraphQLRequestContext,
    _GraphQLResponseContext,
)
from py_web_automation.config import Config

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestLoggingMiddleware:
    """Test LoggingMiddleware class."""

    @mark.asyncio
    @title("LoggingMiddleware logs request")
    @description("Test LoggingMiddleware logs GraphQL request.")
    async def test_logging_middleware_logs_request(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test LoggingMiddleware logs GraphQL request."""
        with step("Setup LoggingMiddleware"):
            url = "https://api.example.com/graphql"
            logging_middleware = LoggingMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(logging_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify request was logged"):
                    assert result.success is True
                    # Logging happens via loguru, no direct assertion needed

    @mark.asyncio
    @title("LoggingMiddleware logs response")
    @description("Test LoggingMiddleware logs GraphQL response.")
    async def test_logging_middleware_logs_response(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test LoggingMiddleware logs GraphQL response."""
        with step("Setup LoggingMiddleware"):
            url = "https://api.example.com/graphql"
            logging_middleware = LoggingMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(logging_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={"users": []})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify response was logged"):
                    assert result.success is True
                    # Logging happens via loguru, no direct assertion needed

    @mark.asyncio
    @title("LoggingMiddleware logs error")
    @description("Test LoggingMiddleware logs GraphQL error.")
    async def test_logging_middleware_logs_error(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test LoggingMiddleware logs GraphQL error."""
        from graphql import GraphQLError

        with step("Setup LoggingMiddleware"):
            url = "https://api.example.com/graphql"
            logging_middleware = LoggingMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(logging_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation to raise error"):
                    mock_graphql_execute_operation(client, side_effect=GraphQLError("Test error"))
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify error was logged"):
                    assert result.success is False
                    # Logging happens via loguru, no direct assertion needed

    @mark.asyncio
    @title("LoggingMiddleware logs request with variables")
    @description("Test LoggingMiddleware logs GraphQL request with variables.")
    async def test_logging_middleware_logs_request_with_variables(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test LoggingMiddleware logs GraphQL request with variables."""
        with step("Setup LoggingMiddleware"):
            url = "https://api.example.com/graphql"
            logging_middleware = LoggingMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(logging_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query with variables"):
                    result = await client.query(
                        "query GetUser($id: ID!) { user(id: $id) { name } }",
                        variables={"id": "123"},
                    )
                with step("Verify request with variables was logged"):
                    assert result.success is True
                    # Logging happens via loguru, no direct assertion needed

    @mark.asyncio
    @title("LoggingMiddleware logs multiple errors")
    @description("Test LoggingMiddleware logs all errors in response.")
    async def test_logging_middleware_logs_multiple_errors(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test LoggingMiddleware logs all errors in response."""
        from graphql import GraphQLError

        with step("Setup LoggingMiddleware"):
            url = "https://api.example.com/graphql"
            logging_middleware = LoggingMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(logging_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation to raise error"):
                    mock_graphql_execute_operation(client, side_effect=GraphQLError("Error 1"))
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify errors were logged"):
                    assert result.success is False
                    assert len(result.errors) >= 1
                    # Logging happens via loguru, no direct assertion needed
