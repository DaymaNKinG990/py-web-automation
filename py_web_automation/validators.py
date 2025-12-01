"""
Response validation utilities using msgspec.

This module provides response validation functionality using msgspec
for fast and efficient schema validation of API responses.
"""

from typing import TYPE_CHECKING, Any, TypeVar, get_args

import msgspec
from msgspec import ValidationError as MsgspecValidationError

from .exceptions import ValidationError as FrameworkValidationError

if TYPE_CHECKING:
    from .clients.models import ApiResult

T = TypeVar("T")


def validate_response(
    data: dict[str, Any] | list[Any],
    schema: type[msgspec.Struct] | type[dict[str, Any]] | type[list[Any]],
) -> msgspec.Struct | dict[str, Any] | list[Any]:
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
        FrameworkValidationError: If validation fails

    Example:
        >>> from msgspec import Struct
        >>> class UserResponse(Struct):
        ...     id: int
        ...     name: str
        ...     email: str
        >>> data = {"id": 1, "name": "John", "email": "john@example.com"}
        >>> user = validate_response(data, UserResponse)
        >>> assert isinstance(user, UserResponse)
    """
    try:
        if isinstance(schema, type) and issubclass(schema, msgspec.Struct):
            # Validate against msgspec Struct
            return msgspec.convert(data, schema)
        # Check for dict schema (dict or dict[str, Any] etc.)
        elif schema is dict or (hasattr(schema, "__origin__") and schema.__origin__ is dict):
            # Validate as dict
            if not isinstance(data, dict):
                raise FrameworkValidationError(
                    f"Expected dict, got {type(data).__name__}",
                    f"Data: {data}",
                )
            return data
        # Check for list schema (list or list[Any] etc.)
        elif schema is list or (hasattr(schema, "__origin__") and schema.__origin__ is list):
            # Validate as list
            if not isinstance(data, list):
                raise FrameworkValidationError(
                    f"Expected list, got {type(data).__name__}",
                    f"Data: {data}",
                )
            # Check if list has item type specification (e.g., list[UserSchema])
            args = get_args(schema)
            if args and len(args) > 0:
                item_schema = args[0]
                # If item schema is a Struct or type, validate each item
                if isinstance(item_schema, type) and (
                    issubclass(item_schema, msgspec.Struct) or item_schema in (dict, list, str, int, float, bool)
                ):
                    # Validate each item in the list
                    validated_items: list[Any] = []
                    for item in data:
                        if issubclass(item_schema, msgspec.Struct):
                            # Convert dict to Struct instance
                            validated_items.append(msgspec.convert(item, item_schema))
                        else:
                            # For primitive types, just validate type
                            if not isinstance(item, item_schema):
                                raise FrameworkValidationError(
                                    f"Expected list item of type {item_schema.__name__}, got {type(item).__name__}",
                                    f"Item: {item}",
                                )
                            validated_items.append(item)
                    return validated_items
            # If no item type specified or not a Struct, return as-is
            return data
        else:
            # Try to convert using msgspec with strict mode
            return msgspec.convert(data, schema, strict=True)
    except MsgspecValidationError as e:
        # msgspec.ValidationError has errors() method that returns a list
        try:
            if hasattr(e, "errors") and callable(getattr(e, "errors", None)):
                error_details = "; ".join(str(err) for err in e.errors())
            else:
                error_details = str(e)
        except (AttributeError, TypeError):
            # Fallback if errors() is not available or returns non-iterable
            error_details = str(e)
        raise FrameworkValidationError(
            f"Validation failed for schema {schema.__name__ if hasattr(schema, '__name__') else schema}",
            error_details,
        ) from e
    except Exception as e:
        raise FrameworkValidationError(
            f"Unexpected error during validation: {e}",
            str(e),
        ) from e


def validate_json_response(
    json_data: str | bytes,
    schema: type[msgspec.Struct] | type[dict[str, Any]] | type[list[Any]],
) -> msgspec.Struct | dict[str, Any] | list[Any]:
    """
    Validate JSON string/bytes response against msgspec schema.

    Parses JSON and validates against schema in one step.

    Args:
        json_data: JSON string or bytes to parse and validate
        schema: msgspec Struct class or type annotation

    Returns:
        Validated and decoded data

    Raises:
        FrameworkValidationError: If JSON parsing or validation fails

    Example:
        >>> json_str = '{"id": 1, "name": "John"}'
        >>> user = validate_json_response(json_str, UserResponse)
    """
    try:
        # Parse JSON
        if isinstance(json_data, bytes):
            data = msgspec.json.decode(json_data)
        else:
            data = msgspec.json.decode(json_data.encode("utf-8"))
    except Exception as e:
        json_str = json_data if isinstance(json_data, str) else json_data.decode("utf-8", errors="replace")
        json_preview = json_str[:100] if len(json_str) > 100 else json_str
        raise FrameworkValidationError(
            f"Failed to parse JSON: {e}",
            f"JSON data: {json_preview}",
        ) from e

    # Validate parsed data
    return validate_response(data, schema)


def validate_api_result(
    result: "ApiResult",
    schema: type[msgspec.Struct] | type[dict[str, Any]] | type[list[Any]],
) -> msgspec.Struct | dict[str, Any] | list[Any]:
    """
    Validate ApiResult response body against msgspec schema.

    Convenience method to validate ApiResult.body against a schema.

    Args:
        result: ApiResult instance from API call
        schema: msgspec Struct class or type annotation

    Returns:
        Validated and decoded data

    Raises:
        FrameworkValidationError: If validation fails

    Example:
        >>> from py_web_automation import ApiClient
        >>> from py_web_automation.validators import validate_api_result
        >>> result = await api.make_request("/users/1")
        >>> user = validate_api_result(result, UserResponse)
    """
    from .clients.models import ApiResult as ApiResultType

    if not isinstance(result, ApiResultType):
        raise FrameworkValidationError(
            f"Expected ApiResult, got {type(result).__name__}",
        )

    try:
        data = result.json()
    except ValueError as e:
        if isinstance(result.body, bytes):
            body_preview = result.body[:200].decode("utf-8", errors="replace")
        elif isinstance(result.body, str):
            body_preview = result.body[:200]
        else:
            body_preview = str(result.body)[:200]
        raise FrameworkValidationError(
            f"Failed to parse response as JSON: {e}",
            f"Response body: {body_preview}",
        ) from e

    return validate_response(data, schema)


def create_schema_from_dict(name: str, fields: dict[str, type], frozen: bool = True) -> type[msgspec.Struct]:
    """
    Dynamically create msgspec Struct schema from dictionary.

    Creates a msgspec Struct class at runtime from field definitions.

    Args:
        name: Name for the schema class
        fields: Dictionary mapping field names to types
        frozen: Whether the struct should be frozen (immutable)

    Returns:
        msgspec Struct class

    Example:
        >>> UserSchema = create_schema_from_dict(
        ...     "User",
        ...     {"id": int, "name": str, "email": str}
        ... )
        >>> user = UserSchema(id=1, name="John", email="john@example.com")
    """
    # Create annotations dict
    annotations: dict[str, type] = {}
    defaults: dict[str, Any] = {}

    for field_name, field_type in fields.items():
        if isinstance(field_type, tuple):
            # Handle Optional fields: (type, None) or (type, default_value)
            field_type, default = field_type
            annotations[field_name] = field_type | None
            defaults[field_name] = default
        else:
            annotations[field_name] = field_type

    # Create class dynamically
    # msgspec.defstruct accepts fields as dict with (type, default) tuples for optional fields
    # Convert annotations and defaults to the format expected by defstruct
    defstruct_fields: dict[str, Any] = {}
    for field_name, field_type in annotations.items():
        if field_name in defaults:
            # Field has a default value
            defstruct_fields[field_name] = (field_type, defaults[field_name])
        else:
            # Required field
            defstruct_fields[field_name] = field_type

    schema_class = msgspec.defstruct(
        name,
        defstruct_fields,
        frozen=frozen,
    )

    return schema_class
