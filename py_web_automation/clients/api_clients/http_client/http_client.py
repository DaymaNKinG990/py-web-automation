"""
HTTP REST API client for web automation testing.

This module provides HttpClient for testing HTTP REST API endpoints,
including request handling, authentication, and response validation.
"""

# Python imports
import time
from http import HTTPMethod
from types import TracebackType
from typing import TYPE_CHECKING, Any, Union
from urllib.parse import urlencode

from httpx import AsyncClient, Limits, Response

# Local imports
from ....config import Config
from .http_result import HttpResult

if TYPE_CHECKING:
    from .middleware.context import _HttpRequestContext, _HttpResponseContext
    from .middleware.middleware import MiddlewareChain
    from .request_builder import _RequestBuilder


class HttpClient:
    """
    HTTP REST API client for web automation testing.

    Implements the Strategy pattern for HTTP request handling and follows
    the Single Responsibility Principle by focusing solely on REST API testing.

    Provides methods for testing HTTP REST API endpoints:
    - HTTP request handling (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
    - Authentication token management with automatic header injection
    - Response analysis and validation with comprehensive error handling
    - Query parameter and request body support
    - Custom headers support

    Attributes:
        client: HTTP client instance for making requests

    Example:
        >>> from py_web_automation import Config, HttpClient
        >>> config = Config(timeout=30)
        >>> async with HttpClient("https://api.example.com", config) as api:
        ...     result = await api.make_request("v1/users/", method="GET")
        ...     assert result.success
    """

    def __init__(
        self,
        url: str,
        config: Config,
        middleware: Union["MiddlewareChain", None] = None,
    ) -> None:
        """
        Initialize HTTP client.

        Creates an HTTP client with connection pooling and timeout configuration
        based on the provided config. Optionally supports middleware and rate limiting.

        Args:
            url: Base URL for API endpoints
            config: Configuration object with timeout and retry settings
            middleware: Optional middleware chain for request/response processing
            rate_limiter: Optional rate limiter for controlling request rate

        Raises:
            ValueError: If url is not a string
            ValueError: If url is empty

        Example:
            >>> config = Config(timeout=30)
            >>> client = HttpClient("https://api.example.com", config)
            >>> # With middleware
            >>> from py_web_automation import MiddlewareChain
            >>> chain = MiddlewareChain().add(LoggingMiddleware())
            >>> api = HttpClient("https://api.example.com", config, middleware=chain)
        """
        if not url.strip():
            raise ValueError("url cannot be empty")
        if not isinstance(config, Config):
            raise TypeError("config must be a Config object")
        self.url: str = url
        self.config: Config = config
        self.client: AsyncClient = AsyncClient(
            timeout=self.config.timeout,
            limits=Limits(max_keepalive_connections=5, max_connections=10),
        )
        self._middleware = middleware

    async def __aenter__(self) -> "HttpClient":
        """
        Enter async context manager.

        Returns:
            Self for use in async with statement
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Exit async context manager and close client.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        await self.close()

    async def close(self) -> None:
        """
        Close HTTP client and cleanup resources.

        Closes the underlying HTTP client connection pool and clears
        authentication tokens. This method is automatically called
        when exiting an async context manager.

        Example:
            >>> async with ApiClient(url, config) as api:
            ...     # Use API client
            ...     pass
            # Client is automatically closed here
        """
        await self.client.aclose()

    def build_request(self) -> "_RequestBuilder":
        """
        Create a RequestBuilder for constructing complex requests.

        Returns:
            _RequestBuilder instance for fluent request construction

        Example:
            >>> builder = api.build_request()
            >>> result = await builder.get("/users").params(page=1).execute()
        """
        return _RequestBuilder(self)

    async def _prepare_request_context(
        self,
        method: HTTPMethod,
        endpoint: str,
        headers: dict[str, str] | None,
        data: dict[str, Any] | bytes | str | None,
        params: dict[str, Any] | None,
    ) -> "_HttpRequestContext":
        """
        Prepare request context with middleware.

        Args:
            method: HTTP method (HTTPMethod enum or string)
            endpoint: API endpoint path
            headers: Request headers
            data: Request body data (dict, bytes, str, or None)
            params: Query parameters

        Returns:
            _RequestContext with middleware applied
        """
        request_context = _HttpRequestContext(
            method=method,
            url=endpoint,
            headers=headers.copy() if headers else {},
            data=data,
            params=params,
        )
        if self._middleware:
            await self._middleware.process_request(request_context)
        return request_context

    def _build_request_url(self, endpoint: str, params: dict[str, Any] | None) -> str:
        """
        Build full URL with query parameters.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            Full URL with query parameters
        """
        url = endpoint
        if not url.startswith("http"):
            base_url = self.url.split("?")[0]
            url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"
        if params:
            query_string = urlencode(params)
            if query_string:
                separator = "&" if "?" in url else "?"
                url = f"{url}{separator}{query_string}"
        return url

    def _prepare_request_headers(
        self,
        request_context: "_HttpRequestContext",
        data: dict[str, Any] | bytes | str | None,
    ) -> tuple[dict[str, str], dict[str, Any] | bytes | str | None, bool]:
        """
        Prepare request headers and data with auth token and content type.

        Args:
            request_context: Request context
            data: Request body data

        Returns:
            Tuple of (request headers, request data, use_json_param)
            use_json_param: True if data should be sent via json= parameter (for dict),
                          False if via content= or data= parameter
        """
        request_headers = request_context.headers.copy()
        request_data = request_context.data or data

        if request_data is None:
            return request_headers, None, False

        self._log_request_data(request_data)
        use_json_param = self._should_use_json_param(request_data, request_headers)
        return request_headers, request_data, use_json_param

    def _log_request_data(self, request_data: dict[str, Any] | bytes | str) -> None:
        """
        Log request data representation.

        Args:
            request_data: Request data to log
        """
        # Method exists for potential future logging of request data
        pass

    def _should_use_json_param(
        self, request_data: dict[str, Any] | bytes | str, request_headers: dict[str, str]
    ) -> bool:
        """
        Determine if data should be sent as JSON.

        Args:
            request_data: Request body data
            request_headers: Request headers

        Returns:
            True if data should be sent via json= parameter
        """
        if "Content-Type" in request_headers:
            return False
        if isinstance(request_data, dict):
            return True
        return False

    async def _execute_http_request(
        self,
        method: HTTPMethod | str,
        url: str,
        request_data: dict[str, Any] | bytes | str | None,
        request_headers: dict[str, str],
        use_json_param: bool,
    ) -> Response:
        """
        Execute HTTP request with optional retry.

        Args:
            method: HTTP method
            url: URL to request
            request_data: Request body data (dict, bytes, str, or None)
            request_headers: Request headers
            use_json_param: If True, use json= parameter (for dict), \
                else use content= (for bytes/str)

        Returns:
            Response from HTTP request
        """
        request_kwargs: dict[str, Any] = {"method": method, "url": url, "headers": request_headers}
        if request_data is not None:
            if use_json_param:
                request_kwargs["json"] = request_data
            else:
                request_kwargs["content"] = request_data
        return await self.client.request(**request_kwargs)

    @staticmethod
    def _redact_sensitive_headers(headers: dict[str, str]) -> dict[str, str]:
        """
        Redact sensitive headers from response headers.

        Args:
            headers: Response headers dictionary

        Returns:
            Headers dictionary with sensitive headers redacted
        """
        sensitive_headers = {
            "authorization",
            "cookie",
            "set-cookie",
            "x-api-key",
            "x-auth-token",
        }
        return {
            k.lower(): ("[REDACTED]" if k.lower() in sensitive_headers else v)
            for k, v in headers.items()
        }

    @staticmethod
    def _extract_content_type(headers: dict[str, str]) -> str | None:
        """
        Extract Content-Type header value from headers.

        Args:
            headers: Response headers dictionary

        Returns:
            Content-Type value or None if not found
        """
        for key, value in headers.items():
            if key.lower() == "content-type":
                return value
        return None

    @staticmethod
    def _get_response_time(response: Response) -> float:
        """
        Get response time safely from response object.

        Args:
            response: HTTP response object

        Returns:
            Response time in seconds, or 0.0 if unavailable
        """
        try:
            return response.elapsed.total_seconds()
        except (AttributeError, RuntimeError):
            return 0.0

    def _parse_http_response(
        self,
        response: Response,
        endpoint: str,
        method: HTTPMethod,
        request_context: "_HttpRequestContext",
    ) -> HttpResult:
        """
        Parse HTTP response into HttpResult.

        Args:
            response: HTTP response
            endpoint: API endpoint path
            method: HTTP method
            request_context: Request context

        Returns:
            HttpResult with parsed response data
        """
        response_body = response.content
        response_headers = dict(response.headers)
        redacted_headers = self._redact_sensitive_headers(response_headers)
        content_type = self._extract_content_type(response_headers)
        response_time = self._get_response_time(response)
        reason = getattr(response, "reason_phrase", None)
        return HttpResult(
            endpoint=endpoint,
            method=method,
            informational=response.is_informational,
            success=response.is_success,
            redirect=response.is_redirect,
            client_error=response.is_client_error,
            server_error=response.is_server_error,
            status_code=response.status_code,
            response_time=response_time,
            headers=redacted_headers,
            body=response_body,
            content_type=content_type,
            reason=reason,
            error_message=None,
            metadata=request_context.metadata.copy(),
        )

    async def _process_response(self, result: HttpResult) -> HttpResult:
        """
        Process response through middleware.

        Args:
            result: HttpResult to process

        Returns:
            HttpResult with processed response data
        """
        if self._middleware:
            response_context = _HttpResponseContext(result)
            response_context.metadata.update(result.metadata)
            await self._middleware.process_response(response_context)
            result = response_context.result
        return result

    async def _handle_request_error(
        self,
        error: Exception,
        endpoint: str,
        method: HTTPMethod | str,
        request_context: "_HttpRequestContext",
    ) -> HttpResult:
        """
        Handle request errors and return error HttpResult.

        Args:
            error: Exception that occurred
            endpoint: API endpoint path
            method: HTTP method
            request_context: Request context

        Returns:
            HttpResult with error message and request context metadata
        """
        error_msg = str(error)
        if self._middleware:
            error_result = await self._middleware.process_error(request_context, error)
            if error_result is not None:
                return error_result
        return HttpResult(
            endpoint=endpoint,
            method=method,
            status_code=0,
            response_time=0,
            success=False,
            redirect=False,
            client_error=False,
            server_error=False,
            informational=False,
            headers={},
            body=b"",
            content_type=None,
            reason=None,
            error_message=error_msg,
            metadata=request_context.metadata.copy(),
        )

    async def make_request(
        self,
        endpoint: str,
        method: HTTPMethod = HTTPMethod.GET,
        data: dict[str, Any] | bytes | str | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResult:
        """
        Make HTTP request to API endpoint.

        Supports middleware for rate limiting, retry, and other features.

        Args:
            endpoint: API endpoint path (relative to base URL) or full URL
            method: HTTP method
            data: Request body data:
                - dict: Will be sent as JSON (Content-Type: application/json)
                - bytes/str: Will be sent as raw content (set Content-Type in headers if needed)
                - None: No request body
            params: Query parameters (for GET requests and others)
            headers: Custom request headers (will be merged with auth token if set). \
                Set Content-Type explicitly for non-JSON data \
                (e.g., "multipart/form-data", "text/xml")

        Returns:
            ApiResult with request result including status, headers, body, and timing

        Example:
            >>> # JSON request (automatic Content-Type)
            >>> result = await api.make_request(
            ...     "users/", method=HTTPMethod.POST, data={"name": "John"}
            ... )

            >>> # XML request (explicit Content-Type)
            >>> xml_data = "<user><name>John</name></user>"
            >>> result = await api.make_request(
            ...     "users/",
            ...     method=HTTPMethod.POST,
            ...     data=xml_data,
            ...     headers={"Content-Type": "text/xml"}
            ... )

            >>> # Raw bytes request
            >>> result = await api.make_request(
            ...     "upload/",
            ...     method=HTTPMethod.PUT,
            ...     data=b"binary data",
            ...     headers={"Content-Type": "application/octet-stream"}
            ... )
        """
        request_context = await self._prepare_request_context(
            method=method,
            endpoint=endpoint,
            headers=headers,
            data=data,
            params=params,
        )
        try:
            url = self._build_request_url(request_context.url, request_context.params)
            request_headers, request_data, use_json_param = self._prepare_request_headers(
                request_context=request_context, data=data
            )
            request_context.metadata["start_time"] = time.time()
            response = await self._execute_http_request(
                method=method,
                url=url,
                request_data=request_data,
                request_headers=request_headers,
                use_json_param=use_json_param,
            )
            result = self._parse_http_response(
                response=response,
                endpoint=endpoint,
                method=method,
                request_context=request_context,
            )
            result = await self._process_response(result=result)
            return result
        except Exception as e:
            error_result = await self._handle_request_error(e, endpoint, method, request_context)
            return error_result
