"""
Fixtures for ApiClient testing.
"""

# Python imports
from __future__ import annotations
from datetime import timedelta
from typing import Any, Callable, TYPE_CHECKING
from httpx import Response
from pytest import fixture
from pytest_mock import MockerFixture

# Local imports
from py_web_automation.clients.api_clients.http_client import HttpClient
from py_web_automation.config import Config

if TYPE_CHECKING:
    from py_web_automation.clients.api_clients.graphql_client import GraphQLClient


@fixture
def valid_config() -> Config:
    """Create a valid Config instance."""
    return Config(
        base_url="https://example.com",
        timeout=30,
        retry_count=3,
        retry_delay=1.0,
        log_level="DEBUG",
        browser_headless=True,
        browser_timeout=30000,
    )


@fixture
def mock_httpx_response_200(mocker: MockerFixture) -> Response:
    """Create a mock httpx.Response with status 200."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 200
    response.elapsed = timedelta(seconds=0.5)
    response.is_informational = False
    response.is_success = True
    response.is_redirect = False
    response.is_client_error = False
    response.is_server_error = False
    response.content = b'{"test": "data"}'
    response.headers = {"Content-Type": "application/json", "Content-Length": "15"}
    response.reason_phrase = "OK"
    return response


@fixture
def mock_httpx_response_301(mocker: MockerFixture) -> Response:
    """Create a mock httpx.Response with status 301."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 301
    response.elapsed = timedelta(seconds=0.1)
    response.is_informational = False
    response.is_success = False
    response.is_redirect = True
    response.is_client_error = False
    response.is_server_error = False
    response.content = b"Redirect"
    response.headers = {"Location": "https://example.com/new"}
    response.reason_phrase = "Moved Permanently"
    return response


@fixture
def mock_httpx_response_404(mocker: MockerFixture) -> Response:
    """Create a mock httpx.Response with status 404."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 404
    response.elapsed = timedelta(seconds=0.2)
    response.is_informational = False
    response.is_success = False
    response.is_redirect = False
    response.is_client_error = True
    response.is_server_error = False
    response.content = b"Not Found"
    response.headers = {"Content-Type": "text/plain"}
    response.reason_phrase = "Not Found"
    return response


@fixture
def mock_httpx_response_500(mocker: MockerFixture) -> Response:
    """Create a mock httpx.Response with status 500."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 500
    response.elapsed = timedelta(seconds=1.0)
    response.is_informational = False
    response.is_success = False
    response.is_redirect = False
    response.is_client_error = False
    response.is_server_error = True
    response.content = b"Internal Server Error"
    response.headers = {"Content-Type": "text/plain"}
    response.reason_phrase = "Internal Server Error"
    return response


@fixture
def mock_httpx_response_101(mocker: MockerFixture) -> Response:
    """Create a mock httpx.Response with status 101."""
    response = mocker.MagicMock(spec=Response)
    response.status_code = 101
    response.elapsed = timedelta(seconds=0.05)
    response.is_informational = True
    response.is_success = False
    response.is_redirect = False
    response.is_client_error = False
    response.is_server_error = False
    response.content = b"Switching Protocols"
    response.headers = {"Upgrade": "websocket"}
    response.reason_phrase = "Switching Protocols"
    return response


@fixture
def mock_httpx_client(mocker: MockerFixture) -> Any:
    """Create a mock httpx.AsyncClient instance."""
    client = mocker.AsyncMock()
    client.aclose = mocker.AsyncMock()
    client.request = mocker.AsyncMock()
    return client


@fixture
def api_client_with_config(mocker: MockerFixture, valid_config: Config, mock_httpx_client: Any) -> HttpClient:
    """
    Create HttpClient with valid config and mocked httpx client.
    
    Patches AsyncClient to prevent real HTTP connections and potential memory leaks.
    The patch ensures that when HttpClient.__init__ creates AsyncClient (line 90),
    it returns our mock instead of a real HTTP client.
    Automatically cleans up after test execution.
    """
    mocker.patch(
        "py_web_automation.clients.api_clients.http_client.http_client.AsyncClient",
        return_value=mock_httpx_client,
    )
    api = HttpClient("https://example.com/app", valid_config)
    yield api
    try:
        if hasattr(api, "_middleware"):
            api._middleware = None
    except Exception:
        pass


@fixture
def mock_graphql_execute_operation(
    mocker: MockerFixture
) -> Callable[[GraphQLClient, dict | None, Exception | None], None]:
    """
    Mock fixture for GraphQL _execute_operation method.
    
    Returns a function that mocks the _execute_operation method on a GraphQLClient instance.
    Usage:
        mock_execute = mock_graphql_execute_operation
        mock_execute(client, return_data={"users": []})
        # or
        mock_execute(client, side_effect=GraphQLError("Error"))
    """

    def _mock_execute_operation(
        client: GraphQLClient,
        return_data: dict | None = None,
        side_effect: Exception | None = None
    ) -> None:
        """Mock GraphQL _execute_operation method using mocker."""
        if side_effect:
            client._execute_operation = mocker.AsyncMock(side_effect=side_effect)  # type: ignore[method-assign]
        else:
            # Preserve None values instead of converting to {}
            client._execute_operation = mocker.AsyncMock(return_value=return_data)  # type: ignore[method-assign]
        client._ensure_session = mocker.AsyncMock()  # type: ignore[method-assign]
        if not hasattr(client._transport, "headers"):
            client._transport.headers = {}  # type: ignore[attr-defined]
        return client._execute_operation
    
    return _mock_execute_operation
