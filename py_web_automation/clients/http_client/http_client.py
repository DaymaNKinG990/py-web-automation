"""
HTTP REST API client for web automation testing.

This module provides HttpClient for testing HTTP REST API endpoints,
including request handling, authentication, and response validation.
"""

# Python imports
import time
from http import HTTPMethod
from types import TracebackType
from typing import TYPE_CHECKING, Any, Optional
from urllib.parse import urlencode

from httpx import AsyncClient, Limits, Response
from loguru import logger

from ...config import Config

# Local imports
from .http_result import HttpResult

if TYPE_CHECKING:
    from loguru._logger import Logger

    from ...cache import ResponseCache
    from ...middleware import MiddlewareChain, RequestContext, ResponseContext
    from ...rate_limit import RateLimiter
    from ...retry import retry_on_connection_error
    from .request_builder import RequestBuilder


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
        _auth_token: Current authentication token (private)
        _auth_token_type: Type of authentication token (default: "Bearer")

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
        middleware: Optional["MiddlewareChain"] = None,
        cache: Optional["ResponseCache"] = None,
        rate_limiter: Optional["RateLimiter"] = None,
        enable_auto_retry: bool = True,
    ) -> None:
        """
        Initialize HTTP client.

        Creates an HTTP client with connection pooling and timeout configuration
        based on the provided config. Optionally supports middleware, caching,
        and rate limiting.

        Args:
            url: Base URL for API endpoints
            config: Configuration object with timeout and retry settings
            middleware: Optional middleware chain for request/response processing
            cache: Optional response cache for caching responses
            rate_limiter: Optional rate limiter for controlling request rate
            enable_auto_retry: Enable automatic retry using config.retry_count (default: True)

        Raises:
            ValueError: If url is not a string
            ValueError: If url is empty

        Example:
            >>> config = Config(timeout=30)
            >>> client = HttpClient("https://api.example.com", config)
            >>> # With middleware and cache
            >>> from py_web_automation import MiddlewareChain, ResponseCache
            >>> chain = MiddlewareChain().add(LoggingMiddleware())
            >>> cache = ResponseCache(default_ttl=300)
            >>> api = HttpClient("https://api.example.com", config, middleware=chain, cache=cache)
        """
        if not url.strip():
            raise ValueError("url cannot be empty")
        if not isinstance(config, Config):
            raise TypeError("config must be a Config object")
        self.url: str = url
        self.config: Config = config
        self.__logger: Logger = logger.bind(name=self.__class__.__name__)
        self.client: AsyncClient = AsyncClient(
            timeout=self.config.timeout,
            limits=Limits(max_keepalive_connections=5, max_connections=10),
        )
        self._auth_token: str | None = None
        self._auth_token_type: str = "Bearer"  # noqa: S105
        self._middleware: MiddlewareChain | None = middleware
        self._cache: ResponseCache | None = cache
        self._rate_limiter: RateLimiter | None = rate_limiter
        self._enable_auto_retry = enable_auto_retry

    async def __aenter__(self) -> "HttpClient":
        """
        Enter async context manager.

        Returns:
            Self for use in async with statement
        """
        self.__logger.debug("Entering an ApiClient context manager")
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
        self.__logger.debug("Exiting an ApiClient context manager")
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
        self.__logger.debug("Closing API client")
        await self.client.aclose()
        self.__logger.debug("HTTP client closed")
        self._auth_token = None
        self._auth_token_type = "Bearer"  # noqa: S105
        self.__logger.debug("Authentication tokens cleared")

    def set_auth_token(self, token: str, token_type: str = "Bearer") -> None:
        """
        Set authentication token for all subsequent requests.

        Args:
            token: Authentication token (JWT, API key, etc.)
            token_type: Token type (default: "Bearer")

        Example:
            >>> client = ApiClient("http://api.example.com", config)
            >>> result = await client.make_request("v1/login/", method="POST", data=credentials)
            >>> token_data = json.loads(result.body)
            >>> client.set_auth_token(token_data["access"])
            >>> # All subsequent requests will automatically include the token
            >>> result = await client.make_request("v1/users/", method="GET")
        """
        self._auth_token = token
        self._auth_token_type = token_type
        self.__logger.debug(f"Authentication token set (type: {token_type})")

    def clear_auth_token(self) -> None:
        """Clear authentication token."""
        self._auth_token = None
        self._auth_token_type = "Bearer"  # noqa: S105
        self.__logger.debug("Authentication token cleared")

    def build_request(self) -> "RequestBuilder":
        """
        Create a RequestBuilder for constructing complex requests.

        Returns:
            RequestBuilder instance for fluent request construction

        Example:
            >>> builder = api.build_request()
            >>> result = await builder.get("/users").params(page=1).execute()
        """
        self.__logger.debug("Building request with RequestBuilder")
        return RequestBuilder(self)

    async def _check_cache(
        self,
        method: HTTPMethod,
        endpoint: str,
        headers: dict[str, str] | None,
        params: dict[str, Any] | None,
        data: dict[str, Any] | bytes | str | None,
    ) -> HttpResult | None:
        """
        Check cache for GET requests.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            headers: Request headers
            params: Query parameters
            data: Request body data

        Returns:
            Cached ApiResult if found and not expired, None otherwise
        """
        if not (self._cache and method == HTTPMethod.GET):
            return None
        cache_url = endpoint
        if not endpoint.startswith("http"):
            base_url = self.url.split("?")[0]
            cache_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            self.__logger.debug(f"Cache URL: {cache_url}")
        cached_result = self._cache.get(
            method=method,
            url=cache_url,
            headers=headers,
            params=params,
            data=data,
        )
        if cached_result is not None:
            self.__logger.debug(f"Cache hit for {method} {endpoint}")
            return cached_result
        return None

    async def _prepare_request_context(
        self,
        method: HTTPMethod,
        endpoint: str,
        headers: dict[str, str] | None,
        data: dict[str, Any] | bytes | str | None,
        params: dict[str, Any] | None,
        skip_rate_limit: bool,
    ) -> "RequestContext":
        """
        Prepare request context with middleware and rate limiting.

        Args:
            method: HTTP method (HTTPMethod enum or string)
            endpoint: API endpoint path
            headers: Request headers
            data: Request body data (dict, bytes, str, or None)
            params: Query parameters
            skip_rate_limit: Whether to skip rate limiting

        Returns:
            RequestContext with middleware and rate limiting applied
        """
        request_context = RequestContext(
            method=method,
            url=endpoint,
            headers=headers.copy() if headers else {},
            data=data,
            params=params,
        )
        self.__logger.debug(f"Prepared request context: {request_context}")
        if self._middleware:
            self.__logger.debug(
                f"Processing request through middleware: {request_context.method} "
                f"{request_context.url}"
            )
            await self._middleware.process_request(request_context)
        if self._rate_limiter and not skip_rate_limit:
            self.__logger.debug(
                f"Acquiring rate limit: {request_context.method} {request_context.url}"
            )
            await self._rate_limiter.acquire()
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
        self.__logger.debug(f"Built request URL: {url}")
        return url

    def _prepare_request_headers(
        self,
        request_context: "RequestContext",
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
        if self._auth_token and "Authorization" not in request_headers:
            auth_header = f"{self._auth_token_type} {self._auth_token}"
            request_headers["Authorization"] = auth_header
            self.__logger.debug(f"Authorization header set: {auth_header}")
        self.__logger.debug(f"Request headers: {request_headers}")
        request_data = request_context.data or data
        use_json_param = False
        if request_data is not None:
            data_repr = (
                request_data.decode("utf-8", errors="replace")
                if isinstance(request_data, bytes)
                else str(request_data)
            )
            self.__logger.debug(f"Request data: {data_repr}")
            if "Content-Type" not in request_headers:
                if isinstance(request_data, dict):
                    use_json_param = True
                    self.__logger.debug(
                        "Using json= parameter for dict data "
                        "(Content-Type will be set automatically)"
                    )
                else:
                    self.__logger.debug(
                        f"Data type is {type(request_data).__name__}, "
                        f"Content-Type not set automatically"
                    )
        self.__logger.debug(f"Use JSON parameter: {use_json_param}")
        return request_headers, request_data, use_json_param

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
                data_repr = (
                    request_data.decode("utf-8", errors="replace")
                    if isinstance(request_data, bytes)
                    else str(request_data)
                )
                self.__logger.debug(f"Request data sent as JSON: {data_repr}")
            else:
                request_kwargs["content"] = request_data
                content_repr = (
                    request_data.decode("utf-8", errors="replace")
                    if isinstance(request_data, bytes)
                    else str(request_data)
                )
                self.__logger.debug(f"Request data sent as content: {content_repr}")
        self.__logger.debug(f"Request kwargs: {request_kwargs}")
        if self._enable_auto_retry and self.config.retry_count > 0:

            @retry_on_connection_error(
                max_attempts=self.config.retry_count,
                delay=self.config.retry_delay,
                backoff=2.0,
            )
            async def _make_request_with_retry():
                return await self.client.request(**request_kwargs)

            self.__logger.debug(f"Making request with retry: {method} {url}")
            return await _make_request_with_retry()
        else:
            self.__logger.debug(f"Making request without retry: {method} {url}")
            return await self.client.request(**request_kwargs)

    def _parse_http_response(
        self,
        response: Response,
        endpoint: str,
        method: HTTPMethod,
        request_context: "RequestContext",
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
        sensitive_headers = {
            "authorization",
            "cookie",
            "set-cookie",
            "x-api-key",
            "x-auth-token",
        }
        redacted_headers = {
            k.lower(): ("[REDACTED]" if k.lower() in sensitive_headers else v)
            for k, v in response_headers.items()
        }
        content_type = None
        for key, value in response_headers.items():
            if key.lower() == "content-type":
                content_type = value
                break
        reason = getattr(response, "reason_phrase", None)
        try:
            response_time = response.elapsed.total_seconds()
        except (AttributeError, RuntimeError):
            response_time = 0.0
        self.__logger.info(
            f"Response got: status_code={response.status_code}, "
            f"elapsed={response_time:.3f}s, "
            f"content_length={len(response_body)}"
        )
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

    async def _process_response(
        self,
        result: HttpResult,
        method: HTTPMethod,
        url: str,
        request_headers: dict[str, str],
        request_context: "RequestContext",
        use_cache: bool,
    ) -> HttpResult:
        """
        Process response through middleware and cache if needed.

        Args:
            result: ApiResult to process
            method: HTTP method
            url: URL to request
            request_headers: Request headers
            request_context: Request context
            use_cache: Whether to use cache if available

        Returns:
            HttpResult with processed response data
        """
        if self._middleware:
            response_context = ResponseContext(result)
            response_context.metadata.update(result.metadata)
            self.__logger.debug(f"Processing response through middleware: {response_context}")
            await self._middleware.process_response(response_context)
            result = response_context.result
            self.__logger.debug(f"Processed response: {result}")
        if use_cache and self._cache and method == HTTPMethod.GET and result.success:
            self.__logger.debug(f"Caching response: {result}")
            self._cache.set(
                method=method,
                url=url,
                value=result,
                headers=request_headers,
                params=request_context.params,
                data=request_context.data,
            )
            self.__logger.debug(f"Response cached: {result}")
        return result

    async def _handle_request_error(
        self,
        error: Exception,
        endpoint: str,
        method: HTTPMethod | str,
        request_context: "RequestContext",
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
        self.__logger.error(f"Request failed: {method} {endpoint} - {error_msg}")
        if self._middleware:
            error_result = await self._middleware.process_error(request_context, error)
            if error_result is not None:
                self.__logger.error(f"Error result: {error_result}")
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
        use_cache: bool = True,
        skip_rate_limit: bool = False,
    ) -> HttpResult:
        """
        Make HTTP request to API endpoint.

        Supports middleware, caching, rate limiting, and automatic retry.

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
            use_cache: Whether to use cache if available (default: True)
            skip_rate_limit: Skip rate limiting for this request (default: False)

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
        if use_cache:
            cached_result = await self._check_cache(method, endpoint, headers, params, data)
            self.__logger.debug(f"Cached result: {cached_result}")
            if cached_result is not None:
                self.__logger.debug(f"Returning cached result: {cached_result}")
                return cached_result
        request_context = await self._prepare_request_context(
            method=method,
            endpoint=endpoint,
            headers=headers,
            data=data,
            params=params,
            skip_rate_limit=skip_rate_limit,
        )
        self.__logger.debug(f"Prepared request context: {request_context}")
        try:
            url = self._build_request_url(request_context.url, request_context.params)
            request_headers, request_data, use_json_param = self._prepare_request_headers(
                request_context=request_context, data=data
            )
            self.__logger.info(f"Making request: {method} {url}")
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
            result = await self._process_response(
                result=result,
                method=method,
                url=url,
                request_headers=request_headers,
                request_context=request_context,
                use_cache=use_cache,
            )
            self.__logger.debug(f"Processed response: {result}")
            return result
        except Exception as e:
            error_result = await self._handle_request_error(e, endpoint, method, request_context)
            self.__logger.error(f"Request error: {error_result}")
            return error_result
