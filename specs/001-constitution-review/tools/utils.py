"""
Shared utilities for constitution compliance review.

This module provides common helper functions for file discovery, AST parsing,
and validation used across all checkers.
"""

import ast
from collections.abc import Iterator
from pathlib import Path


def discover_python_files(root_dir: str, exclude_dirs: set[str] | None = None) -> Iterator[Path]:
    """
    Discover all Python files in the given directory.

    Args:
        root_dir: Root directory to search
        exclude_dirs: Set of directory names to exclude (e.g., {'__pycache__', '.git'})

    Yields:
        Path objects for each Python file found
    """
    if exclude_dirs is None:
        exclude_dirs = {"__pycache__", ".git", ".venv", "venv", "node_modules", ".pytest_cache"}

    root_path = Path(root_dir)
    if not root_path.exists():
        return

    for py_file in root_path.rglob("*.py"):
        # Skip if any parent directory is in exclude list
        if any(part in exclude_dirs for part in py_file.parts):
            continue
        yield py_file


def parse_ast(file_path: Path) -> ast.Module | None:
    """
    Parse a Python file into an AST.

    Args:
        file_path: Path to the Python file

    Returns:
        AST Module node, or None if parsing fails
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        return ast.parse(content, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return None


def get_file_lines(file_path: Path, start_line: int, end_line: int | None = None) -> list[str]:
    """
    Get specific lines from a file.

    Args:
        file_path: Path to the file
        start_line: Starting line number (1-indexed)
        end_line: Ending line number (1-indexed, inclusive). If None, returns only start_line

    Returns:
        List of line strings
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
            if end_line is None:
                end_line = start_line
            # Convert to 0-indexed and clamp to valid range
            start_idx = max(0, start_line - 1)
            end_idx = min(len(lines), end_line)
            return [line.rstrip("\n") for line in lines[start_idx:end_idx]]
    except (OSError, UnicodeDecodeError):
        return []


def get_code_snippet(file_path: Path, line_number: int, context_lines: int = 3) -> str:
    """
    Get code snippet around a specific line with context.

    Args:
        file_path: Path to the file
        line_number: Line number to center on (1-indexed)
        context_lines: Number of lines before and after to include

    Returns:
        Code snippet as string
    """
    start_line = max(1, line_number - context_lines)
    end_line = line_number + context_lines
    lines = get_file_lines(file_path, start_line, end_line)
    return "\n".join(lines)


def is_public_api(name: str) -> bool:
    """
    Check if a name represents a public API (doesn't start with underscore).

    Args:
        name: Name to check

    Returns:
        True if name is public (doesn't start with _)
    """
    return not name.startswith("_")


def validate_file_path(file_path: str, project_root: Path) -> bool:
    """
    Validate that a file path exists and is within project root.

    Args:
        file_path: Relative file path to validate
        project_root: Project root directory

    Returns:
        True if path is valid and exists
    """
    try:
        full_path = project_root / file_path
        return full_path.exists() and full_path.is_file()
    except (OSError, ValueError):
        return False


def calculate_compliance_percentage(total_files: int, files_with_violations: int) -> float:
    """
    Calculate compliance percentage.

    Args:
        total_files: Total number of files checked
        files_with_violations: Number of files with violations

    Returns:
        Compliance percentage (0-100)
    """
    if total_files == 0:
        return 100.0
    compliant_files = total_files - files_with_violations
    return (compliant_files / total_files) * 100.0


def get_project_root() -> Path:
    """
    Get the project root directory (where pyproject.toml or .git is located).

    Returns:
        Path to project root
    """
    current = Path.cwd()
    while current != current.parent:
        if (current / "pyproject.toml").exists() or (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()
