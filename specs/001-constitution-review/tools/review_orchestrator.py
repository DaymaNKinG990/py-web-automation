"""
Review orchestrator for coordinating all checkers and generating reports.

This module provides the main orchestration logic that coordinates all
principle and standard checkers and generates compliance reports.
"""

import time
from pathlib import Path
from typing import TYPE_CHECKING

# Import principle checkers
from .check_async import AsyncFirstChecker

# Import standard checkers
from .check_code_style import CodeStyleChecker
from .check_docs import DocumentationChecker
from .check_error_handling import ErrorHandlingChecker
from .check_git import GitWorkflowChecker
from .check_imports import ImportOrganizationChecker
from .check_package_mgmt import PackageManagementChecker
from .check_performance import PerformanceChecker
from .check_resources import ResourceManagementChecker
from .check_separation import SeparationChecker
from .check_solid import SOLIDChecker
from .check_testing_standards import TestingStandardsChecker
from .check_tests import TestFirstChecker
from .check_types import TypeSafetyChecker
from .config import ReviewConfig
from .file_discovery import FileDiscoveryService
from .violation_collector import ViolationCollector

if TYPE_CHECKING:
    from .base_checker import BaseChecker
    from .models import ComplianceReport


class ReviewOrchestrator:
    """Orchestrates the entire constitution compliance review process."""

    def __init__(self, project_root: Path | None = None) -> None:
        """
        Initialize the review orchestrator.

        Args:
            project_root: Root directory of the project. If None, uses ReviewConfig.PROJECT_ROOT.
        """
        self.project_root = project_root or ReviewConfig.PROJECT_ROOT
        self.file_discovery = FileDiscoveryService(self.project_root)
        self.violation_collector = ViolationCollector()
        self.principle_checkers: list[BaseChecker] = []
        self.standard_checkers: list[BaseChecker] = []

        # Auto-register all principle checkers
        self._register_default_checkers()

    def register_principle_checker(self, checker: "BaseChecker") -> None:
        """
        Register a principle checker.

        Args:
            checker: Checker instance to register
        """
        self.principle_checkers.append(checker)

    def register_standard_checker(self, checker: "BaseChecker") -> None:
        """
        Register a standard checker.

        Args:
            checker: Checker instance to register
        """
        self.standard_checkers.append(checker)

    def _register_default_checkers(self) -> None:
        """Register all default principle and standard checkers."""
        # Register principle checkers
        self.register_principle_checker(AsyncFirstChecker(self.project_root))
        self.register_principle_checker(TypeSafetyChecker(self.project_root))
        self.register_principle_checker(TestFirstChecker(self.project_root))
        self.register_principle_checker(SOLIDChecker(self.project_root))
        self.register_principle_checker(PerformanceChecker(self.project_root))
        self.register_principle_checker(PackageManagementChecker(self.project_root))
        self.register_principle_checker(DocumentationChecker(self.project_root))

        # Register standard checkers
        self.register_standard_checker(CodeStyleChecker(self.project_root))
        self.register_standard_checker(ErrorHandlingChecker(self.project_root))
        self.register_standard_checker(ResourceManagementChecker(self.project_root))
        self.register_standard_checker(SeparationChecker(self.project_root))
        self.register_standard_checker(TestingStandardsChecker(self.project_root))
        self.register_standard_checker(ImportOrganizationChecker(self.project_root))
        self.register_standard_checker(GitWorkflowChecker(self.project_root))

    def run_review(self) -> "ComplianceReport":
        """
        Run the complete compliance review.

        Returns:
            ComplianceReport with all findings
        """
        from .models import PrincipleCheck, StandardCheck
        from .utils import calculate_compliance_percentage

        self.violation_collector.clear()

        # Discover all files
        source_files = self.file_discovery.discover_source_files()
        test_files = self.file_discovery.discover_test_files()
        all_files = source_files + test_files

        # Run principle checkers
        principle_checks: list[PrincipleCheck] = []
        for checker in self.principle_checkers:
            check_start = time.time()
            violations = checker.check_multiple_files(all_files)
            check_duration = time.time() - check_start

            files_with_violations = {v.file_path for v in violations}
            compliance_pct = calculate_compliance_percentage(
                len(all_files), len(files_with_violations)
            )

            check_status = (
                "PASS" if len(violations) == 0 else ("PARTIAL" if compliance_pct >= 80 else "FAIL")
            )

            principle_check = PrincipleCheck(
                principle_name=checker.get_name(),
                check_status=check_status,
                violations_found=len(violations),
                files_checked=len(all_files),
                files_with_violations=len(files_with_violations),
                compliance_percentage=compliance_pct,
                check_duration_seconds=check_duration,
                violations=violations,
            )
            principle_checks.append(principle_check)
            self.violation_collector.add_violations(violations)

        # Run standard checkers
        standard_checks: list[StandardCheck] = []
        for checker in self.standard_checkers:
            check_start = time.time()
            violations = checker.check_multiple_files(all_files)
            check_duration = time.time() - check_start

            files_with_violations = {v.file_path for v in violations}
            compliance_pct = calculate_compliance_percentage(
                len(all_files), len(files_with_violations)
            )

            check_status = (
                "PASS" if len(violations) == 0 else ("PARTIAL" if compliance_pct >= 80 else "FAIL")
            )

            standard_check = StandardCheck(
                standard_name=checker.get_name(),
                check_status=check_status,
                violations_found=len(violations),
                files_checked=len(all_files),
                files_with_violations=len(files_with_violations),
                compliance_percentage=compliance_pct,
                check_duration_seconds=check_duration,
                violations=violations,
            )
            standard_checks.append(standard_check)
            self.violation_collector.add_violations(violations)

        # Build compliance report
        all_violations = self.violation_collector.violations
        counts = self.violation_collector.get_violation_counts()

        total_files = len(all_files)
        files_with_violations_set = self.violation_collector.get_files_with_violations()
        files_with_violations_count = len(files_with_violations_set)
        overall_compliance = calculate_compliance_percentage(
            total_files, files_with_violations_count
        )

        # Extract typed counts (type narrowing)
        by_severity = counts["by_severity"]
        assert isinstance(by_severity, dict)  # noqa: S101

        # Generate summary
        self._generate_summary(
            total_files,
            len(all_violations),
            overall_compliance,
            by_severity,
        )

        # Use generate_report module for consistency
        from .generate_report import generate_report

        report = generate_report(
            violations=all_violations,
            principle_checks=principle_checks,
            standard_checks=standard_checks,
            total_files=total_files,
        )

        return report

    def _generate_summary(
        self,
        total_files: int,
        total_violations: int,
        compliance_percentage: float,
        violations_by_severity: dict[str, int],
    ) -> str:
        """
        Generate executive summary of the review.

        Args:
            total_files: Total number of files analyzed
            total_violations: Total number of violations found
            compliance_percentage: Overall compliance percentage
            violations_by_severity: Violations grouped by severity

        Returns:
            Summary text
        """
        summary_lines = [
            "Constitution Compliance Review Summary",
            "",
            f"Files Analyzed: {total_files}",
            f"Total Violations: {total_violations}",
            f"Overall Compliance: {compliance_percentage:.1f}%",
            "",
            "Violations by Severity:",
        ]

        for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            count = violations_by_severity.get(severity, 0)
            summary_lines.append(f"  {severity}: {count}")

        if total_violations == 0:
            summary_lines.append("")
            summary_lines.append(
                "✓ No violations found. Project is fully compliant with the constitution."
            )

        return "\n".join(summary_lines)
