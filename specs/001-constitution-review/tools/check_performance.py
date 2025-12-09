"""
Performance Optimization checker.

This checker verifies that performance-critical components use msgspec (not Pydantic).
"""

import ast
from pathlib import Path

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .models import ComplianceViolation


class PerformanceChecker(BaseChecker):
    """Checker for Performance Optimization principle compliance."""

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Performance Optimization"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for Performance Optimization violations.

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

        # Check for Pydantic imports
        has_pydantic = False
        pydantic_import_line = 0

        for import_node in parser.get_imports():
            if isinstance(import_node, ast.ImportFrom):
                if import_node.module == "pydantic":
                    has_pydantic = True
                    pydantic_import_line = import_node.lineno
                    break
            elif isinstance(import_node, ast.Import):
                for alias in import_node.names:
                    if alias.name == "pydantic":
                        has_pydantic = True
                        pydantic_import_line = import_node.lineno
                        break

        if has_pydantic:
            violations.append(
                ComplianceViolation(
                    principle="Performance Optimization",
                    file_path=str(relative_path),
                    line_number=pydantic_import_line,
                    violation_type="pydantic_usage",
                    violation_description=(
                        "File imports pydantic, but constitution requires msgspec "
                        "for performance-critical components"
                    ),
                    severity="HIGH",
                    remediation_suggestion=(
                        "Replace pydantic with msgspec for data serialization/deserialization"
                    ),
                )
            )

        # Check if msgspec is used for data models
        has_msgspec = False
        for import_node in parser.get_imports():
            if isinstance(import_node, ast.ImportFrom):
                if import_node.module == "msgspec":
                    has_msgspec = True
                    break

        # If file has data models but no msgspec, suggest using it
        has_data_models = any(
            cls.name.endswith("Model") or "Struct" in cls.name for cls in parser.get_classes()
        )
        if has_data_models and not has_msgspec:
            violations.append(
                ComplianceViolation(
                    principle="Performance Optimization",
                    file_path=str(relative_path),
                    line_number=0,
                    violation_type="missing_msgspec",
                    violation_description=(
                        "File contains data models but doesn't use msgspec for serialization"
                    ),
                    severity="MEDIUM",
                    remediation_suggestion=(
                        "Use msgspec.Struct for data models instead of other "
                        "serialization libraries"
                    ),
                )
            )

        return violations
