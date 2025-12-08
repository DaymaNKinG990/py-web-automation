"""
Unit tests for MetricsMiddleware.
"""

# Python imports
from typing import Callable
from allure import title, description, step
from pytest import mark
from pytest_mock import MockerFixture

# Local imports
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.clients.api_clients.graphql_client.middleware import (
    MetricsMiddleware,
    MiddlewareChain,
)
from py_web_automation.clients.api_clients.graphql_client.metrics import Metrics
from py_web_automation.config import Config

# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestMetricsMiddleware:
    """Test MetricsMiddleware class."""

    @mark.asyncio
    @title("MetricsMiddleware records successful request")
    @description("Test MetricsMiddleware records successful request metrics.")
    async def test_metrics_middleware_records_success(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test MetricsMiddleware records successful request metrics."""
        with step("Setup MetricsMiddleware"):
            url = "https://api.example.com/graphql"
            metrics = Metrics()
            metrics_middleware = MetricsMiddleware(metrics)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(metrics_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify metrics were recorded"):
                    assert result.success is True
                    assert metrics.request_count == 1
                    assert metrics.success_count == 1
                    assert metrics.error_count == 0

    @mark.asyncio
    @title("MetricsMiddleware records failed request")
    @description("Test MetricsMiddleware records failed request metrics.")
    async def test_metrics_middleware_records_error(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test MetricsMiddleware records failed request metrics."""
        from graphql import GraphQLError

        with step("Setup MetricsMiddleware"):
            url = "https://api.example.com/graphql"
            metrics = Metrics()
            metrics_middleware = MetricsMiddleware(metrics)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(metrics_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation to raise error"):
                    mock_graphql_execute_operation(client, side_effect=GraphQLError("Test error"))
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify error metrics were recorded"):
                    assert result.success is False
                    assert metrics.request_count == 1
                    assert metrics.success_count == 0
                    assert metrics.error_count == 1

    @mark.asyncio
    @title("MetricsMiddleware creates metrics if None")
    @description("Test MetricsMiddleware creates Metrics instance if None provided.")
    async def test_metrics_middleware_creates_metrics(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test MetricsMiddleware creates Metrics instance if None provided."""
        with step("Setup MetricsMiddleware without metrics"):
            url = "https://api.example.com/graphql"
            metrics_middleware = MetricsMiddleware()
            middleware_chain = MiddlewareChain()
            middleware_chain.add(metrics_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify metrics instance was created"):
                    assert result.success is True
                    assert isinstance(metrics_middleware.metrics, Metrics)
                    assert metrics_middleware.metrics.request_count == 1

    @mark.asyncio
    @title("MetricsMiddleware records unknown error")
    @description("Test MetricsMiddleware records unknown_error when success=False but errors=[].")
    async def test_metrics_middleware_records_unknown_error(
        self, valid_config: Config, mocker: MockerFixture
    ) -> None:
        """Test MetricsMiddleware records unknown_error when success=False but errors=[]."""
        from py_web_automation.clients.api_clients.graphql_client.graphql_result import (
            GraphQLResult,
        )

        with step("Setup MetricsMiddleware"):
            url = "https://api.example.com/graphql"
            metrics = Metrics()
            metrics_middleware = MetricsMiddleware(metrics)
            middleware_chain = MiddlewareChain()
            middleware_chain.add(metrics_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock _process_response to return result with success=False and no errors"):
                    # Create a result that has success=False but errors=[]
                    # This simulates a case where operation fails but no GraphQL errors are returned
                    error_result = GraphQLResult(
                        operation_name="TestQuery",
                        operation_type="query",
                        response_time=0.1,
                        success=False,
                        data=None,
                        errors=[],
                    )
                    # Mock _process_response to return our error result
                    # This ensures process_response is called with the error result
                    original_process_response = client._process_response

                    async def mock_process_response(result, request_context):
                        # Replace the result with our error result before processing
                        return await original_process_response(error_result, request_context)

                    mocker.patch.object(
                        client, "_process_response", side_effect=mock_process_response
                    )  # type: ignore[method-assign]
                    # Mock _execute_operation to return data (so _create_success_result is called)
                    mocker.patch.object(
                        client, "_execute_operation", return_value={}
                    )  # type: ignore[method-assign]
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify unknown_error was recorded"):
                    assert result.success is False
                    assert metrics.error_count == 1
                    assert metrics.errors_by_type.get("unknown_error") == 1
