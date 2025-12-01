"""
Fixtures for integration and unit test mocks.
Provides reusable mock objects for HTTP responses, WebSocket connections, etc.
"""

from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock

from pytest import fixture


@fixture
def mock_soap_response_200(mocker):
    """Create a mock SOAP HTTP response with status 200."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetUserResponse><id>1</id><name>John Doe</name></GetUserResponse></soap:Body></soap:Envelope>'
    mock_response.headers = {"Content-Type": "text/xml"}
    return mock_response


@fixture
def mock_soap_response_500(mocker):
    """Create a mock SOAP HTTP response with status 500 (fault)."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = False
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = True
    mock_response.content = b'<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><soap:Fault><faultcode>Server</faultcode><faultstring>Internal server error</faultstring><detail>Error processing request</detail></soap:Fault></soap:Body></soap:Envelope>'
    mock_response.headers = {"Content-Type": "text/xml"}
    return mock_response


@fixture
def mock_soap_response_authenticated(mocker):
    """Create a mock SOAP HTTP response for authenticated requests."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><AuthenticatedResponse><status>success</status></AuthenticatedResponse></soap:Body></soap:Envelope>'
    mock_response.headers = {"Content-Type": "text/xml"}
    return mock_response


@fixture
def mock_graphql_response_200(mocker):
    """Create a mock GraphQL HTTP response with status 200."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'{"data": {"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}}'
    mock_response.headers = {"Content-Type": "application/json"}
    return mock_response


@fixture
def mock_graphql_response_with_errors(mocker):
    """Create a mock GraphQL HTTP response with errors."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'{"errors": [{"message": "Field not found", "path": ["users", "invalidField"]}, {"message": "Access denied", "path": ["users"]}], "data": null}'
    mock_response.headers = {"Content-Type": "application/json"}
    return mock_response


@fixture
def mock_graphql_response_authenticated(mocker):
    """Create a mock GraphQL HTTP response for authenticated requests."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'{"data": {"authenticatedUser": {"id": 1, "name": "John", "role": "admin"}}}'
    mock_response.headers = {"Content-Type": "application/json"}
    return mock_response


@fixture
def mock_http_response_200_json(mocker):
    """Create a mock HTTP response with status 200 and JSON content."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'{"data": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]}'
    mock_response.headers = {"Content-Type": "application/json", "X-Total-Count": "2"}
    return mock_response


@fixture
def mock_http_response_200_simple(mocker):
    """Create a simple mock HTTP response with status 200."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'{"status": "ok"}'
    mock_response.headers = {"Content-Type": "application/json"}
    return mock_response


@fixture
def mock_http_response_user_data(mocker):
    """Create a mock HTTP response with user data."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'{"user": {"id": 1, "name": "John", "authenticated": true}}'
    mock_response.headers = {"Content-Type": "application/json"}
    return mock_response


@fixture
def mock_websocket_connection(mocker):
    """Create a mock WebSocket connection."""
    mock_ws = AsyncMock()
    mock_ws.send = AsyncMock()
    mock_ws.recv = AsyncMock(
        side_effect=[
            '{"type": "ack", "message": "received"}',
            '{"type": "response", "data": "test"}',
        ]
    )
    mock_ws.close = AsyncMock()
    mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = AsyncMock(return_value=None)
    return mock_ws


@fixture
def mock_websocket_connection_multiple_messages(mocker):
    """Create a mock WebSocket connection with multiple messages."""
    messages = [
        '{"type": "message", "id": 1}',
        '{"type": "message", "id": 2}',
        '{"type": "message", "id": 3}',
        '{"type": "close"}',
    ]
    message_index = [0]

    mock_ws = AsyncMock()
    mock_ws.recv = AsyncMock(
        side_effect=lambda: messages[message_index[0]] if message_index[0] < len(messages) else None
    )
    mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = AsyncMock(return_value=None)
    return mock_ws


@fixture
def mock_websocket_connection_ping(mocker):
    """Create a mock WebSocket connection for ping handler test."""
    mock_ws = AsyncMock()
    mock_ws.recv = AsyncMock(return_value='{"type": "ping", "timestamp": 1234567890}')
    mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = AsyncMock(return_value=None)
    return mock_ws


@fixture
def mock_websocket_connection_order(mocker):
    """Create a mock WebSocket connection for order message."""
    mock_ws = AsyncMock()
    mock_ws.recv = AsyncMock(return_value='{"type": "order", "id": 123, "amount": 99.99, "customer": "John"}')
    mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = AsyncMock(return_value=None)
    return mock_ws


@fixture
def mock_graphql_response_users(mocker):
    """Create a mock GraphQL response with users data."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'{"data": {"users": [{"id": 1, "name": "John", "email": "john@example.com"}]}}'
    mock_response.headers = {"Content-Type": "application/json"}
    return mock_response


@fixture
def mock_soap_response_products(mocker):
    """Create a mock SOAP response with products data."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetProductsResponse><products><product><id>1</id><name>Product 1</name><price>100</price></product><product><id>2</id><name>Product 2</name><price>200</price></product></products></GetProductsResponse></soap:Body></soap:Envelope>'
    mock_response.headers = {"Content-Type": "text/xml"}
    return mock_response


@fixture
def mock_http_response_user_validation(mocker):
    """Create a mock HTTP response for user validation."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.elapsed = timedelta(seconds=0.2)
    mock_response.is_success = True
    mock_response.is_informational = False
    mock_response.is_redirect = False
    mock_response.is_client_error = False
    mock_response.is_server_error = False
    mock_response.content = b'{"id": 1, "name": "John", "email": "john@example.com", "active": true}'
    mock_response.headers = {"Content-Type": "application/json"}
    return mock_response
