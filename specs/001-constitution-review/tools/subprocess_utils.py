"""
Utility functions for safe subprocess execution with proper encoding handling.

This module provides helper functions to run subprocess commands with UTF-8 encoding
and proper error handling, preventing UnicodeDecodeError on Windows.

The main issue on Windows is that subprocess.run() with text=True uses the system
default encoding (cp1251 on Russian Windows), which cannot decode UTF-8 characters.
This module ensures UTF-8 encoding is always used with proper error handling.
"""

import os
import subprocess
from pathlib import Path
from typing import Any


def run_subprocess_safe(
    cmd: list[str],
    *,
    cwd: Path | str | None = None,
    timeout: int | None = None,
    **kwargs: Any,
) -> subprocess.CompletedProcess[str]:
    """
    Run subprocess command with safe UTF-8 encoding.

    This function ensures that subprocess output is decoded using UTF-8,
    preventing UnicodeDecodeError on Windows where cp1251 is the default.

    The function:
    1. Explicitly sets encoding to UTF-8
    2. Uses errors="replace" to handle invalid UTF-8 sequences gracefully
    3. Sets environment variables to ensure UTF-8 output from child processes

    Args:
        cmd: Command to run as list of strings
        cwd: Working directory for the command
        timeout: Timeout in seconds
        **kwargs: Additional arguments to pass to subprocess.run

    Returns:
        CompletedProcess with decoded output

    Raises:
        subprocess.TimeoutExpired: If command times out
        subprocess.SubprocessError: For other subprocess errors
        FileNotFoundError: If command is not found
    """
    # Prepare environment with UTF-8 settings
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"  # Ensure Python subprocesses use UTF-8
    env["LC_ALL"] = "C.UTF-8"  # Set locale to UTF-8 (if supported)
    env["LANG"] = "C.UTF-8"  # Set language to UTF-8 (if supported)

    # Ensure encoding is UTF-8 with error handling
    subprocess_kwargs = {
        "capture_output": True,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",  # Replace invalid characters (U+FFFD) instead of raising error
        "timeout": timeout,
        "cwd": str(cwd) if cwd else None,
        "env": env,  # Pass environment with UTF-8 settings
        **kwargs,
    }

    # Remove None values (but keep env even if it's empty)
    subprocess_kwargs = {k: v for k, v in subprocess_kwargs.items() if v is not None or k == "env"}

    return subprocess.run(cmd, **subprocess_kwargs)
