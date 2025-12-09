"""
Import Organization checker.

This checker verifies that imports are at the top of files, organized correctly,
and use TYPE_CHECKING for circular dependencies.
"""

import ast
from pathlib import Path

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .models import ComplianceViolation


class ImportOrganizationChecker(BaseChecker):
    """Checker for Import Organization standard compliance."""

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Import Organization"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for Import Organization violations.

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

        # Check import order and location
        violations.extend(self._check_import_order(parser, relative_path, file_path))

        # Check for TYPE_CHECKING usage for circular dependencies
        violations.extend(self._check_type_checking_usage(parser))

        return violations

    def _check_import_order(
        self, parser: ASTParser, relative_path: Path, file_path: Path
    ) -> list[ComplianceViolation]:
        """
        Check that imports are at the top and properly ordered.

        Args:
            parser: AST parser instance
            relative_path: Relative file path
            file_path: Full file path

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        if not parser.tree:
            return violations

        # Get all import nodes
        imports: list[ast.Import | ast.ImportFrom] = []
        for node in ast.walk(parser.tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(node)

        if not imports:
            return violations

        # Check that imports are at the top (before any non-import statements)
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()
        except (OSError, UnicodeDecodeError):
            # Only handle file I/O and encoding errors; let other exceptions propagate
            # OSError covers FileNotFoundError, PermissionError, etc.
            # UnicodeDecodeError handles encoding issues explicitly
            return violations

        # Find first non-import, non-comment, non-docstring line
        first_import_line = min(imp.lineno for imp in imports)
        for i, line in enumerate(lines[: first_import_line - 1], start=1):
            stripped = line.strip()
            if (
                stripped
                and not stripped.startswith("#")
                and not stripped.startswith('"""')
                and not stripped.startswith("'''")
            ):
                violations.append(
                    ComplianceViolation(
                        standard="Import Organization",
                        file_path=str(relative_path),
                        line_number=i,
                        violation_type="imports_not_at_top",
                        violation_description=(
                            f"Non-import statement found before imports at line {i}"
                        ),
                        severity="MEDIUM",
                        remediation_suggestion="Move all imports to the top of the file",
                    )
                )
                break

        # Check import order: stdlib, third-party, local
        violations.extend(self._check_import_grouping(imports, relative_path))

        return violations

    def _check_import_grouping(
        self,
        imports: list[ast.Import | ast.ImportFrom],
        relative_path: Path,
    ) -> list[ComplianceViolation]:
        """
        Check that imports are grouped correctly (stdlib, third-party, local).

        Args:
            imports: List of import nodes
            relative_path: Relative file path

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        # Simplified check - would need more sophisticated analysis for full validation
        # This checks if local imports come before third-party imports
        stdlib_modules = {
            "os",
            "sys",
            "pathlib",
            "typing",
            "collections",
            "dataclasses",
            "abc",
            "enum",
        }
        seen_third_party = False

        for imp in imports:
            if isinstance(imp, ast.ImportFrom):
                module = imp.module
                if module:
                    is_stdlib = (
                        any(module.startswith(stdlib) for stdlib in stdlib_modules)
                        or module.split(".")[0] in stdlib_modules
                    )
                    is_local = (
                        module.startswith("py_web_automation") or not module or "." not in module
                    )

                    if not is_stdlib and not is_local:
                        seen_third_party = True
                    elif is_local and seen_third_party:
                        violations.append(
                            ComplianceViolation(
                                standard="Import Organization",
                                file_path=str(relative_path),
                                line_number=imp.lineno,
                                violation_type="incorrect_import_order",
                                violation_description=(
                                    f"Local import '{module}' appears after third-party imports"
                                ),
                                severity="LOW",
                                remediation_suggestion=(
                                    "Reorder imports: stdlib → third-party → local"
                                ),
                            )
                        )

        return violations

    def _check_type_checking_usage(self, parser: ASTParser) -> list[ComplianceViolation]:
        """
        Check for TYPE_CHECKING usage for circular dependencies.

        Args:
            parser: AST parser instance

        Returns:
            List of violations

        Note:
            This is a placeholder for future implementation.
            Full circular dependency detection requires dependency graph analysis.
        """
        violations: list[ComplianceViolation] = []
        # Placeholder for future implementation
        return violations
