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

        # Check public functions for type annotations
        for func in parser.get_public_functions():
            # Check return type annotation
            if func.returns is None:
                violations.append(
                    ComplianceViolation(
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
                )

            # Check parameter type annotations
            for arg in func.args.args:
                if (
                    arg.annotation is None
                    and is_public_api(arg.arg)
                    and arg.arg not in ("self", "cls")
                ):
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

        # Check public classes for type annotations
        for cls in parser.get_public_classes():
            # Check direct class methods only (not nested)
            for node in cls.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Skip private methods (but not dunder methods)
                    if node.name.startswith("_") and not (
                        node.name.startswith("__") and node.name.endswith("__")
                    ):
                        continue
                    # Skip dunder methods (special methods like __init__, __str__, etc.)
                    if node.name.startswith("__") and node.name.endswith("__"):
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
                                    f"'{cls.name}' is missing return type "
                                    "annotation"
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
                                        f"'{cls.name}.{node.name}' is missing "
                                        "type annotation"
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
