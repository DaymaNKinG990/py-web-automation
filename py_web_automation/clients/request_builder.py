"""
Request builder for constructing complex HTTP requests.

This module provides RequestBuilder class following the Builder pattern
for constructing complex HTTP requests with a fluent API.
"""

from typing import TYPE_CHECKING, Any

from ..exceptions import ValidationError
from .models import ApiResult

if TYPE_CHECKING:
    from .api_client import ApiClient


class RequestBuilder:
    """
    Builder for constructing HTTP requests with fluent API.

    Implements the Builder pattern to allow constructing complex HTTP requests
    step by step with a fluent, chainable interface. Follows the Single Responsibility
    Principle by focusing solely on request construction.

    Provides fluent methods for building requests:
    - Method selection (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
    - Endpoint configuration
    - Query parameters
    - Request body (JSON, form data, raw)
    - Headers
    - Authentication

    Attributes:
        _client: ApiClient instance for executing requests
        _method: HTTP method (default: "GET")
        _endpoint: API endpoint path
        _params: Query parameters dictionary
        _data: Request body data
        _headers: Request headers dictionary
        _json_body: Whether to send body as JSON (default: True)

    Example:
        >>> from py_web_automation import Config, ApiClient, RequestBuilder
        >>> config = Config(timeout=30)
        >>> async with ApiClient("https://api.example.com", config) as api:
        ...     builder = RequestBuilder(api)
        ...     result = await (builder
        ...         .get("/users")
        ...         .params({"page": 1, "limit": 10})
        ...         .header("X-Custom-Header", "value")
        ...         .execute())
    """

    def __init__(self, client: "ApiClient") -> None:
        """
        Initialize request builder.

        Args:
            client: ApiClient instance for executing requests

        Raises:
            TypeError: If client is not an ApiClient instance

        Example:
            >>> builder = RequestBuilder(api_client)
        """
        from .api_client import ApiClient

        if not isinstance(client, ApiClient):
            raise TypeError(f"Expected ApiClient, got {type(client).__name__}")

        self._client: ApiClient = client
        self._method: str = "GET"
        self._endpoint: str = ""
        self._params: dict[str, Any] = {}
        self._data: dict[str, Any] | None = None
        self._headers: dict[str, str] = {}
        self._json_body: bool = True

    def get(self, endpoint: str) -> "RequestBuilder":
        """
        Set HTTP method to GET and endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Self for method chaining

        Example:
            >>> builder.get("/users")
        """
        self._method = "GET"
        self._endpoint = endpoint
        return self

    def post(self, endpoint: str) -> "RequestBuilder":
        """
        Set HTTP method to POST and endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Self for method chaining

        Example:
            >>> builder.post("/users")
        """
        self._method = "POST"
        self._endpoint = endpoint
        self._json_body = True
        return self

    def put(self, endpoint: str) -> "RequestBuilder":
        """
        Set HTTP method to PUT and endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Self for method chaining

        Example:
            >>> builder.put("/users/1")
        """
        self._method = "PUT"
        self._endpoint = endpoint
        self._json_body = True
        return self

    def delete(self, endpoint: str) -> "RequestBuilder":
        """
        Set HTTP method to DELETE and endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Self for method chaining

        Example:
            >>> builder.delete("/users/1")
        """
        self._method = "DELETE"
        self._endpoint = endpoint
        return self

    def patch(self, endpoint: str) -> "RequestBuilder":
        """
        Set HTTP method to PATCH and endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Self for method chaining

        Example:
            >>> builder.patch("/users/1")
        """
        self._method = "PATCH"
        self._endpoint = endpoint
        self._json_body = True
        return self

    def head(self, endpoint: str) -> "RequestBuilder":
        """
        Set HTTP method to HEAD and endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Self for method chaining

        Example:
            >>> builder.head("/users")
        """
        self._method = "HEAD"
        self._endpoint = endpoint
        return self

    def options(self, endpoint: str) -> "RequestBuilder":
        """
        Set HTTP method to OPTIONS and endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Self for method chaining

        Example:
            >>> builder.options("/users")
        """
        self._method = "OPTIONS"
        self._endpoint = endpoint
        return self

    def params(self, **kwargs: Any) -> "RequestBuilder":
        """
        Add query parameters.

        Args:
            **kwargs: Query parameters as keyword arguments

        Returns:
            Self for method chaining

        Example:
            >>> builder.params(page=1, limit=10)
            >>> # Or with dict
            >>> builder.params(**{"page": 1, "limit": 10})
        """
        self._params.update(kwargs)
        return self

    def param(self, key: str, value: Any) -> "RequestBuilder":
        """
        Add single query parameter.

        Args:
            key: Parameter name
            value: Parameter value

        Returns:
            Self for method chaining

        Example:
            >>> builder.param("page", 1)
        """
        self._params[key] = value
        return self

    def body(self, data: dict[str, Any]) -> "RequestBuilder":
        """
        Set request body (JSON).

        Args:
            data: Request body data as dictionary

        Returns:
            Self for method chaining

        Example:
            >>> builder.body({"name": "John", "email": "john@example.com"})
        """
        self._data = data
        self._json_body = True
        return self

    def json(self, data: dict[str, Any]) -> "RequestBuilder":
        """
        Set request body as JSON (alias for body).

        Args:
            data: Request body data as dictionary

        Returns:
            Self for method chaining

        Example:
            >>> builder.json({"name": "John"})
        """
        return self.body(data)

    def header(self, key: str, value: str) -> "RequestBuilder":
        """
        Add request header.

        Args:
            key: Header name
            value: Header value

        Returns:
            Self for method chaining

        Example:
            >>> builder.header("X-Custom-Header", "value")
        """
        self._headers[key] = value
        return self

    def headers(self, **kwargs: str) -> "RequestBuilder":
        """
        Add multiple request headers.

        Args:
            **kwargs: Headers as keyword arguments

        Returns:
            Self for method chaining

        Example:
            >>> builder.headers(
            ...     X_Custom_Header="value",
            ...     X_Another_Header="another"
            ... )
        """
        self._headers.update(kwargs)
        return self

    def auth(self, token: str, token_type: str = "Bearer") -> "RequestBuilder":
        """
        Set authentication token.

        Args:
            token: Authentication token
            token_type: Token type (default: "Bearer")

        Returns:
            Self for method chaining

        Example:
            >>> builder.auth("your-token-here")
        """
        self._client.set_auth_token(token, token_type)
        return self

    def validate(self) -> None:
        """
        Validate request configuration.

        Raises:
            ValidationError: If request configuration is invalid

        Example:
            >>> builder.get("/users").validate()
        """
        if not self._endpoint:
            raise ValidationError(
                "Request endpoint is required",
                "Call get(), post(), put(), delete(), etc. to set endpoint",
            )

        if self._method in ("POST", "PUT", "PATCH") and self._data is None:
            # Allow empty body for these methods
            pass

    async def execute(self) -> ApiResult:
        """
        Execute the built request.

        Validates request configuration and executes it using the ApiClient.

        Returns:
            ApiResult with request result

        Raises:
            ValidationError: If request configuration is invalid

        Example:
            >>> result = await builder.get("/users").params(page=1).execute()
        """
        self.validate()

        return await self._client.make_request(
            endpoint=self._endpoint,
            method=self._method,
            data=self._data,
            params=self._params if self._params else None,
            headers=self._headers if self._headers else None,
        )

    def reset(self) -> "RequestBuilder":
        """
        Reset builder to initial state.

        Returns:
            Self for method chaining

        Example:
            >>> builder.reset()
        """
        self._method = "GET"
        self._endpoint = ""
        self._params.clear()
        self._data = None
        self._headers.clear()
        self._json_body = True
        return self
