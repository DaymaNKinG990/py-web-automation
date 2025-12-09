#!/usr/bin/env python3
"""
Entry point script for constitution compliance review.

This script allows running the review tool from project root.

Usage:
    uv run python specs/001-constitution-review/run_review.py
    uv run python specs/001-constitution-review/run_review.py --verbose
"""

import os
import sys
from pathlib import Path

# Change to the directory containing this script so relative imports work
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent.parent))  # Add project root

# Change working directory to script directory
original_cwd = os.getcwd()
os.chdir(script_dir)

try:
    # Now import as module
    from tools import main
finally:
    # Restore original working directory
    os.chdir(original_cwd)


if __name__ == "__main__":
    sys.exit(main())
