"""
Validation middleware for HTTP client.

This module provides ValidationMiddleware for request and response validation.
"""

# Local imports
from ..http_result import HttpResult
from ..validator import _RequestValidator, _ResponseValidator
from .context import _HttpRequestContext, _HttpResponseContext
from .middleware import Middleware


class ValidationMiddleware(Middleware):
    """
    Middleware for request and response validation.

    Validates requests using RequestValidator and responses against schemas
    using ResponseValidator.

    Example:
        >>> from msgspec import Struct
        >>> class User(Struct):
        ...     id: int
        ...     name: str
        >>> chain.add(ValidationMiddleware(User))
    """

    def __init__(self, schema: type) -> None:
        """
        Initialize validation middleware.

        Args:
            schema: msgspec.Struct or dict schema for validation
        """
        self.schema = schema

    async def process_request(self, context: _HttpRequestContext) -> None:
        """
        Validate request configuration.

        Args:
            context: Request context
        """
        validator = _RequestValidator()
        validator.validate(
            endpoint=context.url,
            method=context.method,
            data=context.data,
            headers=context.headers,
            params=context.params,
        )

    async def process_response(self, context: _HttpResponseContext) -> None:
        """
        Validate response against schema.

        Args:
            context: Response context
        """
        validator = _ResponseValidator()
        if context.result.success and context.result.body:
            try:
                validator.validate(context.result, self.schema)
            except Exception as e:
                # Store validation error in metadata
                context.metadata["validation_error"] = str(e)

    async def process_error(
        self, context: _HttpRequestContext, error: Exception
    ) -> HttpResult | None:
        """
        No-op for errors.

        Args:
            context: Request context
            error: Exception that occurred
        """
        return None
