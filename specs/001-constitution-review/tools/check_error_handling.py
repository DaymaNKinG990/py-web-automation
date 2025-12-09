"""
Error Handling checker.

This checker verifies that exceptions use WebAutomationError hierarchy and
proper exception chaining.
"""

import ast
from pathlib import Path
from typing import ClassVar

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .models import ComplianceViolation


class ErrorHandlingChecker(BaseChecker):
    """Checker for Error Handling standard compliance."""

    BASE_EXCEPTION = "WebAutomationError"
    # Whitelist of allowed exception base classes
    ALLOWED_BASE_EXCEPTIONS: ClassVar[set[str]] = {BASE_EXCEPTION}

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Error Handling"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for Error Handling violations.

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

        # Check exception hierarchy
        violations.extend(self._check_exception_hierarchy(parser, relative_path))

        # Check exception chaining
        violations.extend(self._check_exception_chaining(parser, relative_path))

        return violations

    def _is_exception_class(self, cls: ast.ClassDef) -> bool:
        """
        Check if class is an exception class.

        Args:
            cls: Class AST node

        Returns:
            True if class is an exception
        """
        return cls.name.endswith("Error") or cls.name.endswith("Exception")

    def _has_allowed_base(self, cls: ast.ClassDef) -> bool:
        """
        Check if class has allowed base exception.

        Args:
            cls: Class AST node

        Returns:
            True if class has allowed base
        """
        for base in cls.bases:
            if isinstance(base, ast.Name):
                if base.id in self.ALLOWED_BASE_EXCEPTIONS:
                    return True
            elif isinstance(base, ast.Attribute):
                if base.attr in self.ALLOWED_BASE_EXCEPTIONS:
                    return True
        return False

    def _check_exception_hierarchy(
        self, parser: ASTParser, relative_path: Path
    ) -> list[ComplianceViolation]:
        """
        Check that exceptions inherit from WebAutomationError.

        Args:
            parser: AST parser instance
            relative_path: Relative file path

        Returns:
            List of violations

        Note:
            This check only validates direct inheritance from explicitly allowed
            base classes. Indirect/transitive inheritance (e.g., A inherits from B,
            B inherits from WebAutomationError) cannot be reliably detected without
            cross-file type resolution and is left as a future enhancement.
        """
        violations: list[ComplianceViolation] = []

        for cls in parser.get_classes():
            if not self._is_exception_class(cls):
                continue

            if not self._has_allowed_base(cls) and cls.name != self.BASE_EXCEPTION:
                violations.append(
                    ComplianceViolation(
                        standard="Error Handling",
                        file_path=str(relative_path),
                        line_number=cls.lineno,
                        violation_type="invalid_exception_hierarchy",
                        violation_description=(
                            f"Exception class '{cls.name}' does not inherit from "
                            f"{self.BASE_EXCEPTION}"
                        ),
                        severity="HIGH",
                        remediation_suggestion=(
                            f"Make '{cls.name}' inherit from "
                            f"{self.BASE_EXCEPTION} or its subclasses"
                        ),
                    )
                )

        return violations

    def _get_except_handlers(
        self, func: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> list[ast.ExceptHandler]:
        """
        Extract all except handlers from function.

        Args:
            func: Function AST node

        Returns:
            List of except handlers
        """
        except_handlers: list[ast.ExceptHandler] = []
        for node in ast.walk(func):
            if isinstance(node, ast.ExceptHandler):
                except_handlers.append(node)
        return except_handlers

    def _is_new_exception_in_except(
        self, raise_node: ast.Raise, except_handlers: list[ast.ExceptHandler]
    ) -> bool:
        """
        Check if raise node is a new exception inside except handler.

        Args:
            raise_node: Raise AST node
            except_handlers: List of except handlers

        Returns:
            True if new exception in except handler
        """
        if not isinstance(raise_node.exc, ast.Call):
            return False

        for except_handler in except_handlers:
            if self._is_node_in_handler(raise_node, except_handler):
                return True
        return False

    def _check_exception_chaining(
        self, parser: ASTParser, relative_path: Path
    ) -> list[ComplianceViolation]:
        """
        Check that exceptions use proper exception chaining (from e).

        Args:
            parser: AST parser instance
            relative_path: Relative file path

        Returns:
            List of violations

        Note:
            Only flags newly constructed exceptions (ast.Call) inside except blocks
            that lack 'from' clause. Variable re-raises (raise e) are valid without 'from'.
        """
        violations: list[ComplianceViolation] = []

        for func in parser.get_functions():
            except_handlers = self._get_except_handlers(func)

            for node in ast.walk(func):
                if isinstance(node, ast.Raise):
                    if (
                        node.exc is not None
                        and node.cause is None
                        and self._is_new_exception_in_except(node, except_handlers)
                    ):
                        violations.append(
                            ComplianceViolation(
                                standard="Error Handling",
                                file_path=str(relative_path),
                                line_number=node.lineno,
                                violation_type="missing_exception_chaining",
                                violation_description=(
                                    f"New exception raised at line {node.lineno} "
                                    "inside except handler should use 'from e' "
                                    "for proper exception chaining"
                                ),
                                severity="MEDIUM",
                                remediation_suggestion=(
                                    "Use 'raise NewException from e' for exception chaining"
                                ),
                            )
                        )

        return violations

    def _is_node_in_handler(self, node: ast.Raise, handler: ast.ExceptHandler) -> bool:
        """
        Check if a raise node is within an except handler body.

        Args:
            node: Raise node to check
            handler: ExceptHandler node

        Returns:
            True if node is within handler body
        """
        # Walk the handler body to check if node is a descendant
        for body_node in ast.walk(handler):
            if body_node is node:
                return True
        return False
