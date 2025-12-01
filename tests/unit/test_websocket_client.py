"""
Unit tests for WebSocketClient.
"""

import builtins
from unittest.mock import AsyncMock

import allure
import pytest

from py_web_automation.clients.websocket_client import WebSocketClient
from py_web_automation.exceptions import ConnectionError, OperationError, TimeoutError

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit, pytest.mark.websocket]


class TestWebSocketClient:
    """Test WebSocketClient class."""

    @pytest.mark.asyncio
    @allure.title("TC-WS-001: Initialize WebSocketClient")
    @allure.description("Test WebSocketClient initialization. TC-WS-001")
    async def test_init(self, valid_config):
        """Test WebSocketClient initialization."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)
        assert client.url == url
        assert client.config == valid_config

    @pytest.mark.asyncio
    @allure.title("TC-WS-002: Connect to WebSocket")
    @allure.description("Test connecting to WebSocket. TC-WS-002")
    async def test_connect(self, mocker, valid_config):
        """Test connecting to WebSocket."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        # Mock websocket connection - connect returns an async context manager
        mock_ws = AsyncMock()
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)

        # Mock the connect function to return async context manager
        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()
        assert await client.is_connected() is True

    @pytest.mark.asyncio
    @allure.title("TC-WS-003: Send message")
    @allure.description("Test sending message via WebSocket. TC-WS-003")
    async def test_send(self, mocker, valid_config):
        """Test sending message via WebSocket."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        # Mock websocket connection
        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock()
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()
        await client.send_message('{"type": "test", "data": "message"}')

        mock_ws.send.assert_called_once()

    @pytest.mark.asyncio
    @allure.title("TC-WS-004: Receive message")
    @allure.description("Test receiving message via WebSocket. TC-WS-004")
    async def test_receive(self, mocker, valid_config):
        """Test receiving message via WebSocket."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        # Mock websocket connection
        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(return_value='{"type": "response", "data": "test"}')
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()
        message = await client.receive_message()

        # receive_message parses JSON and returns dict
        assert message == {"type": "response", "data": "test"}

    @pytest.mark.asyncio
    @allure.title("TC-WS-005: Disconnect from WebSocket")
    @allure.description("Test disconnecting from WebSocket. TC-WS-005")
    async def test_disconnect(self, mocker, valid_config):
        """Test disconnecting from WebSocket."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        # Mock websocket connection
        mock_ws = AsyncMock()
        mock_ws.close = AsyncMock()
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()
        await client.disconnect()

        assert await client.is_connected() is False

    @pytest.mark.asyncio
    @allure.title("TC-WS-006: Context manager support")
    @allure.description("Test WebSocketClient as context manager. TC-WS-006")
    async def test_context_manager(self, mocker, valid_config):
        """Test WebSocketClient as context manager."""
        url = "ws://localhost:8080/ws"
        # Mock websocket connection
        mock_ws = AsyncMock()
        mock_ws.__aenter__ = AsyncMock(return_value=mock_ws)
        mock_ws.__aexit__ = AsyncMock(return_value=None)

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        async with WebSocketClient(url, valid_config) as client:
            assert client.url == url
            assert client.config == valid_config

    @pytest.mark.asyncio
    @allure.title("TC-WS-007: send_message с dict конвертирует в JSON")
    @allure.description("Test send_message with dict converts to JSON. TC-WS-007")
    async def test_send_message_with_dict(self, mocker, valid_config, mock_websocket_connection):
        """Test send_message with dict converts to JSON."""
        with allure.step("Подготовка WebSocket клиента"):
            url = "ws://localhost:8080/ws"
            client = WebSocketClient(url, valid_config)

        with allure.step("Мокирование WebSocket соединения"):

            async def mock_connect(*args, **kwargs):
                return mock_websocket_connection

            mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        with allure.step("Подключение к WebSocket"):
            await client.connect()

        with allure.step("Отправка сообщения с dict"):
            await client.send_message({"type": "test", "data": "message"})

        with allure.step("Проверка что JSON был отправлен"):
            call_args = mock_websocket_connection.send.call_args
            sent_message = call_args[0][0]
            assert '"type": "test"' in sent_message
            assert '"data": "message"' in sent_message

    @pytest.mark.asyncio
    @allure.title("TC-WS-008: send_message с str отправляет как есть")
    @allure.description("Test send_message with str sends as-is. TC-WS-008")
    async def test_send_message_with_str(self, mocker, valid_config, mock_websocket_connection):
        """Test send_message with str sends as-is."""
        with allure.step("Подготовка WebSocket клиента"):
            url = "ws://localhost:8080/ws"
            client = WebSocketClient(url, valid_config)

        with allure.step("Мокирование WebSocket соединения"):

            async def mock_connect(*args, **kwargs):
                return mock_websocket_connection

            mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        with allure.step("Подключение к WebSocket"):
            await client.connect()

        with allure.step("Отправка сообщения со строкой"):
            message_str = '{"type": "test", "data": "message"}'
            await client.send_message(message_str)

        with allure.step("Проверка что строка была отправлена как есть"):
            call_args = mock_websocket_connection.send.call_args
            assert call_args[0][0] == message_str

    @pytest.mark.asyncio
    @allure.title("TC-WS-009: send_message выбрасывает ConnectionError если не подключен")
    @allure.description("Test send_message raises ConnectionError if not connected. TC-WS-009")
    async def test_send_message_not_connected(self, valid_config):
        """Test send_message raises ConnectionError if not connected."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        with pytest.raises(ConnectionError, match="Not connected"):
            await client.send_message("test message")

    @pytest.mark.asyncio
    @allure.title("TC-WS-010: send_message обрабатывает ошибки отправки")
    @allure.description("Test send_message handles send errors. TC-WS-010")
    async def test_send_message_handles_errors(self, mocker, valid_config):
        """Test send_message handles send errors."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.send = AsyncMock(side_effect=Exception("Send failed"))

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()

        with pytest.raises(OperationError, match="Failed to send message"):
            await client.send_message("test message")

    @pytest.mark.asyncio
    @allure.title("TC-WS-011: receive_message с timeout параметром")
    @allure.description("Test receive_message with timeout parameter. TC-WS-011")
    async def test_receive_message_with_timeout(self, mocker, valid_config):
        """Test receive_message with timeout parameter."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(return_value='{"type": "response"}')

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()
        message = await client.receive_message(timeout=5.0)

        assert message == {"type": "response"}

    @pytest.mark.asyncio
    @allure.title("TC-WS-012: receive_message парсит JSON сообщения")
    @allure.description("Test receive_message parses JSON messages. TC-WS-012")
    async def test_receive_message_parses_json(self, mocker, valid_config):
        """Test receive_message parses JSON messages."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(return_value='{"type": "test", "id": 123}')

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()
        message = await client.receive_message()

        assert isinstance(message, dict)
        assert message["type"] == "test"
        assert message["id"] == 123

    @pytest.mark.asyncio
    @allure.title("TC-WS-013: receive_message возвращает plain text для не-JSON")
    @allure.description("Test receive_message returns plain text for non-JSON. TC-WS-013")
    async def test_receive_message_plain_text(self, mocker, valid_config):
        """Test receive_message returns plain text for non-JSON."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(return_value="plain text message")

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()
        message = await client.receive_message()

        assert message == "plain text message"
        assert isinstance(message, str)

    @pytest.mark.asyncio
    @allure.title("TC-WS-014: receive_message выбрасывает TimeoutError при таймауте")
    @allure.description("Test receive_message raises TimeoutError on timeout. TC-WS-014")
    async def test_receive_message_timeout(self, mocker, valid_config):
        """Test receive_message raises TimeoutError on timeout."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(side_effect=builtins.TimeoutError())

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()

        with pytest.raises(TimeoutError, match="Timeout waiting for message"):
            await client.receive_message(timeout=0.1)

    @pytest.mark.asyncio
    @allure.title("TC-WS-015: receive_message выбрасывает ConnectionError если не подключен")
    @allure.description("Test receive_message raises ConnectionError if not connected. TC-WS-015")
    async def test_receive_message_not_connected(self, valid_config):
        """Test receive_message raises ConnectionError if not connected."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        with pytest.raises(ConnectionError, match="Not connected"):
            await client.receive_message()

    @pytest.mark.asyncio
    @allure.title("TC-WS-016: receive_message обрабатывает ошибки получения")
    @allure.description("Test receive_message handles receive errors. TC-WS-016")
    async def test_receive_message_handles_errors(self, mocker, valid_config):
        """Test receive_message handles receive errors."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(side_effect=Exception("Receive failed"))

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()

        with pytest.raises(OperationError, match="Failed to receive message"):
            await client.receive_message()

    @pytest.mark.asyncio
    @allure.title("TC-WS-017: listen возвращает async iterator")
    @allure.description("Test listen returns async iterator. TC-WS-017")
    async def test_listen_returns_iterator(self, mocker, valid_config):
        """Test listen returns async iterator."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(side_effect=['{"type": "msg1"}', '{"type": "msg2"}', StopAsyncIteration()])

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()

        messages = []
        async for message in client.listen():
            messages.append(message)
            if len(messages) >= 2:
                break

        assert len(messages) >= 1

    @pytest.mark.asyncio
    @allure.title("TC-WS-018: listen вызывает handler для каждого сообщения")
    @allure.description("Test listen calls handler for each message. TC-WS-018")
    async def test_listen_calls_handler(self, mocker, valid_config):
        """Test listen calls handler for each message."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(return_value='{"type": "test"}')

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()

        handler_calls = []

        def handler(message):
            handler_calls.append(message)

        async def collect_messages():
            count = 0
            async for _message in client.listen(handler=handler):
                count += 1
                if count >= 2:
                    break

        await collect_messages()

        assert len(handler_calls) >= 1

    @pytest.mark.asyncio
    @allure.title("TC-WS-019: listen выбрасывает ConnectionError если не подключен")
    @allure.description("Test listen raises ConnectionError if not connected. TC-WS-019")
    async def test_listen_not_connected(self, valid_config):
        """Test listen raises ConnectionError if not connected."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        with pytest.raises(ConnectionError, match="Not connected"):
            async for _ in client.listen():
                pass

    @pytest.mark.asyncio
    @allure.title("TC-WS-020: listen обрабатывает ошибки в handler")
    @allure.description("Test listen handles errors in handler. TC-WS-020")
    async def test_listen_handles_handler_errors(self, mocker, valid_config):
        """Test listen handles errors in handler."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(return_value='{"type": "test"}')

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()

        def handler(message):
            raise Exception("Handler error")

        with pytest.raises(OperationError, match="Error in WebSocket listener"):
            async for _ in client.listen(handler=handler):
                break

    @pytest.mark.asyncio
    @allure.title("TC-WS-021: listen останавливается при disconnect")
    @allure.description("Test listen stops on disconnect. TC-WS-021")
    async def test_listen_stops_on_disconnect(self, mocker, valid_config):
        """Test listen stops on disconnect."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.recv = AsyncMock(return_value='{"type": "test"}')

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()

        messages_received = []

        async def collect():
            async for message in client.listen():
                messages_received.append(message)
                if len(messages_received) >= 1:
                    await client.disconnect()
                    break

        await collect()

        assert len(messages_received) >= 1

    @pytest.mark.asyncio
    @allure.title("TC-WS-022: register_handler регистрирует handler")
    @allure.description("Test register_handler registers handler. TC-WS-022")
    async def test_register_handler(self, valid_config):
        """Test register_handler registers handler."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        def handler(message):
            pass

        client.register_handler("test_type", handler)

        assert "test_type" in client._message_handlers
        assert client._message_handlers["test_type"] == handler

    @pytest.mark.asyncio
    @allure.title("TC-WS-023: register_handler перезаписывает существующий handler")
    @allure.description("Test register_handler overwrites existing handler. TC-WS-023")
    async def test_register_handler_overwrites(self, valid_config):
        """Test register_handler overwrites existing handler."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        def handler1(message):
            pass

        def handler2(message):
            pass

        client.register_handler("test_type", handler1)
        assert client._message_handlers["test_type"] == handler1

        client.register_handler("test_type", handler2)
        assert client._message_handlers["test_type"] == handler2

    @pytest.mark.asyncio
    @allure.title("TC-WS-024: close очищает message_handlers")
    @allure.description("Test close clears message_handlers. TC-WS-024")
    async def test_close_clears_handlers(self, mocker, valid_config):
        """Test close clears message_handlers."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        def handler(message):
            pass

        client.register_handler("test_type", handler)
        assert len(client._message_handlers) > 0

        mock_ws = AsyncMock()
        mock_ws.close = AsyncMock()

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()
        await client.close()

        assert len(client._message_handlers) == 0

    @pytest.mark.asyncio
    @allure.title("TC-WS-025: connect обрабатывает WebSocketException")
    @allure.description("Test connect handles WebSocketException. TC-WS-025")
    async def test_connect_handles_websocket_exception(self, mocker, valid_config):
        """Test connect handles WebSocketException."""
        from websockets.exceptions import WebSocketException

        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mocker.patch(
            "py_web_automation.clients.websocket_client.connect", side_effect=WebSocketException("Connection failed")
        )

        with pytest.raises(ConnectionError, match="Failed to connect"):
            await client.connect()

    @pytest.mark.asyncio
    @allure.title("TC-WS-026: connect обрабатывает общие Exception")
    @allure.description("Test connect handles general Exception. TC-WS-026")
    async def test_connect_handles_general_exception(self, mocker, valid_config):
        """Test connect handles general Exception."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=Exception("Unexpected error"))

        with pytest.raises(ConnectionError, match="Unexpected error connecting"):
            await client.connect()

    @pytest.mark.asyncio
    @allure.title("TC-WS-027: connect не переподключается если уже подключен")
    @allure.description("Test connect does not reconnect if already connected. TC-WS-027")
    async def test_connect_already_connected(self, mocker, valid_config):
        """Test connect does not reconnect if already connected."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()

        async def mock_connect(*args, **kwargs):
            return mock_ws

        connect_mock = mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        await client.connect()
        assert await client.is_connected() is True

        # Try to connect again
        await client.connect()

        # connect should only be called once
        assert connect_mock.call_count == 1

    @pytest.mark.asyncio
    @allure.title("TC-WS-028: __aenter__ вызывает connect")
    @allure.description("Test __aenter__ calls connect. TC-WS-028")
    async def test_aenter_calls_connect(self, mocker, valid_config):
        """Test __aenter__ calls connect."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()

        async def mock_connect(*args, **kwargs):
            return mock_ws

        connect_mock = mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        async with client:
            assert await client.is_connected() is True

        assert connect_mock.called

    @pytest.mark.asyncio
    @allure.title("TC-WS-029: __aexit__ вызывает close")
    @allure.description("Test __aexit__ calls close. TC-WS-029")
    async def test_aexit_calls_close(self, mocker, valid_config):
        """Test __aexit__ calls close."""
        url = "ws://localhost:8080/ws"
        client = WebSocketClient(url, valid_config)

        mock_ws = AsyncMock()
        mock_ws.close = AsyncMock()

        async def mock_connect(*args, **kwargs):
            return mock_ws

        mocker.patch("py_web_automation.clients.websocket_client.connect", side_effect=mock_connect)

        async with client:
            pass

        # close should have been called, which calls disconnect
        assert await client.is_connected() is False
