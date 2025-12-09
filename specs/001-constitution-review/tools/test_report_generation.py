"""
Validation tests for report generation.

This module provides tests to verify report structure and completeness.
"""

from .generate_report import (
    export_json,
    export_markdown,
    generate_remediation_plan,
    generate_report,
)
from .models import ComplianceViolation


def test_report_structure() -> bool:
    """
    Test that generated reports have correct structure.

    Returns:
        True if structure is valid
    """
    # Create sample violations
    violations = [
        ComplianceViolation(
            principle="Type Safety",
            file_path="test_file.py",
            line_number=10,
            violation_type="missing_type_annotation",
            violation_description="Function missing return type",
            severity="HIGH",
            remediation_suggestion="Add return type annotation",
        )
    ]

    # Generate report
    report = generate_report(
        violations=violations,
        principle_checks=[],
        standard_checks=[],
        total_files=1,
    )

    # Validate report structure
    assert report.report_id != ""  # noqa: S101
    assert report.total_files_analyzed == 1  # noqa: S101
    assert report.total_violations == 1  # noqa: S101
    assert 0 <= report.compliance_percentage <= 100  # noqa: S101
    assert "Type Safety" in report.violations_by_principle  # noqa: S101

    return True


def test_json_export() -> bool:
    """
    Test JSON export format.

    Returns:
        True if JSON export is valid
    """
    violations = [
        ComplianceViolation(
            principle="Async-First",
            file_path="test_file.py",
            line_number=5,
            violation_type="blocking_io",
            violation_description="Blocking I/O in sync function",
            severity="CRITICAL",
        )
    ]

    report = generate_report(
        violations=violations,
        principle_checks=[],
        standard_checks=[],
        total_files=1,
    )

    json_data = export_json(report)

    # Validate JSON structure
    assert "report_id" in json_data  # noqa: S101
    assert "generated_at" in json_data  # noqa: S101
    assert "summary" in json_data  # noqa: S101
    assert "principles" in json_data  # noqa: S101
    assert "standards" in json_data  # noqa: S101

    assert json_data["summary"]["total_files_analyzed"] == 1  # noqa: S101
    assert json_data["summary"]["total_violations"] == 1  # noqa: S101

    return True


def test_markdown_export() -> bool:
    """
    Test Markdown export format.

    Returns:
        True if Markdown export is valid
    """
    violations = [
        ComplianceViolation(
            standard="Code Style",
            file_path="test_file.py",
            line_number=20,
            violation_type="line_too_long",
            violation_description="Line exceeds 100 characters",
            severity="LOW",
        )
    ]

    report = generate_report(
        violations=violations,
        principle_checks=[],
        standard_checks=[],
        total_files=1,
    )

    markdown = export_markdown(report)

    # Validate Markdown structure
    assert "# Constitution Compliance Report" in markdown  # noqa: S101
    assert "Executive Summary" in markdown  # noqa: S101
    assert "Compliance by Principle" in markdown  # noqa: S101
    assert "Compliance by Standard" in markdown  # noqa: S101

    return True


def test_remediation_plan() -> bool:
    """
    Test remediation plan generation.

    Returns:
        True if remediation plan is valid
    """
    violations = [
        ComplianceViolation(
            principle="Type Safety",
            file_path="file1.py",
            line_number=10,
            violation_type="missing_type_annotation",
            violation_description="Missing type",
            severity="HIGH",
            remediation_suggestion="Add type",
        ),
        ComplianceViolation(
            principle="Type Safety",
            file_path="file1.py",
            line_number=15,
            violation_type="missing_type_annotation",
            violation_description="Missing type",
            severity="HIGH",
            remediation_suggestion="Add type",
        ),
    ]

    steps = generate_remediation_plan(violations)

    # Validate remediation steps
    assert len(steps) > 0  # noqa: S101
    assert all(  # noqa: S101
        step.priority in ("CRITICAL", "HIGH", "MEDIUM", "LOW") for step in steps
    )
    assert all(step.affected_files for step in steps)  # noqa: S101
    assert all(step.violation_ids for step in steps)  # noqa: S101

    return True


if __name__ == "__main__":
    """Run validation tests."""
    print("Running report generation validation tests...")
    print()

    tests = [
        ("Report Structure", test_report_structure),
        ("JSON Export", test_json_export),
        ("Markdown Export", test_markdown_export),
        ("Remediation Plan", test_remediation_plan),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✓ {test_name}: PASSED")
                passed += 1
            else:
                print(f"✗ {test_name}: FAILED")
                failed += 1
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
            failed += 1

    print()
    print(f"Tests: {passed} passed, {failed} failed")

    if failed == 0:
        print("All validation tests passed!")
        exit(0)
    else:
        print("Some validation tests failed!")
        exit(1)
