"""
Async-First principle checker.

This checker verifies that all I/O operations use async/await patterns.
"""

import ast
from pathlib import Path

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .models import ComplianceViolation


class AsyncFirstChecker(BaseChecker):
    """Checker for Async-First principle compliance."""

    # I/O modules that should use async
    IO_MODULES = {"httpx", "aiohttp", "websockets", "aiosqlite", "asyncpg", "aiomysql", "aiofiles"}

    # I/O function names
    IO_FUNCTIONS = {"open", "read", "write", "readline", "readlines"}

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Async-First"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for Async-First principle violations.

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

        # Check all functions for I/O operations
        for func in parser.get_functions():
            # Check if function performs I/O but is not async
            if isinstance(func, ast.FunctionDef):  # Synchronous function
                # Check for I/O operations in function body
                has_io = self._has_io_operations(func)
                if has_io:
                    violations.append(
                        ComplianceViolation(
                            principle="Async-First",
                            file_path=str(relative_path),
                            line_number=func.lineno,
                            violation_type="blocking_io_in_sync_function",
                            violation_description=(
                                f"Function '{func.name}' performs I/O operations but is not async"
                            ),
                            severity="CRITICAL",
                            code_snippet=self._get_function_snippet(file_path, func),
                            remediation_suggestion=(
                                f"Convert function '{func.name}' to async function (async def)"
                            ),
                        )
                    )

            # Check for async with usage (should use async with for async context managers)
            if isinstance(func, ast.AsyncFunctionDef):
                # Check if function uses 'with' instead of 'async with' for async resources
                has_sync_with = self._has_sync_with_for_async(func)
                if has_sync_with:
                    violations.append(
                        ComplianceViolation(
                            principle="Async-First",
                            file_path=str(relative_path),
                            line_number=func.lineno,
                            violation_type="sync_with_in_async_function",
                            violation_description=(
                                f"Function '{func.name}' uses 'with' instead of "
                                "'async with' for async resources"
                            ),
                            severity="HIGH",
                            code_snippet=self._get_function_snippet(file_path, func),
                            remediation_suggestion=(
                                f"Replace 'with' with 'async with' in function '{func.name}'"
                            ),
                        )
                    )

        return violations

    def _has_io_operations(self, func: ast.FunctionDef) -> bool:
        """
        Check if a function contains I/O operations.

        Args:
            func: Function node to check

        Returns:
            True if function contains I/O operations
        """
        for node in ast.walk(func):
            if isinstance(node, ast.Call):
                # Check for I/O module calls
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        if node.func.value.id in self.IO_MODULES:
                            return True
                # Check for I/O function calls
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.IO_FUNCTIONS:
                        return True

        return False

    def _has_sync_with_for_async(self, func: ast.AsyncFunctionDef) -> bool:
        """
        Check if async function uses sync 'with' for async resources.

        Args:
            func: Async function node to check

        Returns:
            True if function uses sync 'with' for async resources
        """
        for node in ast.walk(func):
            if isinstance(node, ast.With):
                # Check if context manager is from async module
                if isinstance(node.items[0].context_expr, ast.Call):
                    call = node.items[0].context_expr
                    if isinstance(call.func, ast.Attribute):
                        if isinstance(call.func.value, ast.Name):
                            if call.func.value.id in self.IO_MODULES:
                                return True

        return False

    def _get_function_snippet(
        self, file_path: Path, func: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> str:
        """
        Get code snippet for a function.

        Args:
            file_path: Path to the file
            func: Function node

        Returns:
            Code snippet as string
        """
        from .utils import get_code_snippet

        return get_code_snippet(file_path, func.lineno, context_lines=5)
