"""
Resource Management checker.

This checker verifies that all clients implement context managers.
"""

import ast
from pathlib import Path
from typing import ClassVar

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .models import ComplianceViolation


class ResourceManagementChecker(BaseChecker):
    """Checker for Resource Management standard compliance."""

    CLIENT_CLASS_NAMES: ClassVar[set[str]] = {
        "Client",
        "HttpClient",
        "GraphQLClient",
        "GrpcClient",
        "SoapClient",
        "WebSocketClient",
        "UiClient",
        "AsyncUiClient",
        "SyncUiClient",
        "DBClient",
        "SQLiteClient",
        "PostgreSQLClient",
        "MySQLClient",
        "KafkaClient",
        "RabbitMQClient",
    }

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Resource Management"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for Resource Management violations.

        Args:
            file_path: Path to the file to check

        Returns:
            List of compliance violations found
        """
        violations: list[ComplianceViolation] = []
        parser = ASTParser(file_path)

        if not parser.is_valid():
            return violations

        relative_path = file_path.relative_to(self.project_root)

        # Check client classes for context manager implementation
        for cls in parser.get_classes():
            if cls.name in self.CLIENT_CLASS_NAMES or "Client" in cls.name:
                if not self._has_context_manager_methods(cls):
                    violations.append(
                        ComplianceViolation(
                            standard="Resource Management",
                            file_path=str(relative_path),
                            line_number=cls.lineno,
                            violation_type="missing_context_manager",
                            violation_description=(
                                f"Client class '{cls.name}' does not implement "
                                "context manager methods (__enter__/__aenter__ "
                                "and __exit__/__aexit__)"
                            ),
                            severity="CRITICAL",
                            remediation_suggestion=(
                                f"Implement context manager methods in class "
                                f"'{cls.name}' for proper resource cleanup"
                            ),
                        )
                    )

        return violations

    def _has_context_manager_methods(self, cls: ast.ClassDef) -> bool:
        """
        Check if class implements context manager methods.

        Args:
            cls: Class node to check

        Returns:
            True if class has complete context manager method pairs:
            - Sync pair: __enter__ and __exit__
            - Async pair: __aenter__ and __aexit__
        """
        has_sync_enter = False
        has_sync_exit = False
        has_async_enter = False
        has_async_exit = False

        for node in ast.walk(cls):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == "__enter__":
                    has_sync_enter = True
                elif node.name == "__exit__":
                    has_sync_exit = True
                elif node.name == "__aenter__":
                    has_async_enter = True
                elif node.name == "__aexit__":
                    has_async_exit = True

        # Return True only if a complete matching pair is found
        return (has_sync_enter and has_sync_exit) or (has_async_enter and has_async_exit)
