"""
Authentication middleware for HTTP client.

This module provides AuthMiddleware for automatic authentication header injection.
"""

# Local imports
from ..http_result import HttpResult
from .context import _RequestContext, _ResponseContext
from .middleware import Middleware


class AuthMiddleware(Middleware):
    """
    Middleware for automatic authentication header injection.

    Automatically adds authentication headers to requests.
    Supports dynamic token updates for scenarios like token refresh.

    Attributes:
        token: Current authentication token (can be updated dynamically)
        token_type: Token type (default: "Bearer")

    Example:
        >>> from py_web_automation import Config, HttpClient
        >>> from py_web_automation.clients.http_client.middleware.auth_middleware import (
        ...     AuthMiddleware,
        ...     MiddlewareChain,
        ... )
        >>> config = Config(timeout=30)
        >>> auth_middleware = AuthMiddleware(token="initial-token", token_type="Bearer")
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(auth_middleware)
        >>> async with HttpClient(
        ...     "https://api.example.com", config, middleware=middleware_chain
        ... ) as http_client:
        ...     # Token is automatically added to all requests
        ...     result = await http_client.build_request().get("/users").execute()
        ...     # Update token dynamically (e.g., after refresh)
        ...     auth_middleware.update_token("new-refreshed-token")
        ...     result = await http_client.build_request().get("/profile").execute()
    """

    def __init__(self, token: str | None = None, token_type: str = "Bearer") -> None:
        """
        Initialize auth middleware.

        Args:
            token: Authentication token (can be None, then set via update_token())
            token_type: Token type (default: "Bearer")
        """
        self.token: str | None = token
        self.token_type: str = token_type

    def update_token(self, token: str, token_type: str | None = None) -> None:
        """
        Update authentication token dynamically.

        Useful for token refresh scenarios where token needs to be updated
        after initial authentication.

        Args:
            token: New authentication token
            token_type: Token type (default: uses existing token_type)

        Example:
            >>> auth_middleware = AuthMiddleware(token="initial-token")
            >>> # Later, after token refresh
            >>> auth_middleware.update_token("refreshed-token")
        """
        self.token = token
        if token_type is not None:
            self.token_type = token_type

    def clear_token(self) -> None:
        """
        Clear authentication token.

        Removes token from middleware, so no Authorization header will be added.

        Example:
            >>> auth_middleware.clear_token()
        """
        self.token = None

    async def process_request(self, context: _RequestContext) -> None:
        """
        Add authentication header to request.

        Args:
            context: Request context
        """
        if self.token and "Authorization" not in context.headers:
            context.headers["Authorization"] = f"{self.token_type} {self.token}"

    async def process_response(self, context: _ResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(self, context: _RequestContext, error: Exception) -> HttpResult | None:
        """
        No-op for errors.

        Args:
            context: Request context
            error: Exception that occurred
        """
        return None
