"""
Unit tests for GraphQLClient.
"""

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock

import allure
import pytest

from py_web_automation.clients.graphql_client import GraphQLClient

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit, pytest.mark.graphql]


class TestGraphQLClient:
    """Test GraphQLClient class."""

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-001: Initialize GraphQLClient")
    @allure.description("Test GraphQLClient initialization. TC-GRAPHQL-001")
    async def test_init(self, valid_config):
        """Test GraphQLClient initialization."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)
        assert client.url == url
        assert client.config == valid_config

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-002: Execute GraphQL query")
    @allure.description("Test executing a GraphQL query. TC-GRAPHQL-002")
    async def test_execute_query(self, mocker, valid_config):
        """Test executing a GraphQL query."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.content = b'{"data": {"users": [{"id": 1, "name": "Test"}]}}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        query = "{ users { id name } }"
        result = await client.query(query)

        assert result.status_code == 200
        assert "data" in result.body.decode()

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-003: Execute GraphQL mutation")
    @allure.description("Test executing a GraphQL mutation. TC-GRAPHQL-003")
    async def test_execute_mutation(self, mocker, valid_config):
        """Test executing a GraphQL mutation."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.content = b'{"data": {"createUser": {"id": 1, "name": "New User"}}}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        mutation = 'mutation { createUser(name: "New User") { id name } }'
        result = await client.mutate(mutation)

        assert result.status_code == 200
        assert "createUser" in result.body.decode()

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-004: Handle GraphQL errors")
    @allure.description("Test handling GraphQL errors. TC-GRAPHQL-004")
    async def test_handle_errors(self, mocker, valid_config):
        """Test handling GraphQL errors."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        # Mock HTTP response with GraphQL errors
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.content = b'{"errors": [{"message": "Field not found"}]}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        query = "{ invalidField }"
        result = await client.query(query)

        assert result.status_code == 200
        assert "errors" in result.body.decode()

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-005: Context manager support")
    @allure.description("Test GraphQLClient as context manager. TC-GRAPHQL-005")
    async def test_context_manager(self, valid_config):
        """Test GraphQLClient as context manager."""
        url = "https://api.example.com/graphql"
        async with GraphQLClient(url, valid_config) as client:
            assert client.url == url
            assert client.config == valid_config

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-006: Close client")
    @allure.description("Test closing GraphQLClient. TC-GRAPHQL-006")
    async def test_close(self, valid_config):
        """Test closing GraphQLClient."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)
        await client.close()
        # Verify client is closed (no exception raised)

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-007: set_auth_token устанавливает токен")
    @allure.description("Test set_auth_token sets authentication token. TC-GRAPHQL-007")
    async def test_set_auth_token(self, valid_config):
        """Test set_auth_token sets authentication token."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        client.set_auth_token("test-token-123", "Bearer")
        assert client._auth_token == "test-token-123"
        assert client._auth_token_type == "Bearer"

        client.set_auth_token("custom-token", "Custom")
        assert client._auth_token == "custom-token"
        assert client._auth_token_type == "Custom"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-008: clear_auth_token очищает токен")
    @allure.description("Test clear_auth_token clears authentication token. TC-GRAPHQL-008")
    async def test_clear_auth_token(self, valid_config):
        """Test clear_auth_token clears authentication token."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        client.set_auth_token("test-token-123")
        assert client._auth_token == "test-token-123"

        client.clear_auth_token()
        assert client._auth_token is None
        assert client._auth_token_type == "Bearer"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-009: query с variables")
    @allure.description("Test query with variables. TC-GRAPHQL-009")
    async def test_query_with_variables(self, mocker, valid_config, mock_graphql_response_200):
        """Test query with variables."""
        with allure.step("Подготовка GraphQL клиента"):
            url = "https://api.example.com/graphql"
            client = GraphQLClient(url, valid_config)

        with allure.step("Мокирование HTTP ответа"):
            # Override content for this specific test
            mock_graphql_response_200.content = b'{"data": {"user": {"id": 1, "name": "Test"}}}'
            client.client.post = AsyncMock(return_value=mock_graphql_response_200)  # type: ignore[method-assign]

        with allure.step("Выполнение query с variables"):
            query = "query GetUser($id: ID!) { user(id: $id) { name } }"
            variables = {"id": "1"}
            result = await client.query(query, variables=variables)

        with allure.step("Проверка результата"):
            assert result.status_code == 200

        with allure.step("Проверка что variables были включены в запрос"):
            call_args = client.client.post.call_args
            payload = call_args.kwargs["json"]
            assert "variables" in payload
            assert payload["variables"] == variables

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-010: query с operation_name")
    @allure.description("Test query with operation_name. TC-GRAPHQL-010")
    async def test_query_with_operation_name(self, mocker, valid_config, mock_graphql_response_200):
        """Test query with operation_name."""
        with allure.step("Подготовка GraphQL клиента"):
            url = "https://api.example.com/graphql"
            client = GraphQLClient(url, valid_config)

        with allure.step("Мокирование HTTP ответа"):
            # Override content for this specific test
            mock_graphql_response_200.content = b'{"data": {"users": []}}'
            client.client.post = AsyncMock(return_value=mock_graphql_response_200)  # type: ignore[method-assign]

        with allure.step("Выполнение query с operation_name"):
            query = "query GetUsers { users { id } } query GetPosts { posts { id } }"
            result = await client.query(query, operation_name="GetUsers")

        with allure.step("Проверка результата"):
            assert result.status_code == 200

        with allure.step("Проверка что operation_name был включен в запрос"):
            call_args = client.client.post.call_args
            payload = call_args.kwargs["json"]
            assert "operationName" in payload
            assert payload["operationName"] == "GetUsers"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-011: query с custom headers")
    @allure.description("Test query with custom headers. TC-GRAPHQL-011")
    async def test_query_with_custom_headers(self, mocker, valid_config, mock_graphql_response_200):
        """Test query with custom headers."""
        with allure.step("Подготовка GraphQL клиента"):
            url = "https://api.example.com/graphql"
            client = GraphQLClient(url, valid_config)

        with allure.step("Мокирование HTTP ответа"):
            # Override content for this specific test
            mock_graphql_response_200.content = b'{"data": {}}'
            client.client.post = AsyncMock(return_value=mock_graphql_response_200)  # type: ignore[method-assign]

        with allure.step("Выполнение query с custom headers"):
            custom_headers = {"X-Custom-Header": "value"}
            result = await client.query("{ users { id } }", headers=custom_headers)

        with allure.step("Проверка результата"):
            assert result.status_code == 200

        with allure.step("Проверка что custom headers были включены в запрос"):
            call_args = client.client.post.call_args
            assert "X-Custom-Header" in call_args.kwargs["headers"]
            assert call_args.kwargs["headers"]["X-Custom-Header"] == "value"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-012: query с authentication token")
    @allure.description("Test query with authentication token. TC-GRAPHQL-012")
    async def test_query_with_auth_token(self, mocker, valid_config):
        """Test query with authentication token."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)
        client.set_auth_token("test-token-123")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.is_informational = False
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"data": {}}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result = await client.query("{ users { id } }")

        assert result.status_code == 200
        # Verify Authorization header was added
        call_args = client.client.post.call_args
        assert "Authorization" in call_args.kwargs["headers"]
        assert call_args.kwargs["headers"]["Authorization"] == "Bearer test-token-123"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-013: mutate с variables")
    @allure.description("Test mutate with variables. TC-GRAPHQL-013")
    async def test_mutate_with_variables(self, mocker, valid_config):
        """Test mutate with variables."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.is_informational = False
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"data": {"createUser": {"id": 1}}}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        mutation = "mutation CreateUser($input: UserInput!) { createUser(input: $input) { id } }"
        variables = {"input": {"name": "John"}}
        result = await client.mutate(mutation, variables=variables)

        assert result.status_code == 200
        # Verify variables were included
        call_args = client.client.post.call_args
        payload = call_args.kwargs["json"]
        assert "variables" in payload
        assert payload["variables"] == variables

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-014: mutate с operation_name")
    @allure.description("Test mutate with operation_name. TC-GRAPHQL-014")
    async def test_mutate_with_operation_name(self, mocker, valid_config):
        """Test mutate with operation_name."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.is_informational = False
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"data": {"createUser": {"id": 1}}}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        mutation = "mutation CreateUser { createUser { id } }"
        result = await client.mutate(mutation, operation_name="CreateUser")

        assert result.status_code == 200
        # Verify operation_name was included
        call_args = client.client.post.call_args
        payload = call_args.kwargs["json"]
        assert "operationName" in payload
        assert payload["operationName"] == "CreateUser"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-015: mutate с custom headers")
    @allure.description("Test mutate with custom headers. TC-GRAPHQL-015")
    async def test_mutate_with_custom_headers(self, mocker, valid_config):
        """Test mutate with custom headers."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.is_informational = False
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"data": {"createUser": {"id": 1}}}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        custom_headers = {"X-Custom-Header": "value"}
        result = await client.mutate("mutation { createUser { id } }", headers=custom_headers)

        assert result.status_code == 200
        # Verify custom headers were included
        call_args = client.client.post.call_args
        assert "X-Custom-Header" in call_args.kwargs["headers"]

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-016: mutate с authentication token")
    @allure.description("Test mutate with authentication token. TC-GRAPHQL-016")
    async def test_mutate_with_auth_token(self, mocker, valid_config):
        """Test mutate with authentication token."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)
        client.set_auth_token("test-token-123")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.is_informational = False
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"data": {"createUser": {"id": 1}}}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result = await client.mutate("mutation { createUser { id } }")

        assert result.status_code == 200
        # Verify Authorization header was added
        call_args = client.client.post.call_args
        assert "Authorization" in call_args.kwargs["headers"]
        assert call_args.kwargs["headers"]["Authorization"] == "Bearer test-token-123"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-017: _execute строит правильный endpoint URL")
    @allure.description("Test _execute builds correct endpoint URL. TC-GRAPHQL-017")
    async def test_execute_builds_endpoint_url(self, mocker, valid_config):
        """Test _execute builds correct endpoint URL."""
        url = "https://api.example.com"
        client = GraphQLClient(url, valid_config, endpoint="/graphql")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.is_informational = False
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"data": {}}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        await client.query("{ users { id } }")

        # Verify correct URL was used
        call_args = client.client.post.call_args
        assert call_args.kwargs["url"] == "https://api.example.com/graphql"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-018: _execute обрабатывает HTTP ошибки")
    @allure.description("Test _execute handles HTTP errors. TC-GRAPHQL-018")
    async def test_execute_handles_http_errors(self, mocker, valid_config):
        """Test _execute handles HTTP errors."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = False
        mock_response.is_informational = False
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = True
        mock_response.content = b'{"errors": [{"message": "Server error"}]}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result = await client.query("{ users { id } }")

        assert result.status_code == 500
        assert result.server_error is True
        assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-019: _execute обрабатывает network ошибки")
    @allure.description("Test _execute handles network errors. TC-GRAPHQL-019")
    async def test_execute_handles_network_errors(self, mocker, valid_config):
        """Test _execute handles network errors."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        client.client.post = AsyncMock(side_effect=Exception("Network error"))  # type: ignore[method-assign]

        result = await client.query("{ users { id } }")

        assert result.status_code == 0
        assert result.success is False
        assert result.error_message == "Network error"
        assert result.body == b""

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-020: _execute redacts sensitive headers")
    @allure.description("Test _execute redacts sensitive headers. TC-GRAPHQL-020")
    async def test_execute_redacts_sensitive_headers(self, mocker, valid_config):
        """Test _execute redacts sensitive headers."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.is_informational = False
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"data": {}}'
        mock_response.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer secret-token",
            "X-API-Key": "secret-key",
        }

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result = await client.query("{ users { id } }")

        assert result.status_code == 200
        # Verify sensitive headers were redacted
        assert result.headers.get("authorization") == "[REDACTED]"
        assert result.headers.get("x-api-key") == "[REDACTED]"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-021: _execute обрабатывает отсутствие response.elapsed")
    @allure.description("Test _execute handles missing response.elapsed. TC-GRAPHQL-021")
    async def test_execute_handles_missing_elapsed(self, mocker, valid_config):
        """Test _execute handles missing response.elapsed."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        del mock_response.elapsed  # Remove elapsed attribute
        mock_response.is_success = True
        mock_response.is_informational = False
        mock_response.is_redirect = False
        mock_response.is_client_error = False
        mock_response.is_server_error = False
        mock_response.content = b'{"data": {}}'
        mock_response.headers = {"Content-Type": "application/json"}

        client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result = await client.query("{ users { id } }")

        assert result.status_code == 200
        assert result.response_time == 0.0

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-022: get_errors извлекает errors из JSON")
    @allure.description("Test get_errors extracts errors from JSON. TC-GRAPHQL-022")
    async def test_get_errors_extracts_errors(self, valid_config):
        """Test get_errors extracts errors from JSON."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        from py_web_automation.clients.models import ApiResult

        result = ApiResult(
            endpoint="/graphql",
            method="POST",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"errors": [{"message": "Error 1"}, {"message": "Error 2"}]}',
            content_type="application/json",
        )

        errors = client.get_errors(result)

        assert len(errors) == 2
        assert errors[0]["message"] == "Error 1"
        assert errors[1]["message"] == "Error 2"

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-023: get_errors возвращает пустой список если нет errors")
    @allure.description("Test get_errors returns empty list if no errors. TC-GRAPHQL-023")
    async def test_get_errors_no_errors(self, valid_config):
        """Test get_errors returns empty list if no errors."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        from py_web_automation.clients.models import ApiResult

        result = ApiResult(
            endpoint="/graphql",
            method="POST",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"data": {"users": []}}',
            content_type="application/json",
        )

        errors = client.get_errors(result)

        assert errors == []

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-024: get_errors обрабатывает невалидный JSON")
    @allure.description("Test get_errors handles invalid JSON. TC-GRAPHQL-024")
    async def test_get_errors_invalid_json(self, valid_config):
        """Test get_errors handles invalid JSON."""
        url = "https://api.example.com/graphql"
        client = GraphQLClient(url, valid_config)

        from py_web_automation.clients.models import ApiResult

        result = ApiResult(
            endpoint="/graphql",
            method="POST",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b"Not valid JSON",
            content_type="text/plain",
        )

        errors = client.get_errors(result)

        assert errors == []

    @pytest.mark.asyncio
    @allure.title("TC-GRAPHQL-025: Инициализация с custom endpoint")
    @allure.description("Test initialization with custom endpoint. TC-GRAPHQL-025")
    async def test_init_with_custom_endpoint(self, valid_config):
        """Test initialization with custom endpoint."""
        url = "https://api.example.com"
        endpoint = "/api/graphql"
        client = GraphQLClient(url, valid_config, endpoint=endpoint)

        assert client.url == url
        assert client.endpoint == endpoint

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status_code,expected_success,test_id",
        [
            (200, True, "TC-GRAPHQL-STATUS-001"),
            (201, True, "TC-GRAPHQL-STATUS-002"),
            (400, False, "TC-GRAPHQL-STATUS-003"),
            (401, False, "TC-GRAPHQL-STATUS-004"),
            (403, False, "TC-GRAPHQL-STATUS-005"),
            (404, False, "TC-GRAPHQL-STATUS-006"),
            (500, False, "TC-GRAPHQL-STATUS-007"),
            (502, False, "TC-GRAPHQL-STATUS-008"),
            (503, False, "TC-GRAPHQL-STATUS-009"),
        ],
    )
    @allure.title("{test_id}: GraphQLClient handles status code {status_code}")
    @allure.description("Test GraphQLClient handles various HTTP status codes. {test_id}")
    async def test_graphql_client_status_codes(self, mocker, valid_config, status_code, expected_success, test_id):
        """Test GraphQLClient handles various HTTP status codes."""
        with allure.step(f"Prepare GraphQLClient for status {status_code}"):
            url = "https://api.example.com/graphql"
            client = GraphQLClient(url, valid_config)

        with allure.step(f"Create mock response with status_code {status_code}"):
            mock_response = MagicMock()
            mock_response.status_code = status_code
            mock_response.elapsed = timedelta(seconds=0.2)
            mock_response.is_success = expected_success
            mock_response.is_redirect = 300 <= status_code < 400
            mock_response.is_client_error = 400 <= status_code < 500
            mock_response.is_server_error = 500 <= status_code < 600
            mock_response.is_informational = 100 <= status_code < 200
            mock_response.content = b'{"data": {"test": "value"}}'
            mock_response.headers = {"Content-Type": "application/json"}

        with allure.step("Mock HTTP client post method"):
            client.client.post = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        with allure.step("Execute query and verify status code"):
            query = "{ users { id name } }"
            result = await client.query(query)

            assert result.status_code == status_code
            assert result.success == expected_success
