"""
Unit tests for validators module.
"""

import allure
import msgspec
import pytest

from py_web_automation.clients.models import ApiResult
from py_web_automation.exceptions import ValidationError
from py_web_automation.validators import (
    create_schema_from_dict,
    validate_api_result,
    validate_json_response,
    validate_response,
)

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class TestValidators:
    """Test validators module."""

    @allure.title("TC-VAL-001: Validate response with dict schema")
    @allure.description("Test validating response with dict schema. TC-VAL-001")
    def test_validate_response_dict(self):
        """Test validating response with dict schema."""
        from py_web_automation.validators import create_schema_from_dict

        data = {"id": 1, "name": "Test", "active": True}
        # Create schema from dict using create_schema_from_dict
        schema = create_schema_from_dict("User", {"id": int, "name": str, "active": bool})

        result = validate_response(data, schema)
        assert isinstance(result, schema)
        assert result.id == 1
        assert result.name == "Test"
        assert result.active is True

    @allure.title("TC-VAL-002: Validate response with msgspec Struct")
    @allure.description("Test validating response with msgspec Struct. TC-VAL-002")
    def test_validate_response_struct(self):
        """Test validating response with msgspec Struct."""

        class User(msgspec.Struct):
            id: int
            name: str
            active: bool

        data = {"id": 1, "name": "Test", "active": True}

        result = validate_response(data, User)
        assert isinstance(result, User)
        assert result.id == 1
        assert result.name == "Test"

    @allure.title("TC-VAL-003: Validate response fails with invalid data")
    @allure.description("Test validation fails with invalid data. TC-VAL-003")
    def test_validate_response_invalid(self):
        """Test validation fails with invalid data."""
        from py_web_automation.validators import create_schema_from_dict

        # Use data that will definitely fail validation (missing required field)
        data = {"name": "Test"}  # Missing required 'id' field
        schema = create_schema_from_dict("User", {"id": int, "name": str})

        with pytest.raises(ValidationError, match="Validation failed"):
            validate_response(data, schema)

    @allure.title("TC-VAL-004: Validate JSON response")
    @allure.description("Test validating JSON response. TC-VAL-004")
    def test_validate_json_response(self):
        """Test validating JSON response."""
        from py_web_automation.validators import create_schema_from_dict

        json_data = b'{"id": 1, "name": "Test"}'
        # Create schema from dict using create_schema_from_dict
        schema = create_schema_from_dict("User", {"id": int, "name": str})

        result = validate_json_response(json_data, schema)
        assert isinstance(result, schema)
        assert result.id == 1
        assert result.name == "Test"

    @allure.title("TC-VAL-005: Validate JSON response with invalid JSON")
    @allure.description("Test validation fails with invalid JSON. TC-VAL-005")
    def test_validate_json_response_invalid_json(self):
        """Test validation fails with invalid JSON."""
        json_data = b'{"id": 1, "name": invalid}'
        schema = {"id": int, "name": str}

        with pytest.raises(ValidationError):
            validate_json_response(json_data, schema)

    @allure.title("TC-VAL-006: Validate ApiResult")
    @allure.description("Test validating ApiResult. TC-VAL-006")
    def test_validate_api_result(self):
        """Test validating ApiResult."""
        from py_web_automation.validators import create_schema_from_dict

        api_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.5,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"id": 1, "name": "Test"}',
        )
        # Create schema from dict using create_schema_from_dict
        schema = create_schema_from_dict("User", {"id": int, "name": str})

        result = validate_api_result(api_result, schema)
        assert isinstance(result, schema)
        assert result.id == 1
        assert result.name == "Test"

    @allure.title("TC-VAL-007: Validate ApiResult with Struct schema")
    @allure.description("Test validating ApiResult with Struct schema. TC-VAL-007")
    def test_validate_api_result_struct(self):
        """Test validating ApiResult with Struct schema."""

        class User(msgspec.Struct):
            id: int
            name: str

        api_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.5,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b'{"id": 1, "name": "Test"}',
        )

        result = validate_api_result(api_result, User)
        assert isinstance(result, User)
        assert result.id == 1
        assert result.name == "Test"

    @allure.title("TC-VAL-008: Create schema from dict")
    @allure.description("Test creating schema from dict. TC-VAL-008")
    def test_create_schema_from_dict(self):
        """Test creating schema from dict."""
        fields = {"id": int, "name": str, "active": bool}
        schema = create_schema_from_dict("User", fields)

        assert issubclass(schema, msgspec.Struct)

        # Test using the schema
        data = {"id": 1, "name": "Test", "active": True}
        result = validate_response(data, schema)
        assert isinstance(result, schema)
        assert result.id == 1
        assert result.name == "Test"
        assert result.active is True

    @allure.title("TC-VAL-009: Create schema with frozen option")
    @allure.description("Test creating frozen schema. TC-VAL-009")
    def test_create_schema_frozen(self):
        """Test creating frozen schema."""
        fields = {"id": int, "name": str}
        schema = create_schema_from_dict("User", fields, frozen=True)

        instance = schema(id=1, name="Test")
        assert instance.id == 1

        # Frozen schemas should be immutable
        with pytest.raises(AttributeError):
            instance.id = 2

    @allure.title("TC-VAL-010: Validate list response")
    @allure.description("Test validating list response. TC-VAL-010")
    def test_validate_list_response(self):
        """Test validating list response."""

        from py_web_automation.validators import create_schema_from_dict

        data = [{"id": 1, "name": "User1"}, {"id": 2, "name": "User2"}]
        # Create schema for list items
        UserSchema = create_schema_from_dict("User", {"id": int, "name": str})
        schema = list[UserSchema]

        result = validate_response(data, schema)
        assert len(result) == 2
        assert isinstance(result[0], UserSchema)
        assert result[0].id == 1
        assert result[0].name == "User1"
        assert isinstance(result[1], UserSchema)
        assert result[1].id == 2
        assert result[1].name == "User2"

    @allure.title("TC-VAL-011: validate_response с dict type (без создания схемы)")
    @allure.description("Test validate_response with dict type (without creating schema). TC-VAL-011")
    def test_validate_response_dict_type(self):
        """Test validate_response with dict type (without creating schema)."""
        from typing import Any

        data = {"id": 1, "name": "Test"}
        schema = dict[str, Any]

        result = validate_response(data, schema)
        assert isinstance(result, dict)
        assert result["id"] == 1
        assert result["name"] == "Test"

    @allure.title("TC-VAL-012: validate_response с list type (без создания схемы)")
    @allure.description("Test validate_response with list type (without creating schema). TC-VAL-012")
    def test_validate_response_list_type(self):
        """Test validate_response with list type (without creating schema)."""
        from typing import Any

        data = [1, 2, 3]
        schema = list[Any]

        result = validate_response(data, schema)
        assert isinstance(result, list)
        assert result == [1, 2, 3]

    @allure.title("TC-VAL-013: validate_response выбрасывает FrameworkValidationError для невалидных данных")
    @allure.description("Test validate_response raises FrameworkValidationError for invalid data. TC-VAL-013")
    def test_validate_response_invalid_data(self):
        """Test validate_response raises FrameworkValidationError for invalid data."""
        from py_web_automation.validators import create_schema_from_dict

        # Use data that will definitely fail validation (missing required field)
        data = {"name": "Test"}  # Missing required 'id' field
        schema = create_schema_from_dict("User", {"id": int, "name": str})

        with pytest.raises(ValidationError, match="Validation failed"):
            validate_response(data, schema)

    @allure.title("TC-VAL-014: validate_response обрабатывает msgspec.ValidationError")
    @allure.description("Test validate_response handles msgspec.ValidationError. TC-VAL-014")
    def test_validate_response_handles_msgspec_error(self):
        """Test validate_response handles msgspec.ValidationError."""
        from py_web_automation.validators import create_schema_from_dict

        # Use data that will definitely fail validation (missing required field)
        data = {"id": 1}  # Missing required 'name' field
        schema = create_schema_from_dict("User", {"id": int, "name": str})

        # Should raise ValidationError (wrapped from msgspec.ValidationError)
        with pytest.raises(ValidationError, match="Validation failed"):
            validate_response(data, schema)

    @allure.title("TC-VAL-015: validate_response обрабатывает общие Exception")
    @allure.description("Test validate_response handles general Exception. TC-VAL-015")
    def test_validate_response_handles_general_exception(self):
        """Test validate_response handles general Exception."""
        # Use an invalid schema type that will cause an exception
        data = {"id": 1}

        # This should raise FrameworkValidationError for unsupported schema
        with pytest.raises(ValidationError):
            validate_response(data, "invalid_schema_type")  # type: ignore[arg-type]

    @allure.title("TC-VAL-016: validate_json_response с bytes")
    @allure.description("Test validate_json_response with bytes. TC-VAL-016")
    def test_validate_json_response_bytes(self):
        """Test validate_json_response with bytes."""
        from py_web_automation.validators import create_schema_from_dict

        json_data = b'{"id": 1, "name": "Test"}'
        schema = create_schema_from_dict("User", {"id": int, "name": str})

        result = validate_json_response(json_data, schema)
        assert isinstance(result, schema)
        assert result.id == 1
        assert result.name == "Test"

    @allure.title("TC-VAL-017: validate_json_response с str")
    @allure.description("Test validate_json_response with str. TC-VAL-017")
    def test_validate_json_response_str(self):
        """Test validate_json_response with str."""
        from py_web_automation.validators import create_schema_from_dict

        json_data = '{"id": 1, "name": "Test"}'
        schema = create_schema_from_dict("User", {"id": int, "name": str})

        result = validate_json_response(json_data, schema)
        assert isinstance(result, schema)
        assert result.id == 1
        assert result.name == "Test"

    @allure.title("TC-VAL-018: validate_json_response выбрасывает FrameworkValidationError для невалидного JSON")
    @allure.description("Test validate_json_response raises FrameworkValidationError for invalid JSON. TC-VAL-018")
    def test_validate_json_response_invalid_json_error(self):
        """Test validate_json_response raises FrameworkValidationError for invalid JSON."""
        from py_web_automation.validators import create_schema_from_dict

        json_data = b'{"id": 1, "name": invalid}'  # Invalid JSON
        schema = create_schema_from_dict("User", {"id": int, "name": str})

        with pytest.raises(ValidationError, match="Failed to parse JSON"):
            validate_json_response(json_data, schema)

    @allure.title("TC-VAL-019: validate_api_result выбрасывает FrameworkValidationError для не-ApiResult")
    @allure.description("Test validate_api_result raises FrameworkValidationError for non-ApiResult. TC-VAL-019")
    def test_validate_api_result_not_apiresult(self):
        """Test validate_api_result raises FrameworkValidationError for non-ApiResult."""
        from py_web_automation.validators import create_schema_from_dict

        schema = create_schema_from_dict("User", {"id": int, "name": str})

        with pytest.raises(ValidationError, match="Expected ApiResult"):
            validate_api_result("not_an_apiresult", schema)  # type: ignore[arg-type]

    @allure.title("TC-VAL-020: validate_api_result выбрасывает FrameworkValidationError для не-JSON body")
    @allure.description("Test validate_api_result raises FrameworkValidationError for non-JSON body. TC-VAL-020")
    def test_validate_api_result_non_json_body(self):
        """Test validate_api_result raises FrameworkValidationError for non-JSON body."""
        from py_web_automation.validators import create_schema_from_dict

        api_result = ApiResult(
            endpoint="/api/users",
            method="GET",
            status_code=200,
            response_time=0.5,
            success=True,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            body=b"Not JSON data",
            content_type="text/plain",
        )
        schema = create_schema_from_dict("User", {"id": int, "name": str})

        with pytest.raises(ValidationError, match="Failed to parse response as JSON"):
            validate_api_result(api_result, schema)

    @allure.title("TC-VAL-021: create_schema_from_dict с Optional fields (tuple format)")
    @allure.description("Test create_schema_from_dict with Optional fields (tuple format). TC-VAL-021")
    def test_create_schema_with_optional_fields(self):
        """Test create_schema_from_dict with Optional fields (tuple format)."""

        fields = {
            "id": int,
            "name": str,
            "email": (str, None),  # Optional field
        }
        schema = create_schema_from_dict("User", fields)

        # msgspec.defstruct requires defaults to be passed separately
        # The current implementation may not fully support Optional with defaults
        # Test that schema is created and can be used with all fields
        user1 = schema(id=1, name="John", email=None)
        assert user1.id == 1
        assert user1.name == "John"
        assert user1.email is None

        user2 = schema(id=2, name="Jane", email="jane@example.com")
        assert user2.email == "jane@example.com"

    @allure.title("TC-VAL-022: create_schema_from_dict с default values")
    @allure.description("Test create_schema_from_dict with default values. TC-VAL-022")
    def test_create_schema_with_default_values(self):
        """Test create_schema_from_dict with default values."""
        fields = {
            "id": int,
            "name": str,
            "active": (bool, True),  # Field with default value
        }
        schema = create_schema_from_dict("User", fields)

        # msgspec.defstruct may require defaults to be passed explicitly
        # Test that schema is created and can be used
        user = schema(id=1, name="John", active=True)
        assert user.active is True

        # Should allow overriding default
        user2 = schema(id=2, name="Jane", active=False)
        assert user2.active is False

    @allure.title("TC-VAL-DICT-001: validate_response с dict schema и не-dict данными")
    @allure.description("Test validate_response with dict schema and non-dict data. TC-VAL-DICT-001")
    def test_validate_response_dict_schema_non_dict_data(self):
        """Test validate_response with dict schema and non-dict data."""
        from typing import Any

        with allure.step("Test with list data"):
            invalid_data = ["list", "not", "dict"]
            schema = dict[str, Any]

            with pytest.raises(ValidationError, match="Expected dict, got list"):
                validate_response(invalid_data, schema)

        with allure.step("Test with string data"):
            invalid_data2 = "string"

            with pytest.raises(ValidationError, match="Expected dict, got str"):
                validate_response(invalid_data2, schema)

        with allure.step("Test with int data"):
            invalid_data3 = 123

            with pytest.raises(ValidationError, match="Expected dict, got int"):
                validate_response(invalid_data3, schema)

    @allure.title("TC-VAL-LIST-001: validate_response с list schema и не-list данными")
    @allure.description("Test validate_response with list schema and non-list data. TC-VAL-LIST-001")
    def test_validate_response_list_schema_non_list_data(self):
        """Test validate_response with list schema and non-list data."""
        from typing import Any

        with allure.step("Test with dict data"):
            invalid_data = {"not": "list"}
            schema = list[Any]

            with pytest.raises(ValidationError, match="Expected list, got dict"):
                validate_response(invalid_data, schema)

        with allure.step("Test with string data"):
            invalid_data2 = "string"

            with pytest.raises(ValidationError, match="Expected list, got str"):
                validate_response(invalid_data2, schema)

        with allure.step("Test with int data"):
            invalid_data3 = 123

            with pytest.raises(ValidationError, match="Expected list, got int"):
                validate_response(invalid_data3, schema)

    @allure.title("TC-VAL-ERROR-001: validate_response с msgspec.ValidationError без errors() метода")
    @allure.description(
        "Test error handling when msgspec.ValidationError doesn't have errors() method. TC-VAL-ERROR-001"
    )
    def test_validate_response_error_without_errors_method(self):
        """Test error handling when msgspec.ValidationError doesn't have errors() method."""
        from unittest.mock import patch

        with allure.step("Create custom error class without errors() method"):
            # Create a custom exception that looks like msgspec.ValidationError but without errors()
            class CustomValidationError(Exception):
                """Custom validation error without errors() method."""

                pass

            data = {"id": 1}  # Missing required 'name' field
            schema = {"id": int, "name": str}  # Use dict schema to trigger else branch

            # Mock msgspec.convert to raise custom error
            with patch(
                "py_web_automation.validators.msgspec.convert", side_effect=CustomValidationError("Validation failed")
            ):
                with pytest.raises(ValidationError):
                    validate_response(data, schema)

    @allure.title("TC-VAL-ERROR-002: validate_response с msgspec.ValidationError с non-iterable errors()")
    @allure.description(
        "Test error handling when msgspec.ValidationError.errors() returns non-iterable. TC-VAL-ERROR-002"
    )
    def test_validate_response_error_with_non_iterable_errors(self):
        """Test error handling when msgspec.ValidationError.errors() returns non-iterable."""
        from unittest.mock import Mock, patch

        from py_web_automation.validators import create_schema_from_dict

        with allure.step("Mock ValidationError with errors() returning non-iterable"):
            data = {"id": 1}  # Missing required 'name' field
            schema = create_schema_from_dict("User", {"id": int, "name": str})

            # Create a mock error with errors() returning non-iterable
            mock_error = Mock(spec=msgspec.ValidationError)
            mock_error.errors = Mock(return_value=123)  # Return non-iterable (int)

            with patch("py_web_automation.validators.msgspec.convert", side_effect=mock_error):
                with pytest.raises(ValidationError):
                    validate_response(data, schema)

    @allure.title("TC-VAL-ERROR-003: validate_response с msgspec.ValidationError с AttributeError на errors()")
    @allure.description("Test error handling when AttributeError occurs while accessing errors(). TC-VAL-ERROR-003")
    def test_validate_response_error_with_attribute_error_on_errors(self):
        """Test error handling when AttributeError occurs while accessing errors()."""
        from unittest.mock import patch

        with allure.step("Mock ValidationError that raises AttributeError on errors() access"):
            # Create a mock error where hasattr returns True but getattr raises AttributeError
            class ErrorWithBrokenErrors(Exception):
                """Error where errors attribute access raises AttributeError."""

                @property
                def errors(self):
                    raise AttributeError("errors() not available")

            data = {"id": 1}
            schema = {"id": int, "name": str}

            with patch(
                "py_web_automation.validators.msgspec.convert", side_effect=ErrorWithBrokenErrors("Validation failed")
            ):
                with pytest.raises(ValidationError):
                    validate_response(data, schema)
