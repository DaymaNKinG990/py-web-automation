"""
Configuration module for constitution compliance review.

This module provides configuration settings and paths for the review process.
"""

from pathlib import Path
from typing import Final


class ReviewConfig:
    """Configuration for constitution compliance review."""

    # Project paths
    PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.parent.parent
    SOURCE_DIR: Final[Path] = PROJECT_ROOT / "py_web_automation"
    TESTS_DIR: Final[Path] = PROJECT_ROOT / "tests"
    TEST_CASES_DIR: Final[Path] = PROJECT_ROOT / "test_cases"
    DOCS_DIR: Final[Path] = PROJECT_ROOT / "docs"
    EXAMPLES_DIR: Final[Path] = PROJECT_ROOT / "examples"

    # Review tool paths
    TOOLS_DIR: Final[Path] = Path(__file__).parent
    REPORTS_DIR: Final[Path] = TOOLS_DIR.parent / "reports"

    # File patterns
    PYTHON_FILES: Final[str] = "*.py"
    MARKDOWN_FILES: Final[str] = "*.md"
    YAML_FILES: Final[str] = "*.yaml"
    YML_FILES: Final[str] = "*.yml"

    # Exclude directories
    EXCLUDE_DIRS: Final[set[str]] = {
        "__pycache__",
        ".git",
        ".venv",
        "venv",
        "node_modules",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "dist",
        "build",
        ".eggs",
        "*.egg-info",
        "report",
        "allure-results",
        "allure-report",
    }

    # Test coverage threshold
    COVERAGE_THRESHOLD: Final[float] = 80.0

    # Report settings
    REPORT_TIMEOUT_SECONDS: Final[int] = 1800  # 30 minutes

    # Severity levels
    SEVERITY_LEVELS: Final[tuple[str, ...]] = ("CRITICAL", "HIGH", "MEDIUM", "LOW")

    # Principle names
    PRINCIPLES: Final[tuple[str, ...]] = (
        "Async-First",
        "Type Safety",
        "Test-First",
        "SOLID Principles",
        "Performance Optimization",
        "Package Management",
        "Documentation Standards",
    )

    # Standard names
    STANDARDS: Final[tuple[str, ...]] = (
        "Code Style",
        "Error Handling",
        "Resource Management",
        "Separation of Concerns",
        "Testing Standards",
        "Import Organization",
        "Git Workflow",
    )

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
