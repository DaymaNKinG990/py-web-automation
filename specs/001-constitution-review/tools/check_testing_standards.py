"""
Testing Standards checker.

This checker verifies testing standards compliance:
- Test decorators (allure.feature, allure.story, allure.title, "
        "allure.testcase, allure.severity, allure.description, pytest.mark)
- allure.step() usage
- Parametrization of identical test algorithms
"""

from pathlib import Path

from .check_tests import TestFirstChecker
from .models import ComplianceViolation


class TestingStandardsChecker(TestFirstChecker):
    """Checker for Testing Standards compliance."""

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Testing Standards"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a test file for Testing Standards violations.

        Args:
            file_path: Path to the test file to check

        Returns:
            List of compliance violations found (only Testing Standards, not Test-First)
        """
        # Get all violations from parent class
        all_violations = super().check(file_path)

        # Filter to only Testing Standards violations (not Test-First principle)
        testing_standards_violations = [
            v for v in all_violations if v.standard == "Testing Standards"
        ]

        return testing_standards_violations
