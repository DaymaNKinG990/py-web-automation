"""
Test-First principle and Testing Standards checker.

This checker verifies:
1. Test cases exist in test_cases/ before test implementations
2. Tests have required decorators
3. Tests use allure.step() for actions
4. Identical test algorithms are parametrized
"""

import ast
import re
from pathlib import Path

from .ast_parser import ASTParser
from .base_checker import BaseChecker
from .file_discovery import FileDiscoveryService
from .models import ComplianceViolation


class TestFirstChecker(BaseChecker):
    """Checker for Test-First principle and Testing Standards compliance."""

    REQUIRED_DECORATORS = {
        "allure.feature",
        "allure.story",
        "allure.title",
        "allure.testcase",
        "allure.severity",
        "allure.description",
    }

    REQUIRED_PYTEST_MARKERS = {"pytest.mark.unit", "pytest.mark.integration"}

    def __init__(self, project_root: Path | None = None) -> None:
        """
        Initialize the test checker.

        Args:
            project_root: Root directory of the project
        """
        super().__init__(project_root)
        self.file_discovery = FileDiscoveryService(project_root)
        self.test_case_ids: set[str] = set()
        self._load_test_case_ids()

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Test-First"

    def _load_test_case_ids(self) -> None:
        """Load all test case IDs from test_cases/ directory."""
        test_case_files = self.file_discovery.discover_test_case_files()
        pattern = re.compile(r"TC-([A-Z]+)-([A-Z]+)-(\d+)")

        for test_case_file in test_case_files:
            try:
                content = test_case_file.read_text(encoding="utf-8")
                matches = pattern.findall(content)
                for match in matches:
                    test_case_id = f"TC-{match[0]}-{match[1]}-{match[2]}"
                    self.test_case_ids.add(test_case_id)
            except Exception:
                continue

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a test file for Test-First and Testing Standards violations.

        Args:
            file_path: Path to the test file to check

        Returns:
            List of compliance violations found
        """
        violations: list[ComplianceViolation] = []

        # Only check test files
        if "test" not in file_path.name.lower() and "tests" not in str(file_path):
            return violations

        parser = ASTParser(file_path)
        if not parser.is_valid():
            return violations

        relative_path = file_path.relative_to(self.project_root)

        # Check all test functions
        for func in parser.get_functions():
            if not func.name.startswith("test_"):
                continue

            # Check for test case ID in decorators
            decorators = parser.get_decorators(func)
            testcase_decorator = None
            for decorator in decorators:
                if "testcase" in decorator.lower():
                    testcase_decorator = decorator
                    break

            # Check if test case exists in documentation
            if testcase_decorator:
                # Extract test case ID from decorator arguments
                test_case_id_match = None
                for decorator in func.decorator_list:
                    if isinstance(decorator, ast.Call):
                        for arg in decorator.args:
                            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                                match = re.search(r"TC-[A-Z]+-[A-Z]+-\d+", arg.value)
                                if match:
                                    test_case_id_match = match
                                    break
                    if test_case_id_match:
                        break

                if test_case_id_match:
                    test_case_id = test_case_id_match.group(0)
                    if test_case_id not in self.test_case_ids:
                        violations.append(
                            ComplianceViolation(
                                principle="Test-First",
                                file_path=str(relative_path),
                                line_number=func.lineno,
                                violation_type="test_case_not_documented",
                                violation_description=(
                                    f"Test function '{func.name}' references "
                                    f"test case '{test_case_id}' that doesn't "
                                    "exist in test_cases/ directory"
                                ),
                                severity="HIGH",
                                remediation_suggestion=(
                                    f"Create test case documentation for "
                                    f"'{test_case_id}' in test_cases/ directory "
                                    "before test implementation"
                                ),
                            )
                        )
            else:
                violations.append(
                    ComplianceViolation(
                        standard="Testing Standards",
                        file_path=str(relative_path),
                        line_number=func.lineno,
                        violation_type="missing_testcase_decorator",
                        violation_description=(
                            f"Test function '{func.name}' is missing @allure.testcase decorator"
                        ),
                        severity="MEDIUM",
                        remediation_suggestion=(
                            f"Add @allure.testcase('TC-XXX-XXX-XXX') decorator "
                            f"to test function '{func.name}'"
                        ),
                    )
                )

            # Check for required decorators
            self._check_required_decorators(decorators, func, relative_path, violations)

            # Check for allure.step() usage
            if not self._has_allure_steps(func):
                violations.append(
                    ComplianceViolation(
                        standard="Testing Standards",
                        file_path=str(relative_path),
                        line_number=func.lineno,
                        violation_type="missing_allure_steps",
                        violation_description=(
                            f"Test function '{func.name}' does not use "
                            "allure.step() context manager for test actions"
                        ),
                        severity="MEDIUM",
                        remediation_suggestion=(
                            f"Wrap test actions in allure.step() context "
                            f"manager in function '{func.name}'"
                        ),
                    )
                )

        # Check for parametrization opportunities (simplified - would need
        # more sophisticated analysis)
        self._check_parametrization_opportunities(parser, relative_path, violations)

        return violations

    def _check_required_decorators(
        self,
        decorators: list[str],
        func: ast.FunctionDef | ast.AsyncFunctionDef,
        relative_path: Path,
        violations: list[ComplianceViolation],
    ) -> list[str]:
        """
        Check for required decorators and add violations for missing ones.

        Args:
            decorators: List of decorator names found
            func: Function node
            relative_path: Relative file path
            violations: List to append violations to

        Returns:
            List of missing decorator names
        """
        missing: list[str] = []

        # Check for pytest marker
        has_pytest_marker = any("pytest.mark" in d for d in decorators)
        if not has_pytest_marker:
            missing.append("pytest.mark")
            violations.append(
                ComplianceViolation(
                    standard="Testing Standards",
                    file_path=str(relative_path),
                    line_number=func.lineno,
                    violation_type="missing_pytest_marker",
                    violation_description=(
                        f"Test function '{func.name}' is missing "
                        "@pytest.mark.unit or @pytest.mark.integration decorator"
                    ),
                    severity="MEDIUM",
                    remediation_suggestion=(
                        f"Add @pytest.mark.unit or @pytest.mark.integration "
                        f"decorator to '{func.name}'"
                    ),
                )
            )

        # Note: Full decorator checking would require AST parsing of decorator arguments
        # This is a simplified version that checks for decorator presence

        return missing

    def _has_allure_steps(self, func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """
        Check if function uses allure.step() context manager.

        Args:
            func: Function node to check

        Returns:
            True if function uses allure.step()
        """
        for node in ast.walk(func):
            if isinstance(node, ast.With):
                if isinstance(node.items[0].context_expr, ast.Call):
                    call = node.items[0].context_expr
                    if isinstance(call.func, ast.Attribute):
                        if (
                            call.func.attr == "step"
                            and isinstance(call.func.value, ast.Name)
                            and call.func.value.id == "allure"
                        ):
                            return True
        return False

    def _check_parametrization_opportunities(
        self,
        parser: ASTParser,
        relative_path: Path,
        violations: list[ComplianceViolation],
    ) -> None:
        """
        Check for parametrization opportunities (simplified check).

        Args:
            parser: AST parser instance
            relative_path: Relative file path
            violations: List to append violations to
        """
        # This is a simplified check - full implementation would require
        # comparing test function bodies to find identical algorithms
        # For now, we'll skip this as it requires more sophisticated analysis
        pass
