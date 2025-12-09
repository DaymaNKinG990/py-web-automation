"""
SOLID Principles and Design Patterns checker.

This checker verifies code follows SOLID principles and uses appropriate design patterns.
"""

import ast
from pathlib import Path

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .models import ComplianceViolation


class SOLIDChecker(BaseChecker):
    """Checker for SOLID Principles and Design Patterns compliance."""

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "SOLID Principles"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for SOLID principles violations.

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

        # Check Single Responsibility Principle
        violations.extend(self._check_single_responsibility(parser, relative_path))

        # Check for design patterns
        violations.extend(self._check_design_patterns(parser))

        return violations

    def _check_single_responsibility(
        self, parser: ASTParser, relative_path: Path
    ) -> list[ComplianceViolation]:
        """
        Check Single Responsibility Principle.

        Args:
            parser: AST parser instance
            relative_path: Relative file path

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        # Check classes for multiple responsibilities (simplified heuristic)
        for cls in parser.get_classes():
            methods = [
                node
                for node in ast.walk(cls)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            method_count = len(methods)

            # Heuristic: classes with too many methods might violate SRP
            if method_count > 20:
                violations.append(
                    ComplianceViolation(
                        principle="SOLID Principles",
                        file_path=str(relative_path),
                        line_number=cls.lineno,
                        violation_type="potential_srp_violation",
                        violation_description=(
                            f"Class '{cls.name}' has {method_count} methods, "
                            "which may indicate violation of Single "
                            "Responsibility Principle"
                        ),
                        severity="LOW",
                        remediation_suggestion=(
                            f"Review class '{cls.name}' and consider splitting "
                            "into smaller, focused classes"
                        ),
                    )
                )

        return violations

    def _check_design_patterns(
        self, parser: ASTParser
    ) -> list[ComplianceViolation]:
        """
        Check for appropriate design pattern usage.

        Args:
            parser: AST parser instance

        Returns:
            List of violations

        Note:
            This is a placeholder for future implementation.
            Full design pattern detection requires more sophisticated analysis
            (e.g., Builder pattern with method chaining, Strategy, Adapter,
            Middleware, Factory, Observer patterns).
        """
        # Placeholder for design pattern detection
        # TODO: Implement pattern detection logic
        return []
