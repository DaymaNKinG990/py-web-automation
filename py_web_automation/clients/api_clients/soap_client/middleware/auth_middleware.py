"""
Authentication middleware for SOAP client.

This module provides AuthMiddleware for automatic authentication header injection
in SOAP operations.
"""

# Local imports
from ..soap_result import SoapResult
from .context import _SoapRequestContext, _SoapResponseContext
from .middleware import Middleware


class AuthMiddleware(Middleware):
    """
    Middleware for automatic authentication header injection in SOAP operations.

    Automatically adds authentication headers to SOAP requests.
    Supports dynamic token updates for scenarios like token refresh.

    Attributes:
        token: Current authentication token (can be updated dynamically)
        token_type: Token type (default: "Bearer")
        header_name: Header name for token (default: "Authorization")

    Example:
        >>> from py_web_automation.clients.soap_client import SoapClient, MiddlewareChain
        >>> from py_web_automation.clients.soap_client.middleware import AuthMiddleware
        >>> auth_middleware = AuthMiddleware(token="initial-token", token_type="Bearer")
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(auth_middleware)
        >>> async with SoapClient(
        ...     "https://api.example.com/soap", config, middleware=middleware_chain
        ... ) as soap:
        ...     result = await soap.call("GetUser", {"userId": "123"})
        ...     auth_middleware.update_token("new-refreshed-token")
        ...     result = await soap.call("GetUser", {"userId": "123"})
    """

    def __init__(
        self,
        token: str | None = None,
        token_type: str = "Bearer",
        header_name: str = "Authorization",
    ) -> None:
        """
        Initialize auth middleware.

        Args:
            token: Authentication token (can be None, then set via update_token())
            token_type: Token type (default: "Bearer")
            header_name: Header name for storing token (default: "Authorization")
        """
        self.token: str | None = token
        self.token_type: str = token_type
        self.header_name: str = header_name

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
            >>> auth_middleware.update_token("refreshed-token")
        """
        self.token = token
        if token_type is not None:
            self.token_type = token_type

    def clear_token(self) -> None:
        """
        Clear authentication token.

        Removes token from middleware, so no authorization header will be added.

        Example:
            >>> auth_middleware.clear_token()
        """
        self.token = None

    async def process_request(self, context: _SoapRequestContext) -> None:
        """
        Add authentication header to request.

        Args:
            context: Request context
        """
        if self.token and self.header_name not in context.headers:
            context.headers[self.header_name] = f"{self.token_type} {self.token}"

    async def process_response(self, context: _SoapResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(
        self, context: _SoapRequestContext, error: Exception
    ) -> SoapResult | None:
        """
        No-op for errors.

        Args:
            context: Request context
            error: Exception that occurred
        """
        return None
