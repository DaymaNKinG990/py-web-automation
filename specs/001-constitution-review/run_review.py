#!/usr/bin/env python3
"""
Entry point script for constitution compliance review.

This script allows running the review tool from project root.

Usage:
    uv run python specs/001-constitution-review/run_review.py
    uv run python specs/001-constitution-review/run_review.py --verbose
"""

import sys
from pathlib import Path

# Add project root to sys.path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent.parent))

# Import main function directly from tools package
# ReviewConfig uses absolute paths, so working directory change is not needed
from tools import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
