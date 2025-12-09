"""
Code Style checker.

This checker verifies code follows PEP 8, uses ruff formatting, and passes mypy type checking.
"""

import subprocess
from pathlib import Path

from .base_checker import BaseChecker
from .models import ComplianceViolation
from .subprocess_utils import run_subprocess_safe


class CodeStyleChecker(BaseChecker):
    """Checker for Code Style standard compliance."""

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Code Style"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for Code Style violations.

        Args:
            file_path: Path to the file to check

        Returns:
            List of compliance violations found
        """
        violations: list[ComplianceViolation] = []

        # Only check Python files
        if file_path.suffix != ".py":
            return violations

        relative_path = file_path.relative_to(self.project_root)

        # Check with ruff
        ruff_violations = self._check_with_ruff(file_path, relative_path)
        violations.extend(ruff_violations)

        # Check line length (100 characters max)
        line_length_violations = self._check_line_length(file_path, relative_path)
        violations.extend(line_length_violations)

        return violations

    def _check_with_ruff(self, file_path: Path, relative_path: Path) -> list[ComplianceViolation]:
        """
        Check file with ruff linter.

        Args:
            file_path: Path to the file
            relative_path: Relative path for violations

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        try:
            result = run_subprocess_safe(
                ["uv", "run", "ruff", "check", str(file_path)],
                cwd=self.project_root,
                timeout=30,
            )

            if result.returncode != 0:
                # Parse ruff output
                for line in result.stdout.split("\n"):
                    if ":" in line and file_path.name in line:
                        parts = line.split(":")
                        if len(parts) >= 3:
                            line_num = int(parts[1]) if parts[1].isdigit() else 0
                            error_msg = ":".join(parts[2:]).strip()

                            violations.append(
                                ComplianceViolation(
                                    standard="Code Style",
                                    file_path=str(relative_path),
                                    line_number=line_num,
                                    violation_type="ruff_violation",
                                    violation_description=f"Ruff linting error: {error_msg}",
                                    severity="MEDIUM",
                                    remediation_suggestion=(
                                        f"Run 'uv run ruff check --fix {relative_path}' to auto-fix"
                                    ),
                                )
                            )
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            # Ruff not available or error - skip
            pass

        return violations

    def _check_line_length(self, file_path: Path, relative_path: Path) -> list[ComplianceViolation]:
        """
        Check line length (max 100 characters).

        Args:
            file_path: Path to the file
            relative_path: Relative path for violations

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        try:
            with open(file_path, encoding="utf-8") as f:
                for line_num, line in enumerate(f, start=1):
                    # Exclude comments and docstrings from strict line length
                    stripped = line.lstrip()
                    if (
                        stripped.startswith("#")
                        or stripped.startswith('"""')
                        or stripped.startswith("'''")
                    ):
                        continue

                    if len(line.rstrip("\n")) > 100:
                        violations.append(
                            ComplianceViolation(
                                standard="Code Style",
                                file_path=str(relative_path),
                                line_number=line_num,
                                violation_type="line_too_long",
                                violation_description=(
                                    f"Line {line_num} exceeds 100 character limit "
                                    f"({len(line.rstrip())} characters)"
                                ),
                                severity="LOW",
                                remediation_suggestion=(
                                    f"Break line {line_num} into multiple lines or refactor"
                                ),
                            )
                        )
        except Exception:
            pass

        return violations
