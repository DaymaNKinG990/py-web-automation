"""
Separation of Concerns checker.

This checker verifies proper separation of client types and module organization.
"""

from pathlib import Path
from typing import ClassVar

from .base_checker import BaseChecker
from .models import ComplianceViolation


class SeparationChecker(BaseChecker):
    """Checker for Separation of Concerns standard compliance."""

    CLIENT_TYPES: ClassVar[set[str]] = {
        "http",
        "graphql",
        "grpc",
        "soap",
        "websocket",
        "ui",
        "db",
        "broker",
    }

    def get_name(self) -> str:
        """Get the name of this checker."""
        return "Separation of Concerns"

    def check(self, file_path: Path) -> list[ComplianceViolation]:
        """
        Check a file for Separation of Concerns violations.

        Args:
            file_path: Path to the file to check

        Returns:
            List of compliance violations found
        """
        violations: list[ComplianceViolation] = []

        # Check module organization
        relative_path = file_path.relative_to(self.project_root)
        path_str = str(relative_path).lower()

        # Check if file is in correct directory based on client type
        # This is a simplified check - full implementation would analyze imports and class types
        if "client" in path_str:
            # Verify file is in appropriate subdirectory
            if "api_clients" in path_str:
                # Should be in specific client subdirectory
                # Use CLIENT_TYPES constant to check all declared client types
                if not any(client_type in path_str for client_type in self.CLIENT_TYPES):
                    violations.append(
                        ComplianceViolation(
                            standard="Separation of Concerns",
                            file_path=str(relative_path),
                            line_number=0,
                            violation_type="incorrect_module_location",
                            violation_description=(
                                "Client file is not in appropriate subdirectory "
                                "based on client type"
                            ),
                            severity="LOW",
                            remediation_suggestion=(
                                "Move file to appropriate client type subdirectory"
                            ),
                        )
                    )

        return violations
