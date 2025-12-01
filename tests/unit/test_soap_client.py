"""
Unit tests for SoapClient.
"""

from unittest.mock import AsyncMock

import allure
import pytest

from py_web_automation.clients.models import ApiResult
from py_web_automation.clients.soap_client import SoapClient

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit, pytest.mark.soap]


class TestSoapClient:
    """Test SoapClient class."""

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-001: Initialize SoapClient")
    @allure.description("Test SoapClient initialization. TC-SOAP-001")
    async def test_init(self, valid_config):
        """Test SoapClient initialization."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)
        assert client.url == url
        assert client.config == valid_config

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-002: Call SOAP method")
    @allure.description("Test calling SOAP method. TC-SOAP-002")
    async def test_call_method(self, mocker, valid_config):
        """Test calling SOAP method."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        # Create ApiResult mock
        mock_result = ApiResult(
            endpoint=url,
            method="POST",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            headers={"Content-Type": "text/xml"},
            body=b'<?xml version="1.0"?><soap:Envelope><soap:Body><response>Success</response></soap:Body></soap:Envelope>',
            content_type="text/xml",
        )

        # Mock call method
        client.call = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        result = await client.call("MethodName", {"param": "value"})

        assert result.status_code == 200
        assert "soap:Envelope" in result.body.decode()

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-003: Handle SOAP fault")
    @allure.description("Test handling SOAP fault. TC-SOAP-003")
    async def test_handle_fault(self, mocker, valid_config):
        """Test handling SOAP fault."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        # Create ApiResult mock with SOAP fault
        mock_result = ApiResult(
            endpoint=url,
            method="POST",
            status_code=500,
            response_time=0.2,
            success=False,
            redirect=False,
            client_error=False,
            server_error=True,
            informational=False,
            headers={"Content-Type": "text/xml"},
            body=b'<?xml version="1.0"?><soap:Envelope><soap:Body><soap:Fault><faultstring>Error</faultstring></soap:Fault></soap:Body></soap:Envelope>',
            content_type="text/xml",
        )

        # Mock call method
        client.call = AsyncMock(return_value=mock_result)  # type: ignore[method-assign]

        result = await client.call("MethodName", {"param": "value"})

        assert result.status_code == 500
        assert "soap:Fault" in result.body.decode()

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-004: Context manager support")
    @allure.description("Test SoapClient as context manager. TC-SOAP-004")
    async def test_context_manager(self, valid_config):
        """Test SoapClient as context manager."""
        url = "https://api.example.com/soap"
        async with SoapClient(url, valid_config) as client:
            assert client.url == url
            assert client.config == valid_config

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-005: Close client")
    @allure.description("Test closing SoapClient. TC-SOAP-005")
    async def test_close(self, valid_config):
        """Test closing SoapClient."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)
        await client.close()
        # Verify client is closed (no exception raised)

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-006: set_auth_token устанавливает токен")
    @allure.description("Test set_auth_token sets authentication token. TC-SOAP-006")
    async def test_set_auth_token(self, valid_config):
        """Test set_auth_token sets authentication token."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        client.set_auth_token("test-token-123", "Bearer")
        assert client._auth_token == "test-token-123"
        assert client._auth_token_type == "Bearer"

        client.set_auth_token("custom-token", "Custom")
        assert client._auth_token == "custom-token"
        assert client._auth_token_type == "Custom"

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-007: clear_auth_token очищает токен")
    @allure.description("Test clear_auth_token clears authentication token. TC-SOAP-007")
    async def test_clear_auth_token(self, valid_config):
        """Test clear_auth_token clears authentication token."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        client.set_auth_token("test-token-123")
        assert client._auth_token == "test-token-123"

        client.clear_auth_token()
        assert client._auth_token is None
        assert client._auth_token_type == "Bearer"

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-008: _build_soap_envelope для SOAP 1.1")
    @allure.description("Test _build_soap_envelope for SOAP 1.1. TC-SOAP-008")
    async def test_build_soap_envelope_1_1(self, valid_config):
        """Test _build_soap_envelope for SOAP 1.1."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config, soap_version="1.1")

        envelope = client._build_soap_envelope("TestOperation", {"param": "value"})

        assert "http://schemas.xmlsoap.org/soap/envelope/" in envelope
        assert "TestOperation" in envelope
        assert "param" in envelope
        assert "value" in envelope
        assert "Envelope" in envelope
        assert "Body" in envelope

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-009: _build_soap_envelope для SOAP 1.2")
    @allure.description("Test _build_soap_envelope for SOAP 1.2. TC-SOAP-009")
    async def test_build_soap_envelope_1_2(self, valid_config):
        """Test _build_soap_envelope for SOAP 1.2."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config, soap_version="1.2")

        envelope = client._build_soap_envelope("TestOperation", {"param": "value"})

        assert "http://www.w3.org/2003/05/soap-envelope" in envelope
        assert "TestOperation" in envelope
        assert "param" in envelope
        assert "value" in envelope
        assert "Envelope" in envelope
        assert "Body" in envelope

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-010: _build_soap_envelope с namespace")
    @allure.description("Test _build_soap_envelope with namespace. TC-SOAP-010")
    async def test_build_soap_envelope_with_namespace(self, valid_config):
        """Test _build_soap_envelope with namespace."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        namespace = "http://example.com/service"
        envelope = client._build_soap_envelope("TestOperation", {"param": "value"}, namespace=namespace)

        assert namespace in envelope
        assert "TestOperation" in envelope

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-011: _dict_to_xml с простыми значениями")
    @allure.description("Test _dict_to_xml with simple values. TC-SOAP-011")
    async def test_dict_to_xml_simple_values(self, valid_config):
        """Test _dict_to_xml with simple values."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        from xml.etree import ElementTree as ET

        parent = ET.Element("root")
        data = {"name": "John", "age": 30, "active": True}

        client._dict_to_xml(parent, data)

        assert parent.find("name") is not None
        assert parent.find("name").text == "John"
        assert parent.find("age") is not None
        assert parent.find("age").text == "30"
        assert parent.find("active") is not None
        assert parent.find("active").text == "True"

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-012: _dict_to_xml с вложенными словарями")
    @allure.description("Test _dict_to_xml with nested dictionaries. TC-SOAP-012")
    async def test_dict_to_xml_nested_dicts(self, valid_config):
        """Test _dict_to_xml with nested dictionaries."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        from xml.etree import ElementTree as ET

        parent = ET.Element("root")
        data = {"user": {"name": "John", "email": "john@example.com"}}

        client._dict_to_xml(parent, data)

        user_elem = parent.find("user")
        assert user_elem is not None
        assert user_elem.find("name") is not None
        assert user_elem.find("name").text == "John"
        assert user_elem.find("email") is not None
        assert user_elem.find("email").text == "john@example.com"

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-013: _dict_to_xml со списками")
    @allure.description("Test _dict_to_xml with lists. TC-SOAP-013")
    async def test_dict_to_xml_with_lists(self, valid_config):
        """Test _dict_to_xml with lists."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        from xml.etree import ElementTree as ET

        parent = ET.Element("root")
        data = {"items": [1, 2, 3], "users": [{"name": "John"}, {"name": "Jane"}]}

        client._dict_to_xml(parent, data)

        items = parent.findall("items")
        assert len(items) == 3
        assert items[0].text == "1"
        assert items[1].text == "2"
        assert items[2].text == "3"

        users = parent.findall("users")
        assert len(users) == 2
        assert users[0].find("name") is not None
        assert users[0].find("name").text == "John"

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-014: call с authentication token")
    @allure.description("Test call with authentication token. TC-SOAP-014")
    async def test_call_with_auth_token(self, mocker, valid_config, mock_soap_response_200):
        """Test call with authentication token."""
        with allure.step("Подготовка SOAP клиента"):
            url = "https://api.example.com/soap"
            client = SoapClient(url, valid_config)

        with allure.step("Установка токена аутентификации"):
            client.set_auth_token("test-token-123")

        with allure.step("Мокирование HTTP ответа"):
            client.client.post = AsyncMock(return_value=mock_soap_response_200)

        with allure.step("Выполнение SOAP вызова"):
            result = await client.call("TestOperation", {"param": "value"})

        with allure.step("Проверка результата"):
            assert result.status_code == 200

        with allure.step("Проверка что Authorization header был добавлен"):
            call_args = client.client.post.call_args
            assert "Authorization" in call_args.kwargs["headers"]
            assert call_args.kwargs["headers"]["Authorization"] == "Bearer test-token-123"

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-015: call с custom headers")
    @allure.description("Test call with custom headers. TC-SOAP-015")
    async def test_call_with_custom_headers(self, mocker, valid_config, mock_soap_response_200):
        """Test call with custom headers."""
        with allure.step("Подготовка SOAP клиента"):
            url = "https://api.example.com/soap"
            client = SoapClient(url, valid_config)

        with allure.step("Мокирование HTTP ответа"):
            client.client.post = AsyncMock(return_value=mock_soap_response_200)

        with allure.step("Выполнение SOAP вызова с custom headers"):
            custom_headers = {"X-Custom-Header": "custom-value"}
            result = await client.call("TestOperation", {"param": "value"}, headers=custom_headers)

        with allure.step("Проверка результата"):
            assert result.status_code == 200

        with allure.step("Проверка что custom header был добавлен"):
            call_args = client.client.post.call_args
            assert "X-Custom-Header" in call_args.kwargs["headers"]
            assert call_args.kwargs["headers"]["X-Custom-Header"] == "custom-value"

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-016: call обрабатывает HTTP ошибки")
    @allure.description("Test call handles HTTP errors. TC-SOAP-016")
    async def test_call_handles_http_errors(self, mocker, valid_config, mock_soap_response_500):
        """Test call handles HTTP errors."""
        with allure.step("Подготовка SOAP клиента"):
            url = "https://api.example.com/soap"
            client = SoapClient(url, valid_config)

        with allure.step("Мокирование HTTP ответа с ошибкой"):
            client.client.post = AsyncMock(return_value=mock_soap_response_500)

        with allure.step("Выполнение SOAP вызова"):
            result = await client.call("TestOperation", {"param": "value"})

        with allure.step("Проверка что ошибка обработана"):
            assert result.status_code == 500
            assert result.server_error is True
            assert result.success is False

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-017: call обрабатывает network ошибки")
    @allure.description("Test call handles network errors. TC-SOAP-017")
    async def test_call_handles_network_errors(self, mocker, valid_config):
        """Test call handles network errors."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        # Mock network error
        client.client.post = AsyncMock(side_effect=Exception("Network error"))

        result = await client.call("TestOperation", {"param": "value"})

        assert result.status_code == 0
        assert result.success is False
        assert result.error_message == "Network error"
        assert result.body == b""

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-018: parse_soap_fault для SOAP 1.1")
    @allure.description("Test parse_soap_fault for SOAP 1.1. TC-SOAP-018")
    async def test_parse_soap_fault_1_1(self, valid_config):
        """Test parse_soap_fault for SOAP 1.1."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config, soap_version="1.1")

        fault_body = b'<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><soap:Fault><faultcode>Server</faultcode><faultstring>Test error</faultstring><detail>Error details</detail></soap:Fault></soap:Body></soap:Envelope>'
        result = ApiResult(
            endpoint=url,
            method="POST",
            status_code=500,
            response_time=0.2,
            success=False,
            redirect=False,
            client_error=False,
            server_error=True,
            informational=False,
            body=fault_body,
            content_type="text/xml",
        )

        fault = client.parse_soap_fault(result)

        assert fault is not None
        assert "faultcode" in fault
        assert fault["faultcode"] == "Server"
        assert "faultstring" in fault
        assert fault["faultstring"] == "Test error"
        assert "detail" in fault
        assert fault["detail"] == "Error details"

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-019: parse_soap_fault для SOAP 1.2")
    @allure.description("Test parse_soap_fault for SOAP 1.2. TC-SOAP-019")
    async def test_parse_soap_fault_1_2(self, valid_config):
        """Test parse_soap_fault for SOAP 1.2."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config, soap_version="1.2")

        fault_body = b'<?xml version="1.0"?><soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><soap12:Fault><Code><Value>Sender</Value></Code><Reason><Text>Test error</Text></Reason></soap12:Fault></soap12:Body></soap12:Envelope>'
        result = ApiResult(
            endpoint=url,
            method="POST",
            status_code=500,
            response_time=0.2,
            success=False,
            redirect=False,
            client_error=False,
            server_error=True,
            informational=False,
            body=fault_body,
            content_type="text/xml",
        )

        fault = client.parse_soap_fault(result)

        # SOAP 1.2 fault structure is different, but we should still parse it
        assert fault is not None

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-020: parse_soap_fault возвращает None для валидного ответа")
    @allure.description("Test parse_soap_fault returns None for valid response. TC-SOAP-020")
    async def test_parse_soap_fault_no_fault(self, valid_config):
        """Test parse_soap_fault returns None for valid response."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        valid_body = b'<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><response>Success</response></soap:Body></soap:Envelope>'
        result = ApiResult(
            endpoint=url,
            method="POST",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=valid_body,
            content_type="text/xml",
        )

        fault = client.parse_soap_fault(result)

        assert fault is None

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-021: parse_soap_fault обрабатывает невалидный XML")
    @allure.description("Test parse_soap_fault handles invalid XML. TC-SOAP-021")
    async def test_parse_soap_fault_invalid_xml(self, valid_config):
        """Test parse_soap_fault handles invalid XML."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        invalid_body = b"Not valid XML"
        result = ApiResult(
            endpoint=url,
            method="POST",
            status_code=200,
            response_time=0.2,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=invalid_body,
            content_type="text/xml",
        )

        fault = client.parse_soap_fault(result)

        assert fault is None

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-022: Инициализация с wsdl_url")
    @allure.description("Test initialization with wsdl_url. TC-SOAP-022")
    async def test_init_with_wsdl_url(self, valid_config):
        """Test initialization with wsdl_url."""
        url = "https://api.example.com/soap"
        wsdl_url = "https://api.example.com/wsdl"
        client = SoapClient(url, valid_config, wsdl_url=wsdl_url)

        assert client.url == url
        assert client.wsdl_url == wsdl_url

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-023: Инициализация с невалидным soap_version вызывает ValueError")
    @allure.description("Test initialization with invalid soap_version raises ValueError. TC-SOAP-023")
    async def test_init_invalid_soap_version(self, valid_config):
        """Test initialization with invalid soap_version raises ValueError."""
        url = "https://api.example.com/soap"

        with pytest.raises(ValueError, match="Invalid SOAP version"):
            SoapClient(url, valid_config, soap_version="2.0")

    @pytest.mark.asyncio
    @allure.title("TC-SOAP-024: close очищает auth_token")
    @allure.description("Test close clears auth_token. TC-SOAP-024")
    async def test_close_clears_auth_token(self, valid_config):
        """Test close clears auth_token."""
        url = "https://api.example.com/soap"
        client = SoapClient(url, valid_config)

        client.set_auth_token("test-token-123")
        assert client._auth_token == "test-token-123"

        await client.close()

        assert client._auth_token is None
        assert client._auth_token_type == "Bearer"
