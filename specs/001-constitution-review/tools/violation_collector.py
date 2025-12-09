"""
Violation collector for aggregating compliance violations from all checkers.

This module provides functionality to collect, organize, and analyze violations
from multiple checkers.
"""

from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import ComplianceViolation


class ViolationCollector:
    """Collects and organizes compliance violations from multiple checkers."""

    def __init__(self) -> None:
        """Initialize the violation collector."""
        self.violations: list[ComplianceViolation] = []

    def add_violations(self, violations: list["ComplianceViolation"]) -> None:
        """
        Add violations to the collection.

        Args:
            violations: List of violations to add
        """
        self.violations.extend(violations)

    def get_violations_by_principle(self) -> dict[str, list["ComplianceViolation"]]:
        """
        Group violations by principle.

        Returns:
            Dictionary mapping principle names to lists of violations
        """
        grouped: dict[str, list[ComplianceViolation]] = defaultdict(list)
        for violation in self.violations:
            if violation.principle:
                grouped[violation.principle].append(violation)
        return dict(grouped)

    def get_violations_by_standard(self) -> dict[str, list["ComplianceViolation"]]:
        """
        Group violations by standard.

        Returns:
            Dictionary mapping standard names to lists of violations
        """
        grouped: dict[str, list[ComplianceViolation]] = defaultdict(list)
        for violation in self.violations:
            if violation.standard:
                grouped[violation.standard].append(violation)
        return dict(grouped)

    def get_violations_by_file(self) -> dict[str, list["ComplianceViolation"]]:
        """
        Group violations by file path.

        Returns:
            Dictionary mapping file paths to lists of violations
        """
        grouped: dict[str, list[ComplianceViolation]] = defaultdict(list)
        for violation in self.violations:
            grouped[violation.file_path].append(violation)
        return dict(grouped)

    def get_violations_by_severity(self) -> dict[str, list["ComplianceViolation"]]:
        """
        Group violations by severity level.

        Returns:
            Dictionary mapping severity levels to lists of violations
        """
        grouped: dict[str, list[ComplianceViolation]] = defaultdict(list)
        for violation in self.violations:
            grouped[violation.severity].append(violation)
        return dict(grouped)

    def get_violation_counts(self) -> dict[str, int | dict[str, int]]:
        """
        Get counts of violations by various categories.

        Returns:
            Dictionary with violation counts. Top level has 'total' (int) and
            category dicts (dict[str, int]) for by_principle, by_standard, etc.
        """
        by_principle = self.get_violations_by_principle()
        by_standard = self.get_violations_by_standard()
        by_file = self.get_violations_by_file()
        by_severity = self.get_violations_by_severity()

        return {
            "total": len(self.violations),
            "by_principle": {k: len(v) for k, v in by_principle.items()},
            "by_standard": {k: len(v) for k, v in by_standard.items()},
            "by_file": {k: len(v) for k, v in by_file.items()},
            "by_severity": {k: len(v) for k, v in by_severity.items()},
        }

    def get_files_with_violations(self) -> set[str]:
        """
        Get set of file paths that have violations.

        Returns:
            Set of file paths with violations
        """
        return {violation.file_path for violation in self.violations}

    def clear(self) -> None:
        """Clear all collected violations."""
        self.violations.clear()

    def get_total_count(self) -> int:
        """
        Get total number of violations.

        Returns:
            Total violation count
        """
        return len(self.violations)
