"""
Utility functions for web automation testing framework.

This module provides helper functions for JSON parsing, response validation,
pagination extraction, and error handling.
"""

import json
from typing import Any


def parse_json(body: bytes) -> dict[str, Any]:
    """
    Parse JSON from bytes.

    Safely parses JSON data from bytes, returning an empty dictionary
    if parsing fails or body is empty.

    Args:
        body: JSON data as bytes

    Returns:
        Parsed JSON data as dictionary, or empty dict if parsing fails

    Example:
        >>> data = b'{"key": "value"}'
        >>> result = parse_json(data)
        >>> assert result == {"key": "value"}
    """
    if not body:
        return {}

    try:
        return json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        return {}


def validate_response_structure(data: dict[str, Any], expected_fields: list[str]) -> bool:
    """
    Validate that response data contains all expected fields.

    Checks if all required fields are present in the response data dictionary.

    Args:
        data: Response data dictionary to validate
        expected_fields: List of field names that must be present

    Returns:
        True if all expected fields are present, False otherwise

    Example:
        >>> data = {"name": "test", "id": 123, "status": "active"}
        >>> expected = ["name", "id", "status"]
        >>> assert validate_response_structure(data, expected) is True
    """
    if not expected_fields:
        return True

    return all(field in data for field in expected_fields)


def extract_pagination_info(data: dict[str, Any]) -> dict[str, Any]:
    """
    Extract pagination information from response data.

    Extracts common pagination fields from API response data,
    providing default values for missing fields.

    Args:
        data: Response data dictionary that may contain pagination fields

    Returns:
        Dictionary with pagination information:
        - count: Total number of items (optional)
        - next: URL to next page (optional)
        - previous: URL to previous page (optional)
        - results: List of items (default: empty list)

    Example:
        >>> data = {
        ...     "count": 100,
        ...     "next": "http://api.example.com/items/?page=2",
        ...     "results": [{"id": 1}, {"id": 2}]
        ... }
        >>> pagination = extract_pagination_info(data)
        >>> assert pagination["count"] == 100
        >>> assert pagination["next"] == "http://api.example.com/items/?page=2"
    """
    return {
        "count": data.get("count"),
        "next": data.get("next"),
        "previous": data.get("previous"),
        "results": data.get("results", []),
    }


def get_error_detail(data: dict[str, Any]) -> str:
    """
    Extract error detail from error response data.

    Attempts to extract error message from response data in the following order:
    1. 'detail' field (preferred)
    2. 'error' field (fallback)
    3. String representation of data (last resort)

    Args:
        data: Error response data dictionary

    Returns:
        Error message string

    Example:
        >>> data = {"detail": "Error message"}
        >>> assert get_error_detail(data) == "Error message"
        >>> data = {"error": "Error message"}
        >>> assert get_error_detail(data) == "Error message"
    """
    if "detail" in data:
        return str(data["detail"])

    if "error" in data:
        return str(data["error"])

    return str(data)
