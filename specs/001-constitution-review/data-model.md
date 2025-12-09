# Data Model: Constitution Compliance Review

**Date**: 2025-12-09  
**Feature**: Project Constitution Compliance Review

## Entities

### ComplianceViolation

Represents a single instance where code does not comply with a constitution principle.

**Attributes**:
- `principle`: str - Name of the violated principle (e.g., "Async-First", "Type Safety")
- `standard`: str - Name of the violated standard (e.g., "Code Style", "Testing Standards")
- `file_path`: str - Relative path to the file containing the violation
- `line_number`: int - Line number where violation occurs (0 if file-level)
- `column_number`: int - Column number where violation occurs (optional, 0 if not applicable)
- `violation_type`: str - Type of violation (e.g., "missing_type_annotation", "blocking_io", "missing_decorator")
- `violation_description`: str - Human-readable description of the violation
- `severity`: str - Severity level: "CRITICAL", "HIGH", "MEDIUM", "LOW"
- `code_snippet`: str - Relevant code snippet showing the violation (optional)
- `remediation_suggestion`: str - Suggested fix for the violation

**Validation Rules**:
- `principle` or `standard` must be provided (at least one)
- `file_path` must be a valid relative path
- `line_number` must be >= 0
- `severity` must be one of the allowed values

**State Transitions**: None (immutable entity)

### ComplianceReport

Aggregated results of the review process.

**Attributes**:
- `report_id`: str - Unique identifier for the report (timestamp-based)
- `generated_at`: datetime - When the report was generated
- `total_files_analyzed`: int - Number of files analyzed
- `total_violations`: int - Total number of violations found
- `violations_by_principle`: dict[str, int] - Count of violations per principle
- `violations_by_standard`: dict[str, int] - Count of violations per standard
- `violations_by_file`: dict[str, int] - Count of violations per file
- `violations_by_severity`: dict[str, int] - Count of violations per severity level
- `compliance_percentage`: float - Overall compliance percentage (0-100)
- `principle_compliance`: dict[str, float] - Compliance percentage per principle
- `standard_compliance`: dict[str, float] - Compliance percentage per standard
- `violations`: list[ComplianceViolation] - List of all violations
- `summary`: str - Executive summary of findings

**Validation Rules**:
- `compliance_percentage` must be between 0 and 100
- `total_violations` must equal sum of all violation counts
- All dictionaries must have consistent keys

**State Transitions**: None (generated once, immutable)

### PrincipleCheck

Represents verification of a single constitution principle.

**Attributes**:
- `principle_name`: str - Name of the principle being checked
- `check_status`: str - Status: "PASS", "FAIL", "PARTIAL"
- `violations_found`: int - Number of violations found
- `files_checked`: int - Number of files analyzed for this principle
- `files_with_violations`: int - Number of files containing violations
- `compliance_percentage`: float - Compliance percentage for this principle (0-100)
- `check_duration_seconds`: float - Time taken to perform the check
- `violations`: list[ComplianceViolation] - List of violations for this principle

**Validation Rules**:
- `check_status` must be one of: "PASS", "FAIL", "PARTIAL"
- `compliance_percentage` must be between 0 and 100
- `violations_found` must equal length of `violations` list

**State Transitions**: None (result of single check, immutable)

### StandardCheck

Represents verification of a single development standard.

**Attributes**:
- `standard_name`: str - Name of the standard being checked
- `check_status`: str - Status: "PASS", "FAIL", "PARTIAL"
- `violations_found`: int - Number of violations found
- `files_checked`: int - Number of files analyzed for this standard
- `files_with_violations`: int - Number of files containing violations
- `compliance_percentage`: float - Compliance percentage for this standard (0-100)
- `check_duration_seconds`: float - Time taken to perform the check
- `violations`: list[ComplianceViolation] - List of violations for this standard

**Validation Rules**:
- `check_status` must be one of: "PASS", "FAIL", "PARTIAL"
- `compliance_percentage` must be between 0 and 100
- `violations_found` must equal length of `violations` list

**State Transitions**: None (result of single check, immutable)

### RemediationStep

Represents an actionable step to fix violations.

**Attributes**:
- `step_id`: str - Unique identifier for the remediation step
- `principle`: str - Principle this step addresses
- `standard`: str - Standard this step addresses (optional)
- `priority`: str - Priority: "CRITICAL", "HIGH", "MEDIUM", "LOW"
- `title`: str - Short title describing the remediation
- `description`: str - Detailed description of what needs to be done
- `affected_files`: list[str] - List of files that need changes
- `estimated_effort`: str - Estimated effort (e.g., "2 hours", "1 day")
- `dependencies`: list[str] - IDs of other remediation steps that must be completed first
- `violation_ids`: list[str] - IDs of violations this step addresses

**Validation Rules**:
- `priority` must be one of the allowed values
- `affected_files` must not be empty
- `violation_ids` must not be empty

**State Transitions**: None (immutable recommendation)

## Relationships

- **ComplianceReport** contains many **ComplianceViolation** (one-to-many)
- **ComplianceReport** contains many **PrincipleCheck** (one-to-many)
- **ComplianceReport** contains many **StandardCheck** (one-to-many)
- **PrincipleCheck** contains many **ComplianceViolation** (one-to-many)
- **StandardCheck** contains many **ComplianceViolation** (one-to-many)
- **RemediationStep** addresses many **ComplianceViolation** (many-to-many)

## Data Flow

1. **Review Process** → Analyzes codebase → Generates **ComplianceViolation** instances
2. **Violations** → Grouped by principle/standard → Creates **PrincipleCheck** and **StandardCheck**
3. **Checks** → Aggregated → Creates **ComplianceReport**
4. **Violations** → Analyzed → Generates **RemediationStep** recommendations
5. **Report** → Exported → Markdown and JSON formats

## Constraints

- Violations must reference existing files in the codebase
- Line numbers must be valid for the referenced files
- Severity levels must be consistent across similar violations
- Compliance percentages must be calculated correctly (no violations = 100%)
- Remediation steps must address at least one violation

