"""
HTTP REST API client for web automation testing.

This module provides ApiClient for testing HTTP REST API endpoints,
including request handling, authentication, and response validation.
"""

# Python imports
from typing import TYPE_CHECKING, Any, Optional
from urllib.parse import urlencode

from httpx import AsyncClient, Limits

from ..config import Config

# Local imports
from .base_client import BaseClient
from .models import ApiResult

if TYPE_CHECKING:
    from ..cache import ResponseCache
    from ..middleware import MiddlewareChain
    from ..rate_limit import RateLimiter
    from .request_builder import RequestBuilder


class ApiClient(BaseClient):
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
        >>> from py_web_automation import Config, ApiClient
        >>> config = Config(timeout=30)
        >>> async with ApiClient("https://api.example.com", config) as api:
        ...     result = await api.make_request("v1/users/", method="GET")
        ...     assert result.success
    """

    def __init__(
        self,
        url: str,
        config: Config | None = None,
        middleware: Optional["MiddlewareChain"] = None,
        cache: Optional["ResponseCache"] = None,
        rate_limiter: Optional["RateLimiter"] = None,
        enable_auto_retry: bool = True,
    ) -> None:
        """
        Initialize API client.

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
            ValueError: If config is None (inherited from BaseClient)

        Example:
            >>> config = Config(timeout=30)
            >>> api = ApiClient("https://api.example.com", config)
            >>> # With middleware and cache
            >>> from py_web_automation import MiddlewareChain, ResponseCache
            >>> chain = MiddlewareChain().add(LoggingMiddleware())
            >>> cache = ResponseCache(default_ttl=300)
            >>> api = ApiClient("https://api.example.com", config, middleware=chain, cache=cache)
        """
        super().__init__(url, config)
        self.client: AsyncClient = AsyncClient(
            timeout=self.config.timeout,
            limits=Limits(max_keepalive_connections=5, max_connections=10),
        )
        self._auth_token: str | None = None
        self._auth_token_type: str = "Bearer"
        self._middleware: MiddlewareChain | None = middleware
        self._cache: ResponseCache | None = cache
        self._rate_limiter: RateLimiter | None = rate_limiter
        self._enable_auto_retry = enable_auto_retry

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
        self._auth_token = None
        self._auth_token_type = "Bearer"

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
        self.logger.debug(f"Authentication token set (type: {token_type})")

    def clear_auth_token(self) -> None:
        """Clear authentication token."""
        self._auth_token = None
        self._auth_token_type = "Bearer"
        self.logger.debug("Authentication token cleared")

    def build_request(self) -> "RequestBuilder":
        """
        Create a RequestBuilder for constructing complex requests.

        Returns:
            RequestBuilder instance for fluent request construction

        Example:
            >>> builder = api.build_request()
            >>> result = await builder.get("/users").params(page=1).execute()
        """
        from .request_builder import RequestBuilder

        return RequestBuilder(self)

    async def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        use_cache: bool = True,
        skip_rate_limit: bool = False,
    ) -> ApiResult:
        """
        Make HTTP request to API endpoint.

        Supports middleware, caching, rate limiting, and automatic retry.

        Args:
            endpoint: API endpoint path (relative to base URL) or full URL
            method: HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
            data: Request body data (for POST, PUT, PATCH) - will be JSON encoded
            params: Query parameters (for GET requests and others)
            headers: Custom request headers (will be merged with auth token if set)
            use_cache: Whether to use cache if available (default: True)
            skip_rate_limit: Skip rate limiting for this request (default: False)

        Returns:
            ApiResult with request result including status, headers, body, and timing

        Example:
            >>> result = await api.make_request("users/", method="GET")
            >>> if result.success:
            ...     users = result.json()
            >>> result = await api.make_request("users/", method="POST", data={"name": "John"})
        """
        # Check cache first (only for GET requests)
        # Build URL early to ensure consistent cache keys
        if use_cache and self._cache and method.upper() == "GET":
            # Build URL for cache key consistency
            cache_url = endpoint
            if not endpoint.startswith("http"):
                base_url = self.url.split("?")[0]
                cache_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

            cached_result = self._cache.get(method, cache_url, headers, params, data)
            if cached_result is not None:
                self.logger.debug(f"Cache hit for {method} {endpoint}")
                return cached_result

        # Create request context
        from ..middleware import RequestContext

        request_context = RequestContext(
            method=method,
            url=endpoint,
            headers=headers.copy() if headers else {},
            data=data,
            params=params,
        )

        # Process request through middleware
        if self._middleware:
            await self._middleware.process_request(request_context)

        # Apply rate limiting
        if self._rate_limiter and not skip_rate_limit:
            await self._rate_limiter.acquire()

        # Build final URL from context (may have been modified by middleware)
        try:
            url = request_context.url
            if not url.startswith("http"):
                # Assume endpoint is relative to base URL
                base_url = self.url.split("?")[0]  # Remove query params
                url = f"{base_url.rstrip('/')}/{url.lstrip('/')}"

            # Add query params to URL (from context, may have been modified)
            if request_context.params:
                query_string = urlencode(request_context.params)
                if query_string:
                    separator = "&" if "?" in url else "?"
                    url = f"{url}{separator}{query_string}"

            # Use headers from context (may have been modified by middleware)
            request_headers = request_context.headers.copy()

            # Automatically add token if set (unless Authorization header is already provided)
            if self._auth_token and "Authorization" not in request_headers:
                auth_header = f"{self._auth_token_type} {self._auth_token}"
                request_headers["Authorization"] = auth_header

            # Set default Content-Type if not specified and data is provided
            request_data = request_context.data or data
            if request_data is not None and "Content-Type" not in request_headers:
                request_headers["Content-Type"] = "application/json"

            self.logger.info(f"Making request: {method} {url}")

            # Store start time for metrics
            import time

            start_time = time.time()
            request_context.metadata["start_time"] = start_time

            # Make request with retry if enabled
            if self._enable_auto_retry and self.config.retry_count > 0:
                from ..retry import retry_on_connection_error

                @retry_on_connection_error(
                    max_attempts=self.config.retry_count,
                    delay=self.config.retry_delay,
                    backoff=2.0,
                )
                async def _make_request_with_retry():
                    return await self.client.request(method=method, url=url, json=request_data, headers=request_headers)

                response = await _make_request_with_retry()
            else:
                response = await self.client.request(method=method, url=url, json=request_data, headers=request_headers)
            # Extract response data before closing
            # response.content automatically reads the response body
            # This must be done before accessing response.elapsed
            response_body = response.content
            response_headers = dict(response.headers)

            # Redact sensitive headers and normalize to lowercase keys
            sensitive_headers = {
                "authorization",
                "cookie",
                "set-cookie",
                "x-api-key",
                "x-auth-token",
            }
            redacted_headers = {
                k.lower(): ("[REDACTED]" if k.lower() in sensitive_headers else v) for k, v in response_headers.items()
            }

            # Get content type (normalize header name)
            content_type = None
            for key, value in response_headers.items():
                if key.lower() == "content-type":
                    content_type = value
                    break

            # Get reason phrase
            reason = getattr(response, "reason_phrase", None)

            # Get response time - elapsed is only available after response is read
            try:
                response_time = response.elapsed.total_seconds()
            except (AttributeError, RuntimeError):
                # If elapsed is not available (e.g., timeout or response not fully read), use 0
                response_time = 0.0

            self.logger.info(
                f"Response got: status_code={response.status_code}, "
                f"elapsed={response_time:.3f}s, "
                f"content_length={len(response_body)}"
            )

            result = ApiResult(
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

            # Process response through middleware
            if self._middleware:
                from ..middleware import ResponseContext

                response_context = ResponseContext(result)
                # Copy metadata from result to response context
                response_context.metadata.update(result.metadata)
                await self._middleware.process_response(response_context)
                result = response_context.result

            # Cache successful GET responses
            if use_cache and self._cache and method.upper() == "GET" and result.success:
                # Use the same URL format as in cache.get() for consistency
                cache_url = url  # Use the final built URL
                self._cache.set(method, cache_url, result, headers=request_headers, params=request_context.params)

            return result
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Request failed: {method} {endpoint} - {error_msg}")

            # Process error through middleware
            if self._middleware:
                error_result = await self._middleware.process_error(request_context, e)
                if error_result is not None:
                    return error_result

            return ApiResult(
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
