"""
GraphQL API client for web automation testing.

This module provides GraphQLClient for testing GraphQL API endpoints,
including query execution, mutation handling, and subscription support.
"""

# Python improts
from __future__ import annotations

from time import time
from types import TracebackType
from typing import TYPE_CHECKING, Any

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import GraphQLError

# Local imports
from ....config import Config
from .graphql_result import GraphQLResult
from .middleware.context import _GraphQLRequestContext, _GraphQLResponseContext

if TYPE_CHECKING:
    from .middleware.middleware import MiddlewareChain


class GraphQLClient:
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
        endpoint: GraphQL endpoint path (default: "/graphql")

    Example:
        >>> from py_web_automation import Config
        >>> from py_web_automation.clients.graphql_client import (
        ...     GraphQLClient,
        ...     MiddlewareChain,
        ... )
        >>> from py_web_automation.clients.graphql_client.middleware import (
        ...     AuthMiddleware,
        ... )
        >>> config = Config(timeout=30)
        >>> auth_middleware = AuthMiddleware(token="your-jwt-token")
        >>> middleware = MiddlewareChain().add(auth_middleware)
        >>> async with GraphQLClient(
        ...     "https://api.example.com", config, middleware=middleware
        ... ) as gql:
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
        validate_queries: bool = False,
        schema: Any = None,
        middleware: MiddlewareChain | None = None,
    ) -> None:
        """
        Initialize GraphQL client.

        Args:
            url: Base URL for GraphQL API
            config: Configuration object with timeout and retry settings
            endpoint: GraphQL endpoint path (default: "/graphql")
            validate_queries: If True, schema will not be automatically fetched from transport.
                Use ValidationMiddleware for query validation instead (default: False)
            schema: GraphQL schema for validation (optional, fetched from server if not provided).
                If provided, schema is passed to ValidationMiddleware via request metadata
            middleware: Optional middleware chain for request/response processing

        Raises:
            ImportError: If gql is not installed
            ValueError: If url is empty or contains only whitespace
            TypeError: If config is not a Config object when provided

        Example:
            >>> config = Config(timeout=30)
            >>> gql = GraphQLClient("https://api.example.com", config, endpoint="/graphql")
            >>> # With middleware
            >>> from py_web_automation.clients.graphql_client.middleware import MiddlewareChain
            >>> chain = MiddlewareChain().add(LoggingMiddleware())
            >>> gql = GraphQLClient("https://api.example.com", config, middleware=chain)
        """
        if not url.strip():
            raise ValueError("url cannot be empty")
        if config is None:
            config = Config()
        elif not isinstance(config, Config):
            raise TypeError("config must be a Config object")
        self.url: str = url
        self.config: Config = config
        base_url = url.split("?")[0]
        graphql_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        transport = AIOHTTPTransport(
            url=graphql_url,
            timeout=self.config.timeout,
        )
        # fetch_schema_from_transport logic:
        # - If validate_queries=True: disable auto-fetch (validation via middleware)
        # - If validate_queries=False and schema=None: enable auto-fetch
        # - If validate_queries=False and schema is provided: disable auto-fetch (schema already available)
        self.client: Client = Client(
            transport=transport,
            fetch_schema_from_transport=not validate_queries and schema is None,
        )
        self.endpoint: str = endpoint
        self._schema: Any = schema
        self._session: Any = None
        self._transport: AIOHTTPTransport = transport
        self._middleware = middleware

    async def __aenter__(self) -> GraphQLClient:
        """
        Async context manager entry.

        Returns:
            Self for use in async with statement

        Example:
            >>> async with GraphQLClient("https://api.example.com", config) as gql:
            ...     result = await gql.query(query="query { user { name } }")
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Async context manager exit.

        Ensures proper cleanup by calling close() method.

        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        """
        try:
            await self.close()
        except Exception:
            # Suppress exceptions during cleanup to follow context manager best practices
            pass

    async def close(self) -> None:
        """
        Close HTTP client and cleanup resources.

        Closes the underlying HTTP client connection pool. This method is
        automatically called when exiting an async context manager.
        Handles errors gracefully to ensure cleanup always completes.
        """
        if self._session:
            try:
                await self.client.close_async()
            except Exception:
                # Suppress errors during close to ensure cleanup completes
                pass
            finally:
                self._session = None

    async def query(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> GraphQLResult:
        """
        Execute GraphQL query using gql.

        Args:
            query: GraphQL query string
            variables: Query variables (optional)
            operation_name: Operation name for multi-operation queries (optional)
            headers: Custom request headers (optional)

        Returns:
            GraphQLResult with query result including data, errors, and metadata

        Raises:
            GraphQLError: If query validation fails or execution fails

        Example:
            >>> result = await gql.query(
            ...     query="query GetUser($id: ID!) { user(id: $id) { name email } }",
            ...     variables={"id": "1"}
            ... )
            >>> if result.success:
            ...     print(result.data)
            >>> else:
            ...     print(result.errors)
        """
        return await self._execute("query", query, variables, operation_name, headers)

    async def mutate(
        self,
        mutation: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> GraphQLResult:
        """
        Execute GraphQL mutation using gql.

        Args:
            mutation: GraphQL mutation string
            variables: Mutation variables (optional)
            operation_name: Operation name for multi-operation queries (optional)
            headers: Custom request headers (optional)

        Returns:
            GraphQLResult with mutation result including data, errors, and metadata

        Raises:
            GraphQLError: If mutation validation fails or execution fails

        Example:
            >>> result = await gql.mutate(
            ...     mutation=(
            ...         "mutation CreateUser($input: UserInput!) "
            ...         "{ createUser(input: $input) { id name } }"
            ...     ),
            ...     variables={"input": {"name": "John", "email": "john@example.com"}}
            ... )
            >>> if result.success:
            ...     print(result.data)
            >>> else:
            ...     print(result.errors)
        """
        return await self._execute("mutation", mutation, variables, operation_name, headers)

    def _get_schema(self) -> Any:
        """Get schema from instance or client."""
        if self._schema:
            return self._schema
        if hasattr(self.client, "schema"):
            return self.client.schema
        return None

    async def _prepare_request_context(
        self,
        operation_type: str,
        query: str,
        variables: dict[str, Any] | None,
        operation_name: str | None,
        headers: dict[str, str] | None,
    ) -> _GraphQLRequestContext:
        """
        Prepare request context with middleware.

        Args:
            operation_type: Type of operation ("query", "mutation", "subscription")
            query: GraphQL query/mutation string
            variables: Operation variables
            operation_name: Operation name (optional)
            headers: Custom request headers

        Returns:
            _GraphQLRequestContext with middleware applied
        """
        request_context = _GraphQLRequestContext(
            query=query,
            operation_type=operation_type,
            variables=variables or {},
            operation_name=operation_name,
            headers=headers.copy() if headers else {},
        )
        # Add schema to metadata for ValidationMiddleware
        schema = self._get_schema()
        if schema:
            request_context.metadata["schema"] = schema
        if self._middleware:
            await self._middleware.process_request(request_context)
        return request_context

    def _apply_transport_headers(self, headers: dict[str, str]) -> None:
        """Apply headers to transport if available."""
        if not headers:
            return
        if not hasattr(self._transport, "headers"):
            return
        transport_headers = getattr(self._transport, "headers", None)
        if transport_headers is not None:
            transport_headers.update(headers)

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

    def _extract_response_headers(self) -> dict[str, str]:
        """Extract response headers from transport if available."""
        if not hasattr(self._transport, "headers"):
            return {}
        transport_headers = getattr(self._transport, "headers", None)
        if transport_headers:
            headers_dict = dict(transport_headers)
            return self._redact_sensitive_headers(headers_dict)
        return {}

    async def _ensure_session(self) -> None:
        """Ensure gql session is created."""
        if self._session is None:
            self._session = await self.client.connect_async()

    async def _execute_operation(self, request_context: _GraphQLRequestContext) -> Any:
        """Execute GraphQL operation and return result data."""
        gql_query = gql(request_context.query)
        return await self._session.execute(
            gql_query,
            variable_values=request_context.variables,
            operation_name=request_context.operation_name,
        )

    def _create_success_result(
        self,
        operation_type: str,
        result_data: Any,
        request_context: _GraphQLRequestContext,
        response_time: float,
        response_headers: dict[str, str],
    ) -> GraphQLResult:
        """Create successful GraphQLResult."""
        return GraphQLResult(
            operation_name=request_context.operation_name,
            operation_type=operation_type,
            response_time=response_time,
            success=True,
            data={"data": result_data} if result_data is not None else None,
            errors=[],
            headers=response_headers,
            metadata=request_context.metadata.copy(),
        )

    async def _execute(
        self,
        operation_type: str,
        query: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> GraphQLResult:
        """
        Execute GraphQL operation (query or mutation) using gql.

        Args:
            operation_type: Type of operation ("query", "mutation", "subscription")
            query: GraphQL query/mutation string
            variables: Operation variables (optional)
            operation_name: Operation name (optional)
            headers: Custom request headers (optional)

        Returns:
            GraphQLResult with operation result including data, errors, and metadata

        Raises:
            GraphQLError: If query validation fails or execution fails
        """
        while True:
            start_time = time()
            request_context = await self._prepare_request_context(
                operation_type=operation_type,
                query=query,
                variables=variables,
                operation_name=operation_name,
                headers=headers,
            )
            request_context.metadata["start_time"] = start_time
            try:
                await self._ensure_session()
                self._apply_transport_headers(request_context.headers)
                result_data = await self._execute_operation(request_context)
                response_time = time() - start_time
                response_headers = self._extract_response_headers()
                result = self._create_success_result(
                    operation_type,
                    result_data,
                    request_context,
                    response_time,
                    response_headers,
                )
                result = await self._process_response(result, request_context)
                return result
            except Exception as e:
                error_result = await self._handle_operation_error(
                    e, operation_type, operation_name, request_context, start_time
                )
                # Check if retry is needed
                if request_context.metadata.get("should_retry"):
                    continue  # Retry the operation (delay already handled by RetryHandler)
                return error_result

    async def _process_response(
        self,
        result: GraphQLResult,
        request_context: _GraphQLRequestContext,
    ) -> GraphQLResult:
        """
        Process response through middleware.

        Args:
            result: GraphQLResult to process
            request_context: Request context

        Returns:
            GraphQLResult with processed response data
        """
        if self._middleware:
            response_context = _GraphQLResponseContext(result)
            response_context.metadata.update(result.metadata)
            await self._middleware.process_response(response_context)
            result = response_context.result
        return result

    async def _handle_operation_error(
        self,
        error: Exception,
        operation_type: str,
        operation_name: str | None,
        request_context: _GraphQLRequestContext,
        start_time: float,
    ) -> GraphQLResult:
        """
        Handle operation errors and return error GraphQLResult.

        Args:
            error: Exception that occurred
            operation_type: Type of operation
            operation_name: Operation name
            request_context: Request context
            start_time: Start time of operation

        Returns:
            GraphQLResult with error information
        """
        response_time = time() - start_time
        error_msg = str(error)
        # Extract GraphQL errors if available
        errors: list[dict[str, Any]] = []
        if isinstance(error, GraphQLError):
            errors = [{"message": error_msg, "extensions": getattr(error, "extensions", {})}]
        else:
            errors = [{"message": error_msg}]
        if self._middleware:
            error_result = await self._middleware.process_error(request_context, error)
            if error_result is not None:
                return error_result
        return GraphQLResult(
            operation_name=operation_name,
            operation_type=operation_type,
            response_time=response_time,
            success=False,
            data=None,
            errors=errors,
            headers={},
            metadata=request_context.metadata.copy(),
        )
