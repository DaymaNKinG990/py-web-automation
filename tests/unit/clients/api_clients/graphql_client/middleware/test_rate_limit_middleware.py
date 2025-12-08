"""
Unit tests for RateLimitMiddleware.
"""

# Python imports
from typing import Callable
from allure import title, description, step
from pytest import mark

# Local imports
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.clients.api_clients.graphql_client.middleware import (
    RateLimitMiddleware,
    MiddlewareChain,
)
from py_web_automation.clients.api_clients.graphql_client.rate_limit import RateLimiter
from py_web_automation.config import Config

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestRateLimitMiddleware:
    """Test RateLimitMiddleware class."""

    @mark.asyncio
    @title("RateLimitMiddleware acquires permission")
    @description("Test RateLimitMiddleware acquires permission from rate limiter.")
    async def test_rate_limit_middleware_acquires_permission(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test RateLimitMiddleware acquires permission from rate limiter."""
        with step("Setup RateLimitMiddleware"):
            url = "https://api.example.com/graphql"
            rate_limiter = RateLimiter(max_requests=10, window=60)
            rate_limit_middleware = RateLimitMiddleware(rate_limiter)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(rate_limit_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify request was allowed"):
                    assert result.success is True
                    assert len(rate_limiter.requests) == 1

    @mark.asyncio
    @title("RateLimitMiddleware blocks when limit exceeded")
    @description("Test RateLimitMiddleware blocks request when rate limit exceeded.")
    async def test_rate_limit_middleware_blocks_when_exceeded(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test RateLimitMiddleware blocks request when rate limit exceeded."""
        with step("Setup RateLimitMiddleware with low limit"):
            url = "https://api.example.com/graphql"
            rate_limiter = RateLimiter(max_requests=1, window=1)
            rate_limit_middleware = RateLimitMiddleware(rate_limiter)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(rate_limit_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute first query"):
                    result1 = await client.query("{ users { id } }")
                    assert result1.success is True
                with step("Execute second query should block"):
                    # Second request should block until window expires
                    import asyncio

                    task = asyncio.create_task(client.query("{ users { id } }"))
                    await asyncio.sleep(0.1)
                    # Task should still be pending (blocked)
                    assert not task.done()
                    task.cancel()

    @mark.asyncio
    @title("RateLimitMiddleware process_error returns None")
    @description("Test RateLimitMiddleware.process_error() returns None.")
    async def test_rate_limit_middleware_process_error(self) -> None:
        """Test RateLimitMiddleware.process_error() returns None."""
        from py_web_automation.clients.api_clients.graphql_client.middleware.context import (
            _GraphQLRequestContext,
        )

        with step("Create RateLimitMiddleware"):
            rate_limiter = RateLimiter(max_requests=10, window=60)
            rate_limit_middleware = RateLimitMiddleware(rate_limiter)
        with step("Create request context"):
            context = _GraphQLRequestContext(
                query="{ users { id } }", operation_type="query"
            )
        with step("Process error"):
            result = await rate_limit_middleware.process_error(context, Exception("Test error"))
        with step("Verify returns None"):
            assert result is None
