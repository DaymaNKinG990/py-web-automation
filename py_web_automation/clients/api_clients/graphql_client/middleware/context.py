"""
Middleware context objects for GraphQL client.

This module provides request and response context objects for GraphQL middleware.
"""

# Python imports
from typing import Any

# Local imports
from ..graphql_result import GraphQLResult


class _GraphQLRequestContext:
    """
    Internal context object passed through GraphQL middleware chain.

    Contains GraphQL request information that can be modified by middleware.
    This is an internal class used only within middleware system.

    Attributes:
        query: GraphQL query/mutation string
        variables: Operation variables (can be modified)
        operation_name: Operation name (optional)
        operation_type: Type of operation ("query", "mutation", "subscription")
        headers: Request headers (can be modified)
        metadata: Custom metadata dictionary for middleware communication
    """

    def __init__(
        self,
        query: str,
        operation_type: str,
        variables: dict[str, Any] | None = None,
        operation_name: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize GraphQL request context."""
        self.query = query
        self.operation_type = operation_type
        self.variables = variables or {}
        self.operation_name = operation_name
        self.headers = headers or {}
        self.metadata: dict[str, Any] = {}


class _GraphQLResponseContext:
    """
    Internal context object for GraphQL response processing.

    Contains GraphQL response information that can be modified by middleware.
    This is an internal class used only within middleware system.

    Attributes:
        result: GraphQLResult object (can be modified)
        metadata: Custom metadata dictionary for middleware communication
    """

    def __init__(self, result: GraphQLResult) -> None:
        """Initialize GraphQL response context."""
        self.result = result
        # Copy metadata from result to context for middleware communication
        self.metadata: dict[str, Any] = result.metadata.copy() if result.metadata else {}
