"""
Base checker abstract class for constitution compliance review.

This module provides the common interface that all principle and standard checkers must implement.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import ComplianceViolation


class BaseChecker(ABC):
    """
    Abstract base class for all constitution compliance checkers.

    All principle and standard checkers must inherit from this class and implement
    the required methods.
    """

    def __init__(self, project_root: Path | None = None) -> None:
        """
        Initialize the checker.

        Args:
            project_root: Root directory of the project. If None, will be auto-detected.
        """
        from .utils import get_project_root

        self.project_root = project_root or get_project_root()

    @abstractmethod
    def check(self, file_path: Path) -> list["ComplianceViolation"]:
        """
        Check a single file for compliance violations.

        Args:
            file_path: Path to the file to check

        Returns:
            List of compliance violations found in the file
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this checker (principle or standard name).

        Returns:
            Name of the principle or standard being checked
        """
        pass

    def check_multiple_files(self, file_paths: list[Path]) -> list["ComplianceViolation"]:
        """
        Check multiple files for compliance violations.

        Args:
            file_paths: List of file paths to check

        Returns:
            List of all compliance violations found
        """
        violations: list[ComplianceViolation] = []
        for file_path in file_paths:
            try:
                violations.extend(self.check(file_path))
            except Exception as e:
                # Log error but continue with other files
                violation = self._create_error_violation(file_path, str(e))
                violations.append(violation)
        return violations

    def _create_error_violation(self, file_path: Path, error_message: str) -> "ComplianceViolation":
        """
        Create a violation representing a checker error.

        Args:
            file_path: Path to the file that caused the error
            error_message: Error message

        Returns:
            ComplianceViolation representing the error
        """
        from .models import ComplianceViolation

        return ComplianceViolation(
            principle=self.get_name() if self._is_principle_checker() else None,
            standard=self.get_name() if not self._is_principle_checker() else None,
            file_path=str(file_path.relative_to(self.project_root)),
            line_number=0,
            violation_type="checker_error",
            violation_description=f"Error during check: {error_message}",
            severity="HIGH",
            remediation_suggestion="Review checker implementation and file content",
        )

    def _is_principle_checker(self) -> bool:
        """
        Determine if this is a principle checker or standard checker.

        Returns:
            True if principle checker, False if standard checker
        """
        from .config import ReviewConfig

        return self.get_name() in ReviewConfig.PRINCIPLES
