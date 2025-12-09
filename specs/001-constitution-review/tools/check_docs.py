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

    def _check_function_docstring_sections(
        self,
        docstring: str,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        relative_path: Path,
    ) -> list[ComplianceViolation]:
        """
        Check if function docstring has required sections.

        Args:
            docstring: Docstring content
            node: Function AST node
            relative_path: Relative file path

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        has_args = "Args:" in docstring or "Arguments:" in docstring
        has_returns = "Returns:" in docstring or "Return:" in docstring
        has_raises = "Raises:" in docstring

        excluded_params = {"self", "cls"}
        has_params = any(arg.arg not in excluded_params for arg in node.args.args)

        # Check for return type annotation
        has_return_type_annotation = node.returns is not None

        # Check if function has return statements with values
        # (return without value is considered as returning None implicitly)
        has_return_stmt = any(
            isinstance(child, ast.Return) and child.value is not None for child in ast.walk(node)
        )

        # Function returns a value if it has return type annotation or return statements
        has_return = has_return_type_annotation or has_return_stmt

        # Check if function has raise statements
        has_raise_stmt = any(isinstance(child, ast.Raise) for child in ast.walk(node))

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
            # Determine violation description based on detection method
            if has_return_type_annotation and has_return_stmt:
                desc = (
                    f"Function '{node.name}' has return type annotation and return "
                    "statements but docstring is missing Returns section"
                )
            elif has_return_type_annotation:
                desc = (
                    f"Function '{node.name}' has return type annotation but docstring "
                    "is missing Returns section"
                )
            else:
                desc = (
                    f"Function '{node.name}' returns values but docstring "
                    "is missing Returns section"
                )

            violations.append(
                ComplianceViolation(
                    standard="Documentation Standards",
                    file_path=str(relative_path),
                    line_number=node.lineno,
                    violation_type="missing_returns_section",
                    violation_description=desc,
                    severity="LOW",
                    remediation_suggestion=(
                        f"Add Returns section to docstring for function '{node.name}'"
                    ),
                )
            )

        if has_raise_stmt and not has_raises:
            violations.append(
                ComplianceViolation(
                    standard="Documentation Standards",
                    file_path=str(relative_path),
                    line_number=node.lineno,
                    violation_type="missing_raises_section",
                    violation_description=(
                        f"Function '{node.name}' raises exceptions but docstring "
                        "is missing Raises section"
                    ),
                    severity="LOW",
                    remediation_suggestion=(
                        f"Add Raises section to docstring for function '{node.name}'"
                    ),
                )
            )

        return violations

    def _check_non_english_content(
        self,
        docstring: str,
        node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
        relative_path: Path,
    ) -> list[ComplianceViolation]:
        """
        Check for non-English content in docstring.

        Args:
            docstring: Docstring content
            node: AST node
            relative_path: Relative file path

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        non_english_patterns = [
            r"[А-Яа-я]",  # Cyrillic
            r"[\u4E00-\u9FFF]",  # CJK Unified Ideographs (broader)
            r"[あ-ん]",  # Japanese Hiragana
            r"[ア-ン]",  # Japanese Katakana
            r"[\uAC00-\uD7AF]",  # Korean Hangul
            r"[\u0600-\u06FF]",  # Arabic
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

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            violations.extend(
                self._check_function_docstring_sections(docstring, node, relative_path)
            )

        violations.extend(self._check_non_english_content(docstring, node, relative_path))

        return violations
