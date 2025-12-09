"""
AST parser wrapper for constitution compliance review.

This module provides enhanced AST parsing capabilities and helper functions
for analyzing Python code structure.
"""

import ast
from pathlib import Path
from typing import TYPE_CHECKING

from .utils import parse_ast

if TYPE_CHECKING:
    from collections.abc import Iterator


class ASTParser:
    """Enhanced AST parser with helper methods for code analysis."""

    def __init__(self, file_path: Path) -> None:
        """
        Initialize the AST parser for a specific file.

        Args:
            file_path: Path to the Python file to parse
        """
        self.file_path = file_path
        self.tree: ast.Module | None = None
        self._parse()

    def _parse(self) -> None:
        """Parse the file into an AST."""
        self.tree = parse_ast(self.file_path)

    def is_valid(self) -> bool:
        """
        Check if the file was successfully parsed.

        Returns:
            True if AST is valid, False otherwise
        """
        return self.tree is not None

    def get_functions(self) -> "Iterator[ast.FunctionDef | ast.AsyncFunctionDef]":
        """
        Get all function definitions in the file.

        Yields:
            FunctionDef or AsyncFunctionDef nodes
        """
        if not self.tree:
            return

        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                yield node

    def get_classes(self) -> "Iterator[ast.ClassDef]":
        """
        Get all class definitions in the file.

        Yields:
            ClassDef nodes
        """
        if not self.tree:
            return

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                yield node

    def get_imports(self) -> "Iterator[ast.Import | ast.ImportFrom]":
        """
        Get all import statements in the file.

        Yields:
            Import or ImportFrom nodes
        """
        if not self.tree:
            return

        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                yield node

    def get_async_functions(self) -> "Iterator[ast.AsyncFunctionDef]":
        """
        Get all async function definitions.

        Yields:
            AsyncFunctionDef nodes
        """
        if not self.tree:
            return

        for node in self.get_functions():
            if isinstance(node, ast.AsyncFunctionDef):
                yield node

    def get_public_functions(self) -> "Iterator[ast.FunctionDef | ast.AsyncFunctionDef]":
        """
        Get all public function definitions (not starting with underscore).

        Yields:
            FunctionDef or AsyncFunctionDef nodes for public functions
        """
        for func in self.get_functions():
            if not func.name.startswith("_"):
                yield func

    def get_public_classes(self) -> "Iterator[ast.ClassDef]":
        """
        Get all public class definitions (not starting with underscore).

        Yields:
            ClassDef nodes for public classes
        """
        for cls in self.get_classes():
            if not cls.name.startswith("_"):
                yield cls

    def has_type_checking_import(self) -> bool:
        """
        Check if the file imports TYPE_CHECKING from typing.

        Returns:
            True if TYPE_CHECKING is imported
        """
        if not self.tree:
            return False

        for node in self.get_imports():
            if isinstance(node, ast.ImportFrom):
                if node.module == "typing" and any(
                    alias.name == "TYPE_CHECKING" for alias in node.names
                ):
                    return True
        return False

    def get_decorators(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef
    ) -> list[str]:
        """
        Get decorator names for a node.

        Args:
            node: Function or class node

        Returns:
            List of decorator names
        """
        decorators: list[str] = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Attribute):
                decorators.append(decorator.attr)
        return decorators

    def has_async_context_manager(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """
        Check if a function uses async context managers (async with).

        Args:
            node: Function node to check

        Returns:
            True if function contains async with statements
        """
        if not self.tree:
            return False

        for child in ast.walk(node):
            if isinstance(child, ast.AsyncWith):
                return True
        return False

    def has_await_calls(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """
        Check if a function contains await calls.

        Args:
            node: Function node to check

        Returns:
            True if function contains await expressions
        """
        if not self.tree:
            return False

        for child in ast.walk(node):
            if isinstance(child, ast.Await):
                return True
        return False

    def is_io_operation(self, node: ast.Call) -> bool:
        """
        Check if a call node represents an I/O operation.

        Args:
            node: Call node to check

        Returns:
            True if the call is an I/O operation
        """
        io_modules = {
            "httpx",
            "aiohttp",
            "websockets",
            "aiosqlite",
            "asyncpg",
            "aiomysql",
            "open",
            "read",
            "write",
        }
        if isinstance(node.func, ast.Name):
            return node.func.id in io_modules
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                return node.func.value.id in io_modules
        return False
