"""
Command-line interface for constitution compliance review.

This module provides a CLI to run the complete compliance review and generate reports.

Usage:
    # Option 1: From project root using wrapper script
    uv run python specs/001-constitution-review/run_review.py

    # Option 2: From review directory
    cd specs/001-constitution-review
    uv run python -m tools

    # With options:
    uv run python specs/001-constitution-review/run_review.py --verbose
    uv run python specs/001-constitution-review/run_review.py --output-dir ./reports
"""

import argparse
import sys
from pathlib import Path

from .config import ReviewConfig
from .generate_report import save_report
from .review_orchestrator import ReviewOrchestrator


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = argparse.ArgumentParser(
        description=(
            "Constitution Compliance Review - "
            "Analyze codebase for compliance with project constitution"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full review
  uv run python -m specs.001_constitution_review.tools

  # Run with custom output directory
  uv run python -m specs.001_constitution_review.tools --output-dir ./custom_reports
        """,
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        help="Directory to save reports (default: specs/001-constitution-review/reports/)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    print("Constitution Compliance Review")
    print("=" * 50)
    print()

    try:
        # Initialize orchestrator
        if args.verbose:
            print("Initializing review orchestrator...")

        orchestrator = ReviewOrchestrator()

        # Discover files
        file_discovery = orchestrator.file_discovery
        source_files = file_discovery.discover_source_files()
        test_files = file_discovery.discover_test_files()

        if args.verbose:
            print(f"Discovered {len(source_files)} source files")
            print(f"Discovered {len(test_files)} test files")
            print(f"Registered {len(orchestrator.principle_checkers)} principle checkers")
            print(f"Registered {len(orchestrator.standard_checkers)} standard checkers")
            print()

        print("Running compliance review...")
        print("This may take a few minutes...")
        print()

        # Run review
        report = orchestrator.run_review()

        # Determine output directory
        output_dir = Path(args.output_dir) if args.output_dir else ReviewConfig.REPORTS_DIR

        # Save reports
        print("Generating reports...")
        saved_files = save_report(report, output_dir)

        print()
        print("=" * 50)
        print("Review Complete!")
        print("=" * 50)
        print()
        print("Reports generated:")
        for format_name, file_path in saved_files.items():
            print(f"  {format_name:15}: {file_path}")

        print()
        print("Summary:")
        print(f"  Files Analyzed: {report.total_files_analyzed}")
        print(f"  Total Violations: {report.total_violations}")
        print(f"  Overall Compliance: {report.compliance_percentage:.1f}%")
        print()

        if report.total_violations > 0:
            print("Violations by Severity:")
            for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
                count = report.violations_by_severity.get(severity, 0)
                if count > 0:
                    print(f"  {severity:8}: {count}")

        return 0

    except KeyboardInterrupt:
        print("\n\nReview interrupted by user")
        return 130
    except Exception as e:
        print(f"\nError during review: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
