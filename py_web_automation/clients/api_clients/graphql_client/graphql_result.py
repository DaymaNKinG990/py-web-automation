"""
Data models for GraphQL API client.

This module provides GraphQLResult class for standardized GraphQL operation results.
"""

# Python imports
from typing import Any

from msgspec import Struct, field


class GraphQLResult(Struct, frozen=True):
    """
    GraphQL operation result.

    Contains complete information about a GraphQL operation execution,
    including data, errors, timing information, and metadata.

    Attributes:
        operation_name: Name of the GraphQL operation (if specified)
        operation_type: Type of operation ("query", "mutation", "subscription")
        response_time: Time taken to execute the operation in seconds
        success: Whether the operation completed successfully (no errors)
        data: Response data from GraphQL operation (None if operation failed)
        errors: List of GraphQL errors (empty if operation succeeded)
        headers: Response headers from HTTP request
        metadata: Custom metadata dictionary for middleware communication

    Example:
        >>> result = await gql.query("query { user { name } }")
        >>> if result.success:
        ...     print(result.data)
        >>> else:
        ...     for error in result.errors:
        ...         print(error)
    """

    operation_name: str | None
    operation_type: str
    response_time: float
    success: bool
    data: dict[str, Any] | None = None
    errors: list[dict[str, Any]] = field(default_factory=list)
    headers: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def raise_for_errors(self) -> None:
        """
        Raise exception if operation has errors.

        Raises:
            Exception: If operation has any GraphQL errors

        Example:
            >>> result = await gql.query("query { user { name } }")
            >>> result.raise_for_errors()  # Raises if errors present
        """
        if not self.errors:
            return
        error_messages = [error.get("message", str(error)) for error in self.errors]
        error_msg = "; ".join(error_messages)
        raise Exception(
            f"GraphQL operation '{self.operation_name or 'unnamed'}' failed: {error_msg}"
        )
