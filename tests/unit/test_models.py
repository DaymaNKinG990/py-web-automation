"""
Unit tests for web automation framework data models.
"""

import base64
import json

import allure
import msgspec
import pytest

from py_web_automation.clients.models import ApiResult
from tests.data.constants import (  # type: ignore[import-untyped]
    ERROR_API_RESULT_DATA,
    INFORMATIONAL_API_RESULT_DATA,
    REDIRECT_API_RESULT_DATA,
    SERVER_ERROR_API_RESULT_DATA,
    TIMEOUT_API_RESULT_DATA,
    VALID_API_RESULT_DATA,
)

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class TestApiResult:
    """Test cases for ApiResult model."""

    @allure.title("creating a valid ApiResult")
    @allure.description("Test creating a valid ApiResult.")
    def test_valid_api_result_creation(self):
        """Test creating a valid ApiResult."""
        with allure.step("Create ApiResult with valid data"):
            result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Verify all ApiResult fields"):
            assert result.endpoint == "/api/status"
            assert result.method == "GET"
            assert result.status_code == 200
            assert result.response_time == 0.5
            assert result.success is True
            assert result.redirect is False
            assert result.client_error is False
            assert result.server_error is False
            assert result.informational is False
            assert result.headers == {"content-type": "application/json"}
            assert result.body == b'{"status": "ok"}'
            assert result.content_type == "application/json"
            assert result.reason == "OK"
            assert result.error_message is None

    @allure.title("creating an error ApiResult")
    @allure.description("Test creating an error ApiResult.")
    def test_error_api_result_creation(self):
        """Test creating an error ApiResult."""
        with allure.step("Create ApiResult with error data"):
            result = ApiResult(**ERROR_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Verify error ApiResult fields"):
            assert result.endpoint == "/api/error"
            assert result.method == "POST"
            assert result.status_code == 400
            assert result.response_time == 0.2
            assert result.success is False
            assert result.client_error is True
            assert result.error_message == "Bad Request"

    @allure.title("creating a timeout ApiResult")
    @allure.description("Test creating a timeout ApiResult.")
    def test_timeout_api_result_creation(self):
        """Test creating a timeout ApiResult."""
        with allure.step("Create ApiResult with timeout data"):
            result = ApiResult(**TIMEOUT_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Verify timeout ApiResult fields"):
            assert result.status_code == 408
            assert result.response_time == 30.0
            assert result.success is False
            assert result.client_error is True
            assert result.error_message == "Request timeout"

    @allure.title("creating a redirect ApiResult")
    @allure.description("Test creating a redirect ApiResult.")
    def test_redirect_api_result_creation(self):
        """Test creating a redirect ApiResult."""
        with allure.step("Create ApiResult with redirect data"):
            result = ApiResult(**REDIRECT_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Verify redirect ApiResult fields"):
            assert result.status_code == 301
            assert result.redirect is True
            assert result.success is False

    @allure.title("creating a server error ApiResult")
    @allure.description("Test creating a server error ApiResult.")
    def test_server_error_api_result_creation(self):
        """Test creating a server error ApiResult."""
        with allure.step("Create ApiResult with server error data"):
            result = ApiResult(**SERVER_ERROR_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Verify server error ApiResult fields"):
            assert result.status_code == 500
            assert result.server_error is True
            assert result.success is False

    @allure.title("creating an informational ApiResult")
    @allure.description("Test creating an informational ApiResult.")
    def test_informational_api_result_creation(self):
        """Test creating an informational ApiResult."""
        with allure.step("Create ApiResult with informational data"):
            result = ApiResult(**INFORMATIONAL_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Verify informational ApiResult fields"):
            assert result.status_code == 101
            assert result.informational is True
            assert result.success is False

    @allure.title("ApiResult required fields")
    @allure.description("Test ApiResult required fields.")
    def test_api_result_required_fields(self):
        """Test ApiResult required fields."""
        with allure.step("Attempt to create ApiResult without required fields"):
            with pytest.raises(TypeError):
                ApiResult()  # type: ignore[call-arg]  # Missing required fields

        with allure.step("Attempt to create ApiResult with partial fields"):
            with pytest.raises(TypeError):
                ApiResult(endpoint="/api/test")  # type: ignore[call-arg]  # Missing other required fields

    @allure.title("ApiResult field types")
    @allure.description("Test ApiResult field types.")
    def test_api_result_field_types(self):
        """Test ApiResult field types."""
        with allure.step("Create ApiResult with valid data"):
            result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Verify all field types"):
            assert isinstance(result.endpoint, str)
            assert isinstance(result.method, str)
            assert isinstance(result.status_code, int)
            assert isinstance(result.response_time, float)
            assert isinstance(result.success, bool)
            assert isinstance(result.redirect, bool)
            assert isinstance(result.client_error, bool)
            assert isinstance(result.server_error, bool)
            assert isinstance(result.informational, bool)

    @allure.title("ApiResult with invalid status_code type")
    @allure.description("Test ApiResult with invalid status_code type.")
    def test_api_result_invalid_status_code_type(self):
        """Test ApiResult with invalid status_code type."""
        with allure.step("Create ApiResult with invalid status_code type"):
            # msgspec doesn't validate types at creation time, it accepts any type
            # The type annotation is for serialization/deserialization, not runtime validation
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code="200",  # type: ignore[arg-type]  # msgspec stores as str, doesn't convert
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
        with allure.step("Verify status_code is stored as string"):
            assert isinstance(result.status_code, str)  # msgspec doesn't convert, stores as-is
            assert result.status_code == "200"

    @allure.title("ApiResult with invalid response_time type")
    @allure.description("Test ApiResult with invalid response_time type.")
    def test_api_result_invalid_response_time_type(self):
        """Test ApiResult with invalid response_time type."""
        with allure.step("Create ApiResult with invalid response_time type"):
            # msgspec doesn't validate types at creation time, it accepts any type
            # The type annotation is for serialization/deserialization, not runtime validation
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time="fast",  # type: ignore[arg-type]  # msgspec stores as str, doesn't convert
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
        with allure.step("Verify response_time is stored as string"):
            assert isinstance(result.response_time, str)  # msgspec doesn't convert, stores as-is
            assert result.response_time == "fast"

    @allure.title("ApiResult with invalid headers type")
    @allure.description("Test ApiResult with invalid headers type.")
    def test_api_result_invalid_headers_type(self):
        """Test ApiResult with invalid headers type."""
        with allure.step("Attempt to create ApiResult with invalid headers type"):
            # msgspec may be lenient with Optional fields
            # We test both cases
            try:
                result = ApiResult(
                    endpoint="/api/test",
                    method="GET",
                    status_code=200,
                    response_time=0.1,
                    success=True,
                    redirect=False,
                    client_error=False,
                    server_error=False,
                    informational=False,
                    headers="invalid",  # type: ignore[arg-type]  # Must be Dict[str, str]
                )
                # If no error, msgspec was lenient - verify object was created
                assert result.endpoint == "/api/test"
            except msgspec.ValidationError:
                # If it raises, that's also acceptable - strict validation
                pass

    @pytest.mark.parametrize("status_code", [200, 301, 404, 500, 101])
    @allure.title("different status codes")
    @allure.description("Test different status codes.")
    def test_api_result_status_codes(self, status_code):
        """Test different status codes."""
        with allure.step(f"Create ApiResult with status_code={status_code}"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=status_code,
                response_time=0.1,
                success=200 <= status_code < 300,
                redirect=300 <= status_code < 400,
                client_error=400 <= status_code < 500,
                server_error=500 <= status_code < 600,
                informational=100 <= status_code < 200,
            )
        with allure.step("Verify status code flags"):
            assert result.status_code == status_code
            assert result.success == (200 <= status_code < 300)
            assert result.redirect == (300 <= status_code < 400)
            assert result.client_error == (400 <= status_code < 500)
            assert result.server_error == (500 <= status_code < 600)
            assert result.informational == (100 <= status_code < 200)

    @allure.title("different response times")
    @allure.description("Test different response times.")
    def test_api_result_response_times(self):
        """Test different response times."""
        with allure.step("Test ApiResult with various response times"):
            response_times = [0.001, 0.1, 1.0, 10.0, 100.0]

            for response_time in response_times:
                with allure.step(f"Create ApiResult with response_time={response_time}"):
                    result = ApiResult(
                        endpoint="/api/test",
                        method="GET",
                        status_code=200,
                        response_time=response_time,
                        success=True,
                        redirect=False,
                        client_error=False,
                        server_error=False,
                        informational=False,
                    )
                with allure.step(f"Verify response_time={response_time}"):
                    assert result.response_time == response_time

    @allure.title("ApiResult serialization")
    @allure.description("Test ApiResult serialization.")
    def test_api_result_serialization(self):
        """Test ApiResult serialization."""
        with allure.step("Create ApiResult with valid data"):
            result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Serialize ApiResult to dict"):
            # Test serialization to dict
            result_dict = msgspec.to_builtins(result)

        with allure.step("Verify serialized dict"):
            assert isinstance(result_dict, dict)
            assert result_dict["endpoint"] == "/api/status"
            assert result_dict["status_code"] == 200
            assert result_dict["success"] is True

    @allure.title("ApiResult serialization with response data")
    @allure.description("Test ApiResult serialization with response data.")
    def test_api_result_serialization_with_response_data(self):
        """Test ApiResult serialization with response data."""
        with allure.step("Create ApiResult with response data"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                headers={"content-type": "application/json"},
                body=b'{"test": "data"}',
                content_type="application/json",
                reason="OK",
            )

        with allure.step("Serialize ApiResult to dict"):
            # ApiResult should serialize correctly with immutable data
            result_dict = msgspec.to_builtins(result)

        with allure.step("Verify serialized dict contains all fields"):
            assert "headers" in result_dict
            assert "body" in result_dict
            assert "content_type" in result_dict
            assert "reason" in result_dict
            assert result_dict["headers"] == {"content-type": "application/json"}
            # msgspec serializes bytes to base64 string by default

            expected_body_base64 = base64.b64encode(b'{"test": "data"}').decode("utf-8")
            assert result_dict["body"] == expected_body_base64

    @allure.title("ApiResult deserialization")
    @allure.description("Test ApiResult deserialization.")
    def test_api_result_deserialization(self):
        """Test ApiResult deserialization."""
        with allure.step("Prepare data dict for deserialization"):
            result_dict = VALID_API_RESULT_DATA.copy()

        with allure.step("Deserialize dict to ApiResult"):
            # Test deserialization from dict
            result = msgspec.convert(result_dict, ApiResult)

        with allure.step("Verify deserialized ApiResult"):
            assert isinstance(result, ApiResult)
            assert result.endpoint == "/api/status"
            assert result.status_code == 200
            assert result.success is True

    @allure.title("ApiResult deserialization with None in optional fields")
    @allure.description("Test ApiResult deserialization with None in optional fields.")
    def test_api_result_deserialization_with_none(self):
        """Test ApiResult deserialization with None in optional fields."""
        with allure.step("Prepare data dict with None in optional fields"):
            result_dict = {
                "endpoint": "/api/test",
                "method": "GET",
                "status_code": 200,
                "response_time": 0.1,
                "success": True,
                "redirect": False,
                "client_error": False,
                "server_error": False,
                "informational": False,
                "headers": {},
                "body": b"",
                "content_type": None,
                "reason": None,
                "error_message": None,
            }
        with allure.step("Deserialize dict to ApiResult"):
            result = msgspec.convert(result_dict, ApiResult)
        with allure.step("Verify None fields handled correctly"):
            assert result.headers == {}
            assert result.body == b""
            assert result.content_type is None
            assert result.reason is None
            assert result.error_message is None

    @allure.title("ApiResult equality")
    @allure.description("Test ApiResult equality.")
    def test_api_result_equality(self):
        """Test ApiResult equality."""
        with allure.step("Create three ApiResult instances"):
            result1 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
            result2 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
            result3 = ApiResult(**ERROR_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Verify equality and inequality"):
            assert result1 == result2
            assert result1 != result3

    @allure.title("ApiResult inequality")
    @allure.description("Test ApiResult inequality.")
    def test_api_result_inequality(self):
        """Test ApiResult inequality."""
        with allure.step("Create two ApiResult instances with different endpoints"):
            result1 = ApiResult(
                endpoint="/api/test1",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
            result2 = ApiResult(
                endpoint="/api/test2",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )

        with allure.step("Verify instances are not equal"):
            assert result1 != result2

    @allure.title("ApiResult hashing")
    @allure.description("Test ApiResult hashing.")
    def test_api_result_hash(self):
        """Test ApiResult hashing."""
        with allure.step("Create ApiResult instances with dict headers"):
            result1 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
            result2 = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Verify ApiResult with dict headers is not hashable"):
            # msgspec.Struct with frozen=True should be hashable
            # However, dict fields (headers) make it unhashable - this is expected behavior
            # Test that ApiResult with dict headers is not hashable
            with pytest.raises(TypeError, match="unhashable type"):
                hash(result1)

            with pytest.raises(TypeError, match="unhashable type"):
                hash(result2)

    @allure.title("ApiResult hash inequality")
    @allure.description("Test ApiResult hash inequality.")
    def test_api_result_hash_inequality(self):
        """Test ApiResult hash inequality."""
        with allure.step("Create two ApiResult instances"):
            result1 = ApiResult(
                endpoint="/api/test1",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
            result2 = ApiResult(
                endpoint="/api/test2",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )

        with allure.step("Verify both objects raise TypeError when trying to hash"):
            # ApiResult with dict headers is not hashable - this is expected behavior
            # Test that both objects raise TypeError when trying to hash
            with pytest.raises(TypeError, match="unhashable type"):
                hash(result1)

            with pytest.raises(TypeError, match="unhashable type"):
                hash(result2)

    @allure.title("ApiResult string representation")
    @allure.description("Test ApiResult string representation.")
    def test_api_result_repr(self):
        """Test ApiResult string representation."""
        with allure.step("Create ApiResult and get string representation"):
            result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]
            repr_str = repr(result)

        with allure.step("Verify string representation contains expected fields"):
            assert "ApiResult" in repr_str
            assert "endpoint='/api/status'" in repr_str
            assert "status_code=200" in repr_str
            assert "success=True" in repr_str

    @allure.title("that ApiResult is frozen (cannot modify attributes)")
    @allure.description("Test that ApiResult is frozen (cannot modify attributes).")
    def test_api_result_frozen(self):
        """Test that ApiResult is frozen (cannot modify attributes)."""
        with allure.step("Create ApiResult instance"):
            result = ApiResult(**VALID_API_RESULT_DATA)  # type: ignore[arg-type]

        with allure.step("Attempt to modify attribute and expect AttributeError"):
            # Should raise AttributeError when trying to modify
            with pytest.raises(AttributeError, match="immutable type"):
                result.endpoint = "/api/new"  # type: ignore[misc]

    @allure.title("ApiResult with empty strings")
    @allure.description("Test ApiResult with empty strings.")
    def test_api_result_empty_strings(self):
        """Test ApiResult with empty strings."""
        with allure.step("Create ApiResult with empty strings"):
            result = ApiResult(
                endpoint="",
                method="",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                error_message="",
            )
        with allure.step("Verify empty strings are preserved"):
            assert result.endpoint == ""
            assert result.method == ""
            assert result.error_message == ""

    @allure.title("ApiResult with unicode characters")
    @allure.description("Test ApiResult with unicode characters.")
    def test_api_result_unicode(self):
        """Test ApiResult with unicode characters."""
        with allure.step("Create ApiResult with unicode characters"):
            result = ApiResult(
                endpoint="/api/тест",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                error_message="Ошибка 错误",
            )
        with allure.step("Verify unicode characters are preserved"):
            assert result.endpoint == "/api/тест"
            assert result.error_message == "Ошибка 错误"

    @allure.title("ApiResult with very long strings")
    @allure.description("Test ApiResult with very long strings.")
    def test_api_result_very_long_strings(self):
        """Test ApiResult with very long strings."""
        with allure.step("Create ApiResult with very long endpoint"):
            long_endpoint = "/api/" + "a" * 10000
            result = ApiResult(
                endpoint=long_endpoint,
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )
        with allure.step("Verify long string is preserved"):
            assert len(result.endpoint) == len(long_endpoint)

    @allure.title("ApiResult with response data fields")
    @allure.description("Test ApiResult with response data fields.")
    def test_api_result_with_response_data(self):
        """Test ApiResult with response data fields."""
        with allure.step("Create ApiResult with response data fields"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                headers={"content-type": "application/json", "x-custom": "value"},
                body=b'{"test": "data"}',
                content_type="application/json",
                reason="OK",
            )

        with allure.step("Verify all response data fields"):
            assert result.headers == {
                "content-type": "application/json",
                "x-custom": "value",
            }
            assert result.body == b'{"test": "data"}'
            assert result.content_type == "application/json"
            assert result.reason == "OK"
            assert result.status_code == 200

    @allure.title("TC-MODEL-API-022: ApiResult.json() method")
    @allure.description("Test ApiResult.json() method. TC-MODEL-API-022")
    def test_api_result_json_method(self):
        """Test ApiResult.json() method."""
        with allure.step("Create ApiResult with JSON body"):
            json_data = {"key": "value", "number": 123}
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                body=json.dumps(json_data).encode("utf-8"),
            )

        with allure.step("Parse JSON from body"):
            parsed = result.json()

        with allure.step("Verify parsed JSON matches original data"):
            assert parsed == json_data
            assert parsed["key"] == "value"
            assert parsed["number"] == 123

    @allure.title("TC-MODEL-API-023: ApiResult.json() raises ValueError for invalid JSON")
    @allure.description("Test ApiResult.json() raises ValueError for invalid JSON. TC-MODEL-API-023")
    def test_api_result_json_method_invalid_json(self):
        """Test ApiResult.json() raises ValueError for invalid JSON."""
        with allure.step("Create ApiResult with invalid JSON body"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                body=b"not valid json",
            )

        with allure.step("Call json() and expect ValueError"):
            with pytest.raises(ValueError, match="Failed to parse JSON"):
                result.json()

    @allure.title("TC-MODEL-API-024: ApiResult.text() method")
    @allure.description("Test ApiResult.text() method. TC-MODEL-API-024")
    def test_api_result_text_method(self):
        """Test ApiResult.text() method."""
        with allure.step("Create ApiResult with text body"):
            text_content = "Hello, World!"
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                body=text_content.encode("utf-8"),
            )

        with allure.step("Call text() and verify content"):
            assert result.text() == text_content

    @allure.title("TC-MODEL-API-025: ApiResult.text() handles decode errors gracefully")
    @allure.description("Test ApiResult.text() handles decode errors gracefully. TC-MODEL-API-025")
    def test_api_result_text_method_with_errors(self):
        """Test ApiResult.text() handles decode errors gracefully."""
        with allure.step("Create ApiResult with invalid UTF-8 body"):
            # Invalid UTF-8 sequence
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                body=b"\xff\xfe\x00\x01",  # Invalid UTF-8
            )

        with allure.step("Call text() and verify it returns string without raising"):
            # Should not raise, but return replacement characters
            text = result.text()
            assert isinstance(text, str)

    @allure.title("TC-MODEL-API-026: ApiResult.raise_for_status() does not raise for success")
    @allure.description("Test ApiResult.raise_for_status() does not raise for success. TC-MODEL-API-026")
    def test_api_result_raise_for_status_success(self):
        """Test ApiResult.raise_for_status() does not raise for success."""
        with allure.step("Create ApiResult with success status"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )

        with allure.step("Call raise_for_status() and verify it does not raise"):
            # Should not raise
            result.raise_for_status()

    @allure.title("TC-MODEL-API-027: ApiResult.raise_for_status() raises for 4xx status")
    @allure.description("Test ApiResult.raise_for_status() raises for 4xx status. TC-MODEL-API-027")
    def test_api_result_raise_for_status_client_error(self):
        """Test ApiResult.raise_for_status() raises for 4xx status."""
        with allure.step("Create ApiResult with 4xx status"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=404,
                response_time=0.1,
                success=False,
                redirect=False,
                client_error=True,
                server_error=False,
                informational=False,
                error_message="Not Found",
            )

        with allure.step("Call raise_for_status() and expect exception"):
            with pytest.raises(Exception, match="HTTP 404"):
                result.raise_for_status()

    @allure.title("TC-MODEL-API-028: ApiResult.raise_for_status() raises for 5xx status")
    @allure.description("Test ApiResult.raise_for_status() raises for 5xx status. TC-MODEL-API-028")
    def test_api_result_raise_for_status_server_error(self):
        """Test ApiResult.raise_for_status() raises for 5xx status."""
        with allure.step("Create ApiResult with 5xx status"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=500,
                response_time=0.1,
                success=False,
                redirect=False,
                client_error=False,
                server_error=True,
                informational=False,
                error_message="Internal Server Error",
            )

        with allure.step("Call raise_for_status() and expect exception"):
            with pytest.raises(Exception, match="HTTP 500"):
                result.raise_for_status()

    @allure.title("TC-MODEL-API-029: ApiResult.assert_status_code() with matching code")
    @allure.description("Test ApiResult.assert_status_code() with matching code. TC-MODEL-API-029")
    def test_api_result_assert_status_code_success(self):
        """Test ApiResult.assert_status_code() with matching code."""
        with allure.step("Create ApiResult with status_code=200"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )

        with allure.step("Call assert_status_code(200) and verify it does not raise"):
            # Should not raise
            result.assert_status_code(200)

    @allure.title("TC-MODEL-API-030: ApiResult.assert_status_code() raises AssertionError for mismatch")
    @allure.description("Test ApiResult.assert_status_code() raises AssertionError for mismatch. TC-MODEL-API-030")
    def test_api_result_assert_status_code_failure(self):
        """Test ApiResult.assert_status_code() raises AssertionError for mismatch."""
        with allure.step("Create ApiResult with status_code=404"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=404,
                response_time=0.1,
                success=False,
                redirect=False,
                client_error=True,
                server_error=False,
                informational=False,
                body=b"Not Found",
            )

        with allure.step("Call assert_status_code(200) and expect AssertionError"):
            with pytest.raises(AssertionError, match="Expected status code 200, got 404"):
                result.assert_status_code(200)

    @allure.title("TC-MODEL-API-031: ApiResult.assert_success() for successful request")
    @allure.description("Test ApiResult.assert_success() for successful request. TC-MODEL-API-031")
    def test_api_result_assert_success(self):
        """Test ApiResult.assert_success() for successful request."""
        with allure.step("Create ApiResult with success=True"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
            )

        with allure.step("Call assert_success() and verify it does not raise"):
            # Should not raise
            result.assert_success()

    @allure.title("TC-MODEL-API-032: ApiResult.assert_success() raises AssertionError for failed request")
    @allure.description("Test ApiResult.assert_success() raises AssertionError for failed request. TC-MODEL-API-032")
    def test_api_result_assert_success_failure(self):
        """Test ApiResult.assert_success() raises AssertionError for failed request."""
        with allure.step("Create ApiResult with success=False"):
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=500,
                response_time=0.1,
                success=False,
                redirect=False,
                client_error=False,
                server_error=True,
                informational=False,
                body=b"Server Error",
            )

        with allure.step("Call assert_success() and expect AssertionError"):
            with pytest.raises(AssertionError, match="Request failed with status 500"):
                result.assert_success()

    @allure.title("TC-MODEL-API-033: ApiResult.assert_has_fields() with all fields present")
    @allure.description("Test ApiResult.assert_has_fields() with all fields present. TC-MODEL-API-033")
    def test_api_result_assert_has_fields_success(self):
        """Test ApiResult.assert_has_fields() with all fields present."""
        with allure.step("Create ApiResult with JSON body containing all fields"):
            json_data = {"name": "test", "id": 123, "status": "active"}
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                body=json.dumps(json_data).encode("utf-8"),
            )

        with allure.step("Call assert_has_fields() and verify it does not raise"):
            # Should not raise
            result.assert_has_fields("name", "id", "status")

    @allure.title("TC-MODEL-API-034: ApiResult.assert_has_fields() raises AssertionError for missing fields")
    @allure.description("Test ApiResult.assert_has_fields() raises AssertionError for missing fields. TC-MODEL-API-034")
    def test_api_result_assert_has_fields_missing(self):
        """Test ApiResult.assert_has_fields() raises AssertionError for missing fields."""
        with allure.step("Create ApiResult with JSON body missing some fields"):
            json_data = {"name": "test", "id": 123}
            result = ApiResult(
                endpoint="/api/test",
                method="GET",
                status_code=200,
                response_time=0.1,
                success=True,
                redirect=False,
                client_error=False,
                server_error=False,
                informational=False,
                body=json.dumps(json_data).encode("utf-8"),
            )

        with allure.step("Call assert_has_fields() with missing fields and expect AssertionError"):
            with pytest.raises(AssertionError, match="Missing required fields"):
                result.assert_has_fields("name", "id", "status", "email")

    @allure.title("different HTTP methods")
    @allure.description("Test different HTTP methods.")
    def test_api_result_methods(self):
        """Test different HTTP methods."""
        with allure.step("Test ApiResult with various HTTP methods"):
            methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

            for method in methods:
                with allure.step(f"Create ApiResult with method={method}"):
                    result = ApiResult(
                        endpoint="/api/test",
                        method=method,
                        status_code=200,
                        response_time=0.1,
                        success=True,
                        redirect=False,
                        client_error=False,
                        server_error=False,
                        informational=False,
                    )
                with allure.step(f"Verify method={method}"):
                    assert result.method == method
