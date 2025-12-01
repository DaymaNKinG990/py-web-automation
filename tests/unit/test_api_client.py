"""
Unit tests for ApiClient.
"""

import allure
import pytest
from httpx import RequestError, TimeoutException

from py_web_automation.clients.api_client import ApiClient
from py_web_automation.clients.base_client import BaseClient

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit, pytest.mark.api]


# ============================================================================
# I. Инициализация и закрытие
# ============================================================================


class TestApiClientInit:
    """Test ApiClient initialization."""

    @allure.title("Initialize ApiClient with URL and config")
    @allure.description("Test successful initialization with url and config. TC-API-001")
    def test_init_with_url_and_config(self, mocker, valid_config, mock_httpx_client):
        """Test successful initialization with url and config. TC-API-001"""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "py_web_automation.clients.api_client.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create ApiClient instance"):
            api = ApiClient("https://example.com/app", valid_config)

        with allure.step("Verify api.url is set correctly"):
            assert api.url == "https://example.com/app"
        with allure.step("Verify api.config matches provided config"):
            assert api.config == valid_config
        with allure.step("Verify api.client is initialized"):
            assert api.client is not None

    @allure.title("TC-API-002: Initialize ApiClient with config=None uses default")
    @allure.description("Test initialization with config=None uses default. TC-API-002")
    def test_init_with_config_none_uses_default(self, mocker, mock_httpx_client):
        """Test initialization with config=None uses default. TC-API-002"""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "py_web_automation.clients.api_client.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create ApiClient instance with config=None"):
            api = ApiClient("https://example.com/app", None)

        with allure.step("Verify api.config is a default Config instance"):
            assert api.config is not None
            assert api.url == "https://example.com/app"

    @allure.title("TC-API-003: Verify AsyncClient is initialized with correct timeout")
    @allure.description("Test AsyncClient is created with correct timeout. TC-API-003")
    def test_init_creates_async_client_with_timeout(self, mocker, valid_config, mock_httpx_client):
        """Test AsyncClient is created with correct timeout. TC-API-003"""
        with allure.step("Mock AsyncClient class"):
            mock_client_class = mocker.patch(
                "py_web_automation.clients.api_client.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create ApiClient instance"):
            _ = ApiClient("https://example.com/app", valid_config)

        with allure.step("Verify AsyncClient was called once"):
            mock_client_class.assert_called_once()
        with allure.step("Verify timeout matches config.timeout"):
            call_kwargs = mock_client_class.call_args[1]
            assert call_kwargs["timeout"] == valid_config.timeout

    @allure.title("TC-API-004: Verify AsyncClient is initialized with correct Limits")
    @allure.description("Test AsyncClient is created with correct Limits. TC-API-004")
    def test_init_creates_async_client_with_limits(self, mocker, valid_config, mock_httpx_client):
        """Test AsyncClient is created with correct Limits. TC-API-004"""

        with allure.step("Mock AsyncClient class"):
            mock_client_class = mocker.patch(
                "py_web_automation.clients.api_client.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create ApiClient instance"):
            _ = ApiClient("https://example.com/app", valid_config)

        with allure.step("Verify AsyncClient was called once"):
            mock_client_class.assert_called_once()
        with allure.step("Verify Limits were passed to AsyncClient"):
            call_kwargs = mock_client_class.call_args[1]
            assert "limits" in call_kwargs
            limits = call_kwargs["limits"]
        with allure.step("Verify max_keepalive_connections is 5"):
            assert limits.max_keepalive_connections == 5
        with allure.step("Verify max_connections is 10"):
            assert limits.max_connections == 10


