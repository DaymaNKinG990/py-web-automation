"""
Documentation Standards checker.

This checker verifies that all documentation is in English and docstrings
follow Google-style format.
"""

import ast
import re
from pathlib import Path

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .models import ComplianceViolation


class DocumentationChecker(BaseChecker):
    """Checker for Documentation Standards compliance."""

    GOOGLE_STYLE_SECTIONS = {"Args", "Returns", "Raises", "Example", "Examples"}

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Documentation Standards"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for Documentation Standards violations.

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

        # Check public functions and classes for docstrings
        for func in parser.get_public_functions():
            if not ast.get_docstring(func):
                violations.append(
                    ComplianceViolation(
                        standard="Documentation Standards",
                        file_path=str(relative_path),
                        line_number=func.lineno,
                        violation_type="missing_docstring",
                        violation_description=f"Public function '{func.name}' is missing docstring",
                        severity="MEDIUM",
                        remediation_suggestion=(
                            f"Add Google-style docstring to function '{func.name}'"
                        ),
                    )
                )
            else:
                # Check docstring format
                docstring = ast.get_docstring(func)
                if docstring:
                    violations.extend(self._check_docstring_format(docstring, func, relative_path))

        # Check public classes
        for cls in parser.get_public_classes():
            if not ast.get_docstring(cls):
                violations.append(
                    ComplianceViolation(
                        standard="Documentation Standards",
                        file_path=str(relative_path),
                        line_number=cls.lineno,
                        violation_type="missing_class_docstring",
                        violation_description=f"Public class '{cls.name}' is missing docstring",
                        severity="MEDIUM",
                        remediation_suggestion=f"Add Google-style docstring to class '{cls.name}'",
                    )
                )
            else:
                docstring = ast.get_docstring(cls)
                if docstring:
                    violations.extend(self._check_docstring_format(docstring, cls, relative_path))

        return violations

    def _check_docstring_format(
        self,
        docstring: str,
        node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
        relative_path: Path,
    ) -> list[ComplianceViolation]:
        """
        Check if docstring follows Google-style format.

        Args:
            docstring: Docstring content
            node: AST node (function or class)
            relative_path: Relative file path

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        # Check for Google-style sections
        has_args = "Args:" in docstring or "Arguments:" in docstring
        has_returns = "Returns:" in docstring or "Return:" in docstring

        # For functions, check if they have parameters/return values
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            has_params = len(node.args.args) > 0 and not all(
                arg.arg == "self" for arg in node.args.args
            )
            has_return = node.returns is not None

            if has_params and not has_args:
                violations.append(
                    ComplianceViolation(
                        standard="Documentation Standards",
                        file_path=str(relative_path),
                        line_number=node.lineno,
                        violation_type="missing_args_section",
                        violation_description=(
                            f"Function '{node.name}' has parameters but docstring "
                            "is missing Args section"
                        ),
                        severity="LOW",
                        remediation_suggestion=(
                            f"Add Args section to docstring for function '{node.name}'"
                        ),
                    )
                )

            if has_return and not has_returns:
                violations.append(
                    ComplianceViolation(
                        standard="Documentation Standards",
                        file_path=str(relative_path),
                        line_number=node.lineno,
                        violation_type="missing_returns_section",
                        violation_description=(
                            f"Function '{node.name}' has return type but docstring "
                            "is missing Returns section"
                        ),
                        severity="LOW",
                        remediation_suggestion=(
                            f"Add Returns section to docstring for function '{node.name}'"
                        ),
                    )
                )

        # Check for non-English content (simplified heuristic)
        # This is a basic check - full language detection would require NLP libraries
        non_english_patterns = [
            r"[А-Яа-я]",  # Cyrillic
            r"[一-龯]",  # Chinese
            r"[あ-ん]",  # Japanese Hiragana
        ]

        for pattern in non_english_patterns:
            if re.search(pattern, docstring):
                violations.append(
                    ComplianceViolation(
                        standard="Documentation Standards",
                        file_path=str(relative_path),
                        line_number=node.lineno,
                        violation_type="non_english_docstring",
                        violation_description=(
                            f"Docstring for '{node.name}' contains non-English content"
                        ),
                        severity="MEDIUM",
                        remediation_suggestion=(
                            f"Translate docstring to English for '{node.name}'"
                        ),
                    )
                )
                break

        return violations
