"""
Request builder for constructing complex HTTP requests.

This module provides RequestBuilder class following the Builder pattern
for constructing complex HTTP requests with a fluent API.
"""

# Python imports
from http import HTTPMethod
from typing import TYPE_CHECKING, Any

from loguru import logger

# Local imports
from .http_result import HttpResult

if TYPE_CHECKING:
    from loguru._logger import Logger

    from .http_client import HttpClient


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
    - Request body (JSON dict, bytes, or str - automatically detected)
    - Headers
    - Authentication

    Request body format is automatically determined by type:
    - dict: Sent as JSON with Content-Type: application/json
    - bytes/str: Sent as raw content (set Content-Type header explicitly)

    Attributes:
        _client: HttpClient instance for executing requests
        _method: HTTP method (default: "GET")
        _endpoint: API endpoint path
        _params: Query parameters dictionary
        _data: Request body data (dict, bytes, str, or None)
        _headers: Request headers dictionary
    """

    def __init__(self, client: "HttpClient") -> None:
        """
        Initialize request builder.

        Args:
            client: HttpClient instance for executing requests

        Raises:
            TypeError: If client is not an HttpClient instance

        Example:
            >>> builder = RequestBuilder(api_client)
        """
        if not isinstance(client, HttpClient):
            raise TypeError(f"Expected HttpClient, got {type(client).__name__}")
        self._client: HttpClient = client
        self._method: HTTPMethod = HTTPMethod.GET
        self._endpoint: str = ""
        self._params: dict[str, Any] = {}
        self._data: dict[str, Any] | bytes | str | None = None
        self._headers: dict[str, str] = {}
        self.__logger: Logger = logger.bind(name=self.__class__.__name__)

    @property
    def get_endpoint(self) -> str:
        """Get request endpoint."""
        return self._endpoint

    @property
    def get_method(self) -> HTTPMethod:
        """Get HTTP method."""
        return self._method

    @property
    def get_data(self) -> dict[str, Any] | bytes | str | None:
        """Get request body data."""
        return self._data

    @property
    def get_headers(self) -> dict[str, str]:
        """Get request headers."""
        return self._headers.copy()

    @property
    def get_params(self) -> dict[str, Any]:
        """Get query parameters."""
        return self._params.copy()

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
        self.__logger.debug(f"Setting HTTP method to GET and endpoint to {endpoint}")
        self._method = HTTPMethod.GET
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
        self.__logger.debug(f"Setting HTTP method to POST and endpoint to {endpoint}")
        self._method = HTTPMethod.POST
        self._endpoint = endpoint
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
        self.__logger.debug(f"Setting HTTP method to PUT and endpoint to {endpoint}")
        self._method = HTTPMethod.PUT
        self._endpoint = endpoint
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
        self.__logger.debug(f"Setting HTTP method to DELETE and endpoint to {endpoint}")
        self._method = HTTPMethod.DELETE
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
        self.__logger.debug(f"Setting HTTP method to PATCH and endpoint to {endpoint}")
        self._method = HTTPMethod.PATCH
        self._endpoint = endpoint
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
        self.__logger.debug(f"Setting HTTP method to HEAD and endpoint to {endpoint}")
        self._method = HTTPMethod.HEAD
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
        self.__logger.debug(f"Setting HTTP method to OPTIONS and endpoint to {endpoint}")
        self._method = HTTPMethod.OPTIONS
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
        self.__logger.debug(f"Adding query parameters: {kwargs}")
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
        self.__logger.debug(f"Adding single query parameter: {key}={value}")
        self._params[key] = value
        return self

    def body(self, data: dict[str, Any] | bytes | str) -> "RequestBuilder":
        """
        Set request body data.

        Supports multiple data types:
        - dict: Will be sent as JSON (Content-Type: application/json)
        - bytes/str: Will be sent as raw content (set Content-Type in headers if needed)

        Args:
            data: Request body data (dict, bytes, or str)

        Returns:
            Self for method chaining

        Example:
            >>> # JSON body (dict)
            >>> builder.body({"name": "John"})
            >>> # XML body (str)
            >>> builder.body("<user><name>John</name></user>").header("Content-Type", "text/xml")
            >>> # Binary body (bytes)
            >>> builder.body(b"binary data").header("Content-Type", "application/octet-stream")
        """
        self.__logger.debug(f"Setting request body: type={type(data).__name__}")
        self._data = data
        return self

    def json(self, data: dict[str, Any]) -> "RequestBuilder":
        """
        Set request body as JSON (alias for body with dict).

        Convenience method for setting JSON body. Type is automatically detected.

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
        self.__logger.debug(f"Adding request header: {key}={value}")
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
        self.__logger.debug(f"Adding multiple request headers: {kwargs}")
        self._headers.update(kwargs)
        return self

    async def execute(self) -> HttpResult:
        """
        Execute the built request.

        Executes the built request using the HttpClient.

        Returns:
            HttpResult with request result

        Example:
            >>> result = await builder.get("/users").params(page=1).execute()
        """
        data_repr = (
            self._data.decode("utf-8", errors="replace")
            if isinstance(self._data, bytes)
            else self._data
        )
        self.__logger.debug(
            "Executing built request: "
            f"endpoint={self._endpoint} "
            f"method={self._method} "
            f"data={data_repr} "
            f"params={self._params} "
            f"headers={self._headers}"
        )
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
        self.__logger.debug("Resetting builder to initial state")
        self._method = HTTPMethod.GET
        self._endpoint = ""
        self._params.clear()
        self._data = None
        self._headers.clear()
        return self
