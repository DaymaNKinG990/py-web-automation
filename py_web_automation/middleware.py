"""
Middleware system for request/response interception and modification.

This module provides a middleware/interceptor system that allows hooking into
the request/response lifecycle for logging, metrics, validation, and modification.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional

from .clients.models import ApiResult

if TYPE_CHECKING:
    from .metrics import Metrics


class RequestContext:
    """
    Context object passed through middleware chain.

    Contains request information that can be modified by middleware.

    Attributes:
        method: HTTP method
        url: Request URL
        headers: Request headers (can be modified)
        data: Request body data (can be modified)
        params: Query parameters (can be modified)
        metadata: Custom metadata dictionary for middleware communication
    """

    def __init__(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> None:
        """Initialize request context."""
        self.method = method
        self.url = url
        self.headers = headers or {}
        self.data = data
        self.params = params or {}
        self.metadata: dict[str, Any] = {}


class ResponseContext:
    """
    Context object for response processing.

    Contains response information that can be modified by middleware.

    Attributes:
        result: ApiResult object (can be modified)
        metadata: Custom metadata dictionary for middleware communication
    """

    def __init__(self, result: ApiResult) -> None:
        """Initialize response context."""
        self.result = result
        # Copy metadata from result to context for middleware communication
        self.metadata: dict[str, Any] = result.metadata.copy() if result.metadata else {}


class Middleware(ABC):
    """
    Base class for middleware implementations.

    Middleware can intercept and modify requests before they are sent
    and responses after they are received.

    Example:
        >>> class LoggingMiddleware(Middleware):
        ...     async def process_request(self, context: RequestContext) -> None:
        ...         print(f"Request: {context.method} {context.url}")
        ...     async def process_response(self, context: ResponseContext) -> None:
        ...         print(f"Response: {context.result.status_code}")
    """

    @abstractmethod
    async def process_request(self, context: RequestContext) -> None:
        """
        Process request before it is sent.

        Can modify context.headers, context.data, context.params, etc.

        Args:
            context: Request context that can be modified
        """
        pass

    @abstractmethod
    async def process_response(self, context: ResponseContext) -> None:
        """
        Process response after it is received.

        Can modify context.result or access context.metadata.

        Args:
            context: Response context that can be modified
        """
        pass

    async def process_error(self, context: RequestContext, error: Exception) -> ApiResult | None:
        """
        Process error that occurred during request.

        Can return a modified ApiResult to replace the error response,
        or return None to let the error propagate.

        Args:
            context: Request context
            error: Exception that occurred

        Returns:
            Optional ApiResult to replace error, or None to propagate error
        """
        return None


class MiddlewareChain:
    """
    Chain of middleware to process requests and responses.

    Executes middleware in order for requests and in reverse order for responses.

    Attributes:
        _middleware: List of middleware instances

    Example:
        >>> chain = MiddlewareChain()
        >>> chain.add(LoggingMiddleware())
        >>> chain.add(MetricsMiddleware())
        >>> # Use chain in ApiClient
    """

    def __init__(self) -> None:
        """Initialize empty middleware chain."""
        self._middleware: list[Middleware] = []

    def add(self, middleware: Middleware) -> "MiddlewareChain":
        """
        Add middleware to the chain.

        Args:
            middleware: Middleware instance to add

        Returns:
            Self for method chaining

        Example:
            >>> chain.add(LoggingMiddleware()).add(MetricsMiddleware())
        """
        self._middleware.append(middleware)
        return self

    def remove(self, middleware: Middleware) -> "MiddlewareChain":
        """
        Remove middleware from the chain.

        Args:
            middleware: Middleware instance to remove

        Returns:
            Self for method chaining
        """
        if middleware in self._middleware:
            self._middleware.remove(middleware)
        return self

    async def process_request(self, context: RequestContext) -> None:
        """
        Process request through all middleware.

        Args:
            context: Request context to process
        """
        for middleware in self._middleware:
            await middleware.process_request(context)

    async def process_response(self, context: ResponseContext) -> None:
        """
        Process response through all middleware (in reverse order).

        Args:
            context: Response context to process
        """
        for middleware in reversed(self._middleware):
            await middleware.process_response(context)

    async def process_error(self, context: RequestContext, error: Exception) -> ApiResult | None:
        """
        Process error through all middleware (in reverse order).

        Args:
            context: Request context
            error: Exception that occurred

        Returns:
            Optional ApiResult to replace error, or None
        """
        for middleware in reversed(self._middleware):
            result = await middleware.process_error(context, error)
            if result is not None:
                return result
        return None


# Built-in middleware implementations


class LoggingMiddleware(Middleware):
    """
    Middleware for logging requests and responses.

    Logs request details before sending and response details after receiving.

    Example:
        >>> chain.add(LoggingMiddleware())
    """

    async def process_request(self, context: RequestContext) -> None:
        """Log request details."""
        from loguru import logger

        logger.info(
            f"Request: {context.method} {context.url} headers={len(context.headers)} params={len(context.params)}"
        )

    async def process_response(self, context: ResponseContext) -> None:
        """Log response details."""
        from loguru import logger

        logger.info(
            f"Response: {context.result.status_code} "
            f"time={context.result.response_time:.3f}s "
            f"success={context.result.success}"
        )

    async def process_error(self, context: RequestContext, error: Exception) -> ApiResult | None:
        """Log error details."""
        from loguru import logger

        logger.error(f"Request error: {context.method} {context.url} - {error}")
        return None


class MetricsMiddleware(Middleware):
    """
    Middleware for collecting performance metrics.

    Collects metrics about request latency, success rate, and error rates.

    Attributes:
        metrics: Metrics object for storing collected data

    Example:
        >>> metrics = Metrics()
        >>> chain.add(MetricsMiddleware(metrics))
    """

    def __init__(self, metrics: Optional["Metrics"] = None) -> None:
        """
        Initialize metrics middleware.

        Args:
            metrics: Metrics object to use (creates new one if None)
        """
        if metrics is None:
            from .metrics import Metrics

            metrics = Metrics()
        self.metrics = metrics

    async def process_request(self, context: RequestContext) -> None:
        """Record request start time."""
        import time

        context.metadata["start_time"] = time.time()

    async def process_response(self, context: ResponseContext) -> None:
        """Record response metrics."""
        start_time = context.metadata.get("start_time")
        if start_time:
            latency = context.result.response_time
            error_type = None
            if not context.result.success:
                if context.result.client_error:
                    error_type = "client_error"
                elif context.result.server_error:
                    error_type = "server_error"
                else:
                    error_type = "unknown_error"

            self.metrics.record_request(
                success=context.result.success,
                latency=latency,
                error_type=error_type,
            )

    async def process_error(self, context: RequestContext, error: Exception) -> ApiResult | None:
        """Record error metrics."""
        error_type = type(error).__name__
        self.metrics.record_request(success=False, latency=0.0, error_type=error_type)
        return None


class AuthMiddleware(Middleware):
    """
    Middleware for automatic authentication header injection.

    Automatically adds authentication headers to requests.

    Example:
        >>> chain.add(AuthMiddleware(token="abc123", token_type="Bearer"))
    """

    def __init__(self, token: str, token_type: str = "Bearer") -> None:
        """
        Initialize auth middleware.

        Args:
            token: Authentication token
            token_type: Token type (default: "Bearer")
        """
        self.token = token
        self.token_type = token_type

    async def process_request(self, context: RequestContext) -> None:
        """Add authentication header to request."""
        if "Authorization" not in context.headers:
            context.headers["Authorization"] = f"{self.token_type} {self.token}"

    async def process_response(self, context: ResponseContext) -> None:
        """No-op for responses."""
        pass

    async def process_error(self, context: RequestContext, error: Exception) -> ApiResult | None:
        """No-op for errors."""
        return None


class ValidationMiddleware(Middleware):
    """
    Middleware for response validation.

    Validates responses against schemas using msgspec.

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

    async def process_request(self, context: RequestContext) -> None:
        """No-op for requests."""
        pass

    async def process_response(self, context: ResponseContext) -> None:
        """Validate response against schema."""
        from .validators import validate_api_result

        if context.result.success and context.result.body:
            try:
                validate_api_result(context.result, self.schema)
            except Exception as e:
                # Store validation error in metadata
                context.metadata["validation_error"] = str(e)

    async def process_error(self, context: RequestContext, error: Exception) -> ApiResult | None:
        """No-op for errors."""
        return None
