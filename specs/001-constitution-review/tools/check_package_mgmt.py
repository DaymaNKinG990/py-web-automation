"""
Package Management checker.

This checker verifies that the project uses uv exclusively (no pip/uv pip).
"""

import re
from pathlib import Path

from .base_checker import BaseChecker
from .models import ComplianceViolation


class PackageManagementChecker(BaseChecker):
    """Checker for Package Management principle compliance."""

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Package Management"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check project files for Package Management violations.

        Args:
            file_path: Path to the file to check (can be any project file)

        Returns:
            List of compliance violations found
        """
        violations: list[ComplianceViolation] = []

        # Only check specific file types
        if file_path.suffix not in (".md", ".yaml", ".yml", ".toml", ".txt", ".sh", ".ps1", ".bat"):
            return violations

        relative_path = file_path.relative_to(self.project_root)

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return violations

        # Check for pip usage
        pip_patterns = [
            (r"pip\s+install", "pip install command"),
            (r"pip\s+sync", "pip sync command"),
            (r"uv\s+pip", "uv pip command"),
            (r"python\s+-m\s+pip", "python -m pip command"),
        ]

        for pattern, description in pip_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_number = content[: match.start()].count("\n") + 1
                violations.append(
                    ComplianceViolation(
                        principle="Package Management",
                        file_path=str(relative_path),
                        line_number=line_number,
                        violation_type="pip_usage",
                        violation_description=(
                            f"File contains {description}, but constitution requires uv exclusively"
                        ),
                        severity="HIGH",
                        remediation_suggestion=(
                            f"Replace {description} with equivalent uv command "
                            "(e.g., 'uv add', 'uv sync')"
                        ),
                    )
                )

        # Check for requirements.txt (should use pyproject.toml with uv)
        if file_path.name == "requirements.txt":
            violations.append(
                ComplianceViolation(
                    principle="Package Management",
                    file_path=str(relative_path),
                    line_number=0,
                    violation_type="requirements_txt_exists",
                    violation_description=(
                        "requirements.txt file exists, but uv uses pyproject.toml for dependencies"
                    ),
                    severity="MEDIUM",
                    remediation_suggestion=(
                        "Remove requirements.txt and use pyproject.toml with uv "
                        "for dependency management"
                    ),
                )
            )

        return violations
