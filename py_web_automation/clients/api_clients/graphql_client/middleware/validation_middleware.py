"""
Validation middleware for GraphQL client.

This module provides ValidationMiddleware for GraphQL query validation.
"""

# Python imports
from typing import TYPE_CHECKING

from graphql import GraphQLError, parse, validate

# Local imports
from ..graphql_result import GraphQLResult
from .context import _GraphQLRequestContext, _GraphQLResponseContext
from .middleware import Middleware

if TYPE_CHECKING:
    from graphql import DocumentNode
    from graphql.type import GraphQLSchema


class ValidationMiddleware(Middleware):
    """
    Middleware for validating GraphQL queries before execution.

    Validates GraphQL queries using graphql-core schema validation.
    Raises GraphQLError if query is invalid.

    Attributes:
        schema: GraphQL schema for validation
        enabled: Whether validation is enabled

    Example:
        >>> from py_web_automation.clients.graphql_client import (
        ...     GraphQLClient,
        ...     MiddlewareChain,
        ... )
        >>> from py_web_automation.clients.graphql_client.middleware import (
        ...     ValidationMiddleware,
        ... )
        >>> from graphql import build_schema
        >>> schema = build_schema("type Query { user: User } type User { id: ID! name: String! }")
        >>> validation_middleware = ValidationMiddleware(schema=schema, enabled=True)
        >>> middleware_chain = MiddlewareChain().add(validation_middleware)
        >>> async with GraphQLClient(
        ...     "https://api.example.com", config, middleware=middleware_chain
        ... ) as gql:
        ...     result = await gql.query("query { user { name } }")
    """

    def __init__(
        self,
        schema: "GraphQLSchema" | None = None,
        enabled: bool = True,
    ) -> None:
        """
        Initialize validation middleware.

        Args:
            schema: GraphQL schema for validation (optional)
            enabled: Whether validation is enabled (default: True)
        """
        self.schema = schema
        self.enabled = enabled

    def _get_schema(self, context: _GraphQLRequestContext) -> "GraphQLSchema" | None:
        """
        Get schema from metadata or use instance schema.

        Args:
            context: Request context that may contain schema in metadata

        Returns:
            GraphQL schema or None if not available
        """
        # Check if schema is provided in metadata (set by GraphQLClient)
        schema = context.metadata.get("schema")
        if schema:
            return schema
        return self.schema

    def _validate_query(
        self, schema: "GraphQLSchema", document: "DocumentNode"
    ) -> None:
        """Validate GraphQL query and raise GraphQLError if invalid."""
        validation_errors = validate(schema, document)
        if validation_errors:
            error_messages = [str(err) for err in validation_errors]
            error_msg = f"Query validation failed: {'; '.join(error_messages)}"
            raise GraphQLError(error_msg) from validation_errors[0]

    async def process_request(self, context: _GraphQLRequestContext) -> None:
        """
        Validate GraphQL query before execution.

        Validates the query using graphql-core and raises GraphQLError
        if validation fails.

        Args:
            context: Request context containing query to validate

        Raises:
            GraphQLError: If query validation fails
        """
        if not self.enabled:
            return
        try:
            # Parse query
            document = parse(context.query)
            # Get schema for validation
            schema = self._get_schema(context)
            if schema is None:
                return
            # Validate query
            self._validate_query(schema, document)
        except GraphQLError:
            # Re-raise GraphQLError as-is
            raise
        except Exception:
            pass
            # Don't fail on validation errors - allow query to proceed
            # This prevents validation from blocking queries when schema is unavailable

    async def process_response(self, context: _GraphQLResponseContext) -> None:
        """
        No-op for responses.

        Args:
            context: Response context
        """
        pass

    async def process_error(
        self, context: _GraphQLRequestContext, error: Exception
    ) -> GraphQLResult | None:
        """
        No-op for errors.

        Args:
            context: Request context
            error: Exception that occurred
        """
        return None
