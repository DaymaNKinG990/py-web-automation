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

    def _check_pydantic_import(
        self, parser: ASTParser, relative_path: Path
    ) -> ComplianceViolation | None:
        """
        Check for Pydantic imports.

        Args:
            parser: AST parser instance
            relative_path: Relative file path

        Returns:
            ComplianceViolation if found, None otherwise
        """
        for import_node in parser.get_imports():
            if isinstance(import_node, ast.ImportFrom):
                if import_node.module == "pydantic":
                    return ComplianceViolation(
                        principle="Performance Optimization",
                        file_path=str(relative_path),
                        line_number=import_node.lineno,
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
            elif isinstance(import_node, ast.Import):
                for alias in import_node.names:
                    if alias.name == "pydantic":
                        return ComplianceViolation(
                            principle="Performance Optimization",
                            file_path=str(relative_path),
                            line_number=import_node.lineno,
                            violation_type="pydantic_usage",
                            violation_description=(
                                "File imports pydantic, but constitution requires msgspec "
                                "for performance-critical components"
                            ),
                            severity="HIGH",
                            remediation_suggestion=(
                                "Replace pydantic with msgspec for data "
                                "serialization/deserialization"
                            ),
                        )
        return None

    def _has_msgspec_import(self, parser: ASTParser) -> bool:
        """
        Check if file imports msgspec.

        Args:
            parser: AST parser instance

        Returns:
            True if msgspec is imported
        """
        for import_node in parser.get_imports():
            if isinstance(import_node, ast.ImportFrom):
                if import_node.module == "msgspec" or (
                    import_node.module and import_node.module.startswith("msgspec.")
                ):
                    return True
            elif isinstance(import_node, ast.Import):
                for alias in import_node.names:
                    if alias.name == "msgspec" or alias.name.startswith("msgspec."):
                        return True
        return False

    def _has_data_models(self, parser: ASTParser) -> bool:
        """
        Check if file contains data model classes.

        Args:
            parser: AST parser instance

        Returns:
            True if data models are found
        """
        return any(
            cls.name.endswith("Model") or "Struct" in cls.name for cls in parser.get_classes()
        )

    def _check_msgspec_usage(
        self, parser: ASTParser, relative_path: Path
    ) -> ComplianceViolation | None:
        """
        Check if data models use msgspec.

        Args:
            parser: AST parser instance
            relative_path: Relative file path

        Returns:
            ComplianceViolation if missing, None otherwise
        """
        has_msgspec = self._has_msgspec_import(parser)
        has_data_models = self._has_data_models(parser)

        if has_data_models and not has_msgspec:
            return ComplianceViolation(
                principle="Performance Optimization",
                file_path=str(relative_path),
                line_number=0,
                violation_type="missing_msgspec",
                violation_description=(
                    "File contains data models but doesn't use msgspec for serialization"
                ),
                severity="MEDIUM",
                remediation_suggestion=(
                    "Use msgspec.Struct for data models instead of other serialization libraries"
                ),
            )

        return None

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

        pydantic_violation = self._check_pydantic_import(parser, relative_path)
        if pydantic_violation:
            violations.append(pydantic_violation)

        msgspec_violation = self._check_msgspec_usage(parser, relative_path)
        if msgspec_violation:
            violations.append(msgspec_violation)

        return violations
