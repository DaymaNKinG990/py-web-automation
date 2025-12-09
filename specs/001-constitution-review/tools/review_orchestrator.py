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
        total_files = len(all_files)

        # Use generate_report module for consistency
        # Note: generate_report() internally generates the summary,
        # so we don't need to call self._generate_summary() separately
        from .generate_report import generate_report

        report = generate_report(
            violations=all_violations,
            principle_checks=principle_checks,
            standard_checks=standard_checks,
            total_files=total_files,
        )

        return report
