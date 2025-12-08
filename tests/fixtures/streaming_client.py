"""
Fixtures for integration and unit test mocks.
Provides reusable mock objects for HTTP responses, WebSocket connections, etc.
"""

from pytest import fixture
from pytest_mock import MockerFixture


@fixture
def mock_websocket_connection(mocker: MockerFixture) -> MockerFixture:
    """Create a mock WebSocket connection."""
    mock_ws = mocker.AsyncMock()
    mock_ws.send = mocker.AsyncMock()
    mock_ws.recv = mocker.AsyncMock(
        side_effect=[
            '{"type": "ack", "message": "received"}',
            '{"type": "response", "data": "test"}',
        ]
    )
    mock_ws.close = mocker.AsyncMock()
    mock_ws.__aenter__ = mocker.AsyncMock(return_value=mock_ws)
    mock_ws.__aexit__ = mocker.AsyncMock(return_value=None)
    return mock_ws
