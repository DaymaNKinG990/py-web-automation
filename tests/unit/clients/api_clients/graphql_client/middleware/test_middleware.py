"""
Unit tests for Middleware and MiddlewareChain.
"""

# Python imports
from typing import Callable
from allure import title, description, step
from pytest import mark
from pytest_mock import MockerFixture
from graphql import GraphQLError

# Local imports
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.clients.api_clients.graphql_client.middleware import MiddlewareChain
from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
    _GraphQLResponseContext,
)
from py_web_automation.clients.api_clients.graphql_client.graphql_result import GraphQLResult
from py_web_automation.config import Config

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestMiddlewareChain:
    """Test MiddlewareChain class."""

    @mark.asyncio
    @title("Middleware process_request modifies context")
    @description("Test middleware process_request modifies context.")
    async def test_middleware_process_request_modifies_context(
        self, valid_config: Config, mock_graphql_execute_operation: Callable, mocker: MockerFixture
    ) -> None:
        """Test middleware process_request modifies context."""
        with step("Create custom middleware"):
            class TestMiddleware:
                async def process_request(self, context) -> None:
                    context.headers["X-Test"] = "test-value"

                async def process_response(self, context) -> None:
                    pass

                async def process_error(self, context, error) -> None:
                    return None

            middleware = TestMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(middleware)  # type: ignore[arg-type]

        with step("Create GraphQLClient with middleware"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    await client.query("{ users { id } }")
                with step("Verify middleware modified context"):
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    if call_args:
                        request_context = call_args[0][0]
                        assert "X-Test" in request_context.headers
                        assert request_context.headers["X-Test"] == "test-value"

    @mark.asyncio
    @title("Middleware process_response modifies result")
    @description("Test middleware process_response modifies result.")
    async def test_middleware_process_response_modifies_result(
        self, valid_config: Config, mock_graphql_execute_operation: Callable, mocker: MockerFixture
    ) -> None:
        """Test middleware process_response modifies result."""
        with step("Create custom middleware"):
            class TestMiddleware:
                async def process_request(self, context) -> None:
                    pass

                async def process_response(self, context: _GraphQLResponseContext) -> None:
                    context.result.metadata["processed"] = True

                async def process_error(self, context, error) -> None:
                    return None

            middleware = TestMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(middleware)  # type: ignore[arg-type]

        with step("Create GraphQLClient with middleware"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify middleware modified result"):
                    assert result.success is True
                    assert result.metadata.get("processed") is True

    @mark.asyncio
    @title("Middleware process_error returns result")
    @description("Test middleware process_error returns result if returned.")
    async def test_middleware_process_error_returns_result(
        self, valid_config: Config, mock_graphql_execute_operation: Callable, mocker: MockerFixture
    ) -> None:
        """Test middleware process_error returns result if returned."""
        with step("Create custom middleware"):
            class TestMiddleware:
                async def process_request(self, context) -> None:
                    pass

                async def process_response(self, context) -> None:
                    pass

                async def process_error(self, context, error) -> GraphQLResult | None:
                    return GraphQLResult(
                        operation_name=None,
                        operation_type="query",
                        response_time=0.0,
                        success=False,
                        data=None,
                        errors=[{"message": "Custom error from middleware"}],
                        headers={},
                        metadata={},
                    )

            middleware = TestMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(middleware)  # type: ignore[arg-type]

        with step("Create GraphQLClient with middleware"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation to raise error"):
                    mock_graphql_execute_operation(
                        client, side_effect=GraphQLError("Original error")
                    )
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify middleware error result is used"):
                    assert result.success is False
                    assert len(result.errors) > 0
                    assert result.errors[0]["message"] == "Custom error from middleware"

    @mark.asyncio
    @title("Middleware process_error returns None")
    @description("Test default error result when middleware returns None.")
    async def test_middleware_process_error_returns_none(
        self, valid_config: Config, mock_graphql_execute_operation: Callable, mocker: MockerFixture
    ) -> None:
        """Test default error result when middleware returns None."""
        with step("Create custom middleware"):
            class TestMiddleware:
                async def process_request(self, context) -> None:
                    pass

                async def process_response(self, context) -> None:
                    pass

                async def process_error(self, context, error) -> None:
                    return None

            middleware = TestMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(middleware)  # type: ignore[arg-type]

        with step("Create GraphQLClient with middleware"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation to raise error"):
                    mock_graphql_execute_operation(
                        client, side_effect=GraphQLError("Original error")
                    )
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify default error result is used"):
                    assert result.success is False
                    assert len(result.errors) > 0
                    assert result.errors[0]["message"] == "Original error"

    @mark.asyncio
    @title("Middleware None skips processing")
    @description("Test middleware=None skips processing.")
    async def test_middleware_none_skips_processing(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test middleware=None skips processing."""
        with step("Create GraphQLClient without middleware"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config, middleware=None) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify result is successful"):
                    assert result.success is True
                    # Middleware should not be called, so no modifications

    @mark.asyncio
    @title("MiddlewareChain add returns self")
    @description("Test MiddlewareChain.add() returns self for chaining.")
    async def test_middleware_chain_add_returns_self(self) -> None:
        """Test MiddlewareChain.add() returns self for chaining."""
        with step("Create MiddlewareChain"):
            chain = MiddlewareChain()
        with step("Add middleware and verify chaining"):
            class TestMiddleware:
                async def process_request(self, context) -> None:
                    pass

                async def process_response(self, context) -> None:
                    pass

            middleware1 = TestMiddleware()  # type: ignore
            middleware2 = TestMiddleware()  # type: ignore
            result = chain.add(middleware1).add(middleware2)  # type: ignore[arg-type]
            assert result is chain
            assert len(chain._middleware) == 2

    @mark.asyncio
    @title("MiddlewareChain remove removes middleware")
    @description("Test MiddlewareChain.remove() removes middleware.")
    async def test_middleware_chain_remove(self) -> None:
        """Test MiddlewareChain.remove() removes middleware."""
        with step("Create MiddlewareChain with middleware"):
            chain = MiddlewareChain()

            class TestMiddleware:
                async def process_request(self, context) -> None:
                    pass

                async def process_response(self, context) -> None:
                    pass

            middleware1 = TestMiddleware()  # type: ignore
            middleware2 = TestMiddleware()  # type: ignore
            chain.add(middleware1).add(middleware2)  # type: ignore[arg-type]
        with step("Remove middleware"):
            result = chain.remove(middleware1)  # type: ignore[arg-type]
            assert result is chain
            assert len(chain._middleware) == 1
            assert middleware2 in chain._middleware

    @mark.asyncio
    @title("Middleware base process_error returns None")
    @description("Test base Middleware.process_error() returns None.")
    async def test_middleware_base_process_error(self) -> None:
        """Test base Middleware.process_error() returns None."""
        from py_web_automation.clients.api_clients.graphql_client.middleware.middleware import (
            Middleware,
        )
        from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
            _GraphQLRequestContext,
        )

        with step("Create concrete Middleware implementation"):
            # Middleware is abstract, so we create a concrete implementation for testing
            class TestMiddleware(Middleware):
                async def process_request(self, context) -> None:
                    pass

                async def process_response(self, context) -> None:
                    pass

            middleware = TestMiddleware()
        with step("Create request context"):
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query"
            )
        with step("Process error"):
            result = await middleware.process_error(context, Exception("Test error"))
        with step("Verify returns None"):
            assert result is None
