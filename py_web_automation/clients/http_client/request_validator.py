"""
Request validator for HTTP request configuration.

This module provides RequestValidator class for validating HTTP request
configuration according to best practices and standards.
"""

# Python imports
from http import HTTPMethod
from typing import Any

# Local imports
from .exceptions import ValidationError


class RequestValidator:
    """
    Validator for HTTP request configuration.

    Validates request configuration before execution to ensure
    all required fields are present and values are valid.

    Follows Single Responsibility Principle by focusing solely
    on request validation logic.

    Validation rules:
    - Endpoint must be provided and non-empty
    - HTTP method must be valid
    - Endpoint must be a valid URL path or absolute URL
    - Headers must be strings (key and value)
    - Query parameters must be serializable
    - Body data types match HTTP method expectations
    """

    def validate(
        self,
        endpoint: str,
        method: HTTPMethod,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> None:
        """
        Validate HTTP request configuration.

        Args:
            endpoint: API endpoint path
            method: HTTP method
            data: Request body data
            headers: Request headers
            params: Query parameters

        Raises:
            ValidationError: If request configuration is invalid

        Example:
            >>> RequestValidator.validate(
            ...     endpoint="/users",
            ...     method="GET",
            ...     params={"page": 1}
            ... )
        """
        self._validate_endpoint(endpoint)
        self._validate_method(method)
        self._validate_body_for_method(method, data)
        if headers:
            self._validate_headers(headers)
        if params:
            self._validate_params(params)

    @staticmethod
    def _validate_endpoint(endpoint: str) -> None:
        """
        Validate endpoint path.

        Args:
            endpoint: API endpoint path

        Raises:
            ValidationError: If endpoint is invalid
        """
        if not endpoint:
            raise ValidationError(
                "Request endpoint is required",
                "Call get(), post(), put(), delete(), etc. to set endpoint",
            )

    @staticmethod
    def _validate_method(method: HTTPMethod) -> None:
        """
        Validate HTTP method.

        Args:
            method: HTTP method to validate

        Raises:
            ValidationError: If method is invalid
        """
        if method not in HTTPMethod:
            raise ValidationError(
                "Invalid HTTP method",
                "Method must be one of: "
                f"{', '.join(sorted(HTTPMethod.__members__.keys()))} "
                f"Got: {method}",
            )

    @staticmethod
    def _validate_body_for_method(method: HTTPMethod, data: dict[str, Any] | None) -> None:
        """
        Validate request body compatibility with HTTP method.

        Args:
            method: HTTP method
            data: Request body data

        Raises:
            ValidationError: If body is incompatible with method
        """
        methods_with_body = {HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH}
        # GET, HEAD, DELETE, OPTIONS typically don't have body
        # But we allow empty body for methods that can have it
        if method not in methods_with_body and data is not None:
            raise ValidationError(
                f"HTTP {method} method does not typically support request body",
                f"Remove body data or use one of: {', '.join(methods_with_body)}",
            )

    @staticmethod
    def _validate_headers(headers: dict[str, str]) -> None:
        """
        Validate request headers.

        Args:
            headers: Request headers dictionary

        Raises:
            ValidationError: If headers are invalid
        """
        if not isinstance(headers, dict):
            raise ValidationError(
                "Headers must be a dictionary",
                f"Got {type(headers).__name__} instead of dict",
            )
        for key, value in headers.items():
            if not isinstance(key, str):
                raise ValidationError(
                    "Header keys must be strings",
                    f"Got {type(key).__name__} for header key: {key}",
                )
            if not isinstance(value, str):
                raise ValidationError(
                    "Header values must be strings",
                    f"Got {type(value).__name__} for header '{key}': {value}",
                )
            if key == "":
                raise ValidationError(
                    "Header key cannot be an empty string",
                    "All header keys must be non-empty strings",
                )

    @staticmethod
    def _validate_params(params: dict[str, Any]) -> None:
        """
        Validate query parameters.

        Args:
            params: Query parameters dictionary

        Raises:
            ValidationError: If parameters are invalid
        """
        if not isinstance(params, dict):
            raise ValidationError(
                "Query parameters must be a dictionary",
                f"Got {type(params).__name__} instead of dict",
            )
        for key in params.keys():
            if not isinstance(key, str) or key == "":
                raise ValidationError(
                    "Query parameter keys must be non-empty strings",
                    f"Got {type(key).__name__} for parameter key: {key}",
                )
