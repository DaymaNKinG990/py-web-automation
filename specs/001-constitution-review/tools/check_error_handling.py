"""
Error Handling checker.

This checker verifies that exceptions use WebAutomationError hierarchy and
proper exception chaining.
"""

import ast
from pathlib import Path

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .models import ComplianceViolation


class ErrorHandlingChecker(BaseChecker):
    """Checker for Error Handling standard compliance."""

    BASE_EXCEPTION = "WebAutomationError"

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
        """
        violations: list[ComplianceViolation] = []

        # Check exception classes
        for cls in parser.get_classes():
            # Check if class is an exception (ends with Error or Exception)
            if not (cls.name.endswith("Error") or cls.name.endswith("Exception")):
                continue

            # Check base classes
            has_base = False
            for base in cls.bases:
                if isinstance(base, ast.Name):
                    if base.id == self.BASE_EXCEPTION or base.id.endswith("Error"):
                        has_base = True
                        break
                elif isinstance(base, ast.Attribute):
                    if base.attr == self.BASE_EXCEPTION or base.attr.endswith("Error"):
                        has_base = True
                        break

            if not has_base and cls.name != self.BASE_EXCEPTION:
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
        """
        violations: list[ComplianceViolation] = []

        for func in parser.get_functions():
            for node in ast.walk(func):
                if isinstance(node, ast.Raise):
                    if node.exc is not None:
                        # Check if raise uses 'from' for chaining
                        # This is a simplified check - full analysis would require
                        # more AST traversal
                        if node.cause is None:
                            # Check if this is re-raising an exception (could benefit from 'from')
                            if isinstance(node.exc, ast.Name):
                                violations.append(
                                    ComplianceViolation(
                                        standard="Error Handling",
                                        file_path=str(relative_path),
                                        line_number=node.lineno,
                                        violation_type="missing_exception_chaining",
                                        violation_description=(
                                            f"Exception raised at line {node.lineno} "
                                            "should use 'from e' for proper exception "
                                            "chaining"
                                        ),
                                        severity="MEDIUM",
                                        remediation_suggestion=(
                                            "Use 'raise NewException from e' for exception chaining"
                                        ),
                                    )
                                )

        return violations
