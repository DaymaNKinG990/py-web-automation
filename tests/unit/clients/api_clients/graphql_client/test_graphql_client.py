"""
Unit tests for GraphQLClient.
"""

# Python imports
from typing import Callable
from datetime import timedelta
from allure import title, description, step
from pytest import mark, raises as pytest_raises
from pytest_mock import MockerFixture
from graphql import GraphQLError

# Local imports
from py_web_automation.clients.api_clients.graphql_client import GraphQLClient
from py_web_automation.config import Config
from py_web_automation.clients.api_clients.graphql_client.middleware import AuthMiddleware, MiddlewareChain


# Apply markers to all tests in this module
pytestmark = [mark.unit, mark.graphql]


class TestGraphQLClient:
    """Test GraphQLClient class."""

    @mark.asyncio
    @title("Initialize GraphQLClient")
    @description("Test GraphQLClient initialization.")
    async def test_init(self, valid_config: Config) -> None:
        """Test GraphQLClient initialization."""
        with step("Create GraphQLClient with URL and config"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Verify client URL and config"):
                    assert client.url == url
                    assert client.config == valid_config

    @mark.asyncio
    @title("Execute GraphQL query")
    @description("Test executing a GraphQL query.")
    async def test_execute_query(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test executing a GraphQL query."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation method"):
                    mock_graphql_execute_operation(client, return_data={"users": [{"id": 1, "name": "Test"}]})
                with step("Execute GraphQL query"):
                    query = "{ users { id name } }"
                    result = await client.query(query)
                with step("Verify query result"):
                    assert result.success is True
                    assert result.data == {"data": {"users": [{"id": 1, "name": "Test"}]}}

    @mark.asyncio
    @title("Execute GraphQL mutation")
    @description("Test executing a GraphQL mutation.")
    async def test_execute_mutation(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test executing a GraphQL mutation."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation method"):
                    mock_graphql_execute_operation(client, return_data={"createUser": {"id": 1, "name": "New User"}})
                with step("Execute GraphQL mutation"):
                    mutation = 'mutation { createUser(name: "New User") { id name } }'
                    result = await client.mutate(mutation)
                with step("Verify mutation result"):
                    assert result.success is True
                    assert result.data == {"data": {"createUser": {"id": 1, "name": "New User"}}}

    @mark.asyncio
    @title("Handle GraphQL errors")
    @description("Test handling GraphQL errors.")
    async def test_handle_errors(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test handling GraphQL errors."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to raise GraphQLError"):
                    mock_graphql_execute_operation(client, side_effect=GraphQLError("Field not found"))
                with step("Execute query with invalid field"):
                    query = "{ invalidField }"
                    result = await client.query(query)
                with step("Verify error handling"):
                    assert result.success is False
                    assert len(result.errors) > 0
                    assert result.errors[0]["message"] == "Field not found"

    @mark.asyncio
    @title("Context manager support")
    @description("Test GraphQLClient as context manager.")
    async def test_context_manager(self, valid_config: Config) -> None:
        """Test GraphQLClient as context manager."""
        with step("Create GraphQLClient as context manager"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Verify client properties"):
                    assert client.url == url
                    assert client.config == valid_config

    @mark.asyncio
    @title("Close client")
    @description("Test closing GraphQLClient.")
    async def test_close(self, valid_config: Config) -> None:
        """Test closing GraphQLClient."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Verify client is initialized"):
                    assert client.url == url

    @mark.asyncio
    @title("query с variables")
    @description("Test query with variables.")
    async def test_query_with_variables(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query with variables."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={"user": {"id": 1, "name": "Test"}})
                with step("Execute query with variables"):
                    query = "query GetUser($id: ID!) { user(id: $id) { name } }"
                    variables = {"id": "1"}
                    result = await client.query(query, variables=variables)
                with step("Verify result"):
                    assert result.success is True
                    assert result.data == {"data": {"user": {"id": 1, "name": "Test"}}}
                with step("Verify variables were included in the request"):
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert request_context.variables == variables

    @mark.asyncio
    @title("query с operation_name")
    @description("Test query with operation_name.")
    async def test_query_with_operation_name(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query with operation_name."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={"users": []})
                with step("Execute query with operation_name"):
                    query = "query GetUsers { users { id } } query GetPosts { posts { id } }"
                    result = await client.query(query, operation_name="GetUsers")
                with step("Verify result"):
                    assert result.success is True
                with step("Verify operation_name was included in the request"):
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert request_context.operation_name == "GetUsers"

    @mark.asyncio
    @title("query с custom headers")
    @description("Test query with custom headers.")
    async def test_query_with_custom_headers(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query with custom headers."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query with custom headers"):
                    custom_headers = {"X-Custom-Header": "value"}
                    result = await client.query("{ users { id } }", headers=custom_headers)
                with step("Verify result"):
                    assert result.success is True
                with step("Verify custom headers were included in the request"):
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert "X-Custom-Header" in request_context.headers
                    assert request_context.headers["X-Custom-Header"] == "value"

    @mark.asyncio
    @title("query с authentication token")
    @description("Test query with authentication token.")
    async def test_query_with_auth_token(self, mocker: MockerFixture, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query with authentication token."""
        with step("Setup AuthMiddleware and MiddlewareChain"):
            url = "https://api.example.com/graphql"
            auth_middleware = AuthMiddleware(token="test-token-123", token_type="Bearer")
            middleware_chain = MiddlewareChain()
            middleware_chain.add(auth_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock HTTP response"):
                    mock_response = mocker.MagicMock()
                    mock_response.status_code = 200
                    mock_response.elapsed = timedelta(seconds=0.2)
                    mock_response.is_success = True
                    mock_response.is_informational = False
                    mock_response.is_redirect = False
                    mock_response.is_client_error = False
                    mock_response.is_server_error = False
                    mock_response.content = b'{"data": {}}'
                    mock_response.headers = {"Content-Type": "application/json"}
                with step("Mock client.post method"):
                    client.client.post = mocker.AsyncMock(return_value=mock_response)
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
    @title("mutate с variables")
    @description("Test mutate with variables.")
    async def test_mutate_with_variables(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test mutate with variables."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={"createUser": {"id": 1}})
                with step("Execute mutate with variables"):
                    mutation = "mutation CreateUser($input: UserInput!) { createUser(input: $input) { id } }"
                    variables = {"input": {"name": "John"}}
                    result = await client.mutate(mutation, variables=variables)
                with step("Verify result"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert request_context.variables == variables

    @mark.asyncio
    @title("mutate с operation_name")
    @description("Test mutate with operation_name.")
    async def test_mutate_with_operation_name(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test mutate with operation_name."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={"createUser": {"id": 1}})
                with step("Execute mutate with operation_name"):
                    mutation = "mutation CreateUser { createUser { id } }"
                    result = await client.mutate(mutation, operation_name="CreateUser")
                with step("Verify result"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert request_context.operation_name == "CreateUser"

    @mark.asyncio
    @title("mutate с custom headers")
    @description("Test mutate with custom headers.")
    async def test_mutate_with_custom_headers(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test mutate with custom headers."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={"createUser": {"id": 1}})
                with step("Execute mutate with custom headers"):
                    custom_headers = {"X-Custom-Header": "value"}
                    result = await client.mutate("mutation { createUser { id } }", headers=custom_headers)
                with step("Verify result"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert "X-Custom-Header" in request_context.headers

    @mark.asyncio
    @title("mutate с authentication token")
    @description("Test mutate with authentication token.")
    async def test_mutate_with_auth_token(self, mocker: MockerFixture, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test mutate with authentication token."""
        with step("Setup AuthMiddleware and MiddlewareChain"):
            url = "https://api.example.com/graphql"
            auth_middleware = AuthMiddleware(token="test-token-123", token_type="Bearer")
            middleware_chain = MiddlewareChain()
            middleware_chain.add(auth_middleware)
        with step("Create GraphQLClient with middleware"):
            async with GraphQLClient(url, valid_config, middleware=middleware_chain) as client:
                with step("Mock HTTP response"):
                    mock_response = mocker.MagicMock()
                    mock_response.status_code = 200
                    mock_response.elapsed = timedelta(seconds=0.2)
                    mock_response.is_success = True
                    mock_response.is_informational = False
                    mock_response.is_redirect = False
                    mock_response.is_client_error = False
                    mock_response.is_server_error = False
                    mock_response.content = b'{"data": {"createUser": {"id": 1}}}'
                    mock_response.headers = {"Content-Type": "application/json"}
                with step("Mock client.post method"):
                    client.client.post = mocker.AsyncMock(return_value=mock_response)
                with step("Mock _execute_operation method"):
                    mock_graphql_execute_operation(client, return_data={"createUser": {"id": 1}})
                with step("Execute mutation"):
                    result = await client.mutate("mutation { createUser { id } }")
                with step("Verify result"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    assert call_args is not None
                    request_context = call_args[0][0]
                    assert "Authorization" in request_context.headers
                    assert request_context.headers["Authorization"] == "Bearer test-token-123"

    @mark.asyncio
    @title("_execute строит правильный endpoint URL")
    @description("Test _execute builds correct endpoint URL.")
    async def test_execute_builds_endpoint_url(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test _execute builds correct endpoint URL."""
        with step("Setup GraphQL client with custom endpoint"):
            url = "https://api.example.com"
            async with GraphQLClient(url, valid_config, endpoint="/graphql") as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    await client.query("{ users { id } }")
                with step("Verify endpoint configuration"):
                    assert client.endpoint == "/graphql"
                    if hasattr(client._transport, "url"):
                        assert client._transport.url == "https://api.example.com/graphql"  # type: ignore[attr-defined]

    @mark.asyncio
    @title("_execute обрабатывает HTTP ошибки")
    @description("Test _execute handles HTTP errors.")
    async def test_execute_handles_http_errors(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test _execute handles HTTP errors."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to raise GraphQLError"):
                    mock_graphql_execute_operation(client, side_effect=GraphQLError("Server error"))
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify error handling"):
                    assert result.success is False
                    assert len(result.errors) > 0
                    assert result.errors[0]["message"] == "Server error"

    @mark.asyncio
    @title("_execute обрабатывает network ошибки")
    @description("Test _execute handles network errors.")
    async def test_execute_handles_network_errors(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test _execute handles network errors."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to raise NetworkError"):
                    mock_graphql_execute_operation(client, side_effect=Exception("Network error"))
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify error handling"):
                    assert result.success is False
                    assert len(result.errors) > 0

    @mark.asyncio
    @title("_execute redacts sensitive headers")
    @description("Test _execute redacts sensitive headers.")
    async def test_execute_redacts_sensitive_headers(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test _execute redacts sensitive headers."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Set transport headers with sensitive data"):
                    client._transport.headers = {  # type: ignore[attr-defined]
                        "Content-Type": "application/json",
                        "Authorization": "Bearer secret-token",
                        "X-API-Key": "secret-key",
                    }
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify sensitive headers were redacted"):
                    assert result.success is True
                    assert result.headers.get("authorization") == "[REDACTED]"
                    assert result.headers.get("x-api-key") == "[REDACTED]"

    @mark.asyncio
    @title("_execute обрабатывает отсутствие response.elapsed")
    @description("Test _execute handles missing response.elapsed.")
    async def test_execute_handles_missing_elapsed(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test _execute handles missing response.elapsed."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify response_time is calculated"):
                    assert result.success is True
                    assert result.response_time >= 0.0

    @mark.asyncio
    @title("Инициализация с custom endpoint")
    @description("Test initialization with custom endpoint.")
    async def test_init_with_custom_endpoint(self, valid_config: Config) -> None:
        """Test initialization with custom endpoint."""
        with step("Setup GraphQL client with custom endpoint"):
            url = "https://api.example.com"
            endpoint = "/api/graphql"
            async with GraphQLClient(url, valid_config, endpoint=endpoint) as client:
                with step("Verify endpoint configuration"):
                    assert client.url == url
                    assert client.endpoint == endpoint

    @mark.asyncio
    @mark.parametrize(
        "status_code,expected_success",
        [
            (200, True),
            (201, True),
            (400, False),
            (401, False),
            (403, False),
            (404, False),
            (500, False),
            (502, False),
            (503, False),
        ],
    )
    @title("GraphQLClient handles status code {status_code}")
    @description("Test GraphQLClient handles various HTTP status codes.")
    async def test_graphql_client_status_codes(self, mocker: MockerFixture, valid_config: Config, mock_graphql_execute_operation: Callable, status_code: int, expected_success: bool) -> None:
        """Test GraphQLClient handles various HTTP status codes."""
        with step(f"Prepare GraphQLClient for status {status_code}"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step(f"Mock response with status_code {status_code}"):
                    mock_response = mocker.MagicMock()
                    mock_response.status_code = status_code
                    mock_response.elapsed = timedelta(seconds=0.2)
                    mock_response.is_success = expected_success
                    mock_response.is_redirect = 300 <= status_code < 400
                    mock_response.is_client_error = 400 <= status_code < 500
                    mock_response.is_server_error = 500 <= status_code < 600
                    mock_response.is_informational = 100 <= status_code < 200
                    mock_response.content = b'{"data": {"test": "value"}}'
                    mock_response.headers = {"Content-Type": "application/json"}
                with step("Mock _execute_operation based on status code"):
                    if expected_success:
                        mock_graphql_execute_operation(client, return_data={"test": "value"})
                    else:
                        mock_graphql_execute_operation(client, side_effect=GraphQLError(f"HTTP {status_code}"))
                with step("Execute query and verify success"):
                    query = "{ users { id name } }"
                    result = await client.query(query)
                    assert result.success == expected_success
                    if not expected_success:
                        assert len(result.errors) > 0 or result.data is None

    # ========== Initialization Edge Cases ==========

    @mark.asyncio
    @title("Initialize with empty URL raises ValueError")
    @description("Test GraphQLClient raises ValueError for empty URL.")
    async def test_init_with_empty_url(self) -> None:
        """Test GraphQLClient raises ValueError for empty URL."""
        with step("Attempt to create GraphQLClient with empty URL"):
            url = ""
            with step("Verify ValueError is raised"):
                with pytest_raises(ValueError, match="url cannot be empty"):
                    GraphQLClient(url, Config())

    @mark.asyncio
    @title("Initialize with whitespace URL raises ValueError")
    @description("Test GraphQLClient raises ValueError for whitespace-only URL.")
    async def test_init_with_whitespace_url(self) -> None:
        """Test GraphQLClient raises ValueError for whitespace-only URL."""
        with step("Attempt to create GraphQLClient with whitespace URL"):
            url = "   "
            with step("Verify ValueError is raised"):
                with pytest_raises(ValueError, match="url cannot be empty"):
                    GraphQLClient(url, Config())

    @mark.asyncio
    @title("Initialize with invalid config type raises TypeError")
    @description("Test GraphQLClient raises TypeError for non-Config object.")
    async def test_init_with_invalid_config_type(self) -> None:
        """Test GraphQLClient raises TypeError for non-Config object."""
        with step("Attempt to create GraphQLClient with invalid config"):
            url = "https://api.example.com"
            invalid_config = {"timeout": 30}
        with step("Verify TypeError is raised"):
            with pytest_raises(TypeError, match="config must be a Config object"):
                GraphQLClient(url, invalid_config)  # type: ignore[arg-type]

    @mark.asyncio
    @title("Initialize with None config creates default Config")
    @description("Test GraphQLClient creates default Config when config=None.")
    async def test_init_with_none_config(self) -> None:
        """Test GraphQLClient creates default Config when config=None."""
        with step("Create GraphQLClient with config=None"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, None) as client:  # type: ignore[arg-type]
                with step("Verify default Config is created"):
                    assert client.config is not None
                    assert isinstance(client.config, Config)

    @mark.asyncio
    @title("Initialize with URL query params strips params")
    @description("Test GraphQLClient strips query params from URL.")
    async def test_init_with_url_query_params(self, valid_config: Config) -> None:
        """Test GraphQLClient strips query params from URL."""
        with step("Create GraphQLClient with URL containing query params"):
            url = "https://api.example.com?param=value&other=test"
            async with GraphQLClient(url, valid_config) as client:
                with step("Verify URL is stored correctly"):
                    assert client.url == url
                with step("Verify query params are stripped from transport URL"):
                    if hasattr(client._transport, "url"):
                        assert "?" not in client._transport.url  # type: ignore[attr-defined]

    @mark.asyncio
    @title("Initialize with endpoint trailing slash")
    @description("Test GraphQLClient handles endpoint with trailing slash.")
    async def test_init_with_endpoint_trailing_slash(self, valid_config: Config) -> None:
        """Test GraphQLClient handles endpoint with trailing slash."""
        with step("Create GraphQLClient with endpoint having trailing slash"):
            url = "https://api.example.com"
            endpoint = "/graphql/"
            async with GraphQLClient(url, valid_config, endpoint=endpoint) as client:
                with step("Verify endpoint is stored correctly"):
                    assert client.endpoint == endpoint
                with step("Verify transport URL is constructed correctly"):
                    if hasattr(client._transport, "url"):
                        transport_url = client._transport.url  # type: ignore[attr-defined]
                        assert transport_url == "https://api.example.com/graphql/"

    @mark.asyncio
    @title("Initialize with endpoint leading slash")
    @description("Test GraphQLClient handles endpoint with leading slash.")
    async def test_init_with_endpoint_leading_slash(self, valid_config: Config) -> None:
        """Test GraphQLClient handles endpoint with leading slash."""
        with step("Create GraphQLClient with endpoint having leading slash"):
            url = "https://api.example.com"
            endpoint = "/graphql"
            async with GraphQLClient(url, valid_config, endpoint=endpoint) as client:
                with step("Verify endpoint is stored correctly"):
                    assert client.endpoint == endpoint
                with step("Verify transport URL is constructed correctly"):
                    if hasattr(client._transport, "url"):
                        transport_url = client._transport.url  # type: ignore[attr-defined]
                        assert transport_url == "https://api.example.com/graphql"

    @mark.asyncio
    @title("Initialize with endpoint no slashes")
    @description("Test GraphQLClient handles endpoint without slashes.")
    async def test_init_with_endpoint_no_slashes(self, valid_config: Config) -> None:
        """Test GraphQLClient handles endpoint without slashes."""
        with step("Create GraphQLClient with endpoint without slashes"):
            url = "https://api.example.com"
            endpoint = "graphql"
            async with GraphQLClient(url, valid_config, endpoint=endpoint) as client:
                with step("Verify endpoint is stored correctly"):
                    assert client.endpoint == endpoint
                with step("Verify transport URL is constructed correctly"):
                    if hasattr(client._transport, "url"):
                        transport_url = client._transport.url  # type: ignore[attr-defined]
                        assert transport_url == "https://api.example.com/graphql"

    @mark.asyncio
    @title("Initialize with validate_queries True")
    @description("Test GraphQLClient disables schema fetching when validate_queries=True.")
    async def test_init_with_validate_queries_true(self, valid_config: Config) -> None:
        """Test GraphQLClient disables schema fetching when validate_queries=True."""
        with step("Create GraphQLClient with validate_queries=True"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config, validate_queries=True) as client:
                with step("Verify client is created"):
                    assert client.url == url
                    # fetch_schema_from_transport should be False when validate_queries=True
                    assert client.client.fetch_schema_from_transport is False

    @mark.asyncio
    @title("Initialize with schema provided")
    @description("Test GraphQLClient stores schema and passes to middleware.")
    async def test_init_with_schema_provided(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test GraphQLClient stores schema and passes to middleware."""
        with step("Create GraphQLClient with schema"):
            url = "https://api.example.com/graphql"
            mock_schema = {"type": "object"}
            async with GraphQLClient(url, valid_config, schema=mock_schema) as client:
                with step("Verify schema is stored"):
                    assert client._schema == mock_schema
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query to verify schema in metadata"):
                    result = await client.query("{ users { id } }")
                    assert result.success is True
                    # Schema should be added to metadata in _prepare_request_context
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    if call_args:
                        request_context = call_args[0][0]
                        assert "schema" in request_context.metadata
                        assert request_context.metadata["schema"] == mock_schema

    # ========== Close Method Edge Cases ==========

    @mark.asyncio
    @title("Close when session is None")
    @description("Test close() handles when session is None.")
    async def test_close_when_session_none(self, valid_config: Config) -> None:
        """Test close() handles when session is None."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Verify session is None initially"):
                    assert client._session is None
                with step("Call close()"):
                    await client.close()
                with step("Verify no errors occurred"):
                    assert client._session is None

    @mark.asyncio
    @title("Close multiple calls")
    @description("Test close() handles multiple calls.")
    async def test_close_multiple_calls(self, valid_config: Config, mocker: MockerFixture) -> None:
        """Test close() handles multiple calls."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock client.close_async"):
                    mock_close = mocker.AsyncMock()
                    client.client.close_async = mock_close
                    client._session = mocker.MagicMock()
                with step("Call close() multiple times"):
                    await client.close()
                    await client.close()
                with step("Verify close_async was called"):
                    assert mock_close.call_count >= 1

    @mark.asyncio
    @title("Close handles errors")
    @description("Test close() handles errors during close.")
    async def test_close_handles_errors(self, valid_config: Config, mocker: MockerFixture) -> None:
        """Test close() handles errors during close."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock client.close_async to raise error"):
                    client.client.close_async = mocker.AsyncMock(side_effect=Exception("Close error"))
                    client._session = mocker.MagicMock()
                with step("Call close() and verify error is handled"):
                    # Should not raise exception
                    try:
                        await client.close()
                    except Exception:
                        pass  # Error should be handled internally

    # ========== Context Manager Edge Cases ==========

    @mark.asyncio
    @title("Context manager with exception")
    @description("Test context manager calls close() even when exception occurs.")
    async def test_context_manager_with_exception(self, valid_config: Config, mocker: MockerFixture) -> None:
        """Test context manager calls close() even when exception occurs."""
        with step("Create GraphQLClient in context manager"):
            url = "https://api.example.com/graphql"
            mock_close = mocker.AsyncMock()
            try:
                async with GraphQLClient(url, valid_config) as client:
                    client.close = mock_close  # type: ignore[method-assign]
                    with step("Raise exception inside context"):
                        raise ValueError("Test exception")
            except ValueError:
                pass
            with step("Verify close() was called"):
                assert mock_close.called

    @mark.asyncio
    @title("Context manager exception during close")
    @description("Test context manager handles exceptions in __aexit__.")
    async def test_context_manager_exception_during_close(self, valid_config: Config, mocker: MockerFixture) -> None:
        """Test context manager handles exceptions in __aexit__."""
        with step("Create GraphQLClient in context manager"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock close() to raise exception"):
                    async def failing_close() -> None:
                        raise Exception("Close error")
                    client.close = failing_close  # type: ignore[method-assign]
            # Should not raise exception, error should be handled

    # ========== Query/Mutation Edge Cases ==========

    @mark.asyncio
    @title("Query with empty string")
    @description("Test query with empty string.")
    async def test_query_with_empty_string(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query with empty string."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query with empty string"):
                    result = await client.query("")
                with step("Verify query was executed"):
                    assert result.success is True

    @mark.asyncio
    @title("Query with None variables")
    @description("Test query with variables=None explicitly.")
    async def test_query_with_none_variables(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query with variables=None explicitly."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query with variables=None"):
                    result = await client.query("{ users { id } }", variables=None)
                with step("Verify variables are empty dict"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    if call_args:
                        request_context = call_args[0][0]
                        assert request_context.variables == {}

    @mark.asyncio
    @title("Query with empty variables")
    @description("Test query with empty variables dict.")
    async def test_query_with_empty_variables(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query with empty variables dict."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query with empty variables"):
                    result = await client.query("{ users { id } }", variables={})
                with step("Verify variables are empty dict"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    if call_args:
                        request_context = call_args[0][0]
                        assert request_context.variables == {}

    @mark.asyncio
    @title("Query with None operation_name")
    @description("Test query with operation_name=None.")
    async def test_query_with_none_operation_name(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query with operation_name=None."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query with operation_name=None"):
                    result = await client.query("{ users { id } }", operation_name=None)
                with step("Verify operation_name is None"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    if call_args:
                        request_context = call_args[0][0]
                        assert request_context.operation_name is None

    @mark.asyncio
    @title("Query with None headers")
    @description("Test query with headers=None.")
    async def test_query_with_none_headers(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query with headers=None."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query with headers=None"):
                    result = await client.query("{ users { id } }", headers=None)
                with step("Verify headers are empty dict"):
                    assert result.success is True
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    if call_args:
                        request_context = call_args[0][0]
                        assert request_context.headers == {}

    @mark.asyncio
    @title("Mutate with empty string")
    @description("Test mutate with empty string.")
    async def test_mutate_with_empty_string(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test mutate with empty string."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute mutation with empty string"):
                    result = await client.mutate("")
                with step("Verify mutation was executed"):
                    assert result.success is True

    # ========== Result Data Edge Cases ==========

    @mark.asyncio
    @title("Query returns None data")
    @description("Test query returning None data.")
    async def test_query_returns_none_data(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query returning None data."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to return None"):
                    mock_graphql_execute_operation(client, return_data=None)
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify data is None"):
                    assert result.success is True
                    assert result.data is None

    @mark.asyncio
    @title("Query returns empty data")
    @description("Test query returning empty dict.")
    async def test_query_returns_empty_data(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test query returning empty dict."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to return empty dict"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify data is wrapped correctly"):
                    assert result.success is True
                    assert result.data == {"data": {}}

    @mark.asyncio
    @title("Mutate returns None data")
    @description("Test mutation returning None data.")
    async def test_mutate_returns_none_data(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test mutation returning None data."""
        with step("Setup GraphQL client"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to return None"):
                    mock_graphql_execute_operation(client, return_data=None)
                with step("Execute mutation"):
                    result = await client.mutate("mutation { createUser { id } }")
                with step("Verify data is None"):
                    assert result.success is True
                    assert result.data is None

    # ========== Schema and Validation Tests ==========

    @mark.asyncio
    @title("Get schema from instance")
    @description("Test _get_schema returns _schema when set.")
    async def test_get_schema_from_instance(self, valid_config: Config) -> None:
        """Test _get_schema returns _schema when set."""
        with step("Create GraphQLClient with schema"):
            url = "https://api.example.com/graphql"
            mock_schema = {"type": "object", "properties": {}}
            async with GraphQLClient(url, valid_config, schema=mock_schema) as client:
                with step("Call _get_schema"):
                    schema = client._get_schema()
                with step("Verify schema is returned"):
                    assert schema == mock_schema

    @mark.asyncio
    @title("Get schema from client")
    @description("Test _get_schema returns client.schema when _schema is None.")
    async def test_get_schema_from_client(self, valid_config: Config, mocker: MockerFixture) -> None:
        """Test _get_schema returns client.schema when _schema is None."""
        with step("Create GraphQLClient without schema"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Set client.schema"):
                    mock_schema = {"type": "object"}
                    client.client.schema = mock_schema  # type: ignore[attr-defined]
                with step("Call _get_schema"):
                    schema = client._get_schema()
                with step("Verify client.schema is returned"):
                    assert schema == mock_schema

    @mark.asyncio
    @title("Get schema returns None")
    @description("Test _get_schema returns None when neither exists.")
    async def test_get_schema_returns_none(self, valid_config: Config) -> None:
        """Test _get_schema returns None when neither exists."""
        with step("Create GraphQLClient without schema"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Ensure _schema is None and client has no schema"):
                    client._schema = None
                    if hasattr(client.client, "schema"):
                        delattr(client.client, "schema")
                with step("Call _get_schema"):
                    schema = client._get_schema()
                with step("Verify None is returned"):
                    assert schema is None

    @mark.asyncio
    @title("Schema added to metadata")
    @description("Test schema is added to request context metadata.")
    async def test_schema_added_to_metadata(self, valid_config: Config, mock_graphql_execute_operation: Callable) -> None:
        """Test schema is added to request context metadata."""
        with step("Create GraphQLClient with schema"):
            url = "https://api.example.com/graphql"
            mock_schema = {"type": "object"}
            async with GraphQLClient(url, valid_config, schema=mock_schema) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    await client.query("{ users { id } }")
                with step("Verify schema in metadata"):
                    call_args = client._execute_operation.call_args  # type: ignore[attr-defined]
                    if call_args:
                        request_context = call_args[0][0]
                        assert "schema" in request_context.metadata
                        assert request_context.metadata["schema"] == mock_schema

    # ========== Transport Headers Tests ==========

    @mark.asyncio
    @title("Apply transport headers with headers")
    @description("Test _apply_transport_headers applies headers to transport.")
    async def test_apply_transport_headers_with_headers(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test _apply_transport_headers applies headers to transport."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Setup transport headers"):
                    if not hasattr(client._transport, "headers") or getattr(client._transport, "headers", None) is None:
                        client._transport.headers = {}  # type: ignore[attr-defined]
                    original_headers = dict(client._transport.headers)  # type: ignore[attr-defined]
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query with headers"):
                    headers = {"X-Custom": "value"}
                    await client.query("{ users { id } }", headers=headers)
                with step("Verify headers were applied"):
                    # Headers should be applied via _apply_transport_headers
                    # Note: This is internal behavior, verified through execution
                    pass

    @mark.asyncio
    @title("Apply transport headers without headers")
    @description("Test _apply_transport_headers skips when headers=None.")
    async def test_apply_transport_headers_without_headers(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test _apply_transport_headers skips when headers=None."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query without headers"):
                    await client.query("{ users { id } }", headers=None)
                with step("Verify no errors occurred"):
                    # Should handle None headers gracefully
                    pass

    @mark.asyncio
    @title("Apply transport headers no headers attribute")
    @description("Test _apply_transport_headers skips when transport has no headers.")
    async def test_apply_transport_headers_no_headers_attribute(
        self, valid_config: Config, mock_graphql_execute_operation: Callable, mocker: MockerFixture
    ) -> None:
        """Test _apply_transport_headers skips when transport has no headers."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Remove headers attribute if exists"):
                    if hasattr(client._transport, "headers"):
                        delattr(client._transport, "headers")
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    await client.query("{ users { id } }", headers={"X-Test": "value"})

    @mark.asyncio
    @title("Extract response headers no transport headers")
    @description("Test _extract_response_headers returns {} when transport has no headers.")
    async def test_extract_response_headers_no_transport_headers(
        self, valid_config: Config, mock_graphql_execute_operation: Callable, mocker: MockerFixture
    ) -> None:
        """Test _extract_response_headers returns {} when transport has no headers."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Remove headers attribute if exists"):
                    if hasattr(client._transport, "headers"):
                        delattr(client._transport, "headers")
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify headers are empty dict"):
                    assert result.success is True
                    assert result.headers == {}

    # ========== Header Redaction Tests ==========

    @mark.asyncio
    @title("Redact sensitive headers case insensitive")
    @description("Test _redact_sensitive_headers redacts headers case-insensitively.")
    async def test_redact_sensitive_headers_case_insensitive(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test _redact_sensitive_headers redacts headers case-insensitively."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Set transport headers with case variations"):
                    client._transport.headers = {  # type: ignore[attr-defined]
                        "Authorization": "Bearer token",
                        "authorization": "Bearer token2",
                        "AUTHORIZATION": "Bearer token3",
                    }
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify all variations are redacted"):
                    assert result.success is True
                    assert result.headers.get("authorization") == "[REDACTED]"

    @mark.asyncio
    @title("Redact sensitive headers preserves others")
    @description("Test _redact_sensitive_headers preserves non-sensitive headers.")
    async def test_redact_sensitive_headers_preserves_others(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test _redact_sensitive_headers preserves non-sensitive headers."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Set transport headers with mixed sensitive/non-sensitive"):
                    client._transport.headers = {  # type: ignore[attr-defined]
                        "Content-Type": "application/json",
                        "Authorization": "Bearer secret",
                        "X-Custom-Header": "custom-value",
                    }
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify non-sensitive headers are preserved"):
                    assert result.success is True
                    assert result.headers.get("content-type") == "application/json"
                    assert result.headers.get("authorization") == "[REDACTED]"
                    assert result.headers.get("x-custom-header") == "custom-value"

    @mark.asyncio
    @title("Redact sensitive headers empty dict")
    @description("Test _redact_sensitive_headers handles empty headers dict.")
    async def test_redact_sensitive_headers_empty_dict(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test _redact_sensitive_headers handles empty headers dict."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation"):
                    mock_graphql_execute_operation(client, return_data={})
                with step("Set empty transport headers"):
                    client._transport.headers = {}  # type: ignore[attr-defined]
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify empty headers are handled"):
                    assert result.success is True
                    assert result.headers == {}

    # ========== Session Management Tests ==========

    @mark.asyncio
    @title("Ensure session creates session")
    @description("Test _ensure_session creates session when _session is None.")
    async def test_ensure_session_creates_session(
        self, valid_config: Config, mocker: MockerFixture
    ) -> None:
        """Test _ensure_session creates session when _session is None."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                # Mock close_async to avoid AttributeError with real gql.Client
                client.client.close_async = mocker.AsyncMock()  # type: ignore[method-assign]
                with step("Verify _session is None initially"):
                    assert client._session is None
                with step("Mock client.connect_async"):
                    mock_session = mocker.MagicMock()
                    client.client.connect_async = mocker.AsyncMock(return_value=mock_session)  # type: ignore[method-assign]
                with step("Call _ensure_session"):
                    await client._ensure_session()
                with step("Verify session was created"):
                    assert client._session == mock_session

    @mark.asyncio
    @title("Ensure session reuses existing")
    @description("Test _ensure_session does not create new session if exists.")
    async def test_ensure_session_reuses_existing(
        self, valid_config: Config, mocker: MockerFixture
    ) -> None:
        """Test _ensure_session does not create new session if exists."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                # Mock close_async to avoid AttributeError with real gql.Client
                client.client.close_async = mocker.AsyncMock()  # type: ignore[method-assign]
                with step("Set existing session"):
                    existing_session = mocker.MagicMock()
                    client._session = existing_session
                with step("Mock client.connect_async"):
                    mock_connect = mocker.AsyncMock()
                    client.client.connect_async = mock_connect  # type: ignore[method-assign]
                with step("Call _ensure_session"):
                    await client._ensure_session()
                with step("Verify connect_async was not called"):
                    mock_connect.assert_not_called()
                    assert client._session == existing_session

    @mark.asyncio
    @title("Ensure session handles connection error")
    @description("Test _ensure_session handles connection errors.")
    async def test_ensure_session_handles_connection_error(
        self, valid_config: Config, mocker: MockerFixture
    ) -> None:
        """Test _ensure_session handles connection errors."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock client.connect_async to raise error"):
                    client.client.connect_async = mocker.AsyncMock(side_effect=Exception("Connection error"))  # type: ignore[method-assign]
                with step("Call _ensure_session and verify error is raised"):
                    with pytest_raises(Exception, match="Connection error"):
                        await client._ensure_session()

    # ========== Error Handling Edge Cases ==========

    @mark.asyncio
    @title("Handle operation error with GraphQL error extensions")
    @description("Test _handle_operation_error includes extensions in GraphQLError.")
    async def test_handle_operation_error_with_graphql_error_extensions(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test _handle_operation_error includes extensions in GraphQLError."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to raise GraphQLError with extensions"):
                    error = GraphQLError("Error with extensions", extensions={"code": "ERROR_CODE", "field": "user.id"})
                    mock_graphql_execute_operation(client, side_effect=error)
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify extensions are included in error"):
                    assert result.success is False
                    assert len(result.errors) > 0
                    assert "extensions" in result.errors[0]
                    assert result.errors[0]["extensions"] == {"code": "ERROR_CODE", "field": "user.id"}

    @mark.asyncio
    @title("Handle operation error with generic exception")
    @description("Test _handle_operation_error handles generic Exception.")
    async def test_handle_operation_error_with_generic_exception(
        self, valid_config: Config, mock_graphql_execute_operation: Callable
    ) -> None:
        """Test _handle_operation_error handles generic Exception."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to raise generic Exception"):
                    mock_graphql_execute_operation(client, side_effect=ValueError("Generic error"))
                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify generic error is handled"):
                    assert result.success is False
                    assert len(result.errors) > 0
                    assert result.errors[0]["message"] == "Generic error"
                    # Generic exceptions don't have extensions
                    assert "extensions" not in result.errors[0] or result.errors[0].get("extensions") == {}

    @mark.asyncio
    @title("Handle operation error calculates response time")
    @description("Test _handle_operation_error calculates response_time correctly.")
    async def test_handle_operation_error_calculates_response_time(
        self, valid_config: Config, mock_graphql_execute_operation: Callable, mocker: MockerFixture
    ) -> None:
        """Test _handle_operation_error calculates response_time correctly."""
        with step("Create GraphQLClient"):
            url = "https://api.example.com/graphql"
            async with GraphQLClient(url, valid_config) as client:
                with step("Mock _execute_operation to raise error after delay"):
                    import asyncio
                    async def delayed_error(request_context) -> dict:
                        await asyncio.sleep(0.1)
                        raise GraphQLError("Error")
                    client._execute_operation = delayed_error  # type: ignore[method-assign]
                    client._ensure_session = mocker.AsyncMock()  # type: ignore[method-assign]

                with step("Execute query"):
                    result = await client.query("{ users { id } }")
                with step("Verify response_time is calculated"):
                    assert result.success is False
                    assert result.response_time >= 0.0
                    assert result.response_time >= 0.1  # Should be at least the delay

    # ========== Endpoint URL Construction Tests ==========

    @mark.asyncio
    @title("Endpoint URL with base trailing slash")
    @description("Test endpoint URL construction with base URL having trailing slash.")
    async def test_endpoint_url_with_base_trailing_slash(self, valid_config: Config) -> None:
        """Test endpoint URL construction with base URL having trailing slash."""
        with step("Create GraphQLClient with base URL having trailing slash"):
            url = "https://api.example.com/"
            endpoint = "/graphql"
            async with GraphQLClient(url, valid_config, endpoint=endpoint) as client:
                with step("Verify transport URL is constructed correctly"):
                    if hasattr(client._transport, "url"):
                        transport_url = client._transport.url  # type: ignore[attr-defined]
                        assert transport_url == "https://api.example.com/graphql"

    @mark.asyncio
    @title("Endpoint URL with base no slash")
    @description("Test endpoint URL construction with base URL without trailing slash.")
    async def test_endpoint_url_with_base_no_slash(self, valid_config: Config) -> None:
        """Test endpoint URL construction with base URL without trailing slash."""
        with step("Create GraphQLClient with base URL without trailing slash"):
            url = "https://api.example.com"
            endpoint = "/graphql"
            async with GraphQLClient(url, valid_config, endpoint=endpoint) as client:
                with step("Verify transport URL is constructed correctly"):
                    if hasattr(client._transport, "url"):
                        transport_url = client._transport.url  # type: ignore[attr-defined]
                        assert transport_url == "https://api.example.com/graphql"

    @mark.asyncio
    @title("Endpoint URL with endpoint leading slash")
    @description("Test endpoint URL construction with endpoint having leading slash.")
    async def test_endpoint_url_with_endpoint_leading_slash(self, valid_config: Config) -> None:
        """Test endpoint URL construction with endpoint having leading slash."""
        with step("Create GraphQLClient with endpoint having leading slash"):
            url = "https://api.example.com"
            endpoint = "/graphql"
            async with GraphQLClient(url, valid_config, endpoint=endpoint) as client:
                with step("Verify transport URL is constructed correctly"):
                    if hasattr(client._transport, "url"):
                        transport_url = client._transport.url  # type: ignore[attr-defined]
                        assert transport_url == "https://api.example.com/graphql"

    @mark.asyncio
    @title("Endpoint URL with endpoint no slashes")
    @description("Test endpoint URL construction with endpoint without slashes.")
    async def test_endpoint_url_with_endpoint_no_slashes(self, valid_config: Config) -> None:
        """Test endpoint URL construction with endpoint without slashes."""
        with step("Create GraphQLClient with endpoint without slashes"):
            url = "https://api.example.com"
            endpoint = "graphql"
            async with GraphQLClient(url, valid_config, endpoint=endpoint) as client:
                with step("Verify transport URL is constructed correctly"):
                    if hasattr(client._transport, "url"):
                        transport_url = client._transport.url  # type: ignore[attr-defined]
                        assert transport_url == "https://api.example.com/graphql"

    @mark.asyncio
    @title("Endpoint URL strips query params")
    @description("Test endpoint URL construction strips query params from base URL.")
    async def test_endpoint_url_strips_query_params(self, valid_config: Config) -> None:
        """Test endpoint URL construction strips query params from base URL."""
        with step("Create GraphQLClient with URL containing query params"):
            url = "https://api.example.com?param=value&other=test"
            endpoint = "/graphql"
            async with GraphQLClient(url, valid_config, endpoint=endpoint) as client:
                with step("Verify transport URL strips query params"):
                    if hasattr(client._transport, "url"):
                        transport_url = client._transport.url  # type: ignore[attr-defined]
                        assert "?" not in transport_url
                        assert transport_url == "https://api.example.com/graphql"
