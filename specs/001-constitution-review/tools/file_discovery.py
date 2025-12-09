"""
File discovery service for constitution compliance review.

This module provides functionality to discover and filter Python files
in the project for analysis.
"""

from pathlib import Path

from .config import ReviewConfig
from .utils import discover_python_files


class FileDiscoveryService:
    """Service for discovering Python files in the project."""

    def __init__(self, project_root: Path | None = None) -> None:
        """
        Initialize the file discovery service.

        Args:
            project_root: Root directory of the project. If None, uses ReviewConfig.PROJECT_ROOT.
        """
        self.project_root = project_root or ReviewConfig.PROJECT_ROOT

    def discover_source_files(self) -> list[Path]:
        """
        Discover all Python source files in py_web_automation/ directory.

        Returns:
            List of Path objects for source files
        """
        source_dir = self.project_root / ReviewConfig.SOURCE_DIR.name
        if not source_dir.exists():
            return []
        return list(discover_python_files(str(source_dir), ReviewConfig.EXCLUDE_DIRS))

    def discover_test_files(self) -> list[Path]:
        """
        Discover all Python test files in tests/ directory.

        Returns:
            List of Path objects for test files
        """
        tests_dir = self.project_root / ReviewConfig.TESTS_DIR.name
        if not tests_dir.exists():
            return []
        return list(discover_python_files(str(tests_dir), ReviewConfig.EXCLUDE_DIRS))

    def discover_all_python_files(self) -> list[Path]:
        """
        Discover all Python files in both source and test directories.

        Returns:
            List of Path objects for all Python files
        """
        source_files = self.discover_source_files()
        test_files = self.discover_test_files()
        return source_files + test_files

    def discover_test_case_files(self) -> list[Path]:
        """
        Discover all test case documentation files in test_cases/ directory.

        Returns:
            List of Path objects for test case markdown files
        """
        test_cases_dir = self.project_root / "test_cases"
        if not test_cases_dir.exists():
            return []

        markdown_files: list[Path] = []
        for md_file in test_cases_dir.rglob("*.md"):
            # Skip README and SUMMARY files
            if md_file.name in ("README.md", "SUMMARY.md", "MISSING_INTEGRATION_TEST_CASES.md"):
                continue
            markdown_files.append(md_file)

        return markdown_files

    def discover_documentation_files(self) -> list[Path]:
        """
        Discover all documentation files in docs/ directory.

        Returns:
            List of Path objects for documentation markdown files
        """
        docs_dir = self.project_root / ReviewConfig.DOCS_DIR.name
        if not docs_dir.exists():
            return []

        return list(docs_dir.rglob("*.md"))

    def get_file_count(self) -> dict[str, int]:
        """
        Get count of files by category.

        Returns:
            Dictionary with file counts by category
        """
        return {
            "source_files": len(self.discover_source_files()),
            "test_files": len(self.discover_test_files()),
            "test_case_files": len(self.discover_test_case_files()),
            "documentation_files": len(self.discover_documentation_files()),
            "total_python_files": len(self.discover_all_python_files()),
        }
