"""
Unit tests for utility functions.
"""

import json
from typing import Any

import allure
import pytest

from py_web_automation.utils import (
    extract_pagination_info,
    get_error_detail,
    parse_json,
    validate_response_structure,
)

# Apply markers to all tests in this module
pytestmark = [pytest.mark.unit]


class TestParseJson:
    """Test parse_json utility function."""

    @pytest.mark.parametrize(
        "input_data,expected,test_id,description",
        [
            (
                {"key": "value", "number": 123},
                {"key": "value", "number": 123},
                "TC-UTILS-001",
                "parse_json with valid JSON",
            ),
            (
                b"not valid json",
                {},
                "TC-UTILS-002",
                "parse_json with invalid JSON returns empty dict",
            ),
            (
                b"",
                {},
                "TC-UTILS-003",
                "parse_json with empty body",
            ),
            (
                {"message": "Привет", "emoji": "🎉"},
                {"message": "Привет", "emoji": "🎉"},
                "TC-UTILS-004",
                "parse_json with unicode characters",
            ),
        ],
    )
    @allure.title("{test_id}: {description}")
    @allure.description("Test {description}. {test_id}")
    def test_parse_json(self, input_data, expected, test_id, description):
        """Test parse_json with various inputs."""
        with allure.step(f"Prepare input data for {description}"):
            if isinstance(input_data, dict):
                body = json.dumps(input_data, ensure_ascii=False).encode("utf-8")
            else:
                body = input_data

        with allure.step("Call parse_json and verify result"):
            result = parse_json(body)

            assert result == expected
            if isinstance(expected, dict) and expected:
                # Additional checks for valid JSON
                for key, value in expected.items():
                    assert result[key] == value


class TestValidateResponseStructure:
    """Test validate_response_structure utility function."""

    @allure.title("TC-UTILS-005: validate_response_structure with all fields present")
    @allure.description("Test validate_response_structure with all fields present. TC-UTILS-005")
    def test_validate_response_structure_all_fields_present(self):
        """Test validate_response_structure with all fields present."""
        with allure.step("Prepare data with all expected fields"):
            data = {"name": "test", "id": 123, "status": "active"}
            expected_fields = ["name", "id", "status"]

        with allure.step("Call validate_response_structure and verify True"):
            result = validate_response_structure(data, expected_fields)

            assert result is True

    @allure.title("TC-UTILS-006: validate_response_structure with missing fields")
    @allure.description("Test validate_response_structure with missing fields. TC-UTILS-006")
    def test_validate_response_structure_missing_fields(self):
        """Test validate_response_structure with missing fields."""
        with allure.step("Prepare data with missing fields"):
            data = {"name": "test", "id": 123}
            expected_fields = ["name", "id", "status", "email"]

        with allure.step("Call validate_response_structure and verify False"):
            result = validate_response_structure(data, expected_fields)

            assert result is False

    @allure.title("TC-UTILS-007: validate_response_structure with empty expected fields")
    @allure.description("Test validate_response_structure with empty expected fields. TC-UTILS-007")
    def test_validate_response_structure_empty_fields(self):
        """Test validate_response_structure with empty expected fields."""
        with allure.step("Prepare data with empty expected fields list"):
            data = {"name": "test"}
            expected_fields: list[str] = []

        with allure.step("Call validate_response_structure and verify True"):
            result = validate_response_structure(data, expected_fields)

            assert result is True


class TestExtractPaginationInfo:
    """Test extract_pagination_info utility function."""

    @allure.title("TC-UTILS-008: extract_pagination_info with complete pagination data")
    @allure.description("Test extract_pagination_info with complete pagination data. TC-UTILS-008")
    def test_extract_pagination_info_complete(self):
        """Test extract_pagination_info with complete pagination data."""
        with allure.step("Prepare data with complete pagination fields"):
            data = {
                "count": 100,
                "next": "http://api.example.com/items/?page=2",
                "previous": None,
                "results": [{"id": 1}, {"id": 2}],
            }

        with allure.step("Call extract_pagination_info and verify all fields"):
            result = extract_pagination_info(data)

            assert result["count"] == 100
            assert result["next"] == "http://api.example.com/items/?page=2"
            assert result["previous"] is None
            assert result["results"] == [{"id": 1}, {"id": 2}]

    @allure.title("TC-UTILS-009: extract_pagination_info with partial pagination data")
    @allure.description("Test extract_pagination_info with partial pagination data. TC-UTILS-009")
    def test_extract_pagination_info_partial(self):
        """Test extract_pagination_info with partial pagination data."""
        with allure.step("Prepare data with only count field"):
            data = {"count": 50}

        with allure.step("Call extract_pagination_info and verify default values"):
            result = extract_pagination_info(data)

            assert result["count"] == 50
            assert result["next"] is None
            assert result["previous"] is None
            assert result["results"] == []

    @allure.title("TC-UTILS-010: extract_pagination_info with empty data")
    @allure.description("Test extract_pagination_info with empty data. TC-UTILS-010")
    def test_extract_pagination_info_empty(self):
        """Test extract_pagination_info with empty data."""
        with allure.step("Prepare empty data dictionary"):
            data: dict[str, Any] = {}

        with allure.step("Call extract_pagination_info and verify all None/default values"):
            result = extract_pagination_info(data)

            assert result["count"] is None
            assert result["next"] is None
            assert result["previous"] is None
            assert result["results"] == []


class TestGetErrorDetail:
    """Test get_error_detail utility function."""

    @allure.title("TC-UTILS-011: get_error_detail extracts 'detail' field")
    @allure.description("Test get_error_detail extracts 'detail' field. TC-UTILS-011")
    def test_get_error_detail_with_detail(self):
        """Test get_error_detail extracts 'detail' field."""
        with allure.step("Prepare data with 'detail' field"):
            data = {"detail": "Error message"}

        with allure.step("Call get_error_detail and verify 'detail' is extracted"):
            result = get_error_detail(data)

            assert result == "Error message"

    @allure.title("TC-UTILS-012: get_error_detail extracts 'error' field when 'detail' missing")
    @allure.description("Test get_error_detail extracts 'error' field when 'detail' missing. TC-UTILS-012")
    def test_get_error_detail_with_error(self):
        """Test get_error_detail extracts 'error' field when 'detail' missing."""
        with allure.step("Prepare data with 'error' field (no 'detail')"):
            data = {"error": "Error message"}

        with allure.step("Call get_error_detail and verify 'error' is extracted"):
            result = get_error_detail(data)

            assert result == "Error message"

    @allure.title("TC-UTILS-013: get_error_detail falls back to string representation")
    @allure.description("Test get_error_detail falls back to string representation. TC-UTILS-013")
    def test_get_error_detail_fallback(self):
        """Test get_error_detail falls back to string representation."""
        with allure.step("Prepare data without 'detail' or 'error' fields"):
            data = {"message": "Some message"}

        with allure.step("Call get_error_detail and verify fallback to string representation"):
            result = get_error_detail(data)

            assert isinstance(result, str)
            assert "message" in result or "Some message" in result