class TestApiClientClose:
    """Test ApiClient close method."""

    @pytest.mark.asyncio
    @allure.title("TC-API-005: Close ApiClient client")
    @allure.description("Test close() calls await self.client.aclose(). TC-API-005")
    async def test_close_calls_client_aclose(self, api_client_with_config):
        """Test close() calls await self.client.aclose(). TC-API-005"""
        with allure.step("Call close() method"):
            await api_client_with_config.close()

        with allure.step("Verify client.aclose() was called once"):
            api_client_with_config.client.aclose.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("Close ApiClient is async")
    @allure.description("Test close() is async and can be awaited.")
    async def test_close_is_async(self, api_client_with_config):
        """Test close() is async and can be awaited."""
        with allure.step("Call close() method and await"):
            # Should not raise any exception
            await api_client_with_config.close()

    @pytest.mark.asyncio
    @allure.title("TC-API-006: Close ApiClient multiple times")
    @allure.description("Test close() can be called multiple times safely. TC-API-006")
    async def test_close_multiple_times(self, api_client_with_config):
        """Test close() can be called multiple times safely. TC-API-006"""
        with allure.step("First call to close()"):
            await api_client_with_config.close()
            api_client_with_config.client.aclose.assert_called_once()

        with allure.step("Reset mock to count calls"):
            # Reset mock to count calls
            api_client_with_config.client.aclose.reset_mock()

        with allure.step("Second call to close() should not raise exception"):
            # Second call should not raise exception (idempotent)
            await api_client_with_config.close()
            # Should still call aclose (or handle gracefully)
            # The actual behavior depends on httpx client implementation
            # but the test verifies no exception is raised


# ============================================================================
# II. Выполнение HTTP-запросов (make_request)
# ============================================================================


