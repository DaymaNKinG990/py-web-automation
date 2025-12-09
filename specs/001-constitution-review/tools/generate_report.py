"""
Report generation module for constitution compliance review.

This module provides functionality to generate compliance reports in various formats
(Markdown, JSON) and create remediation plans.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from .config import ReviewConfig
from .models import ComplianceReport, RemediationStep

if TYPE_CHECKING:
    pass


def generate_report(
    violations: list,
    principle_checks: list,
    standard_checks: list,
    total_files: int,
) -> ComplianceReport:
    """
    Generate comprehensive compliance report from analysis results.

    Args:
        violations: List of all ComplianceViolation instances
        principle_checks: List of PrincipleCheck instances
        standard_checks: List of StandardCheck instances
        total_files: Total number of files analyzed

    Returns:
        ComplianceReport object with all violations and metrics
    """
    from .utils import calculate_compliance_percentage
    from .violation_collector import ViolationCollector

    collector = ViolationCollector()
    collector.add_violations(violations)

    counts = collector.get_violation_counts()
    files_with_violations = len(collector.get_files_with_violations())
    overall_compliance = calculate_compliance_percentage(total_files, files_with_violations)

    # Build principle compliance dict
    principle_compliance = {
        check.principle_name: check.compliance_percentage for check in principle_checks
    }

    # Build standard compliance dict
    standard_compliance = {
        check.standard_name: check.compliance_percentage for check in standard_checks
    }

    # Extract typed counts (type narrowing)
    by_principle = counts["by_principle"]
    by_standard = counts["by_standard"]
    by_file = counts["by_file"]
    by_severity = counts["by_severity"]

    # Type assertions for mypy (type narrowing)
    # These are runtime type checks for type narrowing, not validation asserts
    if not isinstance(by_principle, dict):
        raise TypeError("by_principle must be a dict")
    if not isinstance(by_standard, dict):
        raise TypeError("by_standard must be a dict")
    if not isinstance(by_file, dict):
        raise TypeError("by_file must be a dict")
    if not isinstance(by_severity, dict):
        raise TypeError("by_severity must be a dict")

    # Generate summary
    summary = _generate_summary_text(
        total_files,
        len(violations),
        overall_compliance,
        by_severity,
    )

    report = ComplianceReport(
        report_id=f"report_{int(datetime.now().timestamp())}",
        total_files_analyzed=total_files,
        total_violations=len(violations),
        violations_by_principle=by_principle,
        violations_by_standard=by_standard,
        violations_by_file=by_file,
        violations_by_severity=by_severity,
        compliance_percentage=overall_compliance,
        principle_compliance=principle_compliance,
        standard_compliance=standard_compliance,
        violations=violations,
        summary=summary,
    )

    return report


def export_json(report: ComplianceReport) -> dict:
    """
    Export compliance report as JSON structure.

    Args:
        report: ComplianceReport object

    Returns:
        Dictionary representation suitable for JSON serialization
    """
    # Convert violations to dictionaries
    violations_data = []
    for violation in report.violations:
        violations_data.append(
            {
                "principle": violation.principle,
                "standard": violation.standard,
                "file_path": violation.file_path,
                "line_number": violation.line_number,
                "column_number": violation.column_number,
                "violation_type": violation.violation_type,
                "violation_description": violation.violation_description,
                "severity": violation.severity,
                "code_snippet": violation.code_snippet,
                "remediation_suggestion": violation.remediation_suggestion,
            }
        )

    # Build principles data
    principles_data = {}
    for principle_name, compliance_pct in report.principle_compliance.items():
        principle_violations = [v for v in report.violations if v.principle == principle_name]
        principles_data[principle_name] = {
            "compliance_percentage": compliance_pct,
            "violations_count": len(principle_violations),
            "violations": [
                {
                    "file_path": v.file_path,
                    "line_number": v.line_number,
                    "violation_type": v.violation_type,
                    "severity": v.severity,
                }
                for v in principle_violations
            ],
        }

    # Build standards data
    standards_data = {}
    for standard_name, compliance_pct in report.standard_compliance.items():
        standard_violations = [v for v in report.violations if v.standard == standard_name]
        standards_data[standard_name] = {
            "compliance_percentage": compliance_pct,
            "violations_count": len(standard_violations),
            "violations": [
                {
                    "file_path": v.file_path,
                    "line_number": v.line_number,
                    "violation_type": v.violation_type,
                    "severity": v.severity,
                }
                for v in standard_violations
            ],
        }

    return {
        "report_id": report.report_id,
        "generated_at": report.generated_at.isoformat(),
        "summary": {
            "total_files_analyzed": report.total_files_analyzed,
            "total_violations": report.total_violations,
            "compliance_percentage": report.compliance_percentage,
            "violations_by_severity": report.violations_by_severity,
        },
        "principles": principles_data,
        "standards": standards_data,
    }


def export_markdown(report: ComplianceReport) -> str:
    """
    Export compliance report as Markdown text.

    Args:
        report: ComplianceReport object

    Returns:
        Markdown-formatted string
    """
    lines = [
        "# Constitution Compliance Report",
        "",
        f"**Report ID**: {report.report_id}",
        f"**Generated**: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Executive Summary",
        "",
        report.summary,
        "",
        "## Compliance by Principle",
        "",
    ]

    # Add principle compliance
    for principle_name in sorted(report.principle_compliance.keys()):
        compliance_pct = report.principle_compliance[principle_name]
        violation_count = report.violations_by_principle.get(principle_name, 0)
        lines.append(f"### {principle_name}")
        lines.append(f"- **Compliance**: {compliance_pct:.1f}%")
        lines.append(f"- **Violations**: {violation_count}")
        lines.append("")

        # Add violation details
        principle_violations = [v for v in report.violations if v.principle == principle_name]
        if principle_violations:
            lines.append("#### Violations:")
            for violation in principle_violations[:10]:  # Limit to first 10
                violation_desc = violation.violation_description
                lines.append(
                    f"- `{violation.file_path}:{violation.line_number}` - {violation_desc}"
                )
                if violation.remediation_suggestion:
                    lines.append(f"  - **Fix**: {violation.remediation_suggestion}")
            if len(principle_violations) > 10:
                lines.append(f"- ... and {len(principle_violations) - 10} more violations")
            lines.append("")

    lines.append("## Compliance by Standard")
    lines.append("")

    # Add standard compliance
    for standard_name in sorted(report.standard_compliance.keys()):
        compliance_pct = report.standard_compliance[standard_name]
        violation_count = report.violations_by_standard.get(standard_name, 0)
        lines.append(f"### {standard_name}")
        lines.append(f"- **Compliance**: {compliance_pct:.1f}%")
        lines.append(f"- **Violations**: {violation_count}")
        lines.append("")

        # Add violation details
        standard_violations = [v for v in report.violations if v.standard == standard_name]
        if standard_violations:
            lines.append("#### Violations:")
            for violation in standard_violations[:10]:  # Limit to first 10
                violation_desc = violation.violation_description
                lines.append(
                    f"- `{violation.file_path}:{violation.line_number}` - {violation_desc}"
                )
                if violation.remediation_suggestion:
                    lines.append(f"  - **Fix**: {violation.remediation_suggestion}")
            if len(standard_violations) > 10:
                lines.append(f"- ... and {len(standard_violations) - 10} more violations")
            lines.append("")

    lines.append("## Detailed Violations")
    lines.append("")
    lines.append(f"Total violations: {report.total_violations}")
    lines.append("")

    # Group by severity
    for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        severity_violations = [v for v in report.violations if v.severity == severity]
        if severity_violations:
            lines.append(f"### {severity} Severity ({len(severity_violations)} violations)")
            lines.append("")
            for violation in severity_violations:
                lines.append(f"**{violation.file_path}:{violation.line_number}**")
                lines.append(f"- Type: {violation.violation_type}")
                lines.append(f"- Description: {violation.violation_description}")
                if violation.code_snippet:
                    lines.append("- Code:")
                    lines.append("```python")
                    lines.append(violation.code_snippet)
                    lines.append("```")
                if violation.remediation_suggestion:
                    lines.append(f"- Remediation: {violation.remediation_suggestion}")
                lines.append("")

    return "\n".join(lines)


def generate_remediation_plan(violations: list) -> list[RemediationStep]:
    """
    Generate prioritized remediation steps from violations.

    Args:
        violations: List of ComplianceViolation instances

    Returns:
        List of RemediationStep instances ordered by priority
    """
    from collections import defaultdict

    # Group violations by principle/standard and file
    grouped: dict[tuple[str | None, str | None], dict[str, list]] = defaultdict(
        lambda: defaultdict(list)
    )

    for violation in violations:
        key = (violation.principle, violation.standard)
        grouped[key][violation.file_path].append(violation)

    remediation_steps: list[RemediationStep] = []
    step_counter = 1

    # Create remediation steps grouped by principle/standard and file
    for (principle, standard), files_dict in grouped.items():
        for file_path, file_violations in files_dict.items():
            # Determine priority based on highest severity violation in this group
            severities = [v.severity for v in file_violations]
            priority = (
                "CRITICAL"
                if "CRITICAL" in severities
                else (
                    "HIGH"
                    if "HIGH" in severities
                    else ("MEDIUM" if "MEDIUM" in severities else "LOW")
                )
            )

            # Group violations by type
            violations_by_type: dict[str, list] = defaultdict(list)
            for violation in file_violations:
                violations_by_type[violation.violation_type].append(violation)

            # Create step for each violation type
            for violation_type, type_violations in violations_by_type.items():
                step_id = f"STEP-{step_counter:03d}"
                step_counter += 1

                # Generate description
                desc = (
                    f"Fix {len(type_violations)} violation(s) of type "
                    f"'{violation_type}' in {file_path}"
                )
                description_parts = [desc]
                if type_violations[0].remediation_suggestion:
                    description_parts.append(
                        f"\nSuggested fix: {type_violations[0].remediation_suggestion}"
                    )

                # Estimate effort based on violation count and type
                effort = _estimate_effort(len(type_violations), violation_type)

                step = RemediationStep(
                    step_id=step_id,
                    principle=principle or "",
                    standard=standard,
                    priority=priority,
                    title=f"Fix {violation_type} in {Path(file_path).name}",
                    description="\n".join(description_parts),
                    affected_files=[file_path],
                    estimated_effort=effort,
                    violation_ids=[f"{v.file_path}:{v.line_number}" for v in type_violations],
                )
                remediation_steps.append(step)

    # Sort by priority
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    remediation_steps.sort(key=lambda s: (priority_order.get(s.priority, 99), s.step_id))

    return remediation_steps


def _estimate_effort(violation_count: int, violation_type: str) -> str:
    """
    Estimate effort for fixing violations.

    Args:
        violation_count: Number of violations
        violation_type: Type of violation

    Returns:
        Estimated effort string (e.g., "2 hours", "1 day")
    """
    # Base effort per violation type (in minutes)
    base_effort = {
        "missing_type_annotation": 5,
        "blocking_io": 15,
        "missing_decorator": 2,
        "missing_test_case": 10,
        "code_style": 1,
        "import_organization": 3,
    }

    minutes = base_effort.get(violation_type, 5) * violation_count

    if minutes < 60:
        return f"{minutes} minutes"
    elif minutes < 480:  # 8 hours
        hours = minutes / 60
        return f"{hours:.1f} hours"
    else:
        days = minutes / 480
        return f"{days:.1f} days"


def _generate_summary_text(
    total_files: int,
    total_violations: int,
    compliance_percentage: float,
    violations_by_severity: dict[str, int],
) -> str:
    """
    Generate executive summary text.

    Args:
        total_files: Total number of files analyzed
        total_violations: Total number of violations found
        compliance_percentage: Overall compliance percentage
        violations_by_severity: Violations grouped by severity

    Returns:
        Summary text
    """
    summary_lines = [
        f"Files Analyzed: {total_files}",
        f"Total Violations: {total_violations}",
        f"Overall Compliance: {compliance_percentage:.1f}%",
        "",
        "Violations by Severity:",
    ]

    for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        count = violations_by_severity.get(severity, 0)
        summary_lines.append(f"  {severity}: {count}")

    if total_violations == 0:
        summary_lines.append("")
        summary_lines.append(
            "✓ No violations found. Project is fully compliant with the constitution."
        )

    return "\n".join(summary_lines)


def save_report(report: ComplianceReport, output_dir: Path | None = None) -> dict[str, Path]:
    """
    Save report in all formats to disk.

    Args:
        report: ComplianceReport to save
        output_dir: Directory to save reports. If None, uses ReviewConfig.REPORTS_DIR.

    Returns:
        Dictionary mapping format names to file paths
    """
    if output_dir is None:
        output_dir = ReviewConfig.REPORTS_DIR
    ReviewConfig.ensure_directories()

    saved_files: dict[str, Path] = {}

    # Save Markdown report
    md_content = export_markdown(report)
    md_path = output_dir / "compliance_report.md"
    md_path.write_text(md_content, encoding="utf-8")
    saved_files["markdown"] = md_path

    # Save JSON report
    json_data = export_json(report)
    json_path = output_dir / "violations_by_principle.json"
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")
    saved_files["json"] = json_path

    # Save remediation plan
    remediation_steps = generate_remediation_plan(report.violations)
    remediation_content = _export_remediation_plan_markdown(remediation_steps)
    remediation_path = output_dir / "remediation_plan.md"
    remediation_path.write_text(remediation_content, encoding="utf-8")
    saved_files["remediation"] = remediation_path

    return saved_files


def _export_remediation_plan_markdown(steps: list[RemediationStep]) -> str:
    """
    Export remediation plan as Markdown.

    Args:
        steps: List of RemediationStep instances

    Returns:
        Markdown-formatted remediation plan
    """
    lines = [
        "# Remediation Plan",
        "",
        f"Total remediation steps: {len(steps)}",
        "",
    ]

    # Group by priority
    for priority in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        priority_steps = [s for s in steps if s.priority == priority]
        if not priority_steps:
            continue

        lines.append(f"## Priority: {priority}")
        lines.append("")

        for step in priority_steps:
            lines.append(f"### {step.step_id}: {step.title}")
            lines.append("")
            lines.append(f"**Principle/Standard**: {step.principle or step.standard}")
            lines.append(f"**Affected Files**: {', '.join(step.affected_files)}")
            lines.append(f"**Estimated Effort**: {step.estimated_effort}")
            lines.append(f"**Violations**: {len(step.violation_ids)}")
            lines.append("")
            lines.append(step.description)
            lines.append("")
            if step.dependencies:
                lines.append(f"**Dependencies**: {', '.join(step.dependencies)}")
                lines.append("")

    return "\n".join(lines)
