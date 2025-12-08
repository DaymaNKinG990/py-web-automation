"""
Unit tests for RetryMiddleware.
"""

# Python imports
from typing import Callable
from allure import title, description, step
from pytest import mark
from pytest_mock import MockerFixture

# Local imports
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.clients.api_clients.graphql_client.middleware import (
    RetryMiddleware,
    MiddlewareChain,
)
from py_web_automation.clients.api_clients.graphql_client.retry import (
    RetryConfig,
    RetryHandler,
)
from py_web_automation.exceptions import ConnectionError
from py_web_automation.config import Config

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestRetryMiddleware:
    """Test RetryMiddleware class."""

    @mark.asyncio
    @title("RetryMiddleware retries on retryable exception")
    @description("Test RetryMiddleware retries operation on retryable exception.")
    async def test_retry_middleware_retries(
        self, mocker: MockerFixture, valid_config: Config
    ) -> None:
        """Test RetryMiddleware retries operation on retryable exception."""
        with step("Setup RetryMiddleware"):
            url = "https://api.example.com/graphql"
            retry_config = RetryConfig(max_attempts=3, delay=0.01, exceptions=(ConnectionError,))
            retry_handler = RetryHandler(retry_config)
            retry_middleware = RetryMiddleware(retry_handler)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(retry_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Setup retry scenario"):
                    attempt = 0

                    async def mock_execute_with_retry(request_context) -> dict:
                        nonlocal attempt
                        attempt += 1
                        if attempt < 2:
                            raise ConnectionError("Temporary error")
                        return {"users": []}

                    # Mock _execute_operation and _ensure_session properly
                    client._execute_operation = mock_execute_with_retry  # type: ignore[method-assign]
                    client._ensure_session = mocker.AsyncMock()  # type: ignore[method-assign]

                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify retry occurred"):
                    assert result.success is True
                    assert attempt == 2

    @mark.asyncio
    @title("RetryMiddleware does not retry non-retryable exception")
    @description("Test RetryMiddleware does not retry on non-retryable exception.")
    async def test_retry_middleware_no_retry_non_retryable(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test RetryMiddleware does not retry on non-retryable exception."""
        from graphql import GraphQLError

        with step("Setup RetryMiddleware"):
            url = "https://api.example.com/graphql"
            retry_config = RetryConfig(
                max_attempts=3, delay=0.01, exceptions=(ConnectionError,)
            )
            retry_handler = RetryHandler(retry_config)
            retry_middleware = RetryMiddleware(retry_handler)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(retry_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation to raise non-retryable error"):
                    mock_graphql_execute_operation(client, side_effect=GraphQLError("Permanent error"))
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify no retry occurred"):
                    assert result.success is False
                    # GraphQLError is not in retry exceptions, so no retry
