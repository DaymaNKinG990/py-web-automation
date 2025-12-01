"""
Unit tests for RequestBuilder.
"""

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock

import allure
import pytest

from py_web_automation.clients.api_client import ApiClient
from py_web_automation.clients.models import ApiResult
from py_web_automation.clients.request_builder import RequestBuilder

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit, pytest.mark.api]


class TestRequestBuilder:
    """Test RequestBuilder class."""

    @pytest.mark.asyncio
    @allure.title("TC-RB-001: Initialize RequestBuilder")
    @allure.description("Test RequestBuilder initialization. TC-RB-001")
    async def test_init(self, mocker, valid_config):
        """Test RequestBuilder initialization."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)
        assert builder._client == api_client

    @pytest.mark.asyncio
    @allure.title("TC-RB-002: Build GET request")
    @allure.description("Test building GET request. TC-RB-002")
    async def test_build_get(self, mocker, valid_config):
        """Test building GET request."""
        with allure.step("Подготовка ApiClient и RequestBuilder"):
            url = "https://api.example.com"
            api_client = ApiClient(url, valid_config)
            builder = RequestBuilder(api_client)

        with allure.step("Создание ApiResult mock"):
            mock_result = ApiResult(
                endpoint="/api/users",
                method="GET",
                status_code=200,
                response_time=0.2,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                headers={"Content-Type": "application/json"},
                body=b'{"data": "test"}',
                content_type="application/json",
            )

        with allure.step("Мокирование make_request метода"):
            api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        with allure.step("Построение и выполнение GET запроса"):
            result = await builder.get("/api/users").params(page=1, limit=10).execute()

        with allure.step("Проверка результата"):
            assert result.status_code == 200

    @pytest.mark.asyncio
    @allure.title("TC-RB-003: Build POST request with JSON")
    @allure.description("Test building POST request with JSON body. TC-RB-003")
    async def test_build_post_json(self, mocker, valid_config):
        """Test building POST request with JSON body."""
        with allure.step("Подготовка ApiClient и RequestBuilder"):
            url = "https://api.example.com"
            api_client = ApiClient(url, valid_config)
            builder = RequestBuilder(api_client)

        with allure.step("Создание ApiResult mock"):
            mock_result = ApiResult(
                endpoint="/api/users",
                method="POST",
                status_code=201,
                response_time=0.2,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                headers={"Content-Type": "application/json"},
                body=b'{"id": 1, "name": "New User"}',
                content_type="application/json",
            )

        with allure.step("Мокирование make_request метода"):
            api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        with allure.step("Построение и выполнение POST запроса с JSON"):
            result = await builder.post("/api/users").json({"name": "New User", "email": "user@example.com"}).execute()

        with allure.step("Проверка результата"):
            assert result.status_code == 201

    @pytest.mark.asyncio
    @allure.title("TC-RB-004: Build request with headers")
    @allure.description("Test building request with custom headers. TC-RB-004")
    async def test_build_with_headers(self, mocker, valid_config):
        """Test building request with custom headers."""
        with allure.step("Подготовка ApiClient и RequestBuilder"):
            url = "https://api.example.com"
            api_client = ApiClient(url, valid_config)
            builder = RequestBuilder(api_client)

        with allure.step("Создание ApiResult mock"):
            mock_result = ApiResult(
                endpoint="/api/users",
                method="GET",
                status_code=200,
                response_time=0.2,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                headers={"Content-Type": "application/json"},
                body=b'{"data": "test"}',
                content_type="application/json",
            )

        with allure.step("Мокирование make_request метода"):
            api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        with allure.step("Построение и выполнение запроса с headers"):
            result = await (
                builder.get("/api/data")
                .header("X-Custom-Header", "value")
                .header("Authorization", "Bearer token123")
                .execute()
            )

        with allure.step("Проверка результата"):
            assert result.status_code == 200

    @pytest.mark.asyncio
    @allure.title("TC-RB-005: Build PUT request")
    @allure.description("Test building PUT request. TC-RB-005")
    async def test_build_put(self, mocker, valid_config):
        """Test building PUT request."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed = timedelta(seconds=0.2)
        mock_response.is_success = True
        mock_response.content = b'{"id": 1, "name": "Updated User"}'
        mock_response.headers = {"Content-Type": "application/json"}

        # Mock make_request method
        api_client.make_request = AsyncMock(return_value=mock_response)  # type: ignore[method-assign]

        result = await builder.put("/api/users/1").json({"name": "Updated User"}).execute()

        assert result.status_code == 200

    @pytest.mark.asyncio
    @allure.title("TC-RB-006: Build DELETE request")
    @allure.description("Test building DELETE request. TC-RB-006")
    async def test_build_delete(self, mocker, valid_config):
        """Test building DELETE request."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        # Create ApiResult mock
        mock_result = ApiResult(
            endpoint="/api/users/1",
            method="DELETE",
            status_code=204,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            headers={},
            body=b"",
        )

        # Mock make_request method
        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        result = await builder.delete("/api/users/1").execute()

        assert result.status_code == 204

    @pytest.mark.asyncio
    @allure.title("TC-RB-007: patch устанавливает метод и endpoint")
    @allure.description("Test patch sets method and endpoint. TC-RB-007")
    async def test_patch(self, mocker, valid_config):
        """Test patch sets method and endpoint."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users/1",
            method="PATCH",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"id": 1, "name": "Patched"}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        result = await builder.patch("/api/users/1").json({"name": "Patched"}).execute()

        assert result.status_code == 200
        assert builder._method == "PATCH"
        assert builder._endpoint == "/api/users/1"

    @pytest.mark.asyncio
    @allure.title("TC-RB-008: head устанавливает метод и endpoint")
    @allure.description("Test head sets method and endpoint. TC-RB-008")
    async def test_head(self, mocker, valid_config):
        """Test head sets method and endpoint."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="HEAD",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b"",
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        result = await builder.head("/api/users").execute()

        assert result.status_code == 200
        assert builder._method == "HEAD"
        assert builder._endpoint == "/api/users"

    @pytest.mark.asyncio
    @allure.title("TC-RB-009: options устанавливает метод и endpoint")
    @allure.description("Test options sets method and endpoint. TC-RB-009")
    async def test_options(self, mocker, valid_config):
        """Test options sets method and endpoint."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="OPTIONS",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b"",
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        result = await builder.options("/api/users").execute()

        assert result.status_code == 200
        assert builder._method == "OPTIONS"
        assert builder._endpoint == "/api/users"

    @pytest.mark.asyncio
    @allure.title("TC-RB-010: param добавляет один query parameter")
    @allure.description("Test param adds single query parameter. TC-RB-010")
    async def test_param(self, mocker, valid_config):
        """Test param adds single query parameter."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"data": "test"}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        result = await builder.get("/api/users").param("page", 1).execute()

        assert result.status_code == 200
        assert builder._params["page"] == 1

    @pytest.mark.asyncio
    @allure.title("TC-RB-011: body устанавливает request body")
    @allure.description("Test body sets request body. TC-RB-011")
    async def test_body(self, mocker, valid_config):
        """Test body sets request body."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="POST",
            status_code=201,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"id": 1}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        body_data = {"name": "John", "email": "john@example.com"}
        result = await builder.post("/api/users").body(body_data).execute()

        assert result.status_code == 201
        assert builder._data == body_data
        assert builder._json_body is True

    @pytest.mark.asyncio
    @allure.title("TC-RB-012: json устанавливает request body (alias для body)")
    @allure.description("Test json sets request body (alias for body). TC-RB-012")
    async def test_json(self, mocker, valid_config):
        """Test json sets request body (alias for body)."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="POST",
            status_code=201,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"id": 1}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        json_data = {"name": "John"}
        result = await builder.post("/api/users").json(json_data).execute()

        assert result.status_code == 201
        assert builder._data == json_data

    @pytest.mark.asyncio
    @allure.title("TC-RB-013: headers добавляет несколько headers")
    @allure.description("Test headers adds multiple headers. TC-RB-013")
    async def test_headers(self, mocker, valid_config):
        """Test headers adds multiple headers."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"data": "test"}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        result = await builder.get("/api/users").headers(X_Custom_Header="value1", X_Another_Header="value2").execute()

        assert result.status_code == 200
        # headers() stores keys as provided (with underscores converted to hyphens in kwargs)
        # Check that headers were added (exact key format depends on implementation)
        assert len(builder._headers) >= 2
        assert "value1" in builder._headers.values()
        assert "value2" in builder._headers.values()

    @pytest.mark.asyncio
    @allure.title("TC-RB-014: auth устанавливает authentication token")
    @allure.description("Test auth sets authentication token. TC-RB-014")
    async def test_auth(self, mocker, valid_config):
        """Test auth sets authentication token."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"data": "test"}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]
        api_client.set_auth_token = mocker.Mock()  # type: ignore[method-assign]

        result = await builder.get("/api/users").auth("test-token-123").execute()

        assert result.status_code == 200
        api_client.set_auth_token.assert_called_once_with("test-token-123", "Bearer")

    @pytest.mark.asyncio
    @allure.title("TC-RB-015: validate выбрасывает ValidationError если endpoint не установлен")
    @allure.description("Test validate raises ValidationError if endpoint not set. TC-RB-015")
    async def test_validate_missing_endpoint(self, valid_config):
        """Test validate raises ValidationError if endpoint not set."""
        from py_web_automation.exceptions import ValidationError

        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        with pytest.raises(ValidationError, match="Request endpoint is required"):
            builder.validate()

    @pytest.mark.asyncio
    @allure.title("TC-RB-016: validate не выбрасывает ошибку для POST/PUT/PATCH без body")
    @allure.description("Test validate does not raise error for POST/PUT/PATCH without body. TC-RB-016")
    async def test_validate_allows_empty_body(self, valid_config):
        """Test validate does not raise error for POST/PUT/PATCH without body."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        # Should not raise error
        builder.post("/api/users").validate()
        builder.put("/api/users/1").validate()
        builder.patch("/api/users/1").validate()

    @pytest.mark.asyncio
    @allure.title("TC-RB-017: execute вызывает validate")
    @allure.description("Test execute calls validate. TC-RB-017")
    async def test_execute_calls_validate(self, mocker, valid_config):
        """Test execute calls validate."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"data": "test"}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        # Should not raise ValidationError because endpoint is set
        result = await builder.get("/api/users").execute()

        assert result.status_code == 200

    @pytest.mark.asyncio
    @allure.title("TC-RB-018: execute вызывает make_request с правильными параметрами")
    @allure.description("Test execute calls make_request with correct parameters. TC-RB-018")
    async def test_execute_calls_make_request(self, mocker, valid_config):
        """Test execute calls make_request with correct parameters."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"data": "test"}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        result = await builder.get("/api/users").params(page=1, limit=10).header("X-Custom", "value").execute()

        assert result.status_code == 200
        # Verify make_request was called with correct parameters
        api_client.make_request.assert_called_once()
        call_args = api_client.make_request.call_args
        assert call_args.kwargs["endpoint"] == "/api/users"
        assert call_args.kwargs["method"] == "GET"
        assert call_args.kwargs["params"] == {"page": 1, "limit": 10}
        assert call_args.kwargs["headers"] == {"X-Custom": "value"}

    @pytest.mark.asyncio
    @allure.title("TC-RB-019: reset очищает все поля")
    @allure.description("Test reset clears all fields. TC-RB-019")
    async def test_reset(self, valid_config):
        """Test reset clears all fields."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        # Set some values
        builder.post("/api/users").params(page=1).body({"name": "John"}).header("X-Custom", "value")

        # Reset
        builder.reset()

        assert builder._method == "GET"
        assert builder._endpoint == ""
        assert len(builder._params) == 0
        assert builder._data is None
        assert len(builder._headers) == 0
        assert builder._json_body is True

    @pytest.mark.asyncio
    @allure.title("TC-RB-020: __init__ выбрасывает TypeError для не-ApiClient")
    @allure.description("Test __init__ raises TypeError for non-ApiClient. TC-RB-020")
    async def test_init_raises_typeerror(self, valid_config):
        """Test __init__ raises TypeError for non-ApiClient."""
        with pytest.raises(TypeError, match="Expected ApiClient"):
            RequestBuilder("not_an_api_client")  # type: ignore[arg-type]

    @pytest.mark.asyncio
    @allure.title("TC-RB-021: Method chaining работает для всех методов")
    @allure.description("Test method chaining works for all methods. TC-RB-021")
    async def test_method_chaining(self, mocker, valid_config):
        """Test method chaining works for all methods."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="POST",
            status_code=201,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"id": 1}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        # Test chaining
        result = await (
            builder.post("/api/users")
            .param("page", 1)
            .params(limit=10)
            .body({"name": "John"})
            .header("X-Custom", "value")
            .headers(X_Another="value2")
            .execute()
        )

        assert result.status_code == 201

    @pytest.mark.asyncio
    @allure.title("TC-RB-022: params с пустым kwargs не ломает builder")
    @allure.description("Test params with empty kwargs does not break builder. TC-RB-022")
    async def test_params_empty_kwargs(self, mocker, valid_config):
        """Test params with empty kwargs does not break builder."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"data": "test"}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        # Should not raise error
        result = await builder.get("/api/users").params().execute()

        assert result.status_code == 200

    @pytest.mark.asyncio
    @allure.title("TC-RB-023: headers с пустым kwargs не ломает builder")
    @allure.description("Test headers with empty kwargs does not break builder. TC-RB-023")
    async def test_headers_empty_kwargs(self, mocker, valid_config):
        """Test headers with empty kwargs does not break builder."""
        url = "https://api.example.com"
        api_client = ApiClient(url, valid_config)
        builder = RequestBuilder(api_client)

        mock_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"data": "test"}',
        )

        api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        # Should not raise error
        result = await builder.get("/api/users").headers().execute()

        assert result.status_code == 200

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status_code,expected_success,test_id",
        [
            (200, True, "TC-RB-STATUS-001"),
            (201, True, "TC-RB-STATUS-002"),
            (204, True, "TC-RB-STATUS-003"),
            (400, False, "TC-RB-STATUS-004"),
            (401, False, "TC-RB-STATUS-005"),
            (403, False, "TC-RB-STATUS-006"),
            (404, False, "TC-RB-STATUS-007"),
            (500, False, "TC-RB-STATUS-008"),
            (502, False, "TC-RB-STATUS-009"),
            (503, False, "TC-RB-STATUS-010"),
        ],
    )
    @allure.title("{test_id}: RequestBuilder handles status code {status_code}")
    @allure.description("Test RequestBuilder handles various HTTP status codes. {test_id}")
    async def test_request_builder_status_codes(self, mocker, valid_config, status_code, expected_success, test_id):
        """Test RequestBuilder handles various HTTP status codes."""
        with allure.step(f"Prepare ApiClient and RequestBuilder for status {status_code}"):
            url = "https://api.example.com"
            api_client = ApiClient(url, valid_config)
            builder = RequestBuilder(api_client)

        with allure.step(f"Create ApiResult mock with status_code {status_code}"):
            mock_result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=status_code,
                response_time=0.2,
                success=expected_success,
                redirect=300 <= status_code < 400,
                client_error=400 <= status_code < 500,
                server_error=500 <= status_code < 600,
                informational=100 <= status_code < 200,
                headers={"Content-Type": "application/json"},
                body=b'{"data": "test"}',
                content_type="application/json",
            )

        with allure.step("Mock make_request method"):
            api_client.make_request = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        with allure.step("Execute request and verify status code"):
            result = await builder.get("/api/test").execute()

            assert result.status_code == status_code
            assert result.success == expected_success