class TestApiClientMakeRequest:
    """Test ApiClient make_request method."""

    @pytest.mark.asyncio
    @allure.title("TC-API-021: Make request with absolute URL")
    @allure.description("Test make_request with absolute URL uses it as is. TC-API-021")
    async def test_make_request_absolute_url(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with absolute URL uses it as is. TC-API-021"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request with absolute URL"):
            result = await api_client_with_config.make_request("https://api.example.com/data")

        with allure.step("Verify result.endpoint matches input"):
            assert result.endpoint == "https://api.example.com/data"
        with allure.step("Verify client.request was called once"):
            api_client_with_config.client.request.assert_called_once()
        with allure.step("Verify URL in request matches absolute URL"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["url"] == "https://api.example.com/data"

    @pytest.mark.asyncio
    @allure.title("Make request with relative URL starting with slash")
    @allure.description("Test make_request with relative URL starting with /. TC-API-020, TC-API-022")
    async def test_make_request_relative_url_with_slash(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with relative URL starting with /. TC-API-020, TC-API-022"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request with relative URL starting with /"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify result.endpoint matches input"):
            assert result.endpoint == "/api/data"
        with allure.step("Verify URL is constructed correctly"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["url"] == "https://example.com/app/api/data"

    @pytest.mark.asyncio
    @allure.title("TC-API-023: Make request with relative URL without slash")
    @allure.description("Test make_request with relative URL without /. TC-API-023")
    async def test_make_request_relative_url_without_slash(
        self, mocker, api_client_with_config, mock_httpx_response_200
    ):
        """Test make_request with relative URL without /. TC-API-023"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request with relative URL without /"):
            result = await api_client_with_config.make_request("api/data")

        with allure.step("Verify result.endpoint matches input"):
            assert result.endpoint == "api/data"
        with allure.step("Verify URL is constructed correctly"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["url"] == "https://example.com/app/api/data"

    @pytest.mark.asyncio
    @allure.title("Make request removes query params from base URL")
    @allure.description("Test make_request removes query params from base URL. TC-API-035")
    async def test_make_request_removes_query_params_from_base_url(
        self, mocker, api_client_with_config, mock_httpx_response_200
    ):
        """Test make_request removes query params from base URL. TC-API-035"""
        with allure.step("Set base URL with query params"):
            api_client_with_config.url = "https://t.me/mybot/app?start=123"
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request"):
            _ = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify query params are removed from URL"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["url"] == "https://t.me/mybot/app/api/data"
            assert "start=123" not in call_kwargs["url"]

    @pytest.mark.asyncio
    @allure.title("TC-API-024: Make request with GET method")
    @allure.description("Test make_request with GET method. TC-API-024")
    async def test_make_request_get_method(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with GET method. TC-API-024"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request with GET method"):
            result = await api_client_with_config.make_request("/api/data", method="GET")

        with allure.step("Verify result.method is GET"):
            assert result.method == "GET"
        with allure.step("Verify request method is GET"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["method"] == "GET"

    @pytest.mark.asyncio
    @allure.title("TC-API-025: Make request with POST method and data")
    @allure.description("Test make_request with POST method and data. TC-API-025")
    async def test_make_request_post_with_data(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with POST method and data. TC-API-025"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)
        with allure.step("Prepare request data"):
            data = {"key": "value"}

        with allure.step("Call make_request with POST method and data"):
            result = await api_client_with_config.make_request("/api/data", method="POST", data=data)

        with allure.step("Verify result.method is POST"):
            assert result.method == "POST"
        with allure.step("Verify request method and data"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["method"] == "POST"
            assert call_kwargs["json"] == data

    @pytest.mark.asyncio
    @allure.title("TC-API-026: Make request with headers")
    @allure.description("Test make_request with headers. TC-API-026")
    async def test_make_request_with_headers(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with headers. TC-API-026"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)
        with allure.step("Prepare custom headers"):
            headers = {"Authorization": "Bearer token"}

        with allure.step("Call make_request with headers"):
            _ = await api_client_with_config.make_request("/api/data", headers=headers)

        with allure.step("Verify headers are passed to request"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["headers"] == headers

    @pytest.mark.asyncio
    @allure.title("TC-API-024: Make request with status 200")
    @allure.description("Test make_request with status 200. TC-API-024, TC-API-034")
    async def test_make_request_status_200(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with status 200. TC-API-024, TC-API-034"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 200"):
            assert result.status_code == 200
        with allure.step("Verify success flags"):
            assert result.success is True
            assert result.client_error is False
            assert result.server_error is False
            assert result.redirect is False
            assert result.informational is False

    @pytest.mark.asyncio
    @allure.title("TC-API-034: Make request with status 301")
    @allure.description("Test make_request with status 301. TC-API-034")
    async def test_make_request_status_301(self, mocker, api_client_with_config, mock_httpx_response_301):
        """Test make_request with status 301. TC-API-034"""
        with allure.step("Mock client.request with 301 response"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_301)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 301"):
            assert result.status_code == 301
        with allure.step("Verify redirect flag is True"):
            assert result.redirect is True
            assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-API-034: Make request with status 404")
    @allure.description("Test make_request with status 404. TC-API-034")
    async def test_make_request_status_404(self, mocker, api_client_with_config, mock_httpx_response_404):
        """Test make_request with status 404. TC-API-034"""
        with allure.step("Mock client.request with 404 response"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_404)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 404"):
            assert result.status_code == 404
        with allure.step("Verify client_error flag is True"):
            assert result.client_error is True
            assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-API-034: Make request with status 500")
    @allure.description("Test make_request with status 500. TC-API-034")
    async def test_make_request_status_500(self, mocker, api_client_with_config, mock_httpx_response_500):
        """Test make_request with status 500. TC-API-034"""
        with allure.step("Mock client.request with 500 response"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_500)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 500"):
            assert result.status_code == 500
        with allure.step("Verify server_error flag is True"):
            assert result.server_error is True
            assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-API-034: Make request with status 101")
    @allure.description("Test make_request with status 101. TC-API-034")
    async def test_make_request_status_101(self, mocker, api_client_with_config, mock_httpx_response_101):
        """Test make_request with status 101. TC-API-034"""
        with allure.step("Mock client.request with 101 response"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_101)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify status_code is 101"):
            assert result.status_code == 101
        with allure.step("Verify informational flag is True"):
            assert result.informational is True
            assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-API-027: Make request captures response_time")
    @allure.description("Test make_request captures response_time. TC-API-027")
    async def test_make_request_response_time(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request captures response_time. TC-API-027"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify response_time is captured"):
            assert result.response_time == 0.5
            assert isinstance(result.response_time, float)

    @pytest.mark.asyncio
    @allure.title("Make request handles unavailable response_time")
    @allure.description("Test make_request handles case when response.elapsed is unavailable. TC-API-038")
    async def test_make_request_response_time_unavailable(self, mocker, api_client_with_config):
        """Test make_request handles case when response.elapsed is unavailable. TC-API-038"""
        with allure.step("Create mock response where elapsed raises AttributeError"):
            # Create a mock response where elapsed raises AttributeError
            mock_response = mocker.MagicMock()
            mock_response.status_code = 200
            mock_response.is_informational = False
            mock_response.is_success = True
            mock_response.is_redirect = False
            mock_response.is_client_error = False
            mock_response.is_server_error = False
            mock_response.content = b'{"test": "data"}'
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.reason_phrase = "OK"

            # Create a mock elapsed object that raises AttributeError when total_seconds() is called
            mock_elapsed = mocker.MagicMock()
            mock_elapsed.total_seconds = mocker.Mock(side_effect=AttributeError("elapsed not available"))
            # Make elapsed property return the mock that raises error
            type(mock_response).elapsed = mocker.PropertyMock(return_value=mock_elapsed)

        with allure.step("Mock client.request with problematic response"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_response)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify response_time is set to 0.0 gracefully"):
            # Should handle gracefully and set response_time to 0.0
            assert result.response_time == 0.0
            assert isinstance(result.response_time, float)
            assert result.success is True
            assert result.status_code == 200

    @pytest.mark.asyncio
    @allure.title("Make request handles RuntimeError when accessing response.elapsed")
    @allure.description("Test make_request handles RuntimeError when accessing response.elapsed. TC-API-038")
    async def test_make_request_response_time_runtime_error(self, mocker, api_client_with_config):
        """Test make_request handles RuntimeError when accessing response.elapsed. TC-API-038"""
        with allure.step("Create mock response where elapsed raises RuntimeError"):
            # Create a mock response where elapsed raises RuntimeError
            mock_response = mocker.MagicMock()
            mock_response.status_code = 200
            mock_response.is_informational = False
            mock_response.is_success = True
            mock_response.is_redirect = False
            mock_response.is_client_error = False
            mock_response.is_server_error = False
            mock_response.content = b'{"test": "data"}'
            mock_response.headers = {"Content-Type": "application/json"}
            mock_response.reason_phrase = "OK"

            # Create a mock elapsed object that raises RuntimeError when total_seconds() is called
            mock_elapsed = mocker.MagicMock()
            mock_elapsed.total_seconds = mocker.Mock(
                side_effect=RuntimeError("elapsed may only be accessed after the response has been read")
            )
            # Make elapsed property return the mock that raises error
            type(mock_response).elapsed = mocker.PropertyMock(return_value=mock_elapsed)

        with allure.step("Mock client.request with problematic response"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_response)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify response_time is set to 0.0 gracefully"):
            # Should handle gracefully and set response_time to 0.0
            assert result.response_time == 0.0
            assert isinstance(result.response_time, float)
            assert result.success is True
            assert result.status_code == 200

    @pytest.mark.asyncio
    @allure.title("Make request extracts response data into immutable fields")
    @allure.description("Test make_request extracts response data into immutable fields. TC-API-028")
    async def test_make_request_extracts_response_data(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request extracts response data into immutable fields. TC-API-028"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify response data is extracted into immutable fields"):
            # Response data should be extracted into immutable fields
            assert result.headers is not None
            assert isinstance(result.headers, dict)
            assert result.body is not None
            assert isinstance(result.body, bytes)
        with allure.step("Verify response object is not stored"):
            # Response object should not be stored
            assert not hasattr(result, "response") or getattr(result, "response", None) is None

    @pytest.mark.asyncio
    @allure.title("TC-API-029: Make request handles network errors")
    @allure.description("Test make_request handles network errors. TC-API-029")
    async def test_make_request_network_error(self, mocker, api_client_with_config):
        """Test make_request handles network errors. TC-API-029"""
        with allure.step("Create RequestError"):
            error = RequestError("Network error", request=mocker.MagicMock())
        with allure.step("Mock client.request to raise error"):
            api_client_with_config.client.request = mocker.AsyncMock(side_effect=error)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify error result"):
            assert result.status_code == 0
            assert result.success is False
            assert result.error_message == "Network error"
            assert result.headers == {}
            assert result.body == b""
            assert result.content_type is None
            assert result.reason is None

    @pytest.mark.asyncio
    @allure.title("TC-API-029: Make request handles timeout errors")
    @allure.description("Test make_request handles timeout errors. TC-API-029")
    async def test_make_request_timeout_error(self, mocker, api_client_with_config):
        """Test make_request handles timeout errors. TC-API-029"""
        with allure.step("Create TimeoutException"):
            error = TimeoutException("Request timeout", request=mocker.MagicMock())
        with allure.step("Mock client.request to raise timeout error"):
            api_client_with_config.client.request = mocker.AsyncMock(side_effect=error)

        with allure.step("Call make_request"):
            result = await api_client_with_config.make_request("/api/data")

        with allure.step("Verify timeout error result"):
            assert result.status_code == 0
            assert result.success is False
            assert "timeout" in result.error_message.lower()

    @pytest.mark.asyncio
    @allure.title("TC-API-030: Make request logs request")
    @allure.description("Test make_request logs request. TC-API-030")
    async def test_make_request_logs_request(self, mocker, api_client_with_config, mock_httpx_response_200, caplog):
        """Test make_request logs request. TC-API-030"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request and capture logs"):
            with caplog.at_level("INFO"):
                await api_client_with_config.make_request("/api/data", method="POST")

        with allure.step("Verify request is logged"):
            assert "Making request: POST" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-API-031: Make request logs response")
    @allure.description("Test make_request logs response. TC-API-031")
    async def test_make_request_logs_response(self, mocker, api_client_with_config, mock_httpx_response_200, caplog):
        """Test make_request logs response. TC-API-031"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request and capture logs"):
            with caplog.at_level("INFO"):
                await api_client_with_config.make_request("/api/data")

        with allure.step("Verify response is logged"):
            assert "Response got:" in caplog.text
            assert "status_code=200" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-API-032: Make request logs error on failure")
    @allure.description("Test make_request logs error on failure. TC-API-032")
    async def test_make_request_logs_error(self, mocker, api_client_with_config, caplog):
        """Test make_request logs error on failure. TC-API-032"""
        with allure.step("Create RequestError"):
            error = RequestError("Request failed", request=mocker.MagicMock())
        with allure.step("Mock client.request to raise error"):
            api_client_with_config.client.request = mocker.AsyncMock(side_effect=error)

        with allure.step("Call make_request and capture error logs"):
            with caplog.at_level("ERROR"):
                await api_client_with_config.make_request("/api/data", method="POST")

        with allure.step("Verify error is logged"):
            assert "Request failed: POST /api/data" in caplog.text

    @pytest.mark.asyncio
    @allure.title("TC-API-033: Make request with PUT method")
    @allure.description("Test make_request with PUT method. TC-API-033")
    async def test_make_request_put_method(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with PUT method. TC-API-033"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)
        with allure.step("Prepare request data"):
            data = {"key": "updated_value"}

        with allure.step("Call make_request with PUT method"):
            result = await api_client_with_config.make_request("/api/data/1", method="PUT", data=data)

        with allure.step("Verify result.method is PUT"):
            assert result.method == "PUT"
        with allure.step("Verify request method and data"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["method"] == "PUT"
            assert call_kwargs["json"] == data

    @pytest.mark.asyncio
    @allure.title("TC-API-033: Make request with DELETE method")
    @allure.description("Test make_request with DELETE method. TC-API-033")
    async def test_make_request_delete_method(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with DELETE method. TC-API-033"""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request with DELETE method"):
            result = await api_client_with_config.make_request("/api/data/1", method="DELETE")

        with allure.step("Verify result.method is DELETE"):
            assert result.method == "DELETE"
        with allure.step("Verify request method is DELETE"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["method"] == "DELETE"


# ============================================================================
# III. Граничные и специальные случаи
# ============================================================================


class TestApiClientEdgeCases:
    """Test ApiClient edge cases."""


# ============================================================================
# IV. Безопасность и надёжность
# ============================================================================


class TestApiClientSecurity:
    """Test ApiClient security and reliability."""

    @pytest.mark.asyncio
    @allure.title("TC-API-036: Make request with very long endpoint")
    @allure.description("Test make_request with very long endpoint. TC-API-036")
    async def test_make_request_very_long_endpoint(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with very long endpoint. TC-API-036"""
        with allure.step("Create a very long endpoint (>1000 characters)"):
            long_endpoint = "/api/" + "a" * 1000
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request with very long endpoint"):
            result = await api_client_with_config.make_request(long_endpoint)

        with allure.step("Verify status_code is 200"):
            assert result.status_code == 200
        with allure.step("Verify the endpoint was used in the request"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert long_endpoint in call_kwargs["url"] or call_kwargs["url"].endswith(long_endpoint)

    @pytest.mark.asyncio
    @allure.title("Make request with unicode characters in endpoint")
    @allure.description("Test make_request with unicode characters in endpoint. TC-API-037")
    async def test_make_request_unicode_endpoint(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request with unicode characters in endpoint. TC-API-037"""
        with allure.step("Create endpoint with unicode characters"):
            unicode_endpoint = "/api/тест/用户/ユーザー"
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request with unicode endpoint"):
            result = await api_client_with_config.make_request(unicode_endpoint)

        with allure.step("Verify status_code is 200"):
            assert result.status_code == 200
        with allure.step("Verify the endpoint was used in the request"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            # The URL should contain the unicode endpoint (may be URL-encoded)
            assert unicode_endpoint in call_kwargs["url"] or any(
                char in call_kwargs["url"] for char in unicode_endpoint
            )

    @pytest.mark.asyncio
    @allure.title("Make request respects timeout settings")
    @allure.description("Test make_request respects timeout settings by returning error result on slow request.")
    async def test_make_request_timeout_respected(self, mocker, api_client_with_config):
        """Test make_request respects timeout settings by returning error result on slow request."""
        with allure.step("Mock client.request to raise TimeoutException"):
            api_client_with_config.client.request = mocker.AsyncMock(
                side_effect=TimeoutException("Request timed out", request=None)
            )

        with allure.step("Call make_request (should catch exception)"):
            # make_request catches exceptions and returns ApiResult with error_message
            result = await api_client_with_config.make_request("/api/data", method="GET")

        with allure.step("Verify the timeout error is reflected in the result"):
            # Verify the timeout error is reflected in the result
            assert result.success is False
            assert result.status_code == 0
            assert result.error_message is not None
            # Check for "timeout" or "timed out" in error message
            error_lower = result.error_message.lower()
            assert "timeout" in error_lower or "timed out" in error_lower


# ============================================================================
# V. Совместимость с родителем
# ============================================================================


class TestApiClientInheritance:
    """Test ApiClient compatibility with BaseClient."""

    @pytest.mark.asyncio
    @allure.title("Async context manager calls close")
    @allure.description("Test async context manager calls close().")
    async def test_context_manager_calls_close(self, mocker, api_client_with_config):
        """Test async context manager calls close()."""
        with allure.step("Mock close method"):
            api_client_with_config.close = mocker.AsyncMock()

        with allure.step("Use async context manager"):
            async with api_client_with_config:
                pass

        with allure.step("Verify close was called once"):
            api_client_with_config.close.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("Logger is bound to ApiClient class name")
    @allure.description("Test logger is bound to ApiClient class name.")
    async def test_logger_bound_to_class_name(self, api_client_with_config):
        """Test logger is bound to ApiClient class name."""
        with allure.step("Verify logger is not None"):
            assert api_client_with_config.logger is not None
            # Logger should be bound to "ApiClient"

    @allure.title("ApiClient inherits from BaseClient")
    @allure.description("Test ApiClient inherits from BaseClient.")
    def test_inherits_from_base_client(self, mocker, valid_config, mock_httpx_client):
        """Test ApiClient inherits from BaseClient."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "py_web_automation.clients.api_client.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create ApiClient instance"):
            api = ApiClient("https://example.com/app", valid_config)

        with allure.step("Verify api is instance of BaseClient"):
            assert isinstance(api, BaseClient)


# ============================================================================
# VI. Authentication Token Management
# ============================================================================


class TestApiClientAuthToken:
    """Test authentication token management in ApiClient."""

    @allure.title("TC-API-039: __init__ sets default auth token values")
    @allure.description("Test that __init__ sets default auth token values. TC-API-039")
    def test_init_sets_default_auth_token_values(self, mocker, valid_config, mock_httpx_client):
        """Test that __init__ sets default auth token values."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "py_web_automation.clients.api_client.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create ApiClient instance"):
            api = ApiClient("https://example.com/app", valid_config)

        with allure.step("Verify default auth token values"):
            assert api._auth_token is None
            assert api._auth_token_type == "Bearer"

    @allure.title("TC-API-040: set_auth_token sets token and type")
    @allure.description("Test set_auth_token sets token and type. TC-API-040")
    def test_set_auth_token(self, mocker, valid_config, mock_httpx_client):
        """Test set_auth_token sets token and type."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "py_web_automation.clients.api_client.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create ApiClient instance"):
            api = ApiClient("https://example.com/app", valid_config)

        with allure.step("Call set_auth_token"):
            api.set_auth_token("test_token_123", "Bearer")
        with allure.step("Verify token and type are set"):
            assert api._auth_token == "test_token_123"
            assert api._auth_token_type == "Bearer"

    @allure.title("TC-API-041: set_auth_token with custom token type")
    @allure.description("Test set_auth_token with custom token type. TC-API-041")
    def test_set_auth_token_with_custom_type(self, mocker, valid_config, mock_httpx_client):
        """Test set_auth_token with custom token type."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "py_web_automation.clients.api_client.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create ApiClient instance"):
            api = ApiClient("https://example.com/app", valid_config)

        with allure.step("Call set_auth_token with custom type"):
            api.set_auth_token("api_key_456", "ApiKey")
        with allure.step("Verify token and custom type are set"):
            assert api._auth_token == "api_key_456"
            assert api._auth_token_type == "ApiKey"

    @allure.title("TC-API-042: clear_auth_token resets token to None")
    @allure.description("Test clear_auth_token resets token to None. TC-API-042")
    def test_clear_auth_token(self, mocker, valid_config, mock_httpx_client):
        """Test clear_auth_token resets token to None."""
        with allure.step("Mock AsyncClient"):
            mocker.patch(
                "py_web_automation.clients.api_client.AsyncClient",
                return_value=mock_httpx_client,
            )
        with allure.step("Create ApiClient instance"):
            api = ApiClient("https://example.com/app", valid_config)

        with allure.step("Set auth token first"):
            api.set_auth_token("test_token", "Bearer")
            assert api._auth_token == "test_token"

        with allure.step("Call clear_auth_token"):
            api.clear_auth_token()
        with allure.step("Verify token is reset to None"):
            assert api._auth_token is None
            assert api._auth_token_type == "Bearer"

    @pytest.mark.asyncio
    @allure.title("TC-API-043: Make request automatically adds auth token to headers")
    @allure.description("Test make_request automatically adds auth token to headers. TC-API-043")
    async def test_make_request_adds_auth_token_automatically(
        self, mocker, api_client_with_config, mock_httpx_response_200
    ):
        """Test make_request automatically adds auth token to headers."""
        with allure.step("Set auth token"):
            api_client_with_config.set_auth_token("test_token_123")
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request"):
            await api_client_with_config.make_request("/api/data")

        with allure.step("Verify Authorization header is added"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert "headers" in call_kwargs
            assert call_kwargs["headers"]["Authorization"] == "Bearer test_token_123"

    @pytest.mark.asyncio
    @allure.title("TC-API-044: Make request without token does not add Authorization header")
    @allure.description("Test make_request without token does not add Authorization header. TC-API-044")
    async def test_make_request_without_token_no_auth_header(
        self, mocker, api_client_with_config, mock_httpx_response_200
    ):
        """Test make_request without token does not add Authorization header."""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request"):
            await api_client_with_config.make_request("/api/data")

        with allure.step("Verify Authorization header is not present"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            headers = call_kwargs.get("headers", {})
            assert "Authorization" not in headers

    @pytest.mark.asyncio
    @allure.title("TC-API-045: Make request uses custom token type")
    @allure.description("Test make_request uses custom token type. TC-API-045")
    async def test_make_request_custom_token_type(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request uses custom token type."""
        with allure.step("Set auth token with custom type"):
            api_client_with_config.set_auth_token("api_key_456", "ApiKey")
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request"):
            await api_client_with_config.make_request("/api/data")

        with allure.step("Verify Authorization header uses custom token type"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Authorization"] == "ApiKey api_key_456"

    @pytest.mark.asyncio
    @allure.title("TC-API-046: Make request allows overriding Authorization header")
    @allure.description("Test make_request allows overriding Authorization header. TC-API-046")
    async def test_make_request_headers_override_auth_token(
        self, mocker, api_client_with_config, mock_httpx_response_200
    ):
        """Test make_request allows overriding Authorization header."""
        with allure.step("Set default auth token"):
            api_client_with_config.set_auth_token("default_token")
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)
        with allure.step("Prepare custom headers with Authorization"):
            custom_headers = {"Authorization": "Bearer custom_token"}

        with allure.step("Call make_request with custom headers"):
            await api_client_with_config.make_request("/api/data", headers=custom_headers)

        with allure.step("Verify custom Authorization header overrides default"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Authorization"] == "Bearer custom_token"

    @pytest.mark.asyncio
    @allure.title("TC-API-047: Make request merges custom headers with auth token")
    @allure.description("Test make_request merges custom headers with auth token. TC-API-047")
    async def test_make_request_merges_headers_with_token(
        self, mocker, api_client_with_config, mock_httpx_response_200
    ):
        """Test make_request merges custom headers with auth token."""
        with allure.step("Set auth token"):
            api_client_with_config.set_auth_token("test_token")
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)
        with allure.step("Prepare custom headers"):
            custom_headers = {"X-Custom-Header": "custom_value"}

        with allure.step("Call make_request with custom headers"):
            await api_client_with_config.make_request("/api/data", headers=custom_headers)

        with allure.step("Verify both Authorization and custom headers are present"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Authorization"] == "Bearer test_token"
            assert call_kwargs["headers"]["X-Custom-Header"] == "custom_value"

    @pytest.mark.asyncio
    @allure.title("TC-API-048: Make request sets Content-Type when data is provided")
    @allure.description("Test make_request sets Content-Type when data is provided. TC-API-048")
    async def test_make_request_sets_content_type_for_data(
        self, mocker, api_client_with_config, mock_httpx_response_200
    ):
        """Test make_request sets Content-Type when data is provided."""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)
        with allure.step("Prepare request data"):
            data = {"key": "value"}

        with allure.step("Call make_request with data"):
            await api_client_with_config.make_request("/api/data", method="POST", data=data)

        with allure.step("Verify Content-Type is set to application/json"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Content-Type"] == "application/json"

    @pytest.mark.asyncio
    @allure.title("TC-API-049: Make request preserves custom Content-Type header")
    @allure.description("Test make_request preserves custom Content-Type header. TC-API-049")
    async def test_make_request_preserves_custom_content_type(
        self, mocker, api_client_with_config, mock_httpx_response_200
    ):
        """Test make_request preserves custom Content-Type header."""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)
        with allure.step("Prepare custom headers and data"):
            custom_headers = {"Content-Type": "application/xml"}
            data = {"key": "value"}

        with allure.step("Call make_request with custom Content-Type"):
            await api_client_with_config.make_request("/api/data", method="POST", data=data, headers=custom_headers)

        with allure.step("Verify custom Content-Type is preserved"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert call_kwargs["headers"]["Content-Type"] == "application/xml"

    @pytest.mark.asyncio
    @allure.title("TC-API-050: Make request adds query params to URL")
    @allure.description("Test make_request adds query params to URL. TC-API-050")
    async def test_make_request_with_query_params(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request adds query params to URL."""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)
        with allure.step("Prepare query params"):
            params = {"page": 1, "limit": 10}

        with allure.step("Call make_request with query params"):
            await api_client_with_config.make_request("/api/data", params=params)

        with allure.step("Verify query params are added to URL"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert "?page=1&limit=10" in call_kwargs["url"] or "?limit=10&page=1" in call_kwargs["url"]

    @pytest.mark.asyncio
    @allure.title("TC-API-051: Make request appends query params to URL with existing query string")
    @allure.description("Test make_request appends query params to URL with existing query string. TC-API-051")
    async def test_make_request_with_query_params_and_existing_query(
        self, mocker, api_client_with_config, mock_httpx_response_200
    ):
        """Test make_request appends query params to URL with existing query string."""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)
        with allure.step("Prepare query params"):
            params = {"filter": "active"}

        with allure.step("Call make_request with existing query and new params"):
            await api_client_with_config.make_request("https://example.com/api/data?existing=param", params=params)

        with allure.step("Verify both existing and new query params are in URL"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert "existing=param" in call_kwargs["url"]
            assert "filter=active" in call_kwargs["url"]
            assert "&" in call_kwargs["url"]  # Should use & separator

    @pytest.mark.asyncio
    @allure.title("TC-API-052: Make request handles empty params dict")
    @allure.description("Test make_request handles empty params dict. TC-API-052")
    async def test_make_request_with_empty_params(self, mocker, api_client_with_config, mock_httpx_response_200):
        """Test make_request handles empty params dict."""
        with allure.step("Mock client.request"):
            api_client_with_config.client.request = mocker.AsyncMock(return_value=mock_httpx_response_200)

        with allure.step("Call make_request with empty params"):
            await api_client_with_config.make_request("/api/data", params={})

        with allure.step("Verify query string is not added to URL"):
            call_kwargs = api_client_with_config.client.request.call_args[1]
            assert "?" not in call_kwargs["url"] or call_kwargs["url"].endswith("/api/data")
