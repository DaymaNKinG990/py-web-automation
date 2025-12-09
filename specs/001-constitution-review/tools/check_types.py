"""
Type Safety principle checker.

This checker verifies that all public APIs have complete type annotations.
"""

import ast
from pathlib import Path

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .models import ComplianceViolation
from .utils import is_public_api


class TypeSafetyChecker(BaseChecker):
    """Checker for Type Safety principle compliance."""

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Type Safety"

    def _check_function_return_type(
        self, func: ast.FunctionDef | ast.AsyncFunctionDef, relative_path: Path
    ) -> ComplianceViolation | None:
        """
        Check if function has return type annotation.

        Args:
            func: Function AST node
            relative_path: Relative file path

        Returns:
            ComplianceViolation if missing, None otherwise
        """
        if func.returns is None:
            return ComplianceViolation(
                principle="Type Safety",
                file_path=str(relative_path),
                line_number=func.lineno,
                violation_type="missing_return_type_annotation",
                violation_description=(
                    f"Public function '{func.name}' is missing return type annotation"
                ),
                severity="HIGH",
                remediation_suggestion=(
                    f"Add return type annotation to function "
                    f"'{func.name}' (e.g., -> int, -> str, -> None)"
                ),
            )
        return None

    def _check_function_parameters(
        self, func: ast.FunctionDef | ast.AsyncFunctionDef, relative_path: Path
    ) -> list[ComplianceViolation]:
        """
        Check if function parameters have type annotations.

        Args:
            func: Function AST node
            relative_path: Relative file path

        Returns:
            List of violations for missing parameter annotations
        """
        violations: list[ComplianceViolation] = []

        for arg in func.args.args:
            if arg.annotation is None and is_public_api(arg.arg) and arg.arg not in ("self", "cls"):
                violations.append(
                    ComplianceViolation(
                        principle="Type Safety",
                        file_path=str(relative_path),
                        line_number=func.lineno,
                        violation_type="missing_parameter_type_annotation",
                        violation_description=(
                            f"Parameter '{arg.arg}' in function "
                            f"'{func.name}' is missing type annotation"
                        ),
                        severity="HIGH",
                        remediation_suggestion=(
                            f"Add type annotation to parameter '{arg.arg}' "
                            f"in function '{func.name}'"
                        ),
                    )
                )

        return violations

    def _is_public_method(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """
        Check if method should be checked (public, not dunder).

        Args:
            node: Method AST node

        Returns:
            True if method should be checked
        """
        # Skip private methods (but not dunder methods)
        if node.name.startswith("_") and not (
            node.name.startswith("__") and node.name.endswith("__")
        ):
            return False
        # Skip dunder methods
        if node.name.startswith("__") and node.name.endswith("__"):
            return False
        return True

    def _check_class_methods(
        self, cls: ast.ClassDef, relative_path: Path
    ) -> list[ComplianceViolation]:
        """
        Check class methods for type annotations.

        Args:
            cls: Class AST node
            relative_path: Relative file path

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        for node in cls.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            if not self._is_public_method(node):
                continue

            # Check return type
            if node.returns is None:
                violations.append(
                    ComplianceViolation(
                        principle="Type Safety",
                        file_path=str(relative_path),
                        line_number=node.lineno,
                        violation_type="missing_method_return_type_annotation",
                        violation_description=(
                            f"Public method '{node.name}' in class "
                            f"'{cls.name}' is missing return type annotation"
                        ),
                        severity="HIGH",
                        remediation_suggestion=(
                            f"Add return type annotation to method '{cls.name}.{node.name}'"
                        ),
                    )
                )

            # Check parameter types
            for arg in node.args.args:
                if (
                    arg.annotation is None
                    and is_public_api(arg.arg)
                    and arg.arg not in ("self", "cls")
                ):
                    violations.append(
                        ComplianceViolation(
                            principle="Type Safety",
                            file_path=str(relative_path),
                            line_number=node.lineno,
                            violation_type="missing_method_parameter_type_annotation",
                            violation_description=(
                                f"Parameter '{arg.arg}' in method "
                                f"'{cls.name}.{node.name}' is missing type annotation"
                            ),
                            severity="HIGH",
                            remediation_suggestion=(
                                f"Add type annotation to parameter "
                                f"'{arg.arg}' in method "
                                f"'{cls.name}.{node.name}'"
                            ),
                        )
                    )

        return violations

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for Type Safety principle violations.

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

        # Check public functions
        for func in parser.get_public_functions():
            return_violation = self._check_function_return_type(func, relative_path)
            if return_violation:
                violations.append(return_violation)
            violations.extend(self._check_function_parameters(func, relative_path))

        # Check public classes
        for cls in parser.get_public_classes():
            violations.extend(self._check_class_methods(cls, relative_path))

        return violations
