"""
Authentication middleware for gRPC client.

This module provides AuthMiddleware for automatic authentication metadata injection
in gRPC calls.
"""

# Local imports
from ..grpc_result import GrpcResult
from .context import _GrpcRequestContext, _GrpcResponseContext
from .middleware import Middleware


class AuthMiddleware(Middleware):
    """
    Middleware for automatic authentication metadata injection in gRPC calls.

    Automatically adds authentication metadata to gRPC requests.
    Supports dynamic token updates for scenarios like token refresh.

    Attributes:
        token: Current authentication token (can be updated dynamically)
        token_type: Token type (default: "Bearer")
        metadata_key: Metadata key for token (default: "authorization")

    Example:
        >>> from py_web_automation.clients.grpc_client import GrpcClient, MiddlewareChain
        >>> from py_web_automation.clients.grpc_client.middleware import AuthMiddleware
        >>> auth_middleware = AuthMiddleware(token="initial-token", token_type="Bearer")
        >>> middleware_chain = MiddlewareChain()
        >>> middleware_chain.add(auth_middleware)
        >>> async with GrpcClient(
        ...     "localhost:50051", config, middleware=middleware_chain
        ... ) as client:
        ...     result = await client.unary_call("UserService", "GetUser", request)
        ...     auth_middleware.update_token("new-refreshed-token")
        ...     result = await client.unary_call("UserService", "GetUser", request)
    """

    def __init__(
        self,
        token: str | None = None,
        token_type: str = "Bearer",
        metadata_key: str = "authorization",
    ) -> None:
        """
        Initialize auth middleware.

        Args:
            token: Authentication token (can be None, then set via update_token())
            token_type: Token type (default: "Bearer")
            metadata_key: Metadata key for storing token (default: "authorization")
        """
        self.token: str | None = token
        self.token_type: str = token_type
        self.metadata_key: str = metadata_key

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

        Removes token from middleware, so no authorization metadata will be added.

        Example:
            >>> auth_middleware.clear_token()
        """
        self.token = None

    async def process_request(self, context: _GrpcRequestContext) -> None:
        """
        Add authentication metadata to request.

        Args:
            context: Request context
        """
        if self.token and self.metadata_key not in context.metadata:
            context.metadata[self.metadata_key] = f"{self.token_type} {self.token}"

    async def process_response(self, context: _GrpcResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(
        self, context: _GrpcRequestContext, error: Exception
    ) -> GrpcResult | None:
        """
        No-op for errors.

        Args:
            context: Request context
            error: Exception that occurred
        """
        return None
