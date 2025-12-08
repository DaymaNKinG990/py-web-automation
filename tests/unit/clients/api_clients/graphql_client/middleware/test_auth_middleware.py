"""
Unit tests for AuthMiddleware.
"""

# Python imports
from typing import Callable
from allure import title, description, step
from pytest import mark
from pytest_mock import MockerFixture

# Local imports
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.clients.api_clients.graphql_client.middleware import AuthMiddleware, MiddlewareChain
from py_web_automation.config import Config

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestAuthMiddleware:
    """Test AuthMiddleware class."""

    @mark.asyncio
    @title("AuthMiddleware sets token")
    @description("Test AuthMiddleware sets authentication token.")
    async def test_auth_middleware_sets_token(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test AuthMiddleware sets authentication token."""
        with step("Setup AuthMiddleware and MiddlewareChain"):
            url = "https://api.example.com/graphql"
            auth_middleware = AuthMiddleware(token="test-token-123", token_type="Bearer")
            middleware_chain = MiddlewareChain()
            middleware_chain.add(auth_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation method"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify result and Authorization header"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert "Authorization" in request_context.headers
                    assert request_context.headers["Authorization"] == "Bearer test-token-123"

    @mark.asyncio
    @title("AuthMiddleware with custom token type")
    @description("Test AuthMiddleware with custom token type.")
    async def test_auth_middleware_custom_token_type(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test AuthMiddleware with custom token type."""
        with step("Setup AuthMiddleware with custom token type"):
            url = "https://api.example.com/graphql"
            auth_middleware = AuthMiddleware(token="custom-token", token_type="Custom")
            middleware_chain = MiddlewareChain()
            middleware_chain.add(auth_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation method"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify result and custom Authorization header"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert "Authorization" in request_context.headers
                    assert request_context.headers["Authorization"] == "Custom custom-token"

    @mark.asyncio
    @title("AuthMiddleware update_token updates token")
    @description("Test AuthMiddleware.update_token() updates token dynamically.")
    async def test_auth_middleware_update_token(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test AuthMiddleware.update_token() updates token dynamically."""
        with step("Setup AuthMiddleware"):
            url = "https://api.example.com/graphql"
            auth_middleware = AuthMiddleware(token="initial-token", token_type="Bearer")
            middleware_chain = MiddlewareChain()
            middleware_chain.add(auth_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation method"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Update token"):
                    auth_middleware.update_token("updated-token")
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify updated token is used"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert request_context.headers["Authorization"] == "Bearer updated-token"

    @mark.asyncio
    @title("AuthMiddleware clear_token removes token")
    @description("Test AuthMiddleware.clear_token() removes token.")
    async def test_auth_middleware_clear_token(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test AuthMiddleware.clear_token() removes token."""
        with step("Setup AuthMiddleware"):
            url = "https://api.example.com/graphql"
            auth_middleware = AuthMiddleware(token="test-token", token_type="Bearer")
            middleware_chain = MiddlewareChain()
            middleware_chain.add(auth_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation method"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Clear token"):
                    auth_middleware.clear_token()
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify token is not in headers"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert "Authorization" not in request_context.headers

    @mark.asyncio
    @title("AuthMiddleware update_token with token_type")
    @description("Test AuthMiddleware.update_token() updates token and token_type.")
    async def test_auth_middleware_update_token_with_token_type(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test AuthMiddleware.update_token() updates token and token_type."""
        with step("Setup AuthMiddleware"):
            url = "https://api.example.com/graphql"
            auth_middleware = AuthMiddleware(token="initial-token", token_type="Bearer")
            middleware_chain = MiddlewareChain()
            middleware_chain.add(auth_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation method"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Update token with new token_type"):
                    auth_middleware.update_token("new-token", token_type="Custom")
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify updated token and token_type are used"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert request_context.headers["Authorization"] == "Custom new-token"
                    assert auth_middleware.token_type == "Custom"

    @mark.asyncio
    @title("AuthMiddleware process_error returns None")
    @description("Test AuthMiddleware.process_error() returns None.")
    async def test_auth_middleware_process_error(self) -> None:
        """Test AuthMiddleware.process_error() returns None."""
        from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
            _GraphQLRequestContext,
        )

        with step("Create AuthMiddleware"):
            auth_middleware = AuthMiddleware(token="test-token")
        with step("Create request context"):
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query"
            )
        with step("Process error"):
            result = await auth_middleware.process_error(context, Exception("Test error"))
        with step("Verify returns None"):
            assert result is None
