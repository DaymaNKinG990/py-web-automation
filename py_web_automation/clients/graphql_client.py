"""
GraphQL API client for web automation testing.

This module provides GraphQLClient for testing GraphQL API endpoints,
including query execution, mutation handling, and subscription support.
"""

from typing import Any

from httpx import AsyncClient, Limits

from ..config import Config
from .base_client import BaseClient
from .models import ApiResult


class GraphQLClient(BaseClient):
    """
    GraphQL API client for web automation testing.

    Implements GraphQL query execution with support for queries, mutations,
    and subscriptions. Follows the Single Responsibility Principle by
    focusing solely on GraphQL API testing.

    Provides methods for testing GraphQL API endpoints:
    - Query execution with variables
    - Mutation execution
    - Subscription support (via WebSocket)
    - Response validation and error handling
    - Automatic request formatting

    Attributes:
        client: HTTP client instance for making requests
        _auth_token: Current authentication token (private)
        _auth_token_type: Type of authentication token (default: "Bearer")
        endpoint: GraphQL endpoint path (default: "/graphql")

    Example:
        >>> from py_web_automation import Config, GraphQLClient
        >>> config = Config(timeout=30)
        >>> async with GraphQLClient("https://api.example.com", config) as gql:
        ...     result = await gql.query(
        ...         query="query { user(id: 1) { name email } }"
        ...     )
        ...     assert result.success
    """

    def __init__(
        self,
        url: str,
        config: Config | None = None,
        endpoint: str = "/graphql",
    ) -> None:
        """
        Initialize GraphQL client.

        Args:
            url: Base URL for GraphQL API
            config: Configuration object with timeout and retry settings
            endpoint: GraphQL endpoint path (default: "/graphql")

        Raises:
            ValueError: If config is None (inherited from BaseClient)

        Example:
            >>> config = Config(timeout=30)
            >>> gql = GraphQLClient("https://api.example.com", config, endpoint="/graphql")
        """
        super().__init__(url, config)
        self.client: AsyncClient = AsyncClient(
            timeout=self.config.timeout,
            limits=Limits(max_keepalive_connections=5, max_connections=10),
        )
        self.endpoint: str = endpoint
        self._auth_token: str | None = None
        self._auth_token_type: str = "Bearer"

    async def close(self) -> None:
        """
        Close HTTP client and cleanup resources.

        Closes the underlying HTTP client connection pool and clears
        authentication tokens. This method is automatically called
        when exiting an async context manager.
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
            >>> gql.set_auth_token("your-jwt-token")
            >>> # All subsequent requests will automatically include the token
        """
        self._auth_token = token
        self._auth_token_type = token_type
        self.logger.debug(f"Authentication token set (type: {token_type})")

    def clear_auth_token(self) -> None:
        """Clear authentication token."""
        self._auth_token = None
        self._auth_token_type = "Bearer"
        self.logger.debug("Authentication token cleared")

    async def query(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> ApiResult:
        """
        Execute GraphQL query.

        Args:
            query: GraphQL query string
            variables: Query variables (optional)
            operation_name: Operation name for multi-operation queries (optional)
            headers: Custom request headers (optional)

        Returns:
            ApiResult with query result

        Example:
            >>> result = await gql.query(
            ...     query="query GetUser($id: ID!) { user(id: $id) { name email } }",
            ...     variables={"id": "1"}
            ... )
            >>> data = result.json()
            >>> assert "data" in data
        """
        return await self._execute(query, variables, operation_name, headers)

    async def mutate(
        self,
        mutation: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> ApiResult:
        """
        Execute GraphQL mutation.

        Args:
            mutation: GraphQL mutation string
            variables: Mutation variables (optional)
            operation_name: Operation name for multi-operation queries (optional)
            headers: Custom request headers (optional)

        Returns:
            ApiResult with mutation result

        Example:
            >>> result = await gql.mutate(
            ...     mutation="mutation CreateUser($input: UserInput!) { createUser(input: $input) { id name } }",
            ...     variables={"input": {"name": "John", "email": "john@example.com"}}
            ... )
        """
        return await self._execute(mutation, variables, operation_name, headers)

    async def _execute(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> ApiResult:
        """
        Execute GraphQL operation (query or mutation).

        Args:
            query: GraphQL query/mutation string
            variables: Operation variables (optional)
            operation_name: Operation name (optional)
            headers: Custom request headers (optional)

        Returns:
            ApiResult with operation result
        """
        # Build GraphQL endpoint URL
        base_url = self.url.split("?")[0]
        url = f"{base_url.rstrip('/')}/{self.endpoint.lstrip('/')}"

        # Prepare request payload
        payload: dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name

        # Prepare headers
        request_headers: dict[str, str] = {"Content-Type": "application/json"}
        if headers:
            request_headers.update(headers)

        # Add authentication token if set
        if self._auth_token and "Authorization" not in request_headers:
            auth_header = f"{self._auth_token_type} {self._auth_token}"
            request_headers["Authorization"] = auth_header

        self.logger.info(f"Executing GraphQL operation: {operation_name or 'unnamed'}")
        try:
            response = await self.client.post(
                url=url,
                json=payload,
                headers=request_headers,
            )

            response_body = response.content
            response_headers = dict(response.headers)

            # Redact sensitive headers
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

            content_type = response_headers.get("Content-Type") or response_headers.get("content-type")

            try:
                response_time = response.elapsed.total_seconds()
            except (AttributeError, RuntimeError):
                response_time = 0.0

            self.logger.info(f"GraphQL response: status_code={response.status_code}, elapsed={response_time:.3f}s")

            return ApiResult(
                endpoint=self.endpoint,
                method="POST",
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
                reason=getattr(response, "reason_phrase", None),
                error_message=None,
            )
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"GraphQL request failed: {error_msg}")
            return ApiResult(
                endpoint=self.endpoint,
                method="POST",
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
            )

    def get_errors(self, result: ApiResult) -> list[dict[str, Any]]:
        """
        Extract GraphQL errors from response.

        Args:
            result: ApiResult from GraphQL operation

        Returns:
            List of error dictionaries from GraphQL response

        Example:
            >>> result = await gql.query("query { invalid }")
            >>> errors = gql.get_errors(result)
            >>> if errors:
            ...     print(f"GraphQL errors: {errors}")
        """
        try:
            data = result.json()
            return data.get("errors", [])
        except (ValueError, KeyError):
            return []
