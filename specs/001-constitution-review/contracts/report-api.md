# Report Generation API Contract

**Date**: 2025-12-09  
**Feature**: Project Constitution Compliance Review

## Overview

This document defines the contract for the compliance report generation API. The report generator provides programmatic access to compliance review results.

## Report Generation Interface

### Input

- **Source**: Codebase analysis results (violations, checks, metrics)
- **Format**: Internal data structures (ComplianceViolation, PrincipleCheck, StandardCheck)

### Output Formats

#### 1. Markdown Report (`compliance_report.md`)

**Structure**:
```markdown
# Constitution Compliance Report

## Executive Summary
- Overall compliance percentage
- Total violations by severity
- Key findings

## Compliance by Principle
- [Principle Name]: X% compliant (Y violations)
  - Violation details with file paths and line numbers

## Compliance by Standard
- [Standard Name]: X% compliant (Y violations)
  - Violation details

## Detailed Violations
- Full list of violations with remediation suggestions

## Remediation Recommendations
- Prioritized list of fixes
```

#### 2. JSON Data Export (`compliance_report.json`)

**Schema**:
```json
{
  "report_id": "string",
  "generated_at": "ISO 8601 datetime",
  "summary": {
    "total_files_analyzed": "integer",
    "total_violations": "integer",
    "compliance_percentage": "float",
    "violations_by_severity": {
      "CRITICAL": "integer",
      "HIGH": "integer",
      "MEDIUM": "integer",
      "LOW": "integer"
    }
  },
  "principles": {
    "principle_name": {
      "compliance_percentage": "float",
      "violations_count": "integer",
      "violations": [...]
    }
  },
  "standards": {
    "standard_name": {
      "compliance_percentage": "float",
      "violations_count": "integer",
      "violations": [...]
    }
  }
}
```

#### 3. Remediation Plan (`remediation_plan.md`)

**Structure**:
```markdown
# Remediation Plan

## Priority: CRITICAL
- [Remediation step with affected files and effort estimate]

## Priority: HIGH
- [Remediation steps...]

## Priority: MEDIUM
- [Remediation steps...]

## Priority: LOW
- [Remediation steps...]
```

## API Methods

### `generate_report(violations: list[ComplianceViolation], principle_checks: list[PrincipleCheck], standard_checks: list[StandardCheck], total_files: int) -> ComplianceReport`

Generates comprehensive compliance report from analysis results.

**Parameters**:
- `violations`: List of all ComplianceViolation instances
- `principle_checks`: List of PrincipleCheck instances containing principle compliance metrics
- `standard_checks`: List of StandardCheck instances containing standard compliance metrics
- `total_files`: Total number of files analyzed (integer)

**Returns**: ComplianceReport object with all violations and metrics

**Note**: This method does not create files on disk. Use `save_report()` to persist reports.

### `export_json(report: ComplianceReport) -> dict`

Exports compliance report as JSON structure.

**Parameters**:
- `report`: ComplianceReport object

**Returns**: Dictionary representation suitable for JSON serialization

### `export_markdown(report: ComplianceReport) -> str`

Exports compliance report as Markdown text.

**Parameters**:
- `report`: ComplianceReport object

**Returns**: Markdown-formatted string

### `generate_remediation_plan(violations: list[ComplianceViolation]) -> list[RemediationStep]`

Generates prioritized remediation steps from violations.

**Parameters**:
- `violations`: List of compliance violations

**Returns**: List of remediation steps ordered by priority

### `save_report(report: ComplianceReport, output_dir: Optional[str] = None) -> str`

Saves report in all formats (Markdown, JSON, Remediation Plan) to disk.

**Parameters**:
- `report`: ComplianceReport object to save
- `output_dir`: Optional directory path to save reports. If None, uses default `reports/` directory from ReviewConfig

**Returns**: Path to the saved reports directory as string

**Side Effects**: 
- Creates report files in `reports/` directory (or specified `output_dir`):
  - `compliance_report.md` - Full markdown report
  - `compliance_report.json` - JSON data export
  - `remediation_plan.md` - Prioritized remediation steps
- Creates output directory if it does not exist

## Error Handling

- **FileNotFoundError**: If source files cannot be found
- **PermissionError**: If report directory cannot be written
- **ValueError**: If report data is invalid or incomplete

## Performance Requirements

- Report generation must complete within 30 minutes for full codebase
- JSON export must complete within 5 seconds
- Markdown export must complete within 10 seconds

