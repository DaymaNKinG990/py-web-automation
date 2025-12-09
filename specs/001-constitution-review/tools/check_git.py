"""
Git Workflow checker.

This checker verifies branching strategy and commit frequency compliance.
"""

import re
import subprocess
from pathlib import Path

from .base_checker import BaseChecker
from .models import ComplianceViolation
from .subprocess_utils import run_subprocess_safe


class GitWorkflowChecker(BaseChecker):
    """Checker for Git Workflow standard compliance."""

    CONVENTIONAL_COMMIT_TYPES = {
        "feat",
        "fix",
        "docs",
        "test",
        "refactor",
        "perf",
        "chore",
        "style",
    }

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Git Workflow"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check git workflow compliance.

        Note: This checker analyzes git history, not individual files.
        It should be called once per review, not per file.

        Args:
            file_path: Path parameter (not used for git checks)

        Returns:
            List of compliance violations found
        """
        violations: list[ComplianceViolation] = []

        # Check branch naming
        violations.extend(self._check_branch_naming())

        # Check commit messages
        violations.extend(self._check_commit_messages())

        return violations

    def _check_branch_naming(self) -> list[ComplianceViolation]:
        """
        Check branch naming convention.

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        try:
            result = run_subprocess_safe(
                ["git", "branch", "--show-current"],
                cwd=self.project_root,
                timeout=5,
            )

            if result.returncode == 0:
                current_branch = result.stdout.strip()
                if current_branch and current_branch != "master" and current_branch != "main":
                    # Check if branch follows naming convention
                    if not re.match(
                        r"^\d+-[a-z-]+$", current_branch
                    ) and not current_branch.startswith("feature/"):
                        violations.append(
                            ComplianceViolation(
                                standard="Git Workflow",
                                file_path=".git",
                                line_number=0,
                                violation_type="invalid_branch_name",
                                violation_description=(
                                    f"Branch '{current_branch}' does not follow "
                                    "naming convention (should be 'feature/name' "
                                    "or '###-name')"
                                ),
                                severity="LOW",
                                remediation_suggestion=(
                                    "Rename branch to follow convention: "
                                    "'feature/name' or '###-name'"
                                ),
                            )
                        )
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            # Git not available - skip
            pass

        return violations

    def _check_commit_messages(self) -> list[ComplianceViolation]:
        """
        Check commit message format (conventional commits).

        Returns:
            List of violations
        """
        violations: list[ComplianceViolation] = []

        try:
            # Get last 20 commits
            result = run_subprocess_safe(
                ["git", "log", "--oneline", "-20"],
                cwd=self.project_root,
                timeout=5,
            )

            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if not line.strip():
                        continue

                    # Extract commit message (after hash)
                    parts = line.split(" ", 1)
                    if len(parts) < 2:
                        continue

                    commit_msg = parts[1]
                    # Check conventional commit format
                    if not any(
                        commit_msg.startswith(f"{ctype}:")
                        for ctype in self.CONVENTIONAL_COMMIT_TYPES
                    ):
                        violations.append(
                            ComplianceViolation(
                                standard="Git Workflow",
                                file_path=".git",
                                line_number=0,
                                violation_type="invalid_commit_message",
                                violation_description=(
                                    f"Commit message does not follow conventional "
                                    f"commit format: '{commit_msg[:50]}...'"
                                ),
                                severity="LOW",
                                remediation_suggestion=(
                                    "Use conventional commit format: "
                                    "'type: description' (e.g., 'feat: add feature', "
                                    "'fix: fix bug')"
                                ),
                            )
                        )
                        # Limit to first violation to avoid spam
                        break
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            # Git not available - skip
            pass

        return violations
