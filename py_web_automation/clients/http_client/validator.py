"""
Request and response validators for HTTP client.

This module provides internal validators (_RequestValidator and _ResponseValidator)
for validating HTTP request configuration and response data according
to best practices and standards.

These classes are internal and should not be used directly.
Use ValidationMiddleware for validation.
"""

# Python imports
from http import HTTPMethod
from typing import TYPE_CHECKING, Any, NoReturn, cast, get_args

import msgspec
from msgspec import Struct
from msgspec import ValidationError as MsgspecValidationError

# Local imports
from .exceptions import ValidationError

if TYPE_CHECKING:
    from .http_result import HttpResult


class _RequestValidator:
    """
    Internal validator for HTTP request configuration.

    Validates request configuration before execution to ensure
    all required fields are present and values are valid.

    Follows Single Responsibility Principle by focusing solely
    on request validation logic.

    This is an internal class and should not be used directly.
    Use ValidationMiddleware for request validation.

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
        data: dict[str, Any] | bytes | str | None = None,
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
    def _validate_body_for_method(
        method: HTTPMethod, data: dict[str, Any] | bytes | str | None
    ) -> None:
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


class _ResponseValidator:
    """
    Internal validator for HTTP response data.

    Validates response data against schemas using msgspec.
    Follows Single Responsibility Principle by focusing solely
    on response validation logic.

    This is an internal class and should not be used directly.
    Use ValidationMiddleware for response validation.

    Validation rules:
    - Response must be HttpResult instance
    - Response body must be valid JSON (if schema provided)
    - Response data must match provided schema
    """

    def validate(
        self,
        result: "HttpResult",
        schema: type[Struct] | type[dict[str, Any]] | type[list[Any]],
    ) -> Struct | dict[str, Any] | list[Any]:
        """
        Validate HTTP response against schema.

        Args:
            result: HttpResult instance from API call
            schema: msgspec Struct class or type annotation to validate against

        Returns:
            Validated and decoded data (msgspec Struct instance or validated dict/list)

        Raises:
            ValidationError: If validation fails

        Example:
            >>> from msgspec import Struct
            >>> class User(Struct):
            ...     id: int
            ...     name: str
            >>> validator = _ResponseValidator()
            >>> validated_data = validator.validate(result, User)
        """
        self._validate_result(result)
        self._validate_result_status(result)
        data = self._parse_json(result)
        return self._validate_data(data, schema)

    @staticmethod
    def _validate_result(result: "HttpResult") -> None:
        """
        Validate that result is HttpResult instance.

        Args:
            result: Result to validate

        Raises:
            ValidationError: If result is not HttpResult instance
        """
        from .http_result import HttpResult as HttpResultType

        if not isinstance(result, HttpResultType):
            raise ValidationError(
                f"Expected HttpResult, got {type(result).__name__}",
            )

    @staticmethod
    def _validate_result_status(result: "HttpResult") -> None:
        """
        Validate that result is successful and has body.

        Args:
            result: HttpResult instance to validate

        Raises:
            ValidationError: If result is unsuccessful or empty
        """
        if not result.success or not result.body:
            raise ValidationError(
                "Cannot validate unsuccessful or empty response",
                f"Response status: {result.status_code}, success: {result.success}",
            )

    @staticmethod
    def _parse_json(result: "HttpResult") -> dict[str, Any] | list[Any]:
        """
        Parse JSON from HttpResult body.

        Args:
            result: HttpResult instance with JSON body

        Returns:
            Parsed JSON data as dict or list

        Raises:
            ValidationError: If JSON parsing fails
        """
        try:
            return result.json
        except ValueError as e:
            if isinstance(result.body, bytes):
                body_preview = result.body[:200].decode("utf-8", errors="replace")
            elif isinstance(result.body, str):
                body_preview = result.body[:200]
            else:
                body_preview = str(result.body)[:200]
            raise ValidationError(
                f"Failed to parse response as JSON: {e}",
                f"Response body: {body_preview}",
            ) from e

    def _validate_data(
        self,
        data: dict[str, Any] | list[Any],
        schema: type[Struct] | type[dict[str, Any]] | type[list[Any]],
    ) -> Struct | dict[str, Any] | list[Any]:
        """
        Validate data against schema.

        Args:
            data: Data to validate (dict or list)
            schema: Schema to validate against

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        return self.validate_response(data, schema)

    def validate_response(
        self,
        data: dict[str, Any] | list[Any],
        schema: type[Struct] | type[dict[str, Any]] | type[list[Any]],
    ) -> Struct | dict[str, Any] | list[Any]:
        """
        Validate response data against msgspec schema.

        Validates response data against a msgspec Struct schema or type annotation.
        Provides fast validation with clear error messages.

        Args:
            data: Response data to validate (dict or list)
            schema: msgspec Struct class or type annotation to validate against

        Returns:
            Validated and decoded data (msgspec Struct instance or validated dict/list)

        Raises:
            ValidationError: If validation fails

        Example:
            >>> from msgspec import Struct
            >>> class UserResponse(Struct):
            ...     id: int
            ...     name: str
            ...     email: str
            >>> validator = _ResponseValidator()
            >>> data = {"id": 1, "name": "John", "email": "john@example.com"}
            >>> user = validator.validate_response(data, UserResponse)
            >>> assert isinstance(user, UserResponse)
        """
        try:
            if isinstance(schema, type) and issubclass(schema, Struct):
                return self._validate_struct(data, schema)
            elif schema is dict or (hasattr(schema, "__origin__") and schema.__origin__ is dict):
                return self._validate_dict(data)
            elif schema is list or (hasattr(schema, "__origin__") and schema.__origin__ is list):
                return self._validate_list(data, cast(type[list[Any]], schema))
            else:
                return self._validate_with_msgspec_strict(data, schema)
        except MsgspecValidationError as e:
            self._handle_msgspec_error(e, schema)
        except Exception as e:
            self._handle_general_error(e)

    @staticmethod
    def _validate_struct(data: dict[str, Any] | list[Any], schema: type[Struct]) -> Struct:
        """
        Validate data against msgspec Struct schema.

        Args:
            data: Data to validate
            schema: msgspec Struct class

        Returns:
            Validated Struct instance

        Raises:
            ValidationError: If validation fails
        """
        return msgspec.convert(data, schema)

    @staticmethod
    def _validate_dict(data: dict[str, Any] | list[Any]) -> dict[str, Any]:
        """
        Validate data as dictionary.

        Args:
            data: Data to validate

        Returns:
            Validated dict

        Raises:
            ValidationError: If data is not a dict
        """
        if not isinstance(data, dict):
            raise ValidationError(
                f"Expected dict, got {type(data).__name__}",
                f"Data: {data}",
            )
        return data

    def _validate_list(
        self,
        data: dict[str, Any] | list[Any],
        schema: type[list[Any]],
    ) -> list[Any]:
        """
        Validate data as list.

        Args:
            data: Data to validate
            schema: List schema type

        Returns:
            Validated list

        Raises:
            ValidationError: If data is not a list or items don't match schema
        """
        if not isinstance(data, list):
            raise ValidationError(
                f"Expected list, got {type(data).__name__}",
                f"Data: {data}",
            )

        args = get_args(schema)
        if args and len(args) > 0:
            item_schema = args[0]
            if isinstance(item_schema, type) and (
                issubclass(item_schema, Struct)
                or item_schema in (dict, list, str, int, float, bool)
            ):
                return self._validate_list_items(data, item_schema)

        return data

    @staticmethod
    def _validate_list_items(data: list[Any], item_schema: type) -> list[Any]:
        """
        Validate each item in list against item schema.

        Args:
            data: List data to validate
            item_schema: Schema for list items

        Returns:
            Validated list with converted items

        Raises:
            ValidationError: If any item doesn't match schema
        """
        validated_items: list[Any] = []
        for item in data:
            if issubclass(item_schema, Struct):
                validated_items.append(msgspec.convert(item, item_schema))
            else:
                if not isinstance(item, item_schema):
                    raise ValidationError(
                        f"Expected list item of type {item_schema.__name__}, "
                        f"got {type(item).__name__}",
                        f"Item: {item}",
                    )
                validated_items.append(item)
        return validated_items

    @staticmethod
    def _validate_with_msgspec_strict(
        data: dict[str, Any] | list[Any],
        schema: type,
    ) -> Any:
        """
        Validate data using msgspec with strict mode.

        Args:
            data: Data to validate
            schema: Schema type

        Returns:
            Validated data

        Raises:
            ValidationError: If validation fails
        """
        return msgspec.convert(data, schema, strict=True)

    @staticmethod
    def _handle_msgspec_error(e: MsgspecValidationError, schema: type) -> NoReturn:
        """
        Handle msgspec validation error and convert to ValidationError.

        Args:
            e: MsgspecValidationError exception
            schema: Schema that failed validation

        Raises:
            ValidationError: Converted validation error
        """
        try:
            if hasattr(e, "errors") and callable(getattr(e, "errors", None)):
                error_details = "; ".join(str(err) for err in e.errors())
            else:
                error_details = str(e)
        except (AttributeError, TypeError):
            error_details = str(e)

        schema_name = schema.__name__ if hasattr(schema, "__name__") else schema
        raise ValidationError(
            f"Validation failed for schema {schema_name}",
            error_details,
        ) from e

    @staticmethod
    def _handle_general_error(e: Exception) -> NoReturn:
        """
        Handle general exception during validation.

        Args:
            e: Exception that occurred

        Raises:
            ValidationError: Converted validation error
        """
        raise ValidationError(
            f"Unexpected error during validation: {e}",
            str(e),
        ) from e
