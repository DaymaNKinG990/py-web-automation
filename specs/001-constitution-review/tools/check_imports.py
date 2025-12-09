"""
Import Organization checker.

This checker verifies that imports are at the top of files, organized correctly,
and use TYPE_CHECKING for circular dependencies.
"""

import ast
import sys
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

    def _get_import_nodes(self, parser: ASTParser) -> list[ast.Import | ast.ImportFrom]:
        """
        Extract all import nodes from AST.

        Args:
            parser: AST parser instance

        Returns:
            List of import nodes
        """
        if not parser.tree:
            return []

        imports: list[ast.Import | ast.ImportFrom] = []
        for node in ast.walk(parser.tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(node)

        return imports

    def _is_meaningful_line(self, line: str) -> bool:
        """
        Check if line is meaningful (not comment or docstring).

        Args:
            line: Line content

        Returns:
            True if line is meaningful

        Note:
            This method cannot reliably detect multi-line docstrings.
            The caller should skip the module docstring using AST.
        """
        stripped = line.strip()
        if not stripped:
            return False
        if stripped.startswith("#"):
            return False
        return True

    def _check_imports_at_top(
        self,
        imports: list[ast.Import | ast.ImportFrom],
        file_path: Path,
        relative_path: Path,
        parser: ASTParser,
    ) -> list[ComplianceViolation]:
        """
        Check that imports are at the top of the file.

        Args:
            imports: List of import nodes
            file_path: Full file path
            relative_path: Relative file path
            parser: AST parser instance

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        if not imports:
            return violations

        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()
        except (OSError, UnicodeDecodeError):
            return violations

        # Get module docstring end line if present
        module_docstring_end = 0
        if (
            parser.tree
            and parser.tree.body
            and isinstance(parser.tree.body[0], ast.Expr)
            and isinstance(parser.tree.body[0].value, ast.Constant)
            and isinstance(parser.tree.body[0].value.value, str)
        ):
            module_docstring_end = parser.tree.body[0].end_lineno or 0

        first_import_line = min(imp.lineno for imp in imports)
        # Start checking after module docstring
        start_line = max(module_docstring_end, 0)
        for i, line in enumerate(lines[start_line : first_import_line - 1], start=start_line + 1):
            if self._is_meaningful_line(line):
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

        imports = self._get_import_nodes(parser)
        if not imports:
            return violations

        violations.extend(self._check_imports_at_top(imports, file_path, relative_path, parser))
        violations.extend(self._check_import_grouping(imports, relative_path))

        return violations

    def _is_stdlib_module(self, module: str | None, stdlib_modules: set[str]) -> bool:
        """
        Check if module is from standard library.

        Args:
            module: Module name
            stdlib_modules: Set of stdlib module names

        Returns:
            True if module is stdlib
        """
        if not module:
            return False
        return (
            any(module.startswith(stdlib) for stdlib in stdlib_modules)
            or module.split(".")[0] in stdlib_modules
        )

    def _is_local_module(self, module: str | None) -> bool:
        """
        Check if module is local (relative or project root).

        Args:
            module: Module name

        Returns:
            True if module is local
        """
        return (
            module is None
            or (module and module.startswith("."))
            or (module and module.startswith("py_web_automation"))
        )

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

        # Use sys.stdlib_module_names for comprehensive stdlib detection (Python 3.10+)
        if hasattr(sys, "stdlib_module_names"):
            stdlib_modules = sys.stdlib_module_names
        else:
            # Fallback for Python < 3.10 with more comprehensive list
            stdlib_modules = {
                "os",
                "sys",
                "pathlib",
                "typing",
                "collections",
                "dataclasses",
                "abc",
                "enum",
                "re",
                "json",
                "datetime",
                "functools",
                "itertools",
                "asyncio",
                "logging",
                "unittest",
                "argparse",
                "subprocess",
                "inspect",
                "contextlib",
                "importlib",
                "threading",
                "multiprocessing",
                "concurrent",
            }

        seen_third_party = False

        for imp in imports:
            module = None
            if isinstance(imp, ast.ImportFrom):
                module = imp.module
            elif isinstance(imp, ast.Import):
                # For regular imports, use the first imported name as the module
                if imp.names:
                    module = imp.names[0].name

            if module is not None:
                is_local = self._is_local_module(module)
                is_stdlib = self._is_stdlib_module(module, stdlib_modules) if module else False

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
